from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from database import get_db
from .models import WorkflowDefinition
from .schemas import (
    WorkflowDefinitionCreate,
    WorkflowDefinitionOut,
    WorkflowDefinitionUpdate,
    WorkflowTrigger,
    WorkflowTriggerOut,
)
from .service import FlowManagerService


def get_router(config: dict) -> APIRouter:
    router = APIRouter(tags=["flowmanager"])

    # ── Liste ────────────────────────────────────────────────────────────────

    @router.get("", response_model=list[WorkflowDefinitionOut])
    async def list_workflows(
        active_only: bool = False,
        db: AsyncSession = Depends(get_db),
        _=Depends(get_current_user),
    ):
        return await FlowManagerService.list_workflows(db, active_only=active_only)

    # ── Création ─────────────────────────────────────────────────────────────

    @router.post("", response_model=WorkflowDefinitionOut, status_code=201)
    async def create_workflow(
        data: WorkflowDefinitionCreate,
        db: AsyncSession = Depends(get_db),
        _=Depends(require_role("admin", "moe")),
    ):
        existing = await FlowManagerService.get_by_name(db, data.name)
        if existing:
            raise HTTPException(status_code=409, detail=f"Workflow '{data.name}' existe déjà")
        return await FlowManagerService.create(db, data)

    # ── Import YAML brut ──────────────────────────────────────────────────────

    @router.post("/import", response_model=WorkflowDefinitionOut, status_code=201)
    async def import_yaml(
        yaml_content: str,
        db: AsyncSession = Depends(get_db),
        _=Depends(require_role("admin", "moe")),
    ):
        try:
            return await FlowManagerService.create_from_yaml(db, yaml_content)
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"YAML invalide : {exc}") from exc

    # ── Lecture ───────────────────────────────────────────────────────────────

    @router.get("/{name}", response_model=WorkflowDefinitionOut)
    async def get_workflow(
        name: str,
        db: AsyncSession = Depends(get_db),
        _=Depends(get_current_user),
    ):
        wf = await FlowManagerService.get_by_name(db, name)
        if not wf:
            raise HTTPException(status_code=404, detail=f"Workflow '{name}' introuvable")
        return wf

    # ── Mise à jour ───────────────────────────────────────────────────────────

    @router.patch("/{name}", response_model=WorkflowDefinitionOut)
    async def update_workflow(
        name: str,
        data: WorkflowDefinitionUpdate,
        db: AsyncSession = Depends(get_db),
        _=Depends(require_role("admin", "moe")),
    ):
        wf = await FlowManagerService.get_by_name(db, name)
        if not wf:
            raise HTTPException(status_code=404, detail=f"Workflow '{name}' introuvable")
        return await FlowManagerService.update(db, wf, data)

    # ── Désactivation ─────────────────────────────────────────────────────────

    @router.delete("/{name}", response_model=WorkflowDefinitionOut)
    async def deactivate_workflow(
        name: str,
        db: AsyncSession = Depends(get_db),
        _=Depends(require_role("admin", "moe")),
    ):
        wf = await FlowManagerService.get_by_name(db, name)
        if not wf:
            raise HTTPException(status_code=404, detail=f"Workflow '{name}' introuvable")
        return await FlowManagerService.deactivate(db, wf)

    # ── Déclenchement ─────────────────────────────────────────────────────────

    @router.post("/{name}/trigger", response_model=WorkflowTriggerOut, status_code=202)
    async def trigger_workflow(
        name: str,
        body: WorkflowTrigger,
        db: AsyncSession = Depends(get_db),
        user=Depends(get_current_user),
    ):
        wf = await FlowManagerService.get_by_name(db, name)
        if not wf or not wf.is_active:
            raise HTTPException(
                status_code=404,
                detail=f"Workflow '{name}' introuvable ou inactif",
            )
        # Import tardif pour éviter les imports circulaires
        from modules.orchestra.service import OrchestraService
        run_id = await OrchestraService.create_run(
            db=db,
            instruction=body.instruction,
            affaire_id=body.affaire_id,
            user_id=str(user.id),
            criticite_override=body.criticite,
            workflow_name=name,
        )
        return WorkflowTriggerOut(run_id=run_id, workflow_name=name)

    return router
