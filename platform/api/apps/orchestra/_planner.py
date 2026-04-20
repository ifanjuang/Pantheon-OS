"""
Orchestra — nœuds de planification (M1).

  preprocess        : Hermès++ normalise la demande + lit la mémoire fonctionnelle
  workflow_precheck : gate entre zeus_distribute et dispatch (trim/upgrade/clarification/blocked)
  zeus_distribute   : Zeus planifie les sous-tâches depuis les capacités statiques des agents
                      (0 appel LLM supplémentaire — SOUL.md LRU cached)
"""

from ._shared import (
    OrchestraState,
    VALID_AGENTS,
    AGENT_TRIGGERS,
    COGNITIVE_LIMITS,
    _get_agent_summary,
    _llm_call,
    _parse_json_response,
    _zeus_system,
    log,
)


def _filter_agents_by_triggers(agents: list[str], criticite: str) -> list[str]:
    """Filtre les agents selon leurs conditions d'activation (amélioration 3).

    Un agent sans entrée dans AGENT_TRIGGERS est toujours activable.
    Un agent avec AGENT_TRIGGERS[agent] = [] n'est jamais activé automatiquement.
    Un agent avec AGENT_TRIGGERS[agent] = ["C4", "C5"] s'active seulement pour ces criticités.
    """
    result = []
    for agent in agents:
        triggers = AGENT_TRIGGERS.get(agent)
        if triggers is None:
            result.append(agent)
        elif criticite in triggers:
            result.append(agent)
        else:
            log.debug("orchestra.agent_trigger_blocked", agent=agent, criticite=criticite)
    return result

# ── Prompt Zeus unifié ───────────────────────────────────────────────

_ZEUS_UNIFIED_PROMPT = """\
Tu reçois une demande et les capacités de {n} agents disponibles.
Organise directement leur collaboration en sous-tâches adaptées.

## Demande
{instruction}

## Contraintes métier actives
{module_behaviors}

## Agents disponibles
{agent_capabilities}

Patterns disponibles :
- "solo"        : un agent seul
- "parallel"    : agents indépendants, en parallèle
- "cascade"     : séquence — chaque agent reçoit les résultats du précédent
- "arena"       : compétition — agents sur la même question, un juge tranche (exige "judge")
- "exploration" : pipeline créatif — Dionysos (options latérales) → Prométhée (critique) → Apollon (vérification)

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
- Prométhée systématiquement pour C4+
- Chronos si impact planning
- Agents disponibles : hermes, argos, athena, hephaistos, promethee, apollon, dionysos,
  themis, chronos, ares, hestia, mnemosyne, iris, aphrodite, dedale
"""


# ── Nœuds ────────────────────────────────────────────────────────────


async def preprocess(state: OrchestraState) -> dict:
    """M1 — Hermès++ : normalise la demande avant zeus_distribute.

    Produit PreprocessedInput (cleaned, reformulated, intent, missing_info,
    confidence, suggested_criticite). Si la confiance ≥ 0.5 et qu'une
    reformulation existe, l'instruction du graphe est remplacée par la
    version reformulée (plus précise pour les agents).

    M3 — lit la mémoire fonctionnelle (Redis TTL) pour enrichir l'hint
    affaire si un thread de session précédent existe.
    """
    from modules.preprocessing.service import PreprocessingService
    from modules.memory.service import FunctionalMemoryService

    affaire_hint = state.get("affaire_id") or None
    phase_hint: str | None = None
    domaine_hint: str | None = None

    thread_id = state.get("thread_id") or ""
    if thread_id:
        fn_ctx = await FunctionalMemoryService.get_context(thread_id)
        if fn_ctx:
            affaire_hint = affaire_hint or fn_ctx.get("affaire_id")
            phase_hint = fn_ctx.get("phase_projet")
            domaine_hint = fn_ctx.get("domaine")
            log.debug(
                "orchestra.preprocess_fn_context",
                thread_id=thread_id,
                keys=list(fn_ctx.keys()),
            )

    result = await PreprocessingService.preprocess(
        state["instruction"],
        affaire_hint=str(affaire_hint) if affaire_hint else None,
        phase_hint=phase_hint,
        domaine_hint=domaine_hint,
    )
    updates: dict = {"preprocessed_input": result.model_dump()}

    if result.confidence >= 0.5 and result.reformulated_question:
        reformulated = result.reformulated_question.strip()
        if reformulated and reformulated != state["instruction"]:
            updates["instruction"] = reformulated

    # M3 — persiste le preprocessed dans la fonctionnelle pour le run suivant
    if thread_id:
        await FunctionalMemoryService.set_context(
            thread_id,
            "last_preprocessed",
            result.model_dump(),
            ttl=3600,
        )
        if state.get("affaire_id"):
            await FunctionalMemoryService.set_context(
                thread_id,
                "affaire_id",
                state["affaire_id"],
                ttl=3600,
            )

    log.info(
        "orchestra.preprocess_done",
        intent=result.intent,
        confidence=round(result.confidence, 2),
        missing=len(result.missing_information),
    )
    return updates


