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
from database import get_db
from modules.orchestra.models import OrchestraRun
from modules.orchestra.schemas import OrchestraRequest, OrchestraResponse
from modules.orchestra.service import run_orchestra, stream_orchestra

log = get_logger("orchestra.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.post("/run", response_model=OrchestraResponse)
    async def orchestra_run(
        payload: OrchestraRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
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

        Le client reçoit les événements au fil de l'exécution :
          run_created   — run_id créé, agents initiaux
          phase_start   — début de chaque phase Zeus
          plans_ready   — plans collectés
          zeus_decision — rôles redistribués par Zeus
          agents_done   — résultats d'exécution (tronqués)
          zeus_verdict  — jugement Zeus (complete / needs_complement)
          final_answer  — réponse finale + run_id complet
          done          — fin du stream
          error         — erreur inattendue

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
            ),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",   # désactive le buffering nginx
            },
        )

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
        duration_ms=run.duration_ms,
    )
