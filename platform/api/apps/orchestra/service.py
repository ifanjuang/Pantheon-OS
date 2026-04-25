"""
OrchestraService — coordinateur LangGraph (graphe + points d'entrée).

Graphe Zeus :
  [preprocess] → [zeus_distribute] → [workflow_precheck]
                      ↑ HITL C4/C5   │ approved|trim|upgrade
                                     │ (clarification|blocked → END)
                                     ▼
                              [dispatch_subtasks] → [veto_check] → [zeus_judge]
                                                                       │ needs_complement
                                                         ┌─────────────┘
                                                         ▼
                                                [execute_complements] ─┐
                                                                       │ complete
                                                         ┌─────────────┘
                                                         ▼
                                                [score_decision] → [synthesize] → [write_memories] → END
                                                 (C4/C5 only)       synthèse       Hestia/Mnémosyne
                                                                                   + wiki C4/C5

Les nœuds sont définis dans les sous-modules :
  _planner    — preprocess, workflow_precheck, zeus_distribute
  _executor   — dispatch_subtasks, execute_complements
  _evaluator  — zeus_judge, veto_check, score_decision
  _synthesizer— synthesize, write_memories
"""

import json
import time
from uuid import UUID

import structlog
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from database import AsyncSessionLocal
from apps.orchestra.models import OrchestraRun

# ── Imports partagés (re-exportés pour router.py / worker.py) ────────
from ._shared import (
    OrchestraState,
    CRITICITE_ROUTING,
    VALID_AGENTS,
    DEFAULT_AGENTS,
    DEFAULT_SYNTHESIS_AGENT,
    get_agent_role,
    log,
)

# ── Nœuds M1 — planification ─────────────────────────────────────────
from ._planner import preprocess, workflow_precheck, zeus_distribute

# ── Nœuds M2 — exécution ─────────────────────────────────────────────
from ._executor import dispatch_subtasks, execute_complements

# ── Nœuds M2 — évaluation ────────────────────────────────────────────
from ._evaluator import zeus_judge, veto_check, score_decision

# ── Nœuds M4 — synthèse ──────────────────────────────────────────────
from ._synthesizer import synthesize, write_memories, hera_supervise, write_error_memory


# ── Routing conditionnel ─────────────────────────────────────────────


def _route_after_judge(state: OrchestraState) -> str:
    if state.get("verdict") == "needs_complement" and not state.get("complement_done"):
        return "execute_complements"
    return "score_decision"


def _route_after_precheck(state: OrchestraState) -> str:
    verdict = state.get("precheck_verdict", "approved")
    if verdict in ("clarification", "blocked"):
        return "end"
    return "dispatch_subtasks"


# ── Graph factory ────────────────────────────────────────────────────


def build_graph(affaire_id: UUID, user_id: UUID | None, checkpointer=None):
    """Construit et compile le graphe Zeus.

    Args:
        checkpointer: si fourni, le graphe est compilé avec persistence
                      (requis pour HITL pause/resume).
    """
    builder = StateGraph(OrchestraState)

    builder.add_node("preprocess", preprocess)
    builder.add_node("zeus_distribute", zeus_distribute)
    builder.add_node("workflow_precheck", workflow_precheck)
    builder.add_node("dispatch_subtasks", dispatch_subtasks)
    builder.add_node("veto_check", veto_check)
    builder.add_node("zeus_judge", zeus_judge)
    builder.add_node("execute_complements", execute_complements)
    builder.add_node("score_decision", score_decision)
    builder.add_node("synthesize", synthesize)
    builder.add_node("hera_supervise", hera_supervise)  # amélioration 4
    builder.add_node("write_memories", write_memories)

    builder.set_entry_point("preprocess")
    builder.add_edge("preprocess", "zeus_distribute")
    builder.add_edge("zeus_distribute", "workflow_precheck")
    builder.add_conditional_edges(
        "workflow_precheck",
        _route_after_precheck,
        {
            "dispatch_subtasks": "dispatch_subtasks",
            "end": END,
        },
    )
    builder.add_edge("dispatch_subtasks", "veto_check")
    builder.add_edge("veto_check", "zeus_judge")
    builder.add_conditional_edges(
        "zeus_judge",
        _route_after_judge,
        {
            "execute_complements": "execute_complements",
            "score_decision": "score_decision",
        },
    )
    builder.add_edge("execute_complements", "score_decision")
    builder.add_edge("score_decision", "synthesize")
    builder.add_edge("synthesize", "hera_supervise")  # amélioration 4 — supervision après synthèse
    builder.add_edge("hera_supervise", "write_memories")
    builder.add_edge("write_memories", END)

    return builder.compile(checkpointer=checkpointer)


