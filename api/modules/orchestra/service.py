"""
OrchestraService — boucle de coordination multi-agents via LangGraph.

Graphe Zeus :
  [plan_agents] → [zeus_distribute] → [execute_agents] → [zeus_judge]
                                                               │
                                          ┌────────────────────┘
                                          │ needs_complement
                                          ▼
                                   [execute_complements] → [synthesize]
                                          │ complete
                                          ▼
                                      [synthesize]
"""
import asyncio
import json
import time
from pathlib import Path
from typing import TypedDict, Optional
from uuid import UUID

from langgraph.graph import StateGraph, END
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.llm_service import LlmService
from core.settings import settings
from database import AsyncSessionLocal
from modules.agent.service import run_agent, _build_system_prompt
from modules.orchestra.models import OrchestraRun

log = get_logger("orchestra.service")

AGENTS_DIR = Path(settings.AGENTS_DIR) if hasattr(settings, "AGENTS_DIR") else Path(__file__).parent.parent.parent.parent / "agents"
DEFAULT_AGENTS = ["themis", "argus", "athena"]
VALID_AGENTS = {"themis", "argus", "hermes", "mnemosyne", "athena"}

# ── Prompts Zeus ────────────────────────────────────────────────────

_ZEUS_PLAN_PROMPT = """\
Tu reçois une demande et les plans de {n} agents. Distribue les rôles.

## Demande
{instruction}

## Plans des agents
{plans}

Réponds en JSON strict (aucun texte en dehors) :
{{
  "reasoning": "...",
  "assignments": [
    {{"agent": "<nom>", "instruction": "<instruction autonome complète>", "priority": 1}}
  ],
  "synthesis_agent": "<nom>"
}}
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

    # Phase 2
    zeus_reasoning: str
    assignments: list           # [{agent, instruction, priority}]
    synthesis_agent: str

    # Phase 3
    agent_results: dict         # {agent_name: result_text}
    agent_run_ids: list         # UUIDs des AgentRun créés

    # Phase 3b — compléments (optionnel, une fois)
    complement_done: bool

    # Phase 4
    final_answer: str


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
        """Phase 2 — Zeus analyse les plans et redistribue les rôles."""
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

        assignments = parsed.get("assignments", [])
        # Fallback : si Zeus ne retourne rien, relancer les agents initiaux tel quel
        if not assignments:
            assignments = [
                {"agent": a, "instruction": state["instruction"], "priority": 1}
                for a in state["initial_agents"]
            ]

        # Filtrer les agents invalides
        assignments = [a for a in assignments if a.get("agent") in VALID_AGENTS]

        log.info("orchestra.zeus_distributed", assignments=[a["agent"] for a in assignments])
        return {
            "zeus_reasoning": parsed.get("reasoning", ""),
            "assignments": assignments,
            "synthesis_agent": parsed.get("synthesis_agent", "mnemosyne"),
        }

    async def execute_agents(state: OrchestraState) -> dict:
        """Phase 3 — exécution parallèle des agents assignés."""
        log.info("orchestra.execute", agents=[a["agent"] for a in state["assignments"]])

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

        agent_results = {}
        agent_run_ids = []
        for r in results:
            if isinstance(r, Exception):
                log.error("orchestra.agent_failed", error=str(r))
                continue
            agent_name, result_text, run_id = r
            agent_results[agent_name] = result_text
            agent_run_ids.append(run_id)

        log.info("orchestra.execution_done", agents=list(agent_results.keys()))
        return {"agent_results": agent_results, "agent_run_ids": agent_run_ids}

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
            # stocker le verdict dans agent_results temporairement pour le routing
            "_verdict": verdict,
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

    return plan_agents, zeus_distribute, execute_agents, zeus_judge, execute_complements, synthesize


def _route_after_judge(state: OrchestraState) -> str:
    if state.get("_verdict") == "needs_complement" and not state.get("complement_done"):
        return "execute_complements"
    return "synthesize"


# ── Graph factory ────────────────────────────────────────────────

def build_graph(affaire_id: UUID, user_id: UUID | None):
    plan_agents, zeus_distribute, execute_agents, zeus_judge, execute_complements, synthesize = \
        _make_nodes(affaire_id, user_id)

    builder = StateGraph(OrchestraState)
    builder.add_node("plan_agents", plan_agents)
    builder.add_node("zeus_distribute", zeus_distribute)
    builder.add_node("execute_agents", execute_agents)
    builder.add_node("zeus_judge", zeus_judge)
    builder.add_node("execute_complements", execute_complements)
    builder.add_node("synthesize", synthesize)

    builder.set_entry_point("plan_agents")
    builder.add_edge("plan_agents", "zeus_distribute")
    builder.add_edge("zeus_distribute", "execute_agents")
    builder.add_edge("execute_agents", "zeus_judge")
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
) -> OrchestraRun:
    t_start = time.monotonic()

    initial_agents = [a for a in (agents or DEFAULT_AGENTS) if a in VALID_AGENTS] or DEFAULT_AGENTS
    log.info("orchestra.start", agents=initial_agents, affaire_id=str(affaire_id))

    # Persister le run
    run = OrchestraRun(
        affaire_id=affaire_id,
        user_id=user_id,
        instruction=instruction,
        initial_agents=initial_agents,
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
            "assignments": [],
            "synthesis_agent": "mnemosyne",
            "agent_results": {},
            "agent_run_ids": [],
            "complement_done": False,
            "final_answer": "",
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
