"""
Router documents

POST /documents/upload          → upload + ingest RAG (moe, collaborateur, admin)
POST /documents/search          → recherche sémantique (tous rôles)
GET  /documents/                → liste documents d'une affaire
DELETE /documents/{document_id} → supprime document + chunks + fichier MinIO (admin/moe)
"""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from core.services.rag_service import RagService
from core.services.storage_service import StorageService
from database import get_db
from modules.documents.models import Document
from modules.documents.schemas import DocumentResponse, IngestResponse, SearchRequest, SearchResult

log = get_logger("documents.router")

ALLOWED_MIME = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
}
MAX_SIZE_BYTES = 50 * 1024 * 1024  # 50 Mo


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.post("/upload", response_model=IngestResponse, status_code=201)
    async def upload_document(
        file: Annotated[UploadFile, File()],
        affaire_id: Annotated[uuid.UUID, Form()],
        couche: Annotated[str, Form()] = "projet",
        source_type: Annotated[str, Form()] = "note",
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        # Validation taille
        content = await file.read()
        if len(content) > MAX_SIZE_BYTES:
            raise HTTPException(status_code=413, detail="Fichier trop volumineux (max 50 Mo)")

        # Validation type MIME
        mime = file.content_type or "application/octet-stream"
        if mime not in ALLOWED_MIME:
            raise HTTPException(
                status_code=415,
                detail=f"Type de fichier non supporté : {mime}",
            )

        nom = file.filename or f"document_{uuid.uuid4()}"

        # 1. Stocker dans MinIO
        storage_key = await StorageService.upload(
            affaire_id=affaire_id,
            module="documents",
            filename=nom,
            content=content,
            content_type=mime,
        )

        # 2. Créer l'enregistrement Document
        doc = Document(
            affaire_id=affaire_id,
            nom=nom,
            couche=couche,
            type_doc=nom.rsplit(".", 1)[-1].lower() if "." in nom else "bin",
            mime_type=mime,
            taille_octets=len(content),
            storage_key=storage_key,
            uploaded_by=current_user.id,
        )
        db.add(doc)
        await db.flush()

        # 3. Ingérer (chunking + embedding → table chunks)
        chunks_created = await RagService.ingest(
            db=db,
            document_id=doc.id,
            file_bytes=content,
            filename=nom,
            source_type=source_type,
            affaire_id=affaire_id,
        )

        await db.commit()
        await db.refresh(doc)

        log.info(
            "documents.upload",
            document_id=str(doc.id),
            nom=nom,
            chunks=chunks_created,
            uploaded_by=str(current_user.id),
        )
        return IngestResponse(
            document_id=doc.id,
            nom=nom,
            storage_key=storage_key,
            chunks_created=chunks_created,
        )

    @router.post("/search", response_model=list[SearchResult])
    async def search(
        payload: SearchRequest,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        results = await RagService.search(
            db=db,
            query=payload.query,
            affaire_id=payload.affaire_id,
            top_k=payload.top_k,
            source_type=payload.source_type,
        )
        return results

    @router.get("/", response_model=list[DocumentResponse])
    async def list_documents(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        result = await db.execute(
            select(Document)
            .where(Document.affaire_id == affaire_id)
            .order_by(Document.created_at.desc())
        )
        return result.scalars().all()

    @router.delete("/{document_id}", status_code=204)
    async def delete_document(
        document_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin", "moe")),
    ):
        doc = await db.get(Document, document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document introuvable")

        # Supprimer chunks
        await RagService.delete_document(db=db, document_id=document_id)

        # Supprimer fichier MinIO
        await StorageService.delete(doc.storage_key)

        # Supprimer enregistrement
        await db.delete(doc)
        await db.commit()

        log.info("documents.delete", document_id=str(document_id))

    return router
