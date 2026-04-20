"""
Router planning

Lots
  POST   /planning/{affaire_id}/lots          → créer lot
  GET    /planning/{affaire_id}/lots          → lister lots
  PATCH  /planning/lots/{lot_id}              → modifier lot
  DELETE /planning/lots/{lot_id}              → supprimer (admin)

Tâches
  POST   /planning/{affaire_id}/taches        → créer tâche
  GET    /planning/{affaire_id}/taches        → lister tâches
  PATCH  /planning/taches/{tache_id}          → modifier tâche
  DELETE /planning/taches/{tache_id}          → supprimer (admin)
  POST   /planning/taches/{tache_id}/propagate → propager décalage en cascade

Jalons
  POST   /planning/{affaire_id}/jalons        → créer jalon
  GET    /planning/{affaire_id}/jalons        → lister jalons
  PATCH  /planning/jalons/{jalon_id}          → modifier jalon
  DELETE /planning/jalons/{jalon_id}          → supprimer (admin)

Liens de dépendance
  POST   /planning/{affaire_id}/liens         → créer lien
  GET    /planning/{affaire_id}/liens         → lister liens
  DELETE /planning/liens/{lien_id}            → supprimer lien

Vues analytiques
  GET    /planning/{affaire_id}/gantt         → lots + tâches + jalons + liens
  POST   /planning/{affaire_id}/critical-path → calculer chemin critique (CPM)
  GET    /planning/{affaire_id}/health        → KPIs de santé
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from database import get_db
from modules.planning.schemas import (
    CriticalPathResult,
    GanttResponse,
    JalonCreate,
    JalonResponse,
    JalonUpdate,
    LienCreate,
    LienResponse,
    LotCreate,
    LotResponse,
    LotUpdate,
    PlanningHealth,
    PropagateRequest,
    PropagationResult,
    TacheCreate,
    TacheResponse,
    TacheUpdate,
)
from modules.planning.service import (
    compute_critical_path,
    create_jalon,
    create_lien,
    create_lot,
    create_tache,
    delete_jalon,
    delete_lien,
    delete_lot,
    delete_tache,
    get_health,
    get_jalon,
    get_lien,
    get_lot,
    get_tache,
    list_jalons,
    list_liens,
    list_lots,
    list_taches,
    propagate_delays,
    update_jalon,
    update_lot,
    update_tache,
)

log = get_logger("planning.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    # ══════════════════════════════════════════════════════════════════
    # LOTS
    # ══════════════════════════════════════════════════════════════════

    @router.post("/{affaire_id}/lots", response_model=LotResponse, status_code=201)
    async def lot_create(
        affaire_id: uuid.UUID,
        payload: LotCreate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        lot = await create_lot(db, affaire_id, **payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(lot)
        log.info("planning.lot_created", affaire_id=str(affaire_id), code=lot.code)
        return lot

    @router.get("/{affaire_id}/lots", response_model=list[LotResponse])
    async def lot_list(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await list_lots(db, affaire_id)

    @router.patch("/lots/{lot_id}", response_model=LotResponse)
    async def lot_update(
        lot_id: uuid.UUID,
        payload: LotUpdate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        lot = await get_lot(db, lot_id)
        if not lot:
            raise HTTPException(404, "Lot introuvable")
        lot = await update_lot(db, lot, payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(lot)
        return lot

    @router.delete("/lots/{lot_id}", status_code=204)
    async def lot_delete(
        lot_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        lot = await get_lot(db, lot_id)
        if not lot:
            raise HTTPException(404, "Lot introuvable")
        await delete_lot(db, lot)
        await db.commit()

    # ══════════════════════════════════════════════════════════════════
    # TÂCHES
    # ══════════════════════════════════════════════════════════════════

    @router.post("/{affaire_id}/taches", response_model=TacheResponse, status_code=201)
    async def tache_create(
        affaire_id: uuid.UUID,
        payload: TacheCreate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        tache = await create_tache(db, affaire_id, **payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(tache)
        log.info("planning.tache_created", affaire_id=str(affaire_id), titre=tache.titre)
        return tache

    @router.get("/{affaire_id}/taches", response_model=list[TacheResponse])
    async def tache_list(
        affaire_id: uuid.UUID,
        lot_id: uuid.UUID | None = None,
        statut: str | None = None,
        critique_only: bool = False,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await list_taches(db, affaire_id, lot_id=lot_id, statut=statut, critique_only=critique_only)

    @router.patch("/taches/{tache_id}", response_model=TacheResponse)
    async def tache_update(
        tache_id: uuid.UUID,
        payload: TacheUpdate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        tache = await get_tache(db, tache_id)
        if not tache:
            raise HTTPException(404, "Tâche introuvable")
        tache = await update_tache(db, tache, payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(tache)
        return tache

    @router.delete("/taches/{tache_id}", status_code=204)
    async def tache_delete(
        tache_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        tache = await get_tache(db, tache_id)
        if not tache:
            raise HTTPException(404, "Tâche introuvable")
        await delete_tache(db, tache)
        await db.commit()

    @router.post("/taches/{tache_id}/propagate", response_model=PropagationResult)
    async def tache_propagate(
        tache_id: uuid.UUID,
        payload: PropagateRequest,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        if not await get_tache(db, tache_id):
            raise HTTPException(404, "Tâche introuvable")
        details = await propagate_delays(db, tache_id, payload.delta_jours)
        await db.commit()
        log.info(
            "planning.delay_propagated",
            tache_id=str(tache_id),
            delta=payload.delta_jours,
            impacted=len(details),
        )
        return PropagationResult(taches_impactees=len(details), details=details)

    # ══════════════════════════════════════════════════════════════════
    # JALONS
    # ══════════════════════════════════════════════════════════════════

    @router.post("/{affaire_id}/jalons", response_model=JalonResponse, status_code=201)
    async def jalon_create(
        affaire_id: uuid.UUID,
        payload: JalonCreate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        jalon = await create_jalon(db, affaire_id, **payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(jalon)
        log.info("planning.jalon_created", affaire_id=str(affaire_id), nom=jalon.nom)
        return jalon

    @router.get("/{affaire_id}/jalons", response_model=list[JalonResponse])
    async def jalon_list(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await list_jalons(db, affaire_id)

    @router.patch("/jalons/{jalon_id}", response_model=JalonResponse)
    async def jalon_update(
        jalon_id: uuid.UUID,
        payload: JalonUpdate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        jalon = await get_jalon(db, jalon_id)
        if not jalon:
            raise HTTPException(404, "Jalon introuvable")
        jalon = await update_jalon(db, jalon, payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(jalon)
        return jalon

    @router.delete("/jalons/{jalon_id}", status_code=204)
    async def jalon_delete(
        jalon_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        jalon = await get_jalon(db, jalon_id)
        if not jalon:
            raise HTTPException(404, "Jalon introuvable")
        await delete_jalon(db, jalon)
        await db.commit()

    # ══════════════════════════════════════════════════════════════════
    # LIENS DE DÉPENDANCE
    # ══════════════════════════════════════════════════════════════════

    @router.post("/{affaire_id}/liens", response_model=LienResponse, status_code=201)
    async def lien_create(
        affaire_id: uuid.UUID,
        payload: LienCreate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        # Vérifier que les deux tâches appartiennent à cette affaire
        pred = await get_tache(db, payload.predecesseur_id)
        succ = await get_tache(db, payload.successeur_id)
        if not pred or pred.affaire_id != affaire_id:
            raise HTTPException(404, "Tâche prédécesseur introuvable dans cette affaire")
        if not succ or succ.affaire_id != affaire_id:
            raise HTTPException(404, "Tâche successeur introuvable dans cette affaire")
        lien = await create_lien(
            db,
            predecesseur_id=payload.predecesseur_id,
            successeur_id=payload.successeur_id,
            type=payload.type,
            delai_jours=payload.delai_jours,
        )
        await db.commit()
        await db.refresh(lien)
        return lien

    @router.get("/{affaire_id}/liens", response_model=list[LienResponse])
    async def lien_list(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await list_liens(db, affaire_id)

    @router.delete("/liens/{lien_id}", status_code=204)
    async def lien_delete(
        lien_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        lien = await get_lien(db, lien_id)
        if not lien:
            raise HTTPException(404, "Lien introuvable")
        await delete_lien(db, lien)
        await db.commit()

    # ══════════════════════════════════════════════════════════════════
    # VUES ANALYTIQUES
    # ══════════════════════════════════════════════════════════════════

    @router.get("/{affaire_id}/gantt", response_model=GanttResponse)
    async def gantt(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        lots, taches, jalons, liens = await _gather_gantt(db, affaire_id)
        return GanttResponse(
            affaire_id=affaire_id,
            lots=lots,
            taches=taches,
            jalons=jalons,
            liens=liens,
        )

    @router.post("/{affaire_id}/critical-path", response_model=CriticalPathResult)
    async def critical_path(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        result = await compute_critical_path(db, affaire_id)
        await db.commit()
        log.info(
            "planning.critical_path_computed",
            affaire_id=str(affaire_id),
            duree=result["duree_projet_jours"],
            critiques=result["nb_taches_critiques"],
        )
        return CriticalPathResult(**result)

    @router.get("/{affaire_id}/health", response_model=PlanningHealth)
    async def health(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        result = await get_health(db, affaire_id)
        return PlanningHealth(**result)

    return router


# ── Helpers ──────────────────────────────────────────────────────────


async def _gather_gantt(db, affaire_id):
    import asyncio

    lots, taches, jalons, liens = await asyncio.gather(
        list_lots(db, affaire_id),
        list_taches(db, affaire_id),
        list_jalons(db, affaire_id),
        list_liens(db, affaire_id),
    )
    return lots, taches, jalons, liens
