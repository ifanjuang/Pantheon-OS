"""
Router guards — endpoints de debug/preview.

POST /guards/veto/preview           → preview du structured_veto
POST /guards/reversibility/preview  → preview du reversibility_guard
POST /guards/criticality/preview    → preview du criticality_guard (règle pure)

Les trois endpoints sont stateless. Ils servent à tester les règles et
les prompts des gardes-fous avant de les câbler dans une orchestration.
"""

from fastapi import APIRouter, Depends, HTTPException

from core.auth import get_current_user
from core.logging import get_logger
from apps.guards.schemas import (
    CriticalityImpacts,
    CriticalityVerdict,
    ReversibilityDecision,
    ReversibilityPreviewRequest,
    VetoDecision,
    VetoPreviewRequest,
)
from apps.guards.service import GuardsService

log = get_logger("guards.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.post("/veto/preview", response_model=VetoDecision)
    async def veto_preview(
        payload: VetoPreviewRequest,
        _user=Depends(get_current_user),
    ):
        """Preview d'un veto structuré sur une sortie agent."""
        try:
            return await GuardsService.structured_veto(
                agent=payload.agent,
                agent_output=payload.agent_output,
                criticite=payload.criticite,
            )
        except Exception as exc:
            log.error("guards.veto_preview_failed", error=str(exc))
            raise HTTPException(status_code=502, detail=str(exc))

    @router.post("/reversibility/preview", response_model=ReversibilityDecision)
    async def reversibility_preview(
        payload: ReversibilityPreviewRequest,
        _user=Depends(get_current_user),
    ):
        """Preview du reversibility_guard sur une décision."""
        try:
            return await GuardsService.reversibility_guard(
                decision=payload.decision,
                criticite=payload.criticite,
                impact_cout=payload.impact_cout,
                impact_delai=payload.impact_delai,
            )
        except Exception as exc:
            log.error("guards.reversibility_preview_failed", error=str(exc))
            raise HTTPException(status_code=502, detail=str(exc))

    @router.post("/criticality/preview", response_model=CriticalityVerdict)
    async def criticality_preview(
        payload: CriticalityImpacts,
        _user=Depends(get_current_user),
    ):
        """Preview du criticality_guard (règle pure, pas de LLM)."""
        return GuardsService.criticality_guard(payload)

    return router
