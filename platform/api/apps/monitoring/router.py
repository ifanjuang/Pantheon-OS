"""
Router monitoring — endpoints d'observabilité.

GET /monitoring/kpis?window=7d        → MonitoringSnapshot complet
GET /monitoring/kpis/orchestra        → uniquement OrchestraKPIs
GET /monitoring/kpis/agents           → uniquement AgentKPIs
GET /monitoring/kpis/scoring          → uniquement ScoringKPIs
GET /monitoring/kpis/guards           → uniquement GuardsKPIs

Fenêtres disponibles : 24h / 7d / 30d / 90d (default: 7d).
Accessible aux rôles admin / moe (même règle que decisions).
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_role
from database import get_db
from apps.monitoring.schemas import (
    AgentKPIs,
    GuardsKPIs,
    MonitoringSnapshot,
    OrchestraKPIs,
    ScoringKPIs,
)
from apps.monitoring.service import MonitoringService


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.get("/kpis", response_model=MonitoringSnapshot)
    async def kpis(
        window: str = Query("7d", pattern="^(24h|7d|30d|90d)$"),
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        return await MonitoringService.snapshot(db, window=window)  # type: ignore[arg-type]

    @router.get("/kpis/orchestra", response_model=OrchestraKPIs)
    async def orchestra_kpis(
        window: str = Query("7d", pattern="^(24h|7d|30d|90d)$"),
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        snap = await MonitoringService.snapshot(db, window=window)  # type: ignore[arg-type]
        return snap.orchestra

    @router.get("/kpis/agents", response_model=AgentKPIs)
    async def agents_kpis(
        window: str = Query("7d", pattern="^(24h|7d|30d|90d)$"),
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        snap = await MonitoringService.snapshot(db, window=window)  # type: ignore[arg-type]
        return snap.agents

    @router.get("/kpis/scoring", response_model=ScoringKPIs)
    async def scoring_kpis(
        window: str = Query("7d", pattern="^(24h|7d|30d|90d)$"),
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        snap = await MonitoringService.snapshot(db, window=window)  # type: ignore[arg-type]
        return snap.scoring

    @router.get("/kpis/guards", response_model=GuardsKPIs)
    async def guards_kpis(
        window: str = Query("7d", pattern="^(24h|7d|30d|90d)$"),
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        snap = await MonitoringService.snapshot(db, window=window)  # type: ignore[arg-type]
        return snap.guards

    return router
