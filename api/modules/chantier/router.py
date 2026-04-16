"""
Router chantier

Observations terrain
  POST   /chantier/{affaire_id}/observations          → créer observation
  GET    /chantier/{affaire_id}/observations          → lister
  PATCH  /chantier/observations/{id}                 → modifier
  DELETE /chantier/observations/{id}                 → supprimer (admin)
  POST   /chantier/observations/{id}/analyze         → lancer analyse Argos (ARQ)

Non-conformités
  POST   /chantier/{affaire_id}/nonconformites        → créer NC
  GET    /chantier/{affaire_id}/nonconformites        → lister
  PATCH  /chantier/nonconformites/{id}               → modifier
  DELETE /chantier/nonconformites/{id}               → supprimer (admin)
  POST   /chantier/nonconformites/{id}/qualify       → qualification Héphaïstos (ARQ)

Dashboard
  GET    /chantier/{affaire_id}/dashboard             → KPIs qualité chantier
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from core.queue import get_queue
from database import get_db
from modules.chantier.schemas import (
    AnalyzeJobResponse,
    ChantierDashboard,
    NonConformiteCreate,
    NonConformiteResponse,
    NonConformiteUpdate,
    ObservationCreate,
    ObservationResponse,
    ObservationUpdate,
)
from modules.chantier.service import (
    create_nonconformite,
    create_observation,
    delete_nonconformite,
    delete_observation,
    get_dashboard,
    get_nonconformite,
    get_observation,
    list_nonconformites,
    list_observations,
    update_nonconformite,
    update_observation,
)

log = get_logger("chantier.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    # ══════════════════════════════════════════════════════════════════
    # OBSERVATIONS
    # ══════════════════════════════════════════════════════════════════

    @router.post("/{affaire_id}/observations", response_model=ObservationResponse, status_code=201)
    async def obs_create(
        affaire_id: uuid.UUID,
        payload: ObservationCreate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe")),
    ):
        data = payload.model_dump(exclude_none=True)
        obs = await create_observation(
            db, affaire_id, auteur_id=current_user.id, **data
        )
        await db.commit()
        await db.refresh(obs)
        log.info("chantier.obs_created", affaire_id=str(affaire_id), source=obs.source)
        return obs

    @router.get("/{affaire_id}/observations", response_model=list[ObservationResponse])
    async def obs_list(
        affaire_id: uuid.UUID,
        source: str | None = None,
        statut: str | None = None,
        lot_id: uuid.UUID | None = None,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await list_observations(db, affaire_id, source=source, statut=statut, lot_id=lot_id)

    @router.patch("/observations/{obs_id}", response_model=ObservationResponse)
    async def obs_update(
        obs_id: uuid.UUID,
        payload: ObservationUpdate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        obs = await get_observation(db, obs_id)
        if not obs:
            raise HTTPException(404, "Observation introuvable")
        obs = await update_observation(db, obs, payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(obs)
        return obs

    @router.delete("/observations/{obs_id}", status_code=204)
    async def obs_delete(
        obs_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        obs = await get_observation(db, obs_id)
        if not obs:
            raise HTTPException(404, "Observation introuvable")
        await delete_observation(db, obs)
        await db.commit()

    @router.post("/observations/{obs_id}/analyze", response_model=AnalyzeJobResponse)
    async def obs_analyze(
        obs_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        """Lance l'analyse Argos sur l'observation en arrière-plan (ARQ)."""
        obs = await get_observation(db, obs_id)
        if not obs:
            raise HTTPException(404, "Observation introuvable")
        if obs.statut == "analyse":
            return AnalyzeJobResponse(
                job_queued=False,
                id=obs_id,
                message="Observation déjà analysée",
            )
        queue = await get_queue()
        await queue.enqueue_job("analyze_chantier_obs_job", str(obs_id))
        log.info("chantier.analyze_queued", obs_id=str(obs_id))
        return AnalyzeJobResponse(
            job_queued=True,
            id=obs_id,
            message="Analyse Argos enfilée — résultat disponible dans quelques instants",
        )

    # ══════════════════════════════════════════════════════════════════
    # NON-CONFORMITÉS
    # ══════════════════════════════════════════════════════════════════

    @router.post("/{affaire_id}/nonconformites", response_model=NonConformiteResponse, status_code=201)
    async def nc_create(
        affaire_id: uuid.UUID,
        payload: NonConformiteCreate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        nc = await create_nonconformite(db, affaire_id, **payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(nc)
        log.info("chantier.nc_created", affaire_id=str(affaire_id), gravite=nc.gravite)
        if nc.arret_chantier:
            log.warning("chantier.ARRET_CHANTIER", nc_id=str(nc.id), affaire_id=str(affaire_id))
        return nc

    @router.get("/{affaire_id}/nonconformites", response_model=list[NonConformiteResponse])
    async def nc_list(
        affaire_id: uuid.UUID,
        gravite: str | None = None,
        statut: str | None = None,
        lot_id: uuid.UUID | None = None,
        ouvertes_seulement: bool = False,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await list_nonconformites(
            db, affaire_id,
            gravite=gravite, statut=statut, lot_id=lot_id,
            ouvertes_seulement=ouvertes_seulement,
        )

    @router.patch("/nonconformites/{nc_id}", response_model=NonConformiteResponse)
    async def nc_update(
        nc_id: uuid.UUID,
        payload: NonConformiteUpdate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        nc = await get_nonconformite(db, nc_id)
        if not nc:
            raise HTTPException(404, "Non-conformité introuvable")
        nc = await update_nonconformite(db, nc, payload.model_dump(exclude_none=True))
        await db.commit()
        await db.refresh(nc)
        return nc

    @router.delete("/nonconformites/{nc_id}", status_code=204)
    async def nc_delete(
        nc_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        nc = await get_nonconformite(db, nc_id)
        if not nc:
            raise HTTPException(404, "Non-conformité introuvable")
        await delete_nonconformite(db, nc)
        await db.commit()

    @router.post("/nonconformites/{nc_id}/qualify", response_model=AnalyzeJobResponse)
    async def nc_qualify(
        nc_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        """Lance la qualification Héphaïstos sur la non-conformité en arrière-plan (ARQ)."""
        nc = await get_nonconformite(db, nc_id)
        if not nc:
            raise HTTPException(404, "Non-conformité introuvable")
        if nc.analyse_hephaistos:
            return AnalyzeJobResponse(
                job_queued=False,
                id=nc_id,
                message="Qualification déjà effectuée",
            )
        queue = await get_queue()
        await queue.enqueue_job("qualify_nc_job", str(nc_id))
        log.info("chantier.qualify_queued", nc_id=str(nc_id))
        return AnalyzeJobResponse(
            job_queued=True,
            id=nc_id,
            message="Qualification Héphaïstos enfilée — résultat disponible dans quelques instants",
        )

    # ══════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════════════════════════

    @router.get("/{affaire_id}/dashboard", response_model=ChantierDashboard)
    async def dashboard(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        result = await get_dashboard(db, affaire_id)
        return ChantierDashboard(**result)

    return router
