"""
Router preprocessing — endpoints de debug/preview.

POST /preprocessing/preview   → preview de la normalisation Hermès
POST /preprocessing/precheck  → preview du gate Precheck sur un plan Zeus

Les deux endpoints sont stateless (pas de persistence). Ils servent
principalement à tester les prompts avant de lancer une orchestration
complète.
"""

from fastapi import APIRouter, Depends, HTTPException

from core.auth import get_current_user
from core.logging import get_logger
from apps.preprocessing.schemas import (
    PrecheckDecision,
    PrecheckRequest,
    PreprocessRequest,
    PreprocessedInput,
)
from apps.preprocessing.service import PreprocessingService

log = get_logger("preprocessing.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.post("/preview", response_model=PreprocessedInput)
    async def preview(
        payload: PreprocessRequest,
        _user=Depends(get_current_user),
    ):
        """Preview du preprocessing Hermès sur un message brut."""
        try:
            return await PreprocessingService.preprocess(
                payload.message,
                affaire_hint=payload.affaire_hint,
                phase_hint=payload.phase_hint,
                domaine_hint=payload.domaine_hint,
            )
        except Exception as exc:
            log.error("preprocessing.preview_failed", error=str(exc))
            raise HTTPException(status_code=502, detail=str(exc))

    @router.post("/precheck", response_model=PrecheckDecision)
    async def precheck(
        payload: PrecheckRequest,
        _user=Depends(get_current_user),
    ):
        """Preview du gate Precheck sur un plan Zeus hypothétique."""
        preprocessed = None
        if payload.preprocessed:
            try:
                preprocessed = PreprocessedInput(**payload.preprocessed)
            except Exception as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"preprocessed invalide : {exc}",
                )
        try:
            return await PreprocessingService.precheck(
                instruction=payload.instruction,
                criticite=payload.criticite,
                subtasks=payload.subtasks,
                preprocessed=preprocessed,
            )
        except Exception as exc:
            log.error("preprocessing.precheck_failed", error=str(exc))
            raise HTTPException(status_code=502, detail=str(exc))

    return router
