"""
OrchestraService — boucle de coordination multi-agents via LangGraph.

Graphe Zeus :
  [plan_agents] → [zeus_distribute] → [dispatch_subtasks] → [veto_check] → [zeus_judge]
                        ↑ HITL C4/C5                               │ needs_complement
                                                    ┌──────────────┘
                                                    ▼
                                           [execute_complements] → [synthesize]
                                                    │ complete
                                                    ▼
                                               [synthesize]

Patterns d'exécution dans dispatch_subtasks :
  solo     — un seul agent
  parallel — agents indépendants simultanés (asyncio.gather)
  cascade  — séquence : chaque agent reçoit le contexte du précédent
  arena    — agents en parallèle + juge qui arbitre
"""
import asyncio
import json
import time
from pathlib import Path
from typing import TypedDict, Optional
from uuid import UUID

from langgraph.graph import StateGraph, END
from langgraph.types import interrupt, Command
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.llm_service import LlmService
from core.settings import settings
from database import AsyncSessionLocal
from modules.agent.service import run_agent, _build_system_prompt
from modules.orchestra.models import OrchestraRun

log = get_logger("orchestra.service")

AGENTS_DIR = Path(settings.AGENTS_DIR) if hasattr(settings, "AGENTS_DIR") else Path(__file__).parent.parent.parent.parent / "agents"
DEFAULT_AGENTS = ["themis", "athena", "chronos"]

# Routing automatique selon criticité
CRITICITE_ROUTING = {
    "C1": {"hitl": False, "zeus": False, "veto_check": False},
    "C2": {"hitl": False, "zeus": False, "veto_check": False},
    "C3": {"hitl": False, "zeus": True,  "veto_check": False},
    "C4": {"hitl": True,  "zeus": True,  "veto_check": False},
    "C5": {"hitl": True,  "zeus": True,  "veto_check": True},
}
VALID_AGENTS = {
    # Perception
    "hermes", "argos",
    # Analyse
    "athena", "hephaistos", "promethee", "apollon", "dionysos",
    # Cadrage
    "themis", "chronos", "ares",
    # Continuité
    "hestia", "mnemosyne",
    # Communication
    "iris", "aphrodite",
    # Production
    "dedale",
}

# ── Prompts Zeus ────────────────────────────────────────────────────

_ZEUS_PLAN_PROMPT = """\
Tu reçois une demande et les plans de {n} agents. Organise leur collaboration en sous-tâches.

## Demande
{instruction}

## Plans des agents
{plans}

Patterns disponibles :
- "solo"     : un agent seul
- "parallel" : agents indépendants, en parallèle
- "cascade"  : séquence — chaque agent reçoit les résultats du précédent
- "arena"    : compétition — agents sur la même question, un juge tranche (exige "judge")

Réponds en JSON strict (aucun texte en dehors) :
{{
  "reasoning": "Pourquoi cette organisation",
  "criticite": "C3",
  "subtasks": [
    {{
      "id": "T1",
      "pattern": "cascade",
      "agents": ["argos", "hephaistos"],
      "instruction": "Instruction spécifique à cette sous-tâche (optionnel)",
      "depends_on": []
    }},
    {{
      "id": "T2",
      "pattern": "arena",
      "agents": ["athena", "dionysos"],
      "judge": "apollon",
      "instruction": "",
      "depends_on": []
    }},
    {{
      "id": "T3",
      "pattern": "solo",
      "agents": ["chronos"],
      "instruction": "",
      "depends_on": ["T1"]
    }}
  ],
  "synthesis_agent": "<nom>"
}}

Règles :
- Au moins une sous-tâche
- "arena" exige "judge" (apollon pour faits/normes, zeus pour arbitrage stratégique)
- "depends_on" = IDs des sous-tâches prérequises ([] = démarre immédiatement)
- Promethée systématiquement pour C4+
- Chronos si impact planning
- Agents disponibles : hermes, argos, athena, hephaistos, promethee, apollon, dionysos,
  themis, chronos, ares, hestia, mnemosyne, iris, aphrodite, dedale
"""

_ZEUS_JUDGE_PROMPT = """\
Tu as orchestré une analyse multi-agents. Juge si les résultats couvrent la demande.

## Demande initiale
{instruction}

## Résultats des agents
{results}

Réponds en JSON strict :
{{
  "verdict": "complete",
  "synthesis_instruction": "Instruction pour la synthèse finale",
  "complement_requests": []
}}

Ou si des compléments sont nécessaires (une seule fois !) :
{{
  "verdict": "needs_complement",
  "synthesis_instruction": "",
  "complement_requests": [
    {{"agent": "<nom>", "instruction": "<complément ciblé>", "priority": 1}}
  ]
}}
"""

_ARENA_JUDGE_PROMPT = """\
Tu arbitres une arène entre {n} agents sur la même question.

## Question
{instruction}

## Propositions des agents
{proposals}

Analyse chaque proposition. Synthétise ou retiens la plus solide.
Structure ta réponse :
1. **Proposition retenue / synthèse** : quelle option et pourquoi
2. **Points forts** : ce qui est solide dans les propositions
3. **Réserves** : ce qui doit être pondéré ou nuancé
4. **Recommandation finale** : ta conclusion opérationnelle
"""

_SYNTHESIS_PROMPT_TEMPLATE = """\
{synthesis_instruction}

## Demande originale
{instruction}

## Analyses des agents
{results}

Produis une réponse finale construite, structurée, en français.
"""