# ── Helpers internes ─────────────────────────────────────────────────


def _build_initial_state(
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    initial_agents: list[str],
    criticite: str = "C2",
    hitl_enabled: bool = False,
    thread_id: str = "",
    orchestra_run_id: str = "",
) -> OrchestraState:
    """Construit l'état initial du graphe Zeus. Factorisé entre les 3 entry points."""
    return {
        "instruction": instruction,
        "affaire_id": str(affaire_id),
        "user_id": str(user_id) if user_id else None,
        "initial_agents": initial_agents,
        "agent_plans": {},
        "agent_summaries": {},
        "zeus_reasoning": "",
        "subtasks": [],
        "subtask_results": {},
        "assignments": [],
        "synthesis_agent": DEFAULT_SYNTHESIS_AGENT,
        "agent_results": {},
        "agent_run_ids": [],
        "complement_done": False,
        "final_answer": "",
        "verdict": "",
        "criticite": criticite,
        "veto_agent": "",
        "veto_motif": "",
        "veto_severity": "",
        "veto_condition_levee": "",
        "hitl_enabled": hitl_enabled,
        "hitl_approval": {},
        "score_id": "",
        "score_verdict": "",
        "score_total": 0,
        "memories_written": 0,
        "wiki_page_id": "",
        "preprocessed_input": {},
        "precheck_verdict": "",
        "precheck_reasoning": "",
        "thread_id": thread_id,
        "orchestra_run_id": orchestra_run_id,
        # Améliorations architecturales
        "run_score": {},
        "hera_verdict": "",
        "hera_feedback": "",
        "fallback_level": 0,
    }


def _persist_run_state(run: OrchestraRun, final_state: dict) -> None:
    """Copie l'état final du graphe dans le run DB."""
    run.agent_plans = final_state.get("agent_plans", {})
    run.zeus_reasoning = final_state.get("zeus_reasoning", "")
    run.assignments = final_state.get("assignments", [])
    run.agent_results = final_state.get("agent_results", {})
    run.agent_run_ids = final_state.get("agent_run_ids", [])
    run.final_answer = final_state.get("final_answer", "")
    run.synthesis_agent = final_state.get("synthesis_agent", "mnemosyne")
    run.subtasks = final_state.get("subtasks", [])
    run.subtask_results = final_state.get("subtask_results", {})
    run.veto_agent = final_state.get("veto_agent", "") or None
    run.veto_motif = final_state.get("veto_motif", "") or None
    run.veto_severity = final_state.get("veto_severity", "") or None
    run.veto_condition_levee = final_state.get("veto_condition_levee", "") or None
    run.score_id = final_state.get("score_id", "") or None
    run.score_verdict = final_state.get("score_verdict", "") or None
    run.score_total = final_state.get("score_total") or None
    run.memories_written = final_state.get("memories_written", 0)
    run.wiki_page_id = final_state.get("wiki_page_id", "") or None
    run.preprocessed_input = final_state.get("preprocessed_input") or None
    run.precheck_verdict = final_state.get("precheck_verdict", "") or None
    run.precheck_reasoning = final_state.get("precheck_reasoning", "") or None
    # Améliorations architecturales
    run.run_score = final_state.get("run_score") or None
    run.hera_verdict = final_state.get("hera_verdict", "") or None
    run.hera_feedback = final_state.get("hera_feedback", "") or None
    run.fallback_level = final_state.get("fallback_level", 0)


