"""
Router finance

Avenants
  POST   /finance/{affaire_id}/avenants          → créer avenant
  GET    /finance/{affaire_id}/avenants          → lister
  PATCH  /finance/avenants/{id}                  → modifier
  DELETE /finance/avenants/{id}                  → supprimer (admin)

Situations de travaux
  POST   /finance/{affaire_id}/situations        → créer situation
  GET    /finance/{affaire_id}/situations        → lister
  PATCH  /finance/situations/{id}                → modifier (validation, paiement)
  DELETE /finance/situations/{id}                → supprimer (admin)

Dashboard
  GET    /finance/{affaire_id}/dashboard         → agrégats financiers + dérive
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from database import get_db
from modules.finance.schemas import (
    AvenantCreate,
    AvenantResponse,
    AvenantUpdate,
    FinanceDashboard,
    SituationCreate,
    SituationResponse,
    SituationUpdate,
)
from modules.finance.service import (
    create_avenant,
    create_situation,
    delete_avenant,
    delete_situation,
    get_avenant,
    get_dashboard,
    get_situation,
    list_avenants,
    list_situations,
    update_avenant,
    update_situation,
)

log = get_logger("finance.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    # ══════════════════════════════════════════════════════════════════
    # AVENANTS
    # ══════════════════════════════════════════════════════════════════

    @router.post("/{affaire_id}/avenants", response_model=AvenantResponse, status_code=201)
    async def avenant_create(
        affaire_id: uuid.UUID,
        payload: AvenantCreate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        av = await create_avenant(db, affaire_id, **payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(av)
        log.info(
            "finance.avenant_created",
            affaire_id=str(affaire_id),
            numero=av.numero,
            montant=float(av.montant_ht),
        )
        return av

    @router.get("/{affaire_id}/avenants", response_model=list[AvenantResponse])
    async def avenant_list(
        affaire_id: uuid.UUID,
        lot_id: uuid.UUID | None = None,
        statut: str | None = None,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await list_avenants(db, affaire_id, lot_id=lot_id, statut=statut)

    @router.patch("/avenants/{av_id}", response_model=AvenantResponse)
    async def avenant_update(
        av_id: uuid.UUID,
        payload: AvenantUpdate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        av = await get_avenant(db, av_id)
        if not av:
            raise HTTPException(404, "Avenant introuvable")
        av = await update_avenant(db, av, payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(av)
        return av

    @router.delete("/avenants/{av_id}", status_code=204)
    async def avenant_delete(
        av_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        av = await get_avenant(db, av_id)
        if not av:
            raise HTTPException(404, "Avenant introuvable")
        await delete_avenant(db, av)
        await db.commit()

    # ══════════════════════════════════════════════════════════════════
    # SITUATIONS DE TRAVAUX
    # ══════════════════════════════════════════════════════════════════

    @router.post("/{affaire_id}/situations", response_model=SituationResponse, status_code=201)
    async def situation_create(
        affaire_id: uuid.UUID,
        payload: SituationCreate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        sit = await create_situation(db, affaire_id, **payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(sit)
        log.info(
            "finance.situation_created",
            affaire_id=str(affaire_id),
            entreprise=sit.entreprise,
            numero=sit.numero,
        )
        return sit

    @router.get("/{affaire_id}/situations", response_model=list[SituationResponse])
    async def situation_list(
        affaire_id: uuid.UUID,
        lot_id: uuid.UUID | None = None,
        statut: str | None = None,
        entreprise: str | None = None,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await list_situations(db, affaire_id, lot_id=lot_id, statut=statut, entreprise=entreprise)

    @router.patch("/situations/{sit_id}", response_model=SituationResponse)
    async def situation_update(
        sit_id: uuid.UUID,
        payload: SituationUpdate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        sit = await get_situation(db, sit_id)
        if not sit:
            raise HTTPException(404, "Situation introuvable")
        sit = await update_situation(db, sit, payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(sit)
        if sit.statut == "validee":
            log.info("finance.situation_validee", sit_id=str(sit_id), montant=float(sit.montant_valide_ht or 0))
        elif sit.statut == "payee":
            log.info("finance.situation_payee", sit_id=str(sit_id))
        return sit

    @router.delete("/situations/{sit_id}", status_code=204)
    async def situation_delete(
        sit_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        sit = await get_situation(db, sit_id)
        if not sit:
            raise HTTPException(404, "Situation introuvable")
        await delete_situation(db, sit)
        await db.commit()

    # ══════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════════════════════════

    @router.get("/{affaire_id}/dashboard", response_model=FinanceDashboard)
    async def dashboard(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        result = await get_dashboard(db, affaire_id)
        return FinanceDashboard(**result)

    return router