# ── État LangGraph ──────────────────────────────────────────────────

class OrchestraState(TypedDict):
    instruction: str
    affaire_id: str
    user_id: Optional[str]
    initial_agents: list[str]

    # Phase 1
    agent_plans: dict           # {agent_name: {plan, needs, difficulties, expected_output}}

    # Phase 2 — Zeus plan
    zeus_reasoning: str
    subtasks: list              # [{id, pattern, agents, judge?, instruction, depends_on}]
    assignments: list           # [{agent, instruction, priority}] — compat + complements
    synthesis_agent: str

    # Phase 3 — exécution
    agent_results: dict         # {agent_name: result_text} — vue plate pour veto/synthèse
    subtask_results: dict       # {task_id: {agent_name: result_text}} — vue structurée
    agent_run_ids: list         # UUIDs des AgentRun créés

    # Phase 3b — compléments (optionnel, une fois)
    complement_done: bool

    # Phase 4
    final_answer: str

    # Routing interne Zeus
    verdict: str                # "complete" | "needs_complement" | "veto"

    # Criticité C1-C5
    criticite: str              # "C1" | "C2" | "C3" | "C4" | "C5"

    # Veto (Thémis / Héphaïstos)
    veto_agent: str             # nom de l'agent ayant émis le veto
    veto_motif: str             # raison du veto

    # Human-in-the-loop
    hitl_enabled: bool
    hitl_approval: dict         # {approved, feedback, modified_assignments}


# ── Helpers LLM ────────────────────────────────────────────────────

def _zeus_system() -> str:
    soul_path = AGENTS_DIR / "zeus" / "SOUL.md"
    return soul_path.read_text(encoding="utf-8") if soul_path.exists() else \
        "Tu es Zeus, orchestrateur. Réponds toujours en JSON strict."


def _parse_json_response(content: str) -> dict:
    """Parse JSON robuste — extrait le bloc JSON même si du texte l'entoure."""
    content = content.strip()
    # Chercher le premier { et le dernier }
    start = content.find("{")
    end = content.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(content[start:end])
        except json.JSONDecodeError:
            pass
    # Fallback — contenu brut dans reasoning
    return {"reasoning": content, "assignments": [], "synthesis_agent": "mnemosyne"}


async def _llm_call(system: str, user: str) -> str:
    response = await LlmService._get_client().chat.completions.create(
        model=settings.effective_llm_model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.2,
        max_tokens=2048,
    )
    return response.choices[0].message.content or ""


async def _get_agent_plan(agent_name: str, instruction: str) -> dict:
    """Demande à un agent son plan sans l'exécuter (pas de boucle ReAct)."""
    system = _build_system_prompt(agent_name)
    plan_request = (
        f"Pour la demande suivante, décris ton plan d'action SANS l'exécuter.\n\n"
        f"Demande : {instruction}\n\n"
        f"Réponds en JSON strict :\n"
        f'{{"plan": "...", "needs": ["..."], "difficulties": ["..."], "expected_output": "..."}}'
    )
    content = await _llm_call(system, plan_request)
    parsed = _parse_json_response(content)
    return {
        "plan": parsed.get("plan", content[:300]),
        "needs": parsed.get("needs", []),
        "difficulties": parsed.get("difficulties", []),
        "expected_output": parsed.get("expected_output", ""),
    }


async def _run_agent_isolated(agent: str, instruction: str, affaire_id: UUID, user_id: UUID | None):
    """Exécute un agent avec sa propre session DB."""
    async with AsyncSessionLocal() as session:
        run = await run_agent(
            db=session,
            instruction=instruction,
            affaire_id=affaire_id,
            user_id=user_id,
            agent_name=agent,
        )
        return agent, run.result or "", str(run.id)


# ── Patterns d'exécution ────────────────────────────────────────────

def _topological_levels(subtasks: list[dict]) -> list[list[dict]]:
    """Groupe les sous-tâches par niveau d'exécution (tri topologique BFS).
    Les sous-tâches sans dépendances forment le niveau 0, etc."""
    if not subtasks:
        return []
    completed: set[str] = set()
    remaining = list(subtasks)
    levels = []
    while remaining:
        ready = [t for t in remaining if all(dep in completed for dep in t.get("depends_on", []))]
        if not ready:
            # Dépendance circulaire ou manquante → tout exécuter
            ready = remaining
        levels.append(ready)
        completed.update(t["id"] for t in ready)
        remaining = [t for t in remaining if t["id"] not in completed]
    return levels


async def _exec_parallel(
    agents_instructions: dict[str, str],
    affaire_uuid: UUID,
    user_uuid: UUID | None,
) -> tuple[dict, list]:
    """Exécute plusieurs agents en parallèle. {agent: instruction} → ({agent: result}, [run_ids])"""
    tasks = [
        _run_agent_isolated(agent, instr, affaire_uuid, user_uuid)
        for agent, instr in agents_instructions.items()
    ]
    raw = await asyncio.gather(*tasks, return_exceptions=True)
    results, run_ids = {}, []
    for r in raw:
        if isinstance(r, Exception):
            log.error("orchestra.parallel_failed", error=str(r))
            continue
        agent_name, result_text, run_id = r
        results[agent_name] = result_text
        run_ids.append(run_id)
    return results, run_ids


