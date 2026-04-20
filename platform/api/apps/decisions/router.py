"""
Router decisions — dashboard mémoire projet.

── Décisions ────────────────────────────────────────────────────────
POST   /decisions/                   → créer
GET    /decisions/                   → lister (filtres affaire/criticite/dette/statut/lot/phase)
GET    /decisions/{id}               → détail
PATCH  /decisions/{id}               → éditer
DELETE /decisions/{id}               → supprimer (admin)

── Vues dashboard ──────────────────────────────────────────────────
GET    /decisions/views/critiques         → C4/C5
GET    /decisions/views/dettes            → D2/D3 ouvertes
GET    /decisions/views/non-validees      → C4/C5 sans validation
GET    /decisions/views/par-lot           → regroupement métier
GET    /decisions/views/timeline          → par phase (APS→DOE)

── KPIs ────────────────────────────────────────────────────────────
GET    /decisions/kpis                    → nb critiques, dette moy, délai, % revues

── Tâches ──────────────────────────────────────────────────────────
POST   /decisions/tasks/                  → créer
GET    /decisions/tasks/{affaire_id}      → lister par affaire
PATCH  /decisions/tasks/{id}              → éditer
DELETE /decisions/tasks/{id}              → supprimer

── Observations ────────────────────────────────────────────────────
POST   /decisions/observations/           → créer
GET    /decisions/observations/{affaire_id} → lister par affaire
PATCH  /decisions/observations/{id}       → éditer
DELETE /decisions/observations/{id}       → supprimer
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from database import get_db
from apps.decisions.models import ProjectDecision, ProjectObservation, ProjectTask
from apps.decisions.schemas import (
    DecisionCreateRequest,
    DecisionKPIs,
    DecisionResponse,
    DecisionRow,
    DecisionUpdateRequest,
    LotBucket,
    ObservationCreateRequest,
    ObservationResponse,
    ObservationUpdateRequest,
    TaskCreateRequest,
    TaskResponse,
    TaskUpdateRequest,
    TimelineBucket,
)
from apps.decisions.service import DecisionsService

log = get_logger("decisions.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    # ── KPIs (déclaré avant les routes paramétriques) ──────────────

    @router.get("/kpis", response_model=DecisionKPIs)
    async def kpis(
        affaire_id: Optional[uuid.UUID] = Query(None),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await DecisionsService.kpis(db, affaire_id)

    # ── Vues dashboard ─────────────────────────────────────────────

    @router.get("/views/critiques", response_model=list[DecisionRow])
    async def view_critiques(
        affaire_id: Optional[uuid.UUID] = Query(None),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await DecisionsService.view_critiques(db, affaire_id)

    @router.get("/views/dettes", response_model=list[DecisionRow])
    async def view_dettes(
        affaire_id: Optional[uuid.UUID] = Query(None),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await DecisionsService.view_dettes(db, affaire_id)

    @router.get("/views/non-validees", response_model=list[DecisionRow])
    async def view_non_validees(
        affaire_id: Optional[uuid.UUID] = Query(None),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await DecisionsService.view_non_validees(db, affaire_id)

    @router.get("/views/par-lot", response_model=list[LotBucket])
    async def view_par_lot(
        affaire_id: Optional[uuid.UUID] = Query(None),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await DecisionsService.view_par_lot(db, affaire_id)

    @router.get("/views/timeline", response_model=list[TimelineBucket])
    async def view_timeline(
        affaire_id: Optional[uuid.UUID] = Query(None),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await DecisionsService.view_timeline(db, affaire_id)

    # ── CRUD Décisions ─────────────────────────────────────────────

    @router.post("/", response_model=DecisionResponse, status_code=201)
    async def create_decision(
        payload: DecisionCreateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        decision = ProjectDecision(**payload.model_dump())
        db.add(decision)
        await db.commit()
        await db.refresh(decision)
        log.info("decisions.created", id=str(decision.id), criticite=decision.criticite)
        return decision

    @router.get("/", response_model=list[DecisionResponse])
    async def list_decisions(
        affaire_id: Optional[uuid.UUID] = Query(None),
        criticite: Optional[str] = Query(None, pattern="^C[1-5]$"),
        dette: Optional[str] = Query(None, pattern="^D[0-3]$"),
        statut: Optional[str] = Query(None),
        lot: Optional[str] = Query(None),
        phase: Optional[str] = Query(None),
        limit: int = Query(100, ge=1, le=500),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        query = select(ProjectDecision)
        if affaire_id:
            query = query.where(ProjectDecision.affaire_id == affaire_id)
        if criticite:
            query = query.where(ProjectDecision.criticite == criticite)
        if dette:
            query = query.where(ProjectDecision.dette == dette)
        if statut:
            query = query.where(ProjectDecision.statut == statut)
        if lot:
            query = query.where(ProjectDecision.lot == lot)
        if phase:
            query = query.where(ProjectDecision.phase == phase)
        query = query.order_by(ProjectDecision.created_at.desc()).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @router.get("/{decision_id}", response_model=DecisionResponse)
    async def get_decision(
        decision_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        decision = await db.get(ProjectDecision, decision_id)
        if not decision:
            raise HTTPException(status_code=404, detail="Décision introuvable")
        return decision

    @router.patch("/{decision_id}", response_model=DecisionResponse)
    async def update_decision(
        decision_id: uuid.UUID,
        payload: DecisionUpdateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe")),
    ):
        decision = await db.get(ProjectDecision, decision_id)
        if not decision:
            raise HTTPException(status_code=404, detail="Décision introuvable")
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(decision, field, value)
        await db.commit()
        await db.refresh(decision)
        return decision

    @router.delete("/{decision_id}", status_code=204)
    async def delete_decision(
        decision_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        decision = await db.get(ProjectDecision, decision_id)
        if not decision:
            raise HTTPException(status_code=404, detail="Décision introuvable")
        await db.delete(decision)
        await db.commit()

    # ── CRUD Tâches ────────────────────────────────────────────────

    @router.post("/tasks/", response_model=TaskResponse, status_code=201)
    async def create_task(
        payload: TaskCreateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        task = ProjectTask(**payload.model_dump())
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @router.get("/tasks/{affaire_id}", response_model=list[TaskResponse])
    async def list_tasks(
        affaire_id: uuid.UUID,
        statut: str = "ouvert,en_cours,bloque",
        decision_id: Optional[uuid.UUID] = Query(None),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        query = select(ProjectTask).where(ProjectTask.affaire_id == affaire_id)
        if statut != "all":
            statuts = [s.strip() for s in statut.split(",")]
            query = query.where(ProjectTask.statut.in_(statuts))
        if decision_id:
            query = query.where(ProjectTask.decision_id == decision_id)
        query = query.order_by(
            ProjectTask.urgence.desc(),
            ProjectTask.echeance.asc().nulls_last(),
        )
        result = await db.execute(query)
        return result.scalars().all()

    @router.patch("/tasks/{task_id}", response_model=TaskResponse)
    async def update_task(
        task_id: uuid.UUID,
        payload: TaskUpdateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        task = await db.get(ProjectTask, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tâche introuvable")
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(task, field, value)
        await db.commit()
        await db.refresh(task)
        return task

    @router.delete("/tasks/{task_id}", status_code=204)
    async def delete_task(
        task_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin", "moe")),
    ):
        task = await db.get(ProjectTask, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tâche introuvable")
        await db.delete(task)
        await db.commit()

    # ── CRUD Observations ──────────────────────────────────────────

    @router.post("/observations/", response_model=ObservationResponse, status_code=201)
    async def create_observation(
        payload: ObservationCreateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        obs = ProjectObservation(**payload.model_dump(), auteur=current_user.id)
        db.add(obs)
        await db.commit()
        await db.refresh(obs)
        return obs

    @router.get("/observations/{affaire_id}", response_model=list[ObservationResponse])
    async def list_observations(
        affaire_id: uuid.UUID,
        traitement: str = "a_traiter,en_cours",
        decision_id: Optional[uuid.UUID] = Query(None),
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        query = select(ProjectObservation).where(ProjectObservation.affaire_id == affaire_id)
        if traitement != "all":
            traitements = [t.strip() for t in traitement.split(",")]
            query = query.where(ProjectObservation.traitement.in_(traitements))
        if decision_id:
            query = query.where(ProjectObservation.decision_id == decision_id)
        query = query.order_by(ProjectObservation.created_at.desc())
        result = await db.execute(query)
        return result.scalars().all()

    @router.patch("/observations/{obs_id}", response_model=ObservationResponse)
    async def update_observation(
        obs_id: uuid.UUID,
        payload: ObservationUpdateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        obs = await db.get(ProjectObservation, obs_id)
        if not obs:
            raise HTTPException(status_code=404, detail="Observation introuvable")
        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(obs, field, value)
        await db.commit()
        await db.refresh(obs)
        return obs

    @router.delete("/observations/{obs_id}", status_code=204)
    async def delete_observation(
        obs_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin", "moe")),
    ):
        obs = await db.get(ProjectObservation, obs_id)
        if not obs:
            raise HTTPException(status_code=404, detail="Observation introuvable")
        await db.delete(obs)
        await db.commit()

    return router