async def workflow_precheck(state: OrchestraState) -> dict:
    """M1 — gate entre zeus_distribute et dispatch_subtasks.

    Évalue si le plan Zeus est bien dimensionné. Verdicts :
      approved | trim | upgrade  → dispatch_subtasks
      clarification | blocked    → END (final_answer = message)
    """
    from modules.preprocessing.schemas import PreprocessedInput
    from modules.preprocessing.service import PreprocessingService

    preprocessed = None
    raw = state.get("preprocessed_input")
    if raw:
        try:
            preprocessed = PreprocessedInput(**raw)
        except Exception:
            preprocessed = None

    decision = await PreprocessingService.precheck(
        instruction=state["instruction"],
        criticite=state.get("criticite", "C2"),
        subtasks=state.get("subtasks", []),
        preprocessed=preprocessed,
    )

    updates: dict = {
        "precheck_verdict": decision.verdict,
        "precheck_reasoning": decision.reasoning,
    }

    if decision.verdict == "trim" and decision.suggested_subtask_ids:
        keep = set(decision.suggested_subtask_ids)
        trimmed = [st for st in state.get("subtasks", []) if st.get("id") in keep]
        if trimmed:
            updates["subtasks"] = trimmed
            new_assignments: list = []
            for st in trimmed:
                for agent in st["agents"]:
                    new_assignments.append(
                        {
                            "agent": agent,
                            "instruction": st.get("instruction", state["instruction"]),
                            "priority": 1,
                        }
                    )
            updates["assignments"] = new_assignments

    if decision.verdict == "upgrade" and decision.suggested_criticite:
        updates["criticite"] = decision.suggested_criticite

    if decision.verdict in ("clarification", "blocked"):
        updates["final_answer"] = decision.clarification_message or (
            "Demande bloquée — reformulation nécessaire."
            if decision.verdict == "blocked"
            else "Précisez votre demande avant de continuer."
        )

    log.info(
        "orchestra.precheck_done",
        verdict=decision.verdict,
        criticite=updates.get("criticite", state.get("criticite")),
    )
    return updates