async def _exec_cascade(
    agents: list[str],
    instruction: str,
    affaire_uuid: UUID,
    user_uuid: UUID | None,
) -> tuple[dict, list]:
    """Exécute les agents en séquence — chaque agent reçoit le contexte des précédents."""
    results, run_ids = {}, []
    for agent in agents:
        if results:
            prior = "\n\n".join(f"### {a}\n{r}" for a, r in results.items())
            agent_instruction = (
                f"{instruction}\n\n"
                f"## Contexte — analyses précédentes\n{prior}\n\n"
                f"Appuie ton analyse sur ce qui précède."
            )
        else:
            agent_instruction = instruction
        try:
            _, result_text, run_id = await _run_agent_isolated(agent, agent_instruction, affaire_uuid, user_uuid)
            results[agent] = result_text
            run_ids.append(run_id)
        except Exception as exc:
            log.error("orchestra.cascade_failed", agent=agent, error=str(exc))
    return results, run_ids


async def _exec_arena(
    agents: list[str],
    judge: str,
    instruction: str,
    affaire_uuid: UUID,
    user_uuid: UUID | None,
) -> tuple[dict, list]:
    """Round 0 : agents en parallèle sur la même question.
    Round 1 : le juge reçoit toutes les propositions et arbitre."""
    # Round 0 — propositions indépendantes
    tasks = [_run_agent_isolated(a, instruction, affaire_uuid, user_uuid) for a in agents]
    raw = await asyncio.gather(*tasks, return_exceptions=True)
    results, run_ids = {}, []
    for r in raw:
        if isinstance(r, Exception):
            log.error("orchestra.arena_round0_failed", error=str(r))
            continue
        agent_name, result_text, run_id = r
        results[agent_name] = result_text
        run_ids.append(run_id)

    if not results:
        return results, run_ids

    # Round 1 — arbitrage du juge
    proposals_text = "\n\n".join(
        f"## Proposition {agent}\n{result}"
        for agent, result in results.items()
    )
    judge_instruction = _ARENA_JUDGE_PROMPT.format(
        n=len(results),
        instruction=instruction,
        proposals=proposals_text,
    )
    judge_key = f"{judge}__verdict"
    try:
        _, judge_result, judge_run_id = await _run_agent_isolated(judge, judge_instruction, affaire_uuid, user_uuid)
        results[judge_key] = judge_result
        run_ids.append(judge_run_id)
    except Exception as exc:
        log.error("orchestra.arena_judge_failed", judge=judge, error=str(exc))

    return results, run_ids


# ── Nœuds LangGraph ────────────────────────────────────────────────

