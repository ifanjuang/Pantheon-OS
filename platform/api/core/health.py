"""
Endpoint /health unifié (§23.3).
Vérifie db, minio, llm, et optionnellement les providers de notification.
Retourne HTTP 200 même en état dégradé — HTTP 503 uniquement si db=error.
Exempté d'auth (comme /auth/login).
"""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from core.logging import get_logger

log = get_logger("health")
router = APIRouter(tags=["health"])


async def _check_db(db: AsyncSession) -> str:
    try:
        await db.execute(text("SELECT 1"))
        return "ok"
    except Exception as e:
        log.error("health.db_error", error=str(e))
        return "error"


async def _check_minio() -> str:
    try:
        from core.services.storage_service import StorageService

        ok = await StorageService.ping()
        return "ok" if ok else "error"
    except Exception:
        return "error"


async def _check_llm() -> str:
    try:
        from core.services.llm_service import LlmService

        ok = await LlmService.ping()
        return "ok" if ok else "error"
    except Exception:
        return "error"


async def _check_redis() -> str:
    try:
        from core.queue import get_queue

        await get_queue()
        # ARQ pool exposes the redis connection
        return "ok"
    except Exception:
        return "unavailable"


async def _check_events() -> str:
    try:
        import core.events as events

        pool = events.get_pool()
        return "ok" if pool else "unavailable"
    except RuntimeError:
        return "unavailable"
    except Exception:
        return "error"


@router.get("/health", include_in_schema=False)
async def health(db: AsyncSession = Depends(get_db)):
    checks: dict = {}
    checks["db"] = await _check_db(db)
    checks["minio"] = await _check_minio()
    checks["llm"] = await _check_llm()
    checks["redis"] = await _check_redis()
    checks["events"] = await _check_events()

    # Circuit breaker LLM (état du disjoncteur local)
    try:
        from core.circuit_breaker import llm_breaker

        checks["llm_circuit"] = llm_breaker.state  # closed | open | half_open
    except Exception:
        pass

    # Provider notifications (si module chargé)
    try:
        from core.registry import registry

        if registry and registry.is_enabled("notifications"):
            from modules.notifications.engine import notification_engine

            checks["notifications"] = await notification_engine.check_all_providers()
    except Exception:
        pass

    overall = "ok" if all(v == "ok" for v in checks.values() if isinstance(v, str)) else "degraded"
    checks["status"] = overall

    status_code = 503 if checks.get("db") == "error" else 200
    log.info("health.check", **checks)
    return JSONResponse(content=checks, status_code=status_code)
