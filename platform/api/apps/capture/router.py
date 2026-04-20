"""
Router capture — NoobScribe

POST /capture/upload                    -> upload audio + lancement pipeline
GET  /capture/sessions/{affaire_id}     -> liste des captures d'une affaire
GET  /capture/sessions/detail/{capture_id} -> detail d'une capture
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from core.services.storage_service import StorageService
from database import get_db
from apps.capture.models import CaptureSession
from apps.capture.schemas import CaptureListResponse, CaptureResponse
from apps.capture.service import transcribe_audio

log = get_logger("capture.router")

ALLOWED_AUDIO_MIME = {
    "audio/mpeg",
    "audio/mp4",
    "audio/wav",
    "audio/webm",
    "audio/ogg",
    "audio/x-m4a",
}
MAX_AUDIO_SIZE = 25 * 1024 * 1024  # 25 Mo


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.post("/upload", response_model=CaptureResponse, status_code=201)
    async def upload_capture(
        background_tasks: BackgroundTasks,
        file: Annotated[UploadFile, File()],
        affaire_id: Annotated[uuid.UUID, Form()],
        duration_seconds: Annotated[int | None, Form()] = None,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        """Upload un fichier audio depuis le chantier et lance le pipeline de traitement."""
        # Validation taille
        content = await file.read()
        if len(content) > MAX_AUDIO_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Fichier audio trop volumineux (max 25 Mo)",
            )

        # Validation type MIME
        mime = file.content_type or "application/octet-stream"
        if mime not in ALLOWED_AUDIO_MIME:
            raise HTTPException(
                status_code=415,
                detail=f"Type audio non supporté : {mime}",
            )

        filename = file.filename or f"capture_{uuid.uuid4()}.audio"

        # 1. Stocker dans MinIO
        audio_key = await StorageService.upload(
            affaire_id=affaire_id,
            module="capture",
            filename=filename,
            content=content,
            content_type=mime,
        )

        # 2. Tenter la transcription
        transcription = await transcribe_audio(content, filename)

        # 3. Créer la CaptureSession
        status = "pending"
        if transcription:
            status = "transcribing"  # transcription ok, processing à venir

        capture = CaptureSession(
            affaire_id=affaire_id,
            user_id=current_user.id,
            audio_key=audio_key,
            duration_seconds=duration_seconds,
            transcription=transcription,
            status=status,
        )
        db.add(capture)
        await db.flush()

        log.info(
            "capture.upload",
            capture_id=str(capture.id),
            affaire_id=str(affaire_id),
            filename=filename,
            size=len(content),
            has_transcription=transcription is not None,
        )

        # 4. Lancer le traitement en arrière-plan si transcription disponible
        if transcription:
            capture_id = capture.id
            user_id = current_user.id

            async def _process():
                from database import AsyncSessionLocal
                from apps.capture.service import process_capture

                async with AsyncSessionLocal() as bg_db:
                    await process_capture(
                        db=bg_db,
                        capture_id=capture_id,
                        transcription=transcription,
                        affaire_id=affaire_id,
                        user_id=user_id,
                    )

            background_tasks.add_task(_process)

        await db.commit()
        await db.refresh(capture)

        return CaptureResponse(
            id=capture.id,
            affaire_id=capture.affaire_id,
            status=capture.status,
            transcription=capture.transcription,
            structured_output=capture.structured_output,
            duration_seconds=capture.duration_seconds,
            agent_run_id=capture.agent_run_id,
            error_message=capture.error_message,
            created_at=capture.created_at.isoformat(),
        )

    @router.get("/sessions/{affaire_id}", response_model=list[CaptureListResponse])
    async def list_captures(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """Liste toutes les captures vocales d'une affaire."""
        result = await db.execute(
            select(CaptureSession)
            .where(CaptureSession.affaire_id == affaire_id)
            .order_by(CaptureSession.created_at.desc())
        )
        captures = result.scalars().all()
        return [
            CaptureListResponse(
                id=c.id,
                affaire_id=c.affaire_id,
                status=c.status,
                duration_seconds=c.duration_seconds,
                created_at=c.created_at.isoformat(),
            )
            for c in captures
        ]

    @router.get("/sessions/detail/{capture_id}", response_model=CaptureResponse)
    async def get_capture(
        capture_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """Retourne le détail d'une capture vocale."""
        capture = await db.get(CaptureSession, capture_id)
        if not capture:
            raise HTTPException(status_code=404, detail="Capture introuvable")
        return CaptureResponse(
            id=capture.id,
            affaire_id=capture.affaire_id,
            status=capture.status,
            transcription=capture.transcription,
            structured_output=capture.structured_output,
            duration_seconds=capture.duration_seconds,
            agent_run_id=capture.agent_run_id,
            error_message=capture.error_message,
            created_at=capture.created_at.isoformat(),
        )

    return router
