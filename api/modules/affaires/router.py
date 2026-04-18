"""
Router affaires

GET    /affaires/              → liste (filtrable par statut)
POST   /affaires/              → créer une affaire (admin, moe)
GET    /affaires/{id}          → détail
PATCH  /affaires/{id}          → modifier
DELETE /affaires/{id}          → supprimer (admin uniquement)
GET    /affaires/{id}/cockpit  → tableau de bord transversal (planning + chantier + comms + finance + alertes)
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from database import get_db
from modules.affaires.cockpit import get_cockpit
from modules.affaires.schemas import AffaireCreate, AffaireResponse, AffaireUpdate
from modules.affaires.service import (
    create_affaire,
    delete_affaire,
    get_affaire,
    get_affaire_by_code,
    list_affaires,
    update_affaire,
)

log = get_logger("affaires.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_model=list[AffaireResponse])
    async def list_(
        statut: str | None = None,
        limit: int = 100,
        offset: int = 0,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await list_affaires(db, statut=statut, limit=limit, offset=offset)

    @router.post("/", response_model=AffaireResponse, status_code=201)
    async def create(
        payload: AffaireCreate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe")),
    ):
        if await get_affaire_by_code(db, payload.code):
            raise HTTPException(status_code=409, detail=f"Code '{payload.code}' déjà utilisé")
        _base = {"code", "nom", "description", "statut"}
        context = {k: v for k, v in payload.model_dump(exclude_none=True).items() if k not in _base}
        affaire = await create_affaire(
            db,
            code=payload.code,
            nom=payload.nom,
            description=payload.description,
            statut=payload.statut,
            created_by=current_user.id,
            **context,
        )
        await db.commit()
        await db.refresh(affaire)
        log.info("affaires.created", code=affaire.code, id=str(affaire.id))
        return affaire

    @router.get("/{affaire_id}", response_model=AffaireResponse)
    async def detail(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        affaire = await get_affaire(db, affaire_id)
        if not affaire:
            raise HTTPException(status_code=404, detail="Affaire introuvable")
        return affaire

    @router.patch("/{affaire_id}", response_model=AffaireResponse)
    async def update(
        affaire_id: uuid.UUID,
        payload: AffaireUpdate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        affaire = await get_affaire(db, affaire_id)
        if not affaire:
            raise HTTPException(status_code=404, detail="Affaire introuvable")
        affaire = await update_affaire(db, affaire, payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(affaire)
        log.info("affaires.updated", id=str(affaire_id))
        return affaire

    @router.delete("/{affaire_id}", status_code=204)
    async def delete(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        affaire = await get_affaire(db, affaire_id)
        if not affaire:
            raise HTTPException(status_code=404, detail="Affaire introuvable")
        await delete_affaire(db, affaire)
        await db.commit()
        log.info("affaires.deleted", id=str(affaire_id))

    @router.get("/{affaire_id}/cockpit")
    async def cockpit(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """
        Tableau de bord transversal — agrège planning, chantier, communications,
        finance et décisions en un seul appel. Retourne aussi une liste d'alertes
        triées par criticité (critical > warning > info).
        """
        affaire = await get_affaire(db, affaire_id)
        if not affaire:
            raise HTTPException(status_code=404, detail="Affaire introuvable")
        return await get_cockpit(db, affaire_id)

    return router