async def zeus_distribute(state: OrchestraState) -> dict:
    """Phase 1 — Zeus organise les sous-tâches depuis les capacités statiques des agents.

    Remplace l'ancien pipeline plan_agents (N appels LLM) + zeus_distribute :
    les capacités sont extraites de SOUL.md (LRU cache, 0 appel LLM) et
    transmises directement à Zeus pour la planification en une seule étape.

    Améliorations :
      - Amélioration 3 : filtre les agents selon AGENT_TRIGGERS + criticité
      - Amélioration 6 : plafonne le nombre d'agents selon COGNITIVE_LIMITS
    """
    from langgraph.types import interrupt

    criticite = state.get("criticite", "C2")
    limits = COGNITIVE_LIMITS.get(criticite, COGNITIVE_LIMITS["C2"])

    # ── Amélioration 3 : activation conditionnelle ────────────────────
    raw_agents = state["initial_agents"]
    agents = _filter_agents_by_triggers(raw_agents, criticite)
    if not agents:
        agents = [a for a in raw_agents if a in VALID_AGENTS] or list(VALID_AGENTS)[:2]

    # ── Amélioration 6 : limite cognitive max_agents ──────────────────
    max_agents = limits["max_agents"]
    if len(agents) > max_agents:
        log.info(
            "orchestra.cognitive_limit_agents",
            criticite=criticite,
            before=len(agents),
            after=max_agents,
        )
        agents = agents[:max_agents]

    agent_summaries = {a: _get_agent_summary(a) for a in agents}
    capabilities_text = "\n\n".join(f"### {agent}\n{summary}" for agent, summary in agent_summaries.items())

    # Behaviors des modules actifs — contraintes métier injectées dynamiquement
    module_behaviors = "(aucune contrainte spécifique)"
    try:
        from core.registry import registry as _reg

        if _reg is not None:
            behaviors = _reg.get_all_behaviors()
            if behaviors:
                module_behaviors = behaviors
    except Exception:
        pass  # Ne pas bloquer l'orchestration si le registry est inaccessible

    # ── Amélioration 6 : limites cognitives injectées dans le prompt ──
    limits_text = (
        f"Contraintes cognitives [{criticite}] : "
        f"max {max_agents} agents, "
        f"max {limits['max_subtasks']} sous-tâches, "
        f"profondeur max {limits['max_depth']} niveaux de dépendances."
    )

    prompt = _ZEUS_UNIFIED_PROMPT.format(
        n=len(agents),
        instruction=state["instruction"],
        agent_capabilities=capabilities_text,
        module_behaviors=f"{module_behaviors}\n\n{limits_text}",
    )
    content = await _llm_call(_zeus_system(), prompt)
    parsed = _parse_json_response(content)

    # ── Parsing subtasks ──────────────────────────────────────────────
    raw_subtasks = parsed.get("subtasks", [])
    subtasks = []
    for st in raw_subtasks:
        valid_agents = [a for a in st.get("agents", []) if a in VALID_AGENTS]
        if not valid_agents:
            continue
        judge = st.get("judge", "")
        if judge and judge not in VALID_AGENTS:
            judge = "apollon"
        subtasks.append(
            {
                "id": st.get("id", f"T{len(subtasks) + 1}"),
                "pattern": st.get("pattern", "parallel"),
                "agents": valid_agents,
                "judge": judge,
                "instruction": st.get("instruction", "") or state["instruction"],
                "depends_on": st.get("depends_on", []),
            }
        )

    # ── Fallback : ancien format assignments ──────────────────────────
    assignments = parsed.get("assignments", [])
    assignments = [a for a in assignments if a.get("agent") in VALID_AGENTS]

    if not subtasks and not assignments:
        assignments = [
            {"agent": a, "instruction": state["instruction"], "priority": 1} for a in state["initial_agents"]
        ]

    if not subtasks and assignments:
        subtasks = [
            {
                "id": "T1",
                "pattern": "parallel",
                "agents": [a["agent"] for a in assignments],
                "judge": "",
                "instruction": state["instruction"],
                "depends_on": [],
                "_agent_instructions": {a["agent"]: a.get("instruction", state["instruction"]) for a in assignments},
            }
        ]

    # Pour compat HITL/synthèse — aplatir subtasks → assignments
    if subtasks and not assignments:
        assignments = []
        for st in subtasks:
            for agent in st["agents"]:
                assignments.append(
                    {
                        "agent": agent,
                        "instruction": st["instruction"],
                        "priority": 1,
                    }
                )
            if st.get("judge"):
                assignments.append(
                    {
                        "agent": st["judge"],
                        "instruction": st["instruction"],
                        "priority": 2,
                    }
                )

    # ── Amélioration 6 : limite cognitive max_subtasks ───────────────
    max_subtasks = limits["max_subtasks"]
    if len(subtasks) > max_subtasks:
        log.info(
            "orchestra.cognitive_limit_subtasks",
            criticite=criticite,
            before=len(subtasks),
            after=max_subtasks,
        )
        subtasks = subtasks[:max_subtasks]

    log.info("orchestra.zeus_distributed", subtasks=[(s["id"], s["pattern"], s["agents"]) for s in subtasks])

    approval = {}
    if state.get("hitl_enabled"):
        approval = interrupt(
            {
                "message": "Zeus a planifié les sous-tâches. Validez pour lancer l'exécution.",
                "reasoning": parsed.get("reasoning", ""),
                "subtasks": subtasks,
                "assignments": assignments,
                "synthesis_agent": parsed.get("synthesis_agent", "mnemosyne"),
            }
        )
        if approval.get("modified_assignments"):
            assignments = [a for a in approval["modified_assignments"] if a.get("agent") in VALID_AGENTS] or assignments

    return {
        "zeus_reasoning": parsed.get("reasoning", ""),
        "subtasks": subtasks,
        "assignments": assignments,
        "synthesis_agent": parsed.get("synthesis_agent", "mnemosyne"),
        "hitl_approval": approval,
        "agent_summaries": agent_summaries,  # pour SSE plans_ready
    }
