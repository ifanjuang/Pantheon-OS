"""
Control plane — lecture temps réel du système ARCEUS.

GET  /control/modules           → état de tous les modules (modules.yaml + manifests)
GET  /control/runs              → liste des orchestra runs (filtrable status/criticite)
GET  /control/runs/{id}/trace   → timeline d'un run reconstruite depuis les données DB
GET  /control/errors            → runs échoués + vetos bloquants
WS   /control/stream            → push temps réel (snapshot + delta toutes 2s)
"""

import asyncio
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_role
from core.settings import settings
from database import get_db
from .schemas import ControlSnapshot, ModuleStatus, RunSummary, ErrorEntry, TraceEvent
from .service import ControlService


def get_router(config: dict) -> APIRouter:
    router = APIRouter(tags=["control"])

    # ── REST ──────────────────────────────────────────────────────

    @router.get("/modules", response_model=list[ModuleStatus])
    async def list_modules(_=Depends(require_role("admin", "moe"))):
        return ControlService.get_modules()

    @router.get("/runs", response_model=list[RunSummary])
    async def list_runs(
        limit: int = Query(50, ge=1, le=200),
        status: str | None = Query(None),
        criticite: str | None = Query(None),
        db: AsyncSession = Depends(get_db),
        _=Depends(require_role("admin", "moe")),
    ):
        return await ControlService.get_runs(db, limit=limit, status=status, criticite=criticite)

    @router.get("/runs/{run_id}/trace", response_model=list[TraceEvent])
    async def get_trace(
        run_id: UUID,
        db: AsyncSession = Depends(get_db),
        _=Depends(require_role("admin", "moe")),
    ):
        return await ControlService.get_trace(db, run_id)

    @router.get("/errors", response_model=list[ErrorEntry])
    async def list_errors(
        limit: int = Query(50, ge=1, le=200),
        db: AsyncSession = Depends(get_db),
        _=Depends(require_role("admin", "moe")),
    ):
        return await ControlService.get_errors(db, limit=limit)

    @router.get("/jobs/failed")
    async def failed_jobs(
        limit: int = Query(20, ge=1, le=100),
        _=Depends(require_role("admin", "moe")),
    ):
        """Retourne les jobs ARQ échoués depuis la Dead-Letter Queue Redis."""
        try:
            import json
            import redis.asyncio as aioredis

            r = await aioredis.from_url(settings.REDIS_URL, decode_responses=True)
            raw = await r.lrange("arq:dlq", 0, limit - 1)
            await r.aclose()
            return [json.loads(entry) for entry in raw]
        except Exception as exc:
            from core.logging import get_logger

            get_logger("control.router").warning("dlq.read_failed", error=str(exc))
            return []

    @router.get("/snapshot", response_model=ControlSnapshot)
    async def snapshot(
        db: AsyncSession = Depends(get_db),
        _=Depends(require_role("admin", "moe")),
    ):
        modules, runs, errors = await asyncio.gather(
            asyncio.to_thread(ControlService.get_modules),
            ControlService.get_runs(db, limit=20),
            ControlService.get_errors(db, limit=20),
        )
        return ControlSnapshot(
            modules=modules,
            runs=runs,
            errors=errors,
            computed_at=datetime.now(timezone.utc),
        )

    # ── WebSocket ─────────────────────────────────────────────────

    @router.websocket("/stream")
    async def control_stream(websocket: WebSocket, db: AsyncSession = Depends(get_db)):
        await websocket.accept()
        run_state: dict[str, str] = {}  # run_id → last known status

        try:
            # Sync initial
            modules = ControlService.get_modules()
            runs = await ControlService.get_runs(db, limit=20)
            errors = await ControlService.get_errors(db, limit=20)

            await websocket.send_json(
                {
                    "type": "init",
                    "modules": [m.model_dump() for m in modules],
                    "runs": [r.model_dump(mode="json") for r in runs],
                    "errors": [e.model_dump(mode="json") for e in errors],
                }
            )

            for run in runs:
                run_state[run.run_id] = run.status

            tick = 0
            while True:
                await asyncio.sleep(2)
                tick += 1

                fresh_runs = await ControlService.get_runs(db, limit=20)
                for run in fresh_runs:
                    if run_state.get(run.run_id) != run.status or run.run_id not in run_state:
                        run_state[run.run_id] = run.status
                        await websocket.send_json(
                            {
                                "type": "run.update",
                                "data": run.model_dump(mode="json"),
                            }
                        )

                # Refresh errors every 10s
                if tick % 5 == 0:
                    fresh_errors = await ControlService.get_errors(db, limit=20)
                    await websocket.send_json(
                        {
                            "type": "errors.refresh",
                            "errors": [e.model_dump(mode="json") for e in fresh_errors],
                        }
                    )

                # Heartbeat every 20s
                if tick % 10 == 0:
                    await websocket.send_json(
                        {
                            "type": "heartbeat",
                            "ts": datetime.now(timezone.utc).isoformat(),
                        }
                    )

        except (WebSocketDisconnect, RuntimeError):
            pass

    return router