def _make_nodes(affaire_uuid: UUID, user_uuid: UUID | None):
    """Crée les nœuds du graphe en clôturant affaire_id et user_id."""

    async def plan_agents(state: OrchestraState) -> dict:
        """Phase 1 — chaque agent déclare son plan."""
        log.info("orchestra.plan", agents=state["initial_agents"])
        plans_list = await asyncio.gather(*[
            _get_agent_plan(a, state["instruction"])
            for a in state["initial_agents"]
        ])
        plans = dict(zip(state["initial_agents"], plans_list))
        log.info("orchestra.plans_collected", count=len(plans))
        return {"agent_plans": plans}

    async def zeus_distribute(state: OrchestraState) -> dict:
        """Phase 2 — Zeus analyse les plans et organise les sous-tâches avec patterns."""
        plans_text = "\n\n".join(
            f"### {agent}\n"
            f"Plan : {p['plan']}\n"
            f"Besoins : {', '.join(p['needs']) or 'aucun'}\n"
            f"Difficultés : {', '.join(p['difficulties']) or 'aucune'}\n"
            f"Résultat attendu : {p['expected_output']}"
            for agent, p in state["agent_plans"].items()
        )
        prompt = _ZEUS_PLAN_PROMPT.format(
            n=len(state["agent_plans"]),
            instruction=state["instruction"],
            plans=plans_text,
        )
        content = await _llm_call(_zeus_system(), prompt)
        parsed = _parse_json_response(content)

        # ── Parsing subtasks (nouveau format) ─────────────────────
        raw_subtasks = parsed.get("subtasks", [])
        subtasks = []
        for st in raw_subtasks:
            agents = [a for a in st.get("agents", []) if a in VALID_AGENTS]
            if not agents:
                continue
            judge = st.get("judge", "")
            if judge and judge not in VALID_AGENTS:
                judge = "apollon"
            subtasks.append({
                "id": st.get("id", f"T{len(subtasks) + 1}"),
                "pattern": st.get("pattern", "parallel"),
                "agents": agents,
                "judge": judge,
                "instruction": st.get("instruction", "") or state["instruction"],
                "depends_on": st.get("depends_on", []),
            })

        # ── Fallback : ancien format assignments ───────────────────
        assignments = parsed.get("assignments", [])
        assignments = [a for a in assignments if a.get("agent") in VALID_AGENTS]

        if not subtasks and not assignments:
            # Fallback total — relancer les agents initiaux en parallèle
            assignments = [
                {"agent": a, "instruction": state["instruction"], "priority": 1}
                for a in state["initial_agents"]
            ]

        if not subtasks and assignments:
            # Convertir l'ancien format en une seule sous-tâche parallèle
            subtasks = [{
                "id": "T1",
                "pattern": "parallel",
                "agents": [a["agent"] for a in assignments],
                "judge": "",
                "instruction": state["instruction"],
                "depends_on": [],
                "_agent_instructions": {a["agent"]: a.get("instruction", state["instruction"]) for a in assignments},
            }]

        # Pour compat HITL/synthèse — aplatir subtasks → assignments
        if subtasks and not assignments:
            assignments = []
            for st in subtasks:
                for agent in st["agents"]:
                    assignments.append({"agent": agent, "instruction": st["instruction"], "priority": 1})
                if st.get("judge"):
                    assignments.append({"agent": st["judge"], "instruction": st["instruction"], "priority": 2})

        log.info("orchestra.zeus_distributed",
                 subtasks=[(s["id"], s["pattern"], s["agents"]) for s in subtasks])

        approval = {}
        # ── Human-in-the-loop : pause avant exécution ─────────────
        if state.get("hitl_enabled"):
            approval = interrupt({
                "message": "Zeus a planifié les sous-tâches. Validez pour lancer l'exécution.",
                "reasoning": parsed.get("reasoning", ""),
                "subtasks": subtasks,
                "assignments": assignments,
                "synthesis_agent": parsed.get("synthesis_agent", "mnemosyne"),
            })
            if approval.get("modified_assignments"):
                assignments = [
                    a for a in approval["modified_assignments"]
                    if a.get("agent") in VALID_AGENTS
                ] or assignments

        return {
            "zeus_reasoning": parsed.get("reasoning", ""),
            "subtasks": subtasks,
            "assignments": assignments,
            "synthesis_agent": parsed.get("synthesis_agent", "mnemosyne"),
            "hitl_approval": approval,
        }

    async def dispatch_subtasks(state: OrchestraState) -> dict:
        """Phase 3 — dispatch des sous-tâches selon leur pattern.
        Exécution niveau par niveau (topologique). Au sein d'un niveau,
        les sous-tâches sans dépendance commune tournent en parallèle."""
        subtasks = state.get("subtasks", [])

        if not subtasks:
            # Fallback : exécution parallèle simple des assignments
            log.info("orchestra.dispatch_fallback", agents=[a["agent"] for a in state["assignments"]])
            agents_instructions = {a["agent"]: a["instruction"] for a in state["assignments"]}
            results, run_ids = await _exec_parallel(agents_instructions, affaire_uuid, user_uuid)
            return {
                "agent_results": results,
                "subtask_results": {"T1": results},
                "agent_run_ids": run_ids,
            }

        agent_results: dict = {}
        subtask_results: dict = {}
        all_run_ids: list = []

        levels = _topological_levels(subtasks)
        log.info("orchestra.dispatch_levels", levels=[[s["id"] for s in lvl] for lvl in levels])

        for level in levels:
            # Exécuter toutes les sous-tâches de ce niveau en parallèle entre elles
            level_tasks = []
            for st in level:
                instruction = st.get("instruction") or state["instruction"]
                pattern = st.get("pattern", "parallel")
                agents = st["agents"]
                judge = st.get("judge", "")

                # Injecter les résultats des dépendances dans l'instruction
                deps_results = {}
                for dep_id in st.get("depends_on", []):
                    deps_results.update(subtask_results.get(dep_id, {}))
                if deps_results:
                    deps_text = "\n\n".join(f"### {a}\n{r}" for a, r in deps_results.items())
                    instruction = (
                        f"{instruction}\n\n"
                        f"## Résultats des sous-tâches précédentes\n{deps_text}"
                    )

                if pattern == "cascade":
                    level_tasks.append((st["id"], _exec_cascade(agents, instruction, affaire_uuid, user_uuid)))
                elif pattern == "arena":
                    eff_judge = judge if judge in VALID_AGENTS else "apollon"
                    level_tasks.append((st["id"], _exec_arena(agents, eff_judge, instruction, affaire_uuid, user_uuid)))
                elif pattern == "solo":
                    single_agent = agents[0]
                    level_tasks.append((st["id"], _exec_parallel({single_agent: instruction}, affaire_uuid, user_uuid)))
                else:  # parallel (default)
                    # Utiliser les instructions personnalisées par agent si disponibles
                    agent_instrs = st.get("_agent_instructions", {a: instruction for a in agents})
                    level_tasks.append((st["id"], _exec_parallel(agent_instrs, affaire_uuid, user_uuid)))

            # Lancer toutes les sous-tâches du niveau en parallèle
            level_coros = [coro for _, coro in level_tasks]
            level_ids = [tid for tid, _ in level_tasks]
            level_results = await asyncio.gather(*level_coros, return_exceptions=True)

            for task_id, result in zip(level_ids, level_results):
                if isinstance(result, Exception):
                    log.error("orchestra.subtask_failed", task_id=task_id, error=str(result))
                    continue
                task_agent_results, task_run_ids = result
                subtask_results[task_id] = task_agent_results
                agent_results.update(task_agent_results)
                all_run_ids.extend(task_run_ids)

        log.info("orchestra.dispatch_done", agents=list(agent_results.keys()))
        return {
            "agent_results": agent_results,
            "subtask_results": subtask_results,
            "agent_run_ids": all_run_ids,
        }

    async def zeus_judge(state: OrchestraState) -> dict:
        """Phase 4a — Zeus juge si les résultats sont complets."""
        results_text = "\n\n".join(
            f"### {agent}\n{result}"
            for agent, result in state["agent_results"].items()
        )
        prompt = _ZEUS_JUDGE_PROMPT.format(
            instruction=state["instruction"],
            results=results_text,
        )
        content = await _llm_call(_zeus_system(), prompt)
        parsed = _parse_json_response(content)

        verdict = parsed.get("verdict", "complete")
        complements = parsed.get("complement_requests", [])
        synthesis_instruction = parsed.get("synthesis_instruction", state["instruction"])

        # Si déjà fait un complément, forcer "complete"
        if state.get("complement_done"):
            verdict = "complete"

        log.info("orchestra.zeus_verdict", verdict=verdict, complements=len(complements))
        return {
            "assignments": complements if verdict == "needs_complement" else state["assignments"],
            "synthesis_agent": state.get("synthesis_agent", "mnemosyne"),
            "instruction": synthesis_instruction if verdict == "complete" else state["instruction"],
            "verdict": verdict,
        }

    async def execute_complements(state: OrchestraState) -> dict:
        """Phase 3b — exécution des compléments demandés par Zeus."""
        log.info("orchestra.complements", agents=[a["agent"] for a in state["assignments"]])
        tasks = [
            _run_agent_isolated(
                agent=a["agent"],
                instruction=a["instruction"],
                affaire_id=affaire_uuid,
                user_id=user_uuid,
            )
            for a in state["assignments"]
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        agent_results = dict(state["agent_results"])  # merge
        agent_run_ids = list(state["agent_run_ids"])
        for r in results:
            if isinstance(r, Exception):
                continue
            agent_name, result_text, run_id = r
            agent_results[agent_name] = result_text
            agent_run_ids.append(run_id)

        return {"agent_results": agent_results, "agent_run_ids": agent_run_ids, "complement_done": True}

    async def synthesize(state: OrchestraState) -> dict:
        """Phase 4b — un agent produit la synthèse finale."""
        synthesis_agent = state.get("synthesis_agent", "mnemosyne")
        results_text = "\n\n".join(
            f"### {agent}\n{result}"
            for agent, result in state["agent_results"].items()
        )
        synthesis_instruction = _SYNTHESIS_PROMPT_TEMPLATE.format(
            synthesis_instruction=state.get("instruction", "Synthétise les analyses."),
            instruction=state["instruction"],
            results=results_text,
        )
        log.info("orchestra.synthesize", agent=synthesis_agent)

        _, final_answer, run_id = await _run_agent_isolated(
            agent=synthesis_agent,
            instruction=synthesis_instruction,
            affaire_id=affaire_uuid,
            user_id=user_uuid,
        )
        agent_run_ids = list(state["agent_run_ids"]) + [run_id]
        return {"final_answer": final_answer, "agent_run_ids": agent_run_ids}

    async def veto_check(state: OrchestraState) -> dict:
        """
        Nœud veto — après execute_agents, vérifie si Thémis ou Héphaïstos
        ont émis un veto dans leurs résultats.
        Si veto détecté ET criticité C5 → interruption HITL obligatoire.
        """
        _VETO_KEYWORDS = ("veto", "🚫", "infaisable", "bloque", "hors responsabilité", "risque majeur")
        results = state.get("agent_results", {})
        criticite = state.get("criticite", "C2")

        veto_agent = ""
        veto_motif = ""

        for agent_name in ("themis", "hephaistos"):
            result_text = results.get(agent_name, "").lower()
            if any(kw in result_text for kw in _VETO_KEYWORDS):
                veto_agent = agent_name
                # Extraire un extrait du motif (100 premiers chars après le mot-clé)
                for kw in _VETO_KEYWORDS:
                    idx = result_text.find(kw)
                    if idx >= 0:
                        veto_motif = results.get(agent_name, "")[max(0, idx-20):idx+200].strip()
                        break
                break

        if veto_agent and criticite in ("C4", "C5"):
            log.warning("orchestra.veto_detected", agent=veto_agent, criticite=criticite)
            # Interruption HITL obligatoire
            hitl_payload = {
                "veto_agent": veto_agent,
                "veto_motif": veto_motif,
                "message": f"⚠️ Veto émis par {veto_agent.upper()} — validation humaine requise avant de poursuivre.",
                "assignments": state.get("assignments", []),
            }
            interrupt(hitl_payload)

        return {"veto_agent": veto_agent, "veto_motif": veto_motif}

    return plan_agents, zeus_distribute, dispatch_subtasks, zeus_judge, execute_complements, synthesize, veto_check


def _route_after_judge(state: OrchestraState) -> str:
    if state.get("verdict") == "needs_complement" and not state.get("complement_done"):
        return "execute_complements"
    return "synthesize"


# ── Graph factory ────────────────────────────────────────────────

def build_graph(affaire_id: UUID, user_id: UUID | None):
    plan_agents, zeus_distribute, dispatch_subtasks, zeus_judge, execute_complements, synthesize, veto_check = \
        _make_nodes(affaire_id, user_id)

    builder = StateGraph(OrchestraState)
    builder.add_node("plan_agents", plan_agents)
    builder.add_node("zeus_distribute", zeus_distribute)
    builder.add_node("dispatch_subtasks", dispatch_subtasks)
    builder.add_node("veto_check", veto_check)
    builder.add_node("zeus_judge", zeus_judge)
    builder.add_node("execute_complements", execute_complements)
    builder.add_node("synthesize", synthesize)

    builder.set_entry_point("plan_agents")
    builder.add_edge("plan_agents", "zeus_distribute")
    builder.add_edge("zeus_distribute", "dispatch_subtasks")
    builder.add_edge("dispatch_subtasks", "veto_check")
    builder.add_edge("veto_check", "zeus_judge")
    builder.add_conditional_edges("zeus_judge", _route_after_judge, {
        "execute_complements": "execute_complements",
        "synthesize": "synthesize",
    })
    builder.add_edge("execute_complements", "synthesize")
    builder.add_edge("synthesize", END)

    return builder.compile()


# ── Point d'entrée principal ────────────────────────────────────────

async def run_orchestra(
    db: AsyncSession,
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    agents: list[str] | None = None,
    criticite: str = "C2",
) -> OrchestraRun:
    t_start = time.monotonic()

    initial_agents = [a for a in (agents or DEFAULT_AGENTS) if a in VALID_AGENTS] or DEFAULT_AGENTS
    log.info("orchestra.start", agents=initial_agents, affaire_id=str(affaire_id))

    # Routing criticité
    criticite = criticite if criticite in CRITICITE_ROUTING else "C2"
    routing = CRITICITE_ROUTING[criticite]
    hitl_auto = routing["hitl"]

    # Persister le run
    run = OrchestraRun(
        affaire_id=affaire_id,
        user_id=user_id,
        instruction=instruction,
        initial_agents=initial_agents,
        criticite=criticite,
        status="running",
    )
    db.add(run)
    await db.flush()

    try:
        graph = build_graph(affaire_id, user_id)
        initial_state: OrchestraState = {
            "instruction": instruction,
            "affaire_id": str(affaire_id),
            "user_id": str(user_id) if user_id else None,
            "initial_agents": initial_agents,
            "agent_plans": {},
            "zeus_reasoning": "",
            "subtasks": [],
            "subtask_results": {},
            "assignments": [],
            "synthesis_agent": "mnemosyne",
            "agent_results": {},
            "agent_run_ids": [],
            "complement_done": False,
            "final_answer": "",
            "verdict": "",
            "criticite": criticite,
            "veto_agent": "",
            "veto_motif": "",
            "hitl_enabled": hitl_auto,
            "hitl_approval": {},
        }

        final_state = await graph.ainvoke(initial_state)

        run.agent_plans    = final_state.get("agent_plans", {})
        run.zeus_reasoning = final_state.get("zeus_reasoning", "")
        run.assignments    = final_state.get("assignments", [])
        run.agent_results  = final_state.get("agent_results", {})
        run.agent_run_ids  = final_state.get("agent_run_ids", [])
        run.final_answer   = final_state.get("final_answer", "")
        run.synthesis_agent = final_state.get("synthesis_agent", "mnemosyne")
        run.status = "completed"

    except Exception as exc:
        log.error("orchestra.failed", run_id=str(run.id), error=str(exc))
        run.status = "failed"
        run.final_answer = f"Erreur lors de l'orchestration : {exc}"

    finally:
        run.duration_ms = int((time.monotonic() - t_start) * 1000)
        await db.commit()
        await db.refresh(run)

    log.info(
        "orchestra.complete",
        run_id=str(run.id),
        status=run.status,
        agents=list(run.agent_results.keys()),
        duration_ms=run.duration_ms,
    )
    return run


async def run_orchestra_from_run_id(
    db: AsyncSession,
    run_id: UUID,
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    agents: list[str] | None = None,
) -> OrchestraRun:
    """
    Variante utilisée par le worker ARQ : le run existe déjà en DB (status=queued).
    Met à jour son statut et exécute le graphe.
    """
    run = await db.get(OrchestraRun, run_id)
    if not run:
        log.error("orchestra.run_not_found", run_id=str(run_id))
        raise ValueError(f"OrchestraRun {run_id} introuvable")

    initial_agents = [a for a in (agents or DEFAULT_AGENTS) if a in VALID_AGENTS] or DEFAULT_AGENTS
    run.status = "running"
    run.initial_agents = initial_agents
    await db.commit()

    t_start = time.monotonic()
    try:
        graph = build_graph(affaire_id, user_id)
        initial_state: OrchestraState = {
            "instruction": instruction,
            "affaire_id": str(affaire_id),
            "user_id": str(user_id) if user_id else None,
            "initial_agents": initial_agents,
            "agent_plans": {}, "zeus_reasoning": "",
            "subtasks": [], "subtask_results": {},
            "assignments": [], "synthesis_agent": "mnemosyne",
            "agent_results": {}, "agent_run_ids": [],
            "complement_done": False, "final_answer": "", "verdict": "",
            "criticite": "C2", "veto_agent": "", "veto_motif": "",
            "hitl_enabled": False, "hitl_approval": {},
        }
        final_state = await graph.ainvoke(initial_state)

        run.agent_plans = final_state.get("agent_plans", {})
        run.zeus_reasoning = final_state.get("zeus_reasoning", "")
        run.assignments = final_state.get("assignments", [])
        run.agent_results = final_state.get("agent_results", {})
        run.agent_run_ids = final_state.get("agent_run_ids", [])
        run.final_answer = final_state.get("final_answer", "")
        run.synthesis_agent = final_state.get("synthesis_agent", "mnemosyne")
        run.status = "completed"
    except Exception as exc:
        log.error("orchestra.worker_failed", run_id=str(run_id), error=str(exc))
        run.status = "failed"
        run.final_answer = f"Erreur : {exc}"
    finally:
        run.duration_ms = int((time.monotonic() - t_start) * 1000)
        await db.commit()
        await db.refresh(run)

    return run


# ── Human-in-the-loop ────────────────────────────────────────────────

async def run_orchestra_hitl(
    db: AsyncSession,
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    agents: list[str] | None = None,
) -> OrchestraRun:
    """
    Lance une orchestration avec pause HITL après la distribution Zeus.
    Retourne avec status="awaiting_approval" et hitl_payload={reasoning, assignments}.
    Reprendre avec resume_orchestra().
    """
    from core.checkpointer import get_checkpointer

    initial_agents = [a for a in (agents or DEFAULT_AGENTS) if a in VALID_AGENTS] or DEFAULT_AGENTS
    thread_id = str(__import__("uuid").uuid4())

    run = OrchestraRun(
        affaire_id=affaire_id,
        user_id=user_id,
        instruction=instruction,
        initial_agents=initial_agents,
        status="running",
        hitl_enabled=True,
        checkpoint_thread_id=thread_id,
    )
    db.add(run)
    await db.flush()

    initial_state: OrchestraState = {
        "instruction": instruction,
        "affaire_id": str(affaire_id),
        "user_id": str(user_id) if user_id else None,
        "initial_agents": initial_agents,
        "agent_plans": {}, "zeus_reasoning": "",
        "subtasks": [], "subtask_results": {},
        "assignments": [], "synthesis_agent": "mnemosyne",
        "agent_results": {}, "agent_run_ids": [],
        "complement_done": False, "final_answer": "", "verdict": "",
        "criticite": "C4", "veto_agent": "", "veto_motif": "",
        "hitl_enabled": True, "hitl_approval": {},
    }
    config = {"configurable": {"thread_id": thread_id}}

    try:
        async with get_checkpointer() as cp:
            graph = build_graph(affaire_id, user_id)
            compiled = graph.compile(checkpointer=cp)
            # Le graphe s'arrête sur interrupt() dans zeus_distribute
            state = await compiled.ainvoke(initial_state, config)

            # Vérifier si le graphe est suspendu (interrupt)
            graph_state = await compiled.aget_state(config)
            if graph_state.next:
                # Suspendu — récupérer le payload de l'interrupt
                interrupt_data = {}
                for task in graph_state.tasks:
                    if hasattr(task, "interrupts") and task.interrupts:
                        interrupt_data = task.interrupts[0].value
                        break

                run.status = "awaiting_approval"
                run.hitl_payload = interrupt_data
                run.zeus_reasoning = interrupt_data.get("reasoning", "")
                run.assignments = interrupt_data.get("assignments", [])
            else:
                # Complété sans interruption (cas inattendu)
                run.status = "completed"
                run.final_answer = state.get("final_answer", "")
                run.agent_results = state.get("agent_results", {})

    except Exception as exc:
        log.error("orchestra.hitl_failed", run_id=str(run.id), error=str(exc))
        run.status = "failed"

    await db.commit()
    await db.refresh(run)
    return run


async def resume_orchestra(
    db: AsyncSession,
    run_id: UUID,
    approved: bool,
    feedback: str | None = None,
    modified_assignments: list[dict] | None = None,
) -> OrchestraRun:
    """
    Reprend un run en attente de validation humaine.
    Si approved=False, le run est annulé.
    """
    from core.checkpointer import get_checkpointer

    run = await db.get(OrchestraRun, run_id)
    if not run or run.status != "awaiting_approval":
        raise ValueError(f"Run {run_id} n'est pas en attente de validation")

    if not approved:
        run.status = "cancelled"
        run.final_answer = f"Annulé par l'utilisateur. Feedback : {feedback or '—'}"
        await db.commit()
        await db.refresh(run)
        return run

    t_start = time.monotonic()
    run.status = "running"
    await db.commit()

    config = {"configurable": {"thread_id": run.checkpoint_thread_id}}
    approval_data = {
        "approved": True,
        "feedback": feedback,
        "modified_assignments": modified_assignments,
    }

    try:
        async with get_checkpointer() as cp:
            graph = build_graph(run.affaire_id, run.user_id)
            compiled = graph.compile(checkpointer=cp)
            final_state = await compiled.ainvoke(Command(resume=approval_data), config)

        run.agent_plans = final_state.get("agent_plans", {})
        run.zeus_reasoning = final_state.get("zeus_reasoning", "")
        run.assignments = final_state.get("assignments", [])
        run.agent_results = final_state.get("agent_results", {})
        run.agent_run_ids = final_state.get("agent_run_ids", [])
        run.final_answer = final_state.get("final_answer", "")
        run.synthesis_agent = final_state.get("synthesis_agent", "mnemosyne")
        run.status = "completed"

    except Exception as exc:
        log.error("orchestra.resume_failed", run_id=str(run_id), error=str(exc))
        run.status = "failed"
        run.final_answer = f"Erreur lors de la reprise : {exc}"

    finally:
        run.duration_ms = int((time.monotonic() - t_start) * 1000)
        await db.commit()
        await db.refresh(run)

    return run


# ── SSE Streaming ────────────────────────────────────────────────────

# Mapping nœud LangGraph → label SSE lisible
_NODE_LABELS = {
    "plan_agents":          ("planning",   "Collecte des plans agents..."),
    "zeus_distribute":      ("zeus",       "Zeus organise les sous-tâches..."),
    "dispatch_subtasks":    ("executing",  "Exécution des agents (cascade / arène / parallèle)..."),
    "veto_check":           ("veto",       "Vérification veto Thémis / Héphaïstos..."),
    "execute_complements":  ("executing",  "Compléments en cours..."),
    "zeus_judge":           ("judging",    "Zeus juge les résultats..."),
    "synthesize":           ("synthesis",  "Synthèse en cours..."),
}


def _sse(event: str, data: dict) -> str:
    """Formate un événement SSE."""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def stream_orchestra(
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    agents: list[str] | None = None,
):
    """
    Générateur async SSE — yield les événements LangGraph au fil de l'exécution.

    Événements émis :
      phase_start   — début d'un nœud {phase, message}
      plans_ready   — fin plan_agents {plans}
      zeus_decision — fin zeus_distribute {reasoning, assignments, synthesis_agent}
      agents_done   — fin execute_agents {results}
      zeus_verdict  — fin zeus_judge {verdict}
      final_answer  — fin synthesize {answer, run_id}
      error         — exception {detail}
    """
    initial_agents = [a for a in (agents or DEFAULT_AGENTS) if a in VALID_AGENTS] or DEFAULT_AGENTS
    t_start = time.monotonic()

    # Créer le run DB avant de streamer
    async with AsyncSessionLocal() as db:
        run = OrchestraRun(
            affaire_id=affaire_id,
            user_id=user_id,
            instruction=instruction,
            initial_agents=initial_agents,
            status="running",
        )
        db.add(run)
        await db.flush()
        run_id = run.id
        await db.commit()

    yield _sse("run_created", {"run_id": str(run_id), "agents": initial_agents})

    graph = build_graph(affaire_id, user_id)
    initial_state: OrchestraState = {
        "instruction": instruction,
        "affaire_id": str(affaire_id),
        "user_id": str(user_id) if user_id else None,
        "initial_agents": initial_agents,
        "agent_plans": {},
        "zeus_reasoning": "",
        "subtasks": [],
        "subtask_results": {},
        "assignments": [],
        "synthesis_agent": "mnemosyne",
        "agent_results": {},
        "agent_run_ids": [],
        "complement_done": False,
        "final_answer": "",
        "verdict": "",
        "criticite": "C2",
        "veto_agent": "",
        "veto_motif": "",
        "hitl_enabled": False,
        "hitl_approval": {},
    }

    final_state: OrchestraState = initial_state.copy()

    try:
        # stream_mode="updates" → un dict {node_name: updates} par nœud terminé
        async for chunk in graph.astream(initial_state, stream_mode="updates"):
            for node_name, updates in chunk.items():
                # Annonce de début de phase (reconstituée depuis le nœud précédent)
                label, message = _NODE_LABELS.get(node_name, (node_name, f"Phase {node_name}..."))
                yield _sse("phase_start", {"phase": label, "node": node_name, "message": message})

                # Mise à jour de l'état cumulé
                final_state.update(updates)

                # Événements sémantiques selon le nœud
                if node_name == "plan_agents":
                    yield _sse("plans_ready", {
                        "plans": {
                            agent: {
                                "plan": p.get("plan", ""),
                                "expected_output": p.get("expected_output", ""),
                            }
                            for agent, p in updates.get("agent_plans", {}).items()
                        }
                    })

                elif node_name == "zeus_distribute":
                    yield _sse("zeus_decision", {
                        "reasoning": updates.get("zeus_reasoning", ""),
                        "subtasks": updates.get("subtasks", []),
                        "assignments": updates.get("assignments", []),
                        "synthesis_agent": updates.get("synthesis_agent", "mnemosyne"),
                    })

                elif node_name in ("dispatch_subtasks", "execute_complements"):
                    # Émettre un événement par sous-tâche si disponible
                    subtask_results = updates.get("subtask_results", {})
                    if subtask_results:
                        for task_id, task_res in subtask_results.items():
                            yield _sse("subtask_done", {
                                "task_id": task_id,
                                "agents": list(task_res.keys()),
                                "results": {a: r[:500] for a, r in task_res.items()},
                            })
                    yield _sse("agents_done", {
                        "results": {
                            agent: result[:500]
                            for agent, result in updates.get("agent_results", {}).items()
                        }
                    })

                elif node_name == "zeus_judge":
                    yield _sse("zeus_verdict", {
                        "verdict": updates.get("verdict", "complete"),
                        "complement_requested": updates.get("verdict") == "needs_complement",
                    })

                elif node_name == "synthesize":
                    yield _sse("final_answer", {
                        "answer": updates.get("final_answer", ""),
                        "run_id": str(run_id),
                    })

        # Persister l'état final
        async with AsyncSessionLocal() as db:
            run = await db.get(OrchestraRun, run_id)
            if run:
                run.agent_plans = final_state.get("agent_plans", {})
                run.zeus_reasoning = final_state.get("zeus_reasoning", "")
                run.assignments = final_state.get("assignments", [])
                run.agent_results = final_state.get("agent_results", {})
                run.agent_run_ids = final_state.get("agent_run_ids", [])
                run.final_answer = final_state.get("final_answer", "")
                run.synthesis_agent = final_state.get("synthesis_agent", "mnemosyne")
                run.status = "completed"
                run.duration_ms = int((time.monotonic() - t_start) * 1000)
                await db.commit()

        yield _sse("done", {
            "run_id": str(run_id),
            "duration_ms": int((time.monotonic() - t_start) * 1000),
        })

    except Exception as exc:
        log.error("orchestra.stream_failed", run_id=str(run_id), error=str(exc))
        async with AsyncSessionLocal() as db:
            run = await db.get(OrchestraRun, run_id)
            if run:
                run.status = "failed"
                run.duration_ms = int((time.monotonic() - t_start) * 1000)
                await db.commit()
        yield _sse("error", {"detail": str(exc), "run_id": str(run_id)})