async def _safe_publish_event(event_type: str, run: OrchestraRun) -> None:
    """Publie un événement orchestra sur le bus PostgreSQL (best-effort)."""
    try:
        import core.events as events

        await events.publish(
            "orchestra_channel",
            {
                "event_type": event_type,
                "run_id": str(run.id),
                "affaire_id": str(run.affaire_id) if run.affaire_id else None,
                "status": run.status,
                "criticite": run.criticite,
                "veto_agent": run.veto_agent,
            },
        )
    except Exception:
        pass


# ── Fallback intelligent (amélioration 2) ────────────────────────────


async def _run_fallback_graph(
    affaire_id: UUID,
    user_id: UUID | None,
    instruction: str,
    agents: list[str],
    criticite: str,
    orchestra_run_id: str,
) -> dict | None:
    """Tente d'exécuter le graphe avec les paramètres donnés.

    Retourne l'état final ou None si l'exécution échoue.
    """
    try:
        graph = build_graph(affaire_id, user_id)
        state = _build_initial_state(
            instruction,
            affaire_id,
            user_id,
            agents,
            criticite,
            orchestra_run_id=orchestra_run_id,
        )
        final = await graph.ainvoke(state)
        return final if final.get("final_answer") else None
    except Exception as exc:
        log.warning("orchestra.fallback_graph_failed", error=str(exc))
        return None


async def _run_with_fallback(
    run: "OrchestraRun",
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    initial_agents: list[str],
    criticite: str,
) -> tuple[dict | None, int]:
    """3 niveaux de fallback si le run principal échoue (amélioration 2).

    Niveau 1 — simplification : agents par défaut seulement, même criticité
    Niveau 2 — stratégie alternative : agent unique athena, criticité abaissée à C2
    Niveau 3 — réponse dégradée : None (l'appelant génère un message d'échec)

    Retourne (final_state | None, fallback_level 1-3).
    """
    run_id = str(run.id)

    # Niveau 1 : agents réduits aux defaults
    simplified = [a for a in initial_agents if a in DEFAULT_AGENTS] or DEFAULT_AGENTS
    if simplified != initial_agents:
        log.info("orchestra.fallback_level1", run_id=run_id, agents=simplified)
        result = await _run_fallback_graph(affaire_id, user_id, instruction, simplified, criticite, run_id)
        if result:
            return result, 1

    # Niveau 2 : agent unique, criticité abaissée à C2
    single_agent = ["athena"] if criticite in ("C3", "C4", "C5") else ["hermes"]
    log.info("orchestra.fallback_level2", run_id=run_id, agents=single_agent)
    result = await _run_fallback_graph(affaire_id, user_id, instruction, single_agent, "C2", run_id)
    if result:
        return result, 2

    # Niveau 3 : réponse dégradée
    log.warning("orchestra.fallback_level3", run_id=run_id)
    return None, 3


