"""
Router orchestra

POST /orchestra/run          → lance une orchestration multi-agents Zeus
GET  /orchestra/runs/{affaire_id} → liste les runs d'une affaire
GET  /orchestra/runs/detail/{run_id} → détail d'un run
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from core.queue import get_queue
from database import get_db
from modules.orchestra.models import OrchestraRun
from modules.orchestra.schemas import ApprovalRequest, OrchestraRequest, OrchestraResponse
from modules.orchestra.service import (
    resume_orchestra,
    run_orchestra,
    run_orchestra_hitl,
    stream_orchestra,
)

log = get_logger("orchestra.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.post("/run", response_model=OrchestraResponse, status_code=202)
    async def orchestra_run(
        payload: OrchestraRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        """
        Enqueue une orchestration Zeus. Retourne immédiatement avec status=queued (HTTP 202).
        Utiliser GET /orchestra/runs/detail/{run_id} pour suivre l'état.
        Pour un résultat en temps réel, utiliser POST /orchestra/stream.
        """
        # Créer le run en DB (status=queued) avant d'enqueuer
        from modules.orchestra.service import VALID_AGENTS, DEFAULT_AGENTS, CRITICITE_ROUTING

        initial_agents = [a for a in (payload.agents or DEFAULT_AGENTS) if a in VALID_AGENTS] or DEFAULT_AGENTS
        effective_criticite = payload.criticite if payload.criticite in CRITICITE_ROUTING else "C2"
        run = OrchestraRun(
            affaire_id=payload.affaire_id,
            user_id=current_user.id,
            instruction=payload.instruction,
            initial_agents=initial_agents,
            criticite=effective_criticite,
            status="queued",
        )
        db.add(run)
        await db.commit()
        await db.refresh(run)

        # Enqueue le job ARQ
        try:
            queue = await get_queue()
            await queue.enqueue_job(
                "orchestra_job",
                str(run.id),
                payload.instruction,
                str(payload.affaire_id),
                str(current_user.id),
                payload.agents,
                effective_criticite,
            )
        except Exception:
            # Si Redis indisponible, exécuter en synchrone (fallback)
            log.warning("orchestra.queue_unavailable, fallback sync")
            run = await run_orchestra(
                db=db,
                instruction=payload.instruction,
                affaire_id=payload.affaire_id,
                user_id=current_user.id,
                agents=payload.agents,
            )

        return _to_response(run)

    @router.post("/stream")
    async def orchestra_stream(
        payload: OrchestraRequest,
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        """
        Même logique que /run mais en Server-Sent Events.

        Le client reçoit les événements au fil de l'exécution.
        Convention : {agent}.{event} — agent = identité, event = action.

          run_created              — run_id créé, agents initiaux
          phase_start              — début de chaque nœud LangGraph
          hermes.preprocess_ready  — intention qualifiée, criticité suggérée
          hermes.precheck_verdict  — verdict gate : approved | trim | blocked
          zeus.plans_ready         — plans agents collectés
          zeus.decision            — plan Zeus : subtasks + assignments
          agent.subtask_done       — résultat d'une sous-tâche (tronqué)
          agent.all_done           — tous les agents ont répondu
          themis.veto_detected     — veto bloquant : {agent, role, motif}
          zeus.verdict             — jugement : complete | needs_complement
          hera.run_score           — score multi-critères du run
          hera.score_computed      — score décisionnel C4/C5 (verdict)
          hera.verdict             — supervision cohérence : aligned | misaligned
          kairos.final_answer      — réponse finale + run_id
          hestia.memories_written  — mémoires persistées
          done                     — fin du stream
          error                    — erreur inattendue

        Consommation côté client :
          const es = new EventSource('/orchestra/stream');  // ou fetch + ReadableStream
          es.addEventListener('final_answer', e => console.log(JSON.parse(e.data)));
        """
        return StreamingResponse(
            stream_orchestra(
                instruction=payload.instruction,
                affaire_id=payload.affaire_id,
                user_id=current_user.id,
                agents=payload.agents,
                criticite=payload.criticite if hasattr(payload, "criticite") else "C2",
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",  # désactive le buffering nginx
            },
        )

    @router.post("/run-hitl", response_model=OrchestraResponse, status_code=202)
    async def orchestra_run_hitl(
        payload: OrchestraRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe")),
    ):
        """
        Lance une orchestration avec validation humaine (HITL).
        Zeus s'arrête après avoir distribué les rôles et attend une approbation.
        Répondre via POST /orchestra/runs/{id}/approve.
        """
        run = await run_orchestra_hitl(
            db=db,
            instruction=payload.instruction,
            affaire_id=payload.affaire_id,
            user_id=current_user.id,
            agents=payload.agents,
        )
        return _to_response(run)

    @router.post("/runs/{run_id}/approve", response_model=OrchestraResponse)
    async def approve_run(
        run_id: UUID,
        payload: ApprovalRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe")),
    ):
        """
        Valide ou rejette la proposition de Zeus.

        - approved=true → les agents s'exécutent avec les rôles proposés (ou modifiés)
        - approved=false → le run est annulé
        - modified_assignments → remplace les assignments de Zeus si fourni
        """
        try:
            run = await resume_orchestra(
                db=db,
                run_id=run_id,
                approved=payload.approved,
                feedback=payload.feedback,
                modified_assignments=payload.modified_assignments,
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return _to_response(run)

    @router.get("/runs/{affaire_id}", response_model=list[OrchestraResponse])
    async def list_runs(
        affaire_id: UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        result = await db.execute(
            select(OrchestraRun)
            .where(OrchestraRun.affaire_id == affaire_id)
            .order_by(OrchestraRun.created_at.desc())
            .limit(50)
        )
        return [_to_response(r) for r in result.scalars().all()]

    @router.get("/runs/detail/{run_id}", response_model=OrchestraResponse)
    async def get_run(
        run_id: UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        run = await db.get(OrchestraRun, run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run introuvable")
        return _to_response(run)

    return router


def _to_response(run: OrchestraRun) -> OrchestraResponse:
    return OrchestraResponse(
        run_id=run.id,
        status=run.status,
        instruction=run.instruction,
        initial_agents=run.initial_agents or [],
        zeus_reasoning=run.zeus_reasoning,
        assignments=run.assignments or [],
        agent_results=run.agent_results or {},
        synthesis_agent=run.synthesis_agent,
        final_answer=run.final_answer,
        subtasks=run.subtasks or [],
        subtask_results=run.subtask_results or {},
        veto_agent=run.veto_agent,
        veto_motif=run.veto_motif,
        error_message=run.error_message,
        criticite=run.criticite or "C2",
        hitl_enabled=run.hitl_enabled or False,
        hitl_payload=run.hitl_payload,
        duration_ms=run.duration_ms,
        # Améliorations 0026
        run_score=run.run_score,
        hera_verdict=run.hera_verdict,
        hera_feedback=run.hera_feedback,
        fallback_level=run.fallback_level or 0,
    )
