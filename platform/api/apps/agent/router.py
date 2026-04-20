"""
Router agent — copilote MOE autonome

POST /agent/run             → lance une exécution agentique
GET  /agent/runs/{affaire_id} → historique des runs d'un projet
GET  /agent/runs/detail/{run_id} → détail d'un run (steps complets)
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from database import get_db
from apps.agent.models import AgentRun
from apps.agent.schemas import AgentRunRequest, AgentRunResponse
from apps.agent.service import run_agent

log = get_logger("agent.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.post("/run", response_model=AgentRunResponse, status_code=201)
    async def agent_run(
        payload: AgentRunRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        """
        Lance l'agent copilote MOE sur une instruction en langage naturel.

        Exemples d'instructions :
        - "Résume les obligations acoustiques mentionnées dans les documents"
        - "Quels sont les délais d'intervention stipulés dans le CCTP ?"
        - "Liste les documents disponibles et identifie ceux manquants"
        """
        run = await run_agent(
            db=db,
            instruction=payload.instruction,
            affaire_id=payload.affaire_id,
            user_id=current_user.id,
            agent_name=payload.agent,
            max_iterations=payload.max_iterations,
        )
        return run

    @router.get("/runs/{affaire_id}", response_model=list[AgentRunResponse])
    async def list_runs(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """Historique des runs pour un projet donné."""
        result = await db.execute(
            select(AgentRun).where(AgentRun.affaire_id == affaire_id).order_by(AgentRun.created_at.desc()).limit(50)
        )
        return result.scalars().all()

    @router.get("/runs/detail/{run_id}", response_model=AgentRunResponse)
    async def get_run(
        run_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """Détail complet d'un run (steps, outils appelés, durées)."""
        run = await db.get(AgentRun, run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Run introuvable")
        return run

    return router