# ── Points d'entrée ──────────────────────────────────────────────────


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
    criticite = criticite if criticite in CRITICITE_ROUTING else "C2"
    routing = CRITICITE_ROUTING[criticite]

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

    structlog.contextvars.bind_contextvars(run_id=str(run.id), run_type="orchestra")
    log.info("orchestra.start", agents=initial_agents, affaire_id=str(affaire_id), criticite=criticite)

    try:
        graph = build_graph(affaire_id, user_id)
        initial_state = _build_initial_state(
            instruction,
            affaire_id,
            user_id,
            initial_agents,
            criticite,
            routing["hitl"],
            orchestra_run_id=str(run.id),
        )
        final_state = await graph.ainvoke(initial_state)
        _persist_run_state(run, final_state)
        run.status = "completed"

    except Exception as exc:
        # ── Amélioration 2 : fallback intelligent 3 niveaux ──────────
        log.warning("orchestra.main_failed_trying_fallback", error=str(exc))
        fallback_state, fallback_level = await _run_with_fallback(
            run, instruction, affaire_id, user_id, initial_agents, criticite
        )
        if fallback_state:
            _persist_run_state(run, fallback_state)
            run.status = "completed"
            run.fallback_level = fallback_level
            log.info("orchestra.fallback_success", level=fallback_level)
        else:
            run.status = "failed"
            run.error_message = str(exc)
            run.fallback_level = 3
            run.final_answer = f"⚠️ Réponse dégradée (niveau 3) — l'orchestration n'a pu aboutir.\nErreur : {exc}"
            # ── Amélioration 5 : mémoire des erreurs ──────────────────
            await write_error_memory(exc, instruction, affaire_id, criticite)

    finally:
        run.duration_ms = int((time.monotonic() - t_start) * 1000)
        await db.commit()
        await db.refresh(run)
        structlog.contextvars.unbind_contextvars("run_id", "run_type")

    log.info(
        "orchestra.complete",
        run_id=str(run.id),
        status=run.status,
        agents=list(run.agent_results.keys()),
        veto_agent=run.veto_agent,
        duration_ms=run.duration_ms,
    )
    await _safe_publish_event("orchestra.completed", run)
    return run


async def run_orchestra_from_run_id(
    db: AsyncSession,
    run_id: UUID,
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    agents: list[str] | None = None,
    criticite: str | None = None,
) -> OrchestraRun:
    """Variante worker ARQ : le run existe déjà en DB (status=queued)."""
    run = await db.get(OrchestraRun, run_id)
    if not run:
        log.error("orchestra.run_not_found", run_id=str(run_id))
        raise ValueError(f"OrchestraRun {run_id} introuvable")

    initial_agents = [a for a in (agents or DEFAULT_AGENTS) if a in VALID_AGENTS] or DEFAULT_AGENTS
    effective_criticite = criticite or run.criticite or "C2"
    routing = CRITICITE_ROUTING.get(effective_criticite, CRITICITE_ROUTING["C2"])

    run.status = "running"
    run.initial_agents = initial_agents
    run.criticite = effective_criticite
    await db.commit()

    structlog.contextvars.bind_contextvars(run_id=str(run.id), run_type="orchestra.worker")
    log.info("orchestra.worker_start", agents=initial_agents, criticite=effective_criticite)

    t_start = time.monotonic()
    try:
        graph = build_graph(affaire_id, user_id)
        initial_state = _build_initial_state(
            instruction,
            affaire_id,
            user_id,
            initial_agents,
            effective_criticite,
            routing["hitl"],
            orchestra_run_id=str(run.id),
        )
        final_state = await graph.ainvoke(initial_state)
        _persist_run_state(run, final_state)
        run.status = "completed"
    except Exception as exc:
        # ── Amélioration 2 : fallback intelligent ──────────────────
        log.warning("orchestra.worker_failed_trying_fallback", error=str(exc))
        fallback_state, fallback_level = await _run_with_fallback(
            run, instruction, affaire_id, user_id, initial_agents, effective_criticite
        )
        if fallback_state:
            _persist_run_state(run, fallback_state)
            run.status = "completed"
            run.fallback_level = fallback_level
        else:
            run.status = "failed"
            run.error_message = str(exc)
            run.fallback_level = 3
            run.final_answer = f"⚠️ Réponse dégradée — orchestration impossible. Erreur : {exc}"
            await write_error_memory(exc, instruction, affaire_id, effective_criticite)
    finally:
        run.duration_ms = int((time.monotonic() - t_start) * 1000)
        await db.commit()
        await db.refresh(run)
        structlog.contextvars.unbind_contextvars("run_id", "run_type")

    await _safe_publish_event("orchestra.completed", run)
    return run


# ── Human-in-the-loop ────────────────────────────────────────────────


