"""
Router communications

Courriers
  POST   /communications/{affaire_id}/courriers          → créer courrier
  GET    /communications/{affaire_id}/courriers          → lister
  GET    /communications/courriers/{id}                  → détail
  PATCH  /communications/courriers/{id}                  → modifier
  DELETE /communications/courriers/{id}                  → supprimer (admin)
  POST   /communications/courriers/{id}/draft-response   → Iris rédige un brouillon (ARQ)

Dashboard
  GET    /communications/{affaire_id}/dashboard          → KPIs registre
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from core.queue import get_queue
from database import get_db
from modules.communications.schemas import (
    CommunicationsDashboard,
    CourrierCreate,
    CourrierResponse,
    CourrierUpdate,
    DraftJobResponse,
)
from modules.communications.service import (
    create_courrier,
    delete_courrier,
    get_courrier,
    get_dashboard,
    list_courriers,
    update_courrier,
)

log = get_logger("communications.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    # ══════════════════════════════════════════════════════════════════
    # COURRIERS
    # ══════════════════════════════════════════════════════════════════

    @router.post("/{affaire_id}/courriers", response_model=CourrierResponse, status_code=201)
    async def courrier_create(
        affaire_id: uuid.UUID,
        payload: CourrierCreate,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe")),
    ):
        courrier = await create_courrier(
            db,
            affaire_id,
            auteur_id=current_user.id,
            **payload.model_dump(exclude_none=True),
        )
        await db.commit()
        await db.refresh(courrier)
        log.info(
            "communications.courrier_created",
            affaire_id=str(affaire_id),
            sens=courrier.sens,
            type_doc=courrier.type_doc,
        )
        if courrier.type_doc == "mise_en_demeure":
            log.warning(
                "communications.MISE_EN_DEMEURE",
                courrier_id=str(courrier.id),
                affaire_id=str(affaire_id),
            )
        # Indexation RAG automatique si du texte est disponible
        if courrier.objet or courrier.resume:
            queue = await get_queue()
            await queue.enqueue_job("ingest_courrier_job", str(courrier.id))
        return courrier

    @router.get("/{affaire_id}/courriers", response_model=list[CourrierResponse])
    async def courrier_list(
        affaire_id: uuid.UUID,
        sens: str | None = None,
        type_doc: str | None = None,
        statut: str | None = None,
        en_retard_seulement: bool = False,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        return await list_courriers(
            db,
            affaire_id,
            sens=sens,
            type_doc=type_doc,
            statut=statut,
            en_retard_seulement=en_retard_seulement,
        )

    @router.get("/courriers/{courrier_id}", response_model=CourrierResponse)
    async def courrier_detail(
        courrier_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        courrier = await get_courrier(db, courrier_id)
        if not courrier:
            raise HTTPException(404, "Courrier introuvable")
        return courrier

    @router.patch("/courriers/{courrier_id}", response_model=CourrierResponse)
    async def courrier_update(
        courrier_id: uuid.UUID,
        payload: CourrierUpdate,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        courrier = await get_courrier(db, courrier_id)
        if not courrier:
            raise HTTPException(404, "Courrier introuvable")
        updated_data = payload.model_dump(exclude_none=True)
        courrier = await update_courrier(db, courrier, updated_data)
        await db.commit()
        await db.refresh(courrier)
        # Réindexation RAG si objet ou résumé mis à jour
        if "objet" in updated_data or "resume" in updated_data:
            queue = await get_queue()
            await queue.enqueue_job("ingest_courrier_job", str(courrier_id))
        return courrier

    @router.delete("/courriers/{courrier_id}", status_code=204)
    async def courrier_delete(
        courrier_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        courrier = await get_courrier(db, courrier_id)
        if not courrier:
            raise HTTPException(404, "Courrier introuvable")
        await delete_courrier(db, courrier)
        await db.commit()

    @router.post("/courriers/{courrier_id}/draft-response", response_model=DraftJobResponse)
    async def courrier_draft(
        courrier_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(require_role("admin", "moe")),
    ):
        """Lance Iris pour rédiger un brouillon de réponse (ARQ)."""
        courrier = await get_courrier(db, courrier_id)
        if not courrier:
            raise HTTPException(404, "Courrier introuvable")
        if courrier.sens != "entrant":
            raise HTTPException(422, "La rédaction de brouillon ne s'applique qu'aux courriers entrants")
        if courrier.draft_iris:
            return DraftJobResponse(
                job_queued=False,
                id=courrier_id,
                message="Brouillon déjà disponible",
            )
        queue = await get_queue()
        await queue.enqueue_job("draft_courrier_job", str(courrier_id))
        log.info("communications.draft_queued", courrier_id=str(courrier_id))
        return DraftJobResponse(
            job_queued=True,
            id=courrier_id,
            message="Rédaction Iris enfilée — brouillon disponible dans quelques instants",
        )

    # ══════════════════════════════════════════════════════════════════
    # DASHBOARD
    # ══════════════════════════════════════════════════════════════════

    @router.get("/{affaire_id}/dashboard", response_model=CommunicationsDashboard)
    async def dashboard(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        result = await get_dashboard(db, affaire_id)
        return CommunicationsDashboard(**result)

    return router
