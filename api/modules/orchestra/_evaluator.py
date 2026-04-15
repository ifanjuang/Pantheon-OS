"""
Orchestra — nœuds d'évaluation (M2).

  zeus_judge   : Zeus juge si les résultats couvrent la demande (loop guard intégré)
  veto_check   : veto structuré Thémis/Héphaïstos/Apollon (layer 0 regex + LLM Instructor)
  score_decision : scoring décisionnel 100pts/5axes pour C4/C5
"""
from uuid import UUID

from ._shared import (
    OrchestraState,
    CRITICITE_ROUTING,
    _llm_call,
    _parse_json_response,
    _zeus_system,
    log,
)

# ── Prompt Zeus juge ─────────────────────────────────────────────────

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


# ── Nœuds LangGraph ──────────────────────────────────────────────────

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

    # Loop guard (M2 — guards module) : empêche les boucles
    # d'enrichissement infinies. Le seuil max_complements dépend de la
    # criticité : C1/C2 = 0, C3 = 1, C4 = 2, C5 = 3.
    from modules.guards.service import GuardsService, MAX_COMPLEMENTS_BY_CRITICITE
    _criticite = state.get("criticite", "C3")
    _max = MAX_COMPLEMENTS_BY_CRITICITE.get(_criticite, 1)
    loop_verdict = GuardsService.loop_guard(state, max_complements=_max)
    if not loop_verdict.should_continue and verdict == "needs_complement":
        log.info(
            "orchestra.loop_guard_stop",
            reason=loop_verdict.reason,
            iteration=loop_verdict.iteration,
        )
        verdict = "complete"

    log.info("orchestra.zeus_verdict", verdict=verdict, complements=len(complements))
    return {
        "assignments": complements if verdict == "needs_complement" else state["assignments"],
        "synthesis_agent": state.get("synthesis_agent", "mnemosyne"),
        "instruction": synthesis_instruction if verdict == "complete" else state["instruction"],
        "verdict": verdict,
    }


async def veto_check(state: OrchestraState) -> dict:
    """Nœud veto — délègue à GuardsService.structured_veto (M2).

    Analyse LLM (Instructor) des sorties Thémis / Héphaïstos / Apollon
    pour détecter un veto structuré (vs détection keyword fragile).
    Retourne le veto le plus sévère (bloquant > reserve > information).

    Si veto.severity == "bloquant" ET criticité C4/C5 → interrupt HITL.
    Pour C3, on trace le veto mais on continue (décision réversible).
    """
    from langgraph.types import interrupt
    from modules.guards.service import GuardsService

    criticite = state.get("criticite", "C2")
    routing = CRITICITE_ROUTING.get(criticite, CRITICITE_ROUTING["C2"])
    if not routing.get("veto_check"):
        log.info("orchestra.veto_skipped", criticite=criticite)
        return {
            "veto_agent": "",
            "veto_motif": "",
            "veto_severity": "",
            "veto_condition_levee": "",
        }

    results = state.get("agent_results", {})
    # Ordre d'évaluation : Thémis (juridique) > Héphaïstos (technique) > Apollon (normatif)
    candidates = [a for a in ("themis", "hephaistos", "apollon") if results.get(a)]

    worst_veto = None
    for agent_name in candidates:
        decision = await GuardsService.structured_veto(
            agent=agent_name,
            agent_output=results.get(agent_name, ""),
            criticite=criticite,
        )
        if decision.veto and decision.severity == "bloquant":
            worst_veto = decision
            break  # priorité Thémis > Héphaïstos > Apollon
        if decision.veto and decision.severity == "reserve" and worst_veto is None:
            worst_veto = decision

    if worst_veto is None:
        return {
            "veto_agent": "",
            "veto_motif": "",
            "veto_severity": "",
            "veto_condition_levee": "",
        }

    update = {
        "veto_agent": worst_veto.agent,
        "veto_motif": worst_veto.motif,
        "veto_severity": worst_veto.severity,
        "veto_condition_levee": worst_veto.condition_levee,
    }

    # Interrupt HITL uniquement si veto bloquant ET criticité engageante
    if worst_veto.severity == "bloquant" and criticite in ("C4", "C5"):
        log.warning(
            "orchestra.veto_blocking",
            agent=worst_veto.agent,
            criticite=criticite,
            condition_levee=worst_veto.condition_levee[:120],
        )
        interrupt({
            "veto_agent": worst_veto.agent,
            "veto_motif": worst_veto.motif,
            "veto_severity": worst_veto.severity,
            "veto_condition_levee": worst_veto.condition_levee,
            "message": (
                f"⚠️ Veto bloquant émis par {worst_veto.agent.upper()} — "
                f"validation humaine requise.\n"
                f"Motif : {worst_veto.motif}\n"
                f"Condition de levée : {worst_veto.condition_levee or '—'}"
            ),
            "assignments": state.get("assignments", []),
        })
    else:
        log.info(
            "orchestra.veto_traced",
            agent=worst_veto.agent,
            severity=worst_veto.severity,
            criticite=criticite,
        )

    return update


async def score_decision(state: OrchestraState) -> dict:
    """Score automatique pour C4/C5 — appelle ScoringService.score_auto().
    Pour C1-C3, nœud passant (no-op)."""
    criticite = state.get("criticite", "C2")
    if criticite not in ("C4", "C5"):
        log.info("orchestra.score_skipped", criticite=criticite)
        return {}

    from modules.scoring.service import ScoringService
    from database import AsyncSessionLocal

    sujet = state["instruction"][:512]
    contexte = "\n\n".join(
        f"### {agent}\n{result}"
        for agent, result in state.get("agent_results", {}).items()
    )

    try:
        async with AsyncSessionLocal() as db:
            score = await ScoringService.score_auto(
                db,
                sujet=sujet,
                contexte=contexte,
                affaire_id=UUID(state["affaire_id"]) if state.get("affaire_id") else None,
                certitude=0.7,
                computed_by=UUID(state["user_id"]) if state.get("user_id") else None,
            )
        log.info(
            "orchestra.score_done",
            score_id=str(score.id),
            verdict=score.verdict,
            total=score.total_final,
        )
        return {
            "score_id": str(score.id),
            "score_verdict": score.verdict,
            "score_total": score.total_final,
        }
    except Exception as exc:
        log.error("orchestra.score_failed", error=str(exc))
        return {}