async def run_orchestra_hitl(
    db: AsyncSession,
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    agents: list[str] | None = None,
    criticite: str = "C4",
) -> OrchestraRun:
    """Lance une orchestration avec pause HITL après zeus_distribute."""
    from core.checkpointer import get_checkpointer
    import uuid as _uuid

    initial_agents = [a for a in (agents or DEFAULT_AGENTS) if a in VALID_AGENTS] or DEFAULT_AGENTS
    effective_criticite = criticite if criticite in CRITICITE_ROUTING else "C4"
    thread_id = str(_uuid.uuid4())

    run = OrchestraRun(
        affaire_id=affaire_id,
        user_id=user_id,
        instruction=instruction,
        initial_agents=initial_agents,
        criticite=effective_criticite,
        status="running",
        hitl_enabled=True,
        checkpoint_thread_id=thread_id,
    )
    db.add(run)
    await db.flush()

    structlog.contextvars.bind_contextvars(run_id=str(run.id), run_type="orchestra.hitl")
    initial_state = _build_initial_state(
        instruction,
        affaire_id,
        user_id,
        initial_agents,
        effective_criticite,
        hitl_enabled=True,
        thread_id=thread_id,
        orchestra_run_id=str(run.id),
    )
    config = {"configurable": {"thread_id": thread_id}}

    try:
        async with get_checkpointer() as cp:
            compiled = build_graph(affaire_id, user_id, checkpointer=cp)
            state = await compiled.ainvoke(initial_state, config)

            graph_state = await compiled.aget_state(config)
            if graph_state.next:
                interrupt_data = {}
                for task in graph_state.tasks:
                    if hasattr(task, "interrupts") and task.interrupts:
                        interrupt_data = task.interrupts[0].value
                        break

                run.status = "awaiting_approval"
                run.hitl_payload = interrupt_data
                run.zeus_reasoning = interrupt_data.get("reasoning", "")
                run.assignments = interrupt_data.get("assignments", [])
                run.subtasks = interrupt_data.get("subtasks", [])
            else:
                _persist_run_state(run, state)
                run.status = "completed"

    except Exception as exc:
        log.error("orchestra.hitl_failed", error=str(exc))
        run.status = "failed"
        run.error_message = str(exc)

    finally:
        await db.commit()
        await db.refresh(run)
        structlog.contextvars.unbind_contextvars("run_id", "run_type")

    await _safe_publish_event(
        "orchestra.hitl_paused" if run.status == "awaiting_approval" else "orchestra.completed",
        run,
    )
    return run


async def resume_orchestra(
    db: AsyncSession,
    run_id: UUID,
    approved: bool,
    feedback: str | None = None,
    modified_assignments: list[dict] | None = None,
) -> OrchestraRun:
    """Reprend un run en attente de validation humaine."""
    from core.checkpointer import get_checkpointer

    run = await db.get(OrchestraRun, run_id)
    if not run or run.status != "awaiting_approval":
        raise ValueError(f"Run {run_id} n'est pas en attente de validation")

    if not approved:
        run.status = "cancelled"
        run.final_answer = f"Annulé par l'utilisateur. Feedback : {feedback or '—'}"
        await db.commit()
        await db.refresh(run)
        await _safe_publish_event("orchestra.cancelled", run)
        return run

    structlog.contextvars.bind_contextvars(run_id=str(run.id), run_type="orchestra.resume")
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
            compiled = build_graph(run.affaire_id, run.user_id, checkpointer=cp)
            final_state = await compiled.ainvoke(Command(resume=approval_data), config)

        _persist_run_state(run, final_state)
        run.status = "completed"

    except Exception as exc:
        log.error("orchestra.resume_failed", error=str(exc))
        run.status = "failed"
        run.error_message = str(exc)
        run.final_answer = f"Erreur lors de la reprise : {exc}"

    finally:
        run.duration_ms = int((time.monotonic() - t_start) * 1000)
        await db.commit()
        await db.refresh(run)
        structlog.contextvars.unbind_contextvars("run_id", "run_type")

    await _safe_publish_event("orchestra.completed", run)
    return run


