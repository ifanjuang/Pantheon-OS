"""
Router evaluation — endpoints OpenClaw.

GET  /evaluation/datasets               → liste des datasets disponibles
GET  /evaluation/datasets/{dataset_id}  → inspecte un dataset (cas + attendus)
POST /evaluation/run/{dataset_id}       → exécute le dataset, retourne EvalReport

Accessible aux rôles admin / moe. L'exécution est synchrone (datasets courts,
< 30 cas). Pour un run sur CI long, passer `dry_run=true` pour valider le
parsing sans coûter de LLM.
"""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_role
from database import get_db
from modules.evaluation.schemas import EvalDataset, EvalReport
from modules.evaluation.service import list_datasets, load_dataset, run_eval


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.get("/datasets", response_model=list[str])
    async def get_datasets(
        _user=Depends(require_role("admin", "moe")),
    ):
        return list_datasets()

    @router.get("/datasets/{dataset_id}", response_model=EvalDataset)
    async def get_dataset(
        dataset_id: str,
        _user=Depends(require_role("admin", "moe")),
    ):
        try:
            return load_dataset(dataset_id)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} introuvable")

    @router.post("/run/{dataset_id}", response_model=EvalReport)
    async def run_dataset(
        dataset_id: str,
        affaire_id: Optional[UUID] = Query(
            None,
            description="Affaire pour contextualiser (sinon UUID sentinelle)",
        ),
        max_cases: Optional[int] = Query(None, ge=1, le=100),
        dry_run: bool = Query(
            False,
            description="Validation du parsing sans exécution réelle (CI)",
        ),
        db: AsyncSession = Depends(get_db),
        user=Depends(require_role("admin", "moe")),
    ):
        try:
            return await run_eval(
                db=db,
                dataset_id=dataset_id,
                affaire_id=affaire_id,
                user_id=user.id,
                max_cases=max_cases,
                dry_run=dry_run,
            )
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_id} introuvable")

    return router
