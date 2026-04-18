"""
Router scoring — calcul et consultation des scores décisionnels.

POST   /scoring/manual         → scoring manuel (utilisateur fournit les axes)
POST   /scoring/auto           → scoring automatique via LLM (Instructor)
GET    /scoring/{score_id}     → détail d'un score
GET    /scoring/                → liste filtrée (affaire, decision, verdict)
GET    /scoring/decision/{id}  → dernier score pour une decision_id
GET    /scoring/stats          → KPIs dashboard (global ou par affaire)
DELETE /scoring/{score_id}     → suppression (admin)
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from database import get_db
from modules.scoring.models import DecisionScore
from modules.scoring.schemas import (
    DecisionScoreResponse,
    ScoreAutoRequest,
    ScoreManualRequest,
    ScoreSummary,
    ScoringStats,
)
from modules.scoring.service import ScoringService

log = get_logger("scoring.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    # ── Calcul ──────────────────────────────────────────────────────

    @router.post("/manual", response_model=DecisionScoreResponse, status_code=201)
    async def score_manual(
        payload: ScoreManualRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        score = await ScoringService.score_manual(
            db,
            sujet=payload.sujet,
            axes=payload.axes,
            affaire_id=payload.affaire_id,
            decision_id=payload.decision_id,
            certitude=payload.certitude,
            dette=payload.dette,
            computed_by=current_user.id,
        )
        return score

    @router.post("/auto", response_model=DecisionScoreResponse, status_code=201)
    async def score_auto(
        payload: ScoreAutoRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        """
        Scoring automatique par LLM.
        Temperature basse + Instructor garantit un résultat valide.
        """
        try:
            score = await ScoringService.score_auto(
                db,
                sujet=payload.sujet,
                contexte=payload.contexte,
                affaire_id=payload.affaire_id,
                decision_id=payload.decision_id,
                certitude=payload.certitude,
                dette=payload.dette,
                computed_by=current_user.id,
            )
        except Exception as exc:
            log.error("scoring.auto_failed", error=str(exc))
            raise HTTPException(status_code=502, detail=f"LLM scoring failed: {exc}")
        return score

    # ── Lecture ─────────────────────────────────────────────────────

    @router.get("/stats", response_model=ScoringStats)
    async def stats(
        affaire_id: Optional[uuid.UUID] = Query(None),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """KPIs dashboard : moyenne, distribution, dettes D3, taux robuste."""
        return await ScoringService.stats_for_affaire(db, affaire_id)

    @router.get("/decision/{decision_id}", response_model=DecisionScoreResponse)
    async def latest_for_decision(
        decision_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """Retourne le score le plus récent pour une project_decision."""
        result = await db.execute(
            select(DecisionScore)
            .where(DecisionScore.decision_id == decision_id)
            .order_by(DecisionScore.computed_at.desc())
            .limit(1)
        )
        score = result.scalar_one_or_none()
        if not score:
            raise HTTPException(status_code=404, detail="Aucun score pour cette décision")
        return score

    @router.get("/", response_model=list[ScoreSummary])
    async def list_scores(
        affaire_id: Optional[uuid.UUID] = Query(None),
        decision_id: Optional[uuid.UUID] = Query(None),
        verdict: Optional[str] = Query(None, pattern="^(robuste|acceptable|fragile|dangereux)$"),
        limit: int = Query(50, ge=1, le=500),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        query = select(DecisionScore)
        if affaire_id:
            query = query.where(DecisionScore.affaire_id == affaire_id)
        if decision_id:
            query = query.where(DecisionScore.decision_id == decision_id)
        if verdict:
            query = query.where(DecisionScore.verdict == verdict)
        query = query.order_by(DecisionScore.computed_at.desc()).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @router.get("/{score_id}", response_model=DecisionScoreResponse)
    async def get_score(
        score_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        score = await db.get(DecisionScore, score_id)
        if not score:
            raise HTTPException(status_code=404, detail="Score introuvable")
        return score

    @router.delete("/{score_id}", status_code=204)
    async def delete_score(
        score_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        score = await db.get(DecisionScore, score_id)
        if not score:
            raise HTTPException(status_code=404, detail="Score introuvable")
        await db.delete(score)
        await db.commit()

    return router