# ── SSE Streaming ────────────────────────────────────────────────────

_NODE_LABELS = {
    "preprocess": ("hermes.preprocess", "Hermès — normalisation et qualification..."),
    "workflow_precheck": ("hermes.precheck", "Hermès — gate precheck dimensionnement..."),
    "zeus_distribute": ("zeus.distribute", "Zeus — organisation des sous-tâches..."),
    "dispatch_subtasks": ("agent.execute", "Exécution agents (cascade / arène / parallèle)..."),
    "execute_complements": ("agent.execute", "Compléments en cours..."),
    "zeus_judge": ("zeus.judge", "Zeus — jugement des résultats..."),
    "veto_check": ("themis.veto", "Thémis — veto structuré (couche 0 + LLM)..."),
    "score_decision": ("hera.score", "Héra — scoring multi-critères..."),
    "synthesize": ("kairos.synthesize", "Kairos — synthèse finale actable..."),
    "hera_supervise": ("hera.supervise", "Héra — vérification cohérence globale..."),
    "write_memories": ("hestia.memories", "Hestia — écriture mémoires projet / agence..."),
}


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def stream_orchestra(
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    agents: list[str] | None = None,
    criticite: str = "C2",
):
    """Générateur async SSE — yield les événements LangGraph au fil de l'exécution."""
    initial_agents = [a for a in (agents or DEFAULT_AGENTS) if a in VALID_AGENTS] or DEFAULT_AGENTS
    effective_criticite = criticite if criticite in CRITICITE_ROUTING else "C2"
    t_start = time.monotonic()

    async with AsyncSessionLocal() as db:
        run = OrchestraRun(
            affaire_id=affaire_id,
            user_id=user_id,
            instruction=instruction,
            initial_agents=initial_agents,
            criticite=effective_criticite,
            status="running",
        )
        db.add(run)
        await db.flush()
        run_id = run.id
        await db.commit()

    yield _sse("run_created", {"run_id": str(run_id), "agents": initial_agents})

    graph = build_graph(affaire_id, user_id)
    initial_state = _build_initial_state(
        instruction,
        affaire_id,
        user_id,
        initial_agents,
        effective_criticite,
        thread_id=str(run_id),
        orchestra_run_id=str(run_id),
    )
    final_state: OrchestraState = initial_state.copy()

    try:
        async for chunk in graph.astream(initial_state, stream_mode="updates"):
            for node_name, updates in chunk.items():
                label, message = _NODE_LABELS.get(node_name, (node_name, f"Phase {node_name}..."))
                yield _sse("phase_start", {"phase": label, "node": node_name, "message": message})

                final_state.update(updates)

                if node_name == "preprocess":
                    pp = updates.get("preprocessed_input", {}) or {}
                    yield _sse(
                        "hermes.preprocess_ready",
                        {
                            "intent": pp.get("intent"),
                            "confidence": pp.get("confidence"),
                            "suggested_criticite": pp.get("suggested_criticite"),
                            "missing_information": pp.get("missing_information", []),
                            "reformulated_question": pp.get("reformulated_question", ""),
                        },
                    )

                elif node_name == "zeus_distribute":
                    yield _sse(
                        "zeus.plans_ready",
                        {
                            "plans": {
                                agent: {"plan": summary, "expected_output": ""}
                                for agent, summary in updates.get("agent_summaries", {}).items()
                            }
                        },
                    )
                    yield _sse(
                        "zeus.decision",
                        {
                            "reasoning": updates.get("zeus_reasoning", ""),
                            "subtasks": updates.get("subtasks", []),
                            "assignments": updates.get("assignments", []),
                            "synthesis_agent": updates.get("synthesis_agent", "mnemosyne"),
                        },
                    )

                elif node_name == "workflow_precheck":
                    precheck_verdict = updates.get("precheck_verdict", "approved")
                    yield _sse(
                        "hermes.precheck_verdict",
                        {
                            "verdict": precheck_verdict,
                            "reasoning": updates.get("precheck_reasoning", ""),
                            "criticite": updates.get("criticite") or final_state.get("criticite"),
                            "subtasks_trimmed": bool(updates.get("subtasks")),
                        },
                    )
                    if precheck_verdict in ("clarification", "blocked") and updates.get("final_answer"):
                        yield _sse(
                            "kairos.final_answer",
                            {
                                "answer": updates.get("final_answer", ""),
                                "run_id": str(run_id),
                                "short_circuited": True,
                            },
                        )

                elif node_name in ("dispatch_subtasks", "execute_complements"):
                    subtask_results = updates.get("subtask_results", {})
                    if subtask_results:
                        for task_id, task_res in subtask_results.items():
                            yield _sse(
                                "agent.subtask_done",
                                {
                                    "task_id": task_id,
                                    "agents": list(task_res.keys()),
                                    "results": {a: r[:500] for a, r in task_res.items()},
                                },
                            )
                    yield _sse(
                        "agent.all_done",
                        {
                            "results": {
                                agent: result[:500] for agent, result in updates.get("agent_results", {}).items()
                            }
                        },
                    )

                elif node_name == "veto_check":
                    if updates.get("veto_agent"):
                        veto_agent = updates.get("veto_agent", "")
                        yield _sse(
                            "themis.veto_detected",
                            {
                                "agent": veto_agent,
                                "role": get_agent_role(veto_agent),
                                "severity": updates.get("veto_severity", ""),
                                "motif": updates.get("veto_motif", ""),
                                "condition_levee": updates.get("veto_condition_levee", ""),
                            },
                        )

                elif node_name == "zeus_judge":
                    yield _sse(
                        "zeus.verdict",
                        {
                            "verdict": updates.get("verdict", "complete"),
                            "complement_requested": updates.get("verdict") == "needs_complement",
                        },
                    )

                elif node_name == "score_decision":
                    if updates.get("run_score"):
                        yield _sse(
                            "hera.run_score",
                            {"score": updates.get("run_score", {})},
                        )
                    if updates.get("score_id"):
                        yield _sse(
                            "hera.score_computed",
                            {
                                "score_id": updates.get("score_id", ""),
                                "verdict": updates.get("score_verdict", ""),
                                "total": updates.get("score_total", 0),
                            },
                        )

                elif node_name == "hera_supervise":
                    yield _sse(
                        "hera.verdict",
                        {
                            "verdict": updates.get("hera_verdict", "aligned"),
                            "feedback": updates.get("hera_feedback", ""),
                        },
                    )

                elif node_name == "synthesize":
                    yield _sse(
                        "kairos.final_answer",
                        {
                            "answer": updates.get("final_answer", ""),
                            "run_id": str(run_id),
                        },
                    )

                elif node_name == "write_memories":
                    yield _sse(
                        "hestia.memories_written",
                        {
                            "count": updates.get("memories_written", 0),
                            "wiki_page_id": updates.get("wiki_page_id", ""),
                        },
                    )

        async with AsyncSessionLocal() as db:
            run = await db.get(OrchestraRun, run_id)
            if run:
                _persist_run_state(run, final_state)
                run.status = "completed"
                run.duration_ms = int((time.monotonic() - t_start) * 1000)
                await db.commit()

        yield _sse(
            "done",
            {
                "run_id": str(run_id),
                "duration_ms": int((time.monotonic() - t_start) * 1000),
            },
        )

    except Exception as exc:
        log.error("orchestra.stream_failed", run_id=str(run_id), error=str(exc))
        try:
            async with AsyncSessionLocal() as db:
                run = await db.get(OrchestraRun, run_id)
                if run and run.status == "running":
                    run.status = "failed"
                    run.error_message = str(exc)
                    run.duration_ms = int((time.monotonic() - t_start) * 1000)
                    await db.commit()
        except Exception:
            pass
        yield _sse("error", {"detail": str(exc), "run_id": str(run_id)})
