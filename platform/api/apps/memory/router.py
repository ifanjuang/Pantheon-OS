"""
Router memory — mémoire fonctionnelle TTL (session).

GET    /memory/context/{thread_id}   → état courant (json)
POST   /memory/context               → set_context (batch de MemoryEntry)
DELETE /memory/context/{thread_id}   → purge complète d'un thread
DELETE /memory/context/{thread_id}/{key} → purge d'une clé
POST   /memory/promote               → promote_to_project (→ Hestia)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user
from core.logging import get_logger
from database import get_db
from modules.memory.schemas import (
    GetContextResponse,
    PromoteRequest,
    PromoteResponse,
    SetContextRequest,
)
from modules.memory.service import FunctionalMemoryService

log = get_logger("memory.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.get("/context/{thread_id}", response_model=GetContextResponse)
    async def get_context(thread_id: str, _user=Depends(get_current_user)):
        ctx = await FunctionalMemoryService.get_context(thread_id)
        return GetContextResponse(
            thread_id=thread_id,
            context=ctx,
            keys_count=len(ctx),
        )

    @router.post("/context", response_model=GetContextResponse)
    async def set_context(
        payload: SetContextRequest,
        _user=Depends(get_current_user),
    ):
        written = 0
        for entry in payload.entries:
            ok = await FunctionalMemoryService.set_context(
                payload.thread_id,
                entry.key,
                entry.value,
                ttl=entry.ttl,
            )
            if ok:
                written += 1
        ctx = await FunctionalMemoryService.get_context(payload.thread_id)
        return GetContextResponse(
            thread_id=payload.thread_id,
            context=ctx,
            keys_count=len(ctx),
        )

    @router.delete("/context/{thread_id}")
    async def delete_thread(thread_id: str, _user=Depends(get_current_user)):
        deleted = await FunctionalMemoryService.delete_context(thread_id)
        return {"thread_id": thread_id, "deleted": deleted}

    @router.delete("/context/{thread_id}/{key}")
    async def delete_key(
        thread_id: str,
        key: str,
        _user=Depends(get_current_user),
    ):
        deleted = await FunctionalMemoryService.delete_context(thread_id, key)
        return {"thread_id": thread_id, "key": key, "deleted": deleted}

    @router.post("/promote", response_model=PromoteResponse)
    async def promote(
        payload: PromoteRequest,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        try:
            ok, memory_id = await FunctionalMemoryService.promote_to_project(
                db,
                thread_id=payload.thread_id,
                affaire_id=payload.affaire_id,
                lesson=payload.lesson,
                category=payload.category or "general",
                agent=payload.agent,
            )
            if not ok:
                return PromoteResponse(
                    promoted=False,
                    reason="Échec de la promotion (voir logs)",
                )
            await db.commit()
            return PromoteResponse(promoted=True, memory_id=memory_id)
        except Exception as exc:
            await db.rollback()
            log.error("memory.promote_failed", error=str(exc))
            raise HTTPException(status_code=500, detail=str(exc))

    return router
