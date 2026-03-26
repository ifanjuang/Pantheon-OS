"""
Router admin — endpoints config YAML + serving de l'interface HTML.

Routes :
  GET  /admin/              → UI HTML (navigateur)
  GET  /admin/modules       → liste des modules + statut
  POST /admin/modules/{n}/toggle  → activer/désactiver
  GET  /admin/config/modules      → modules.yaml brut
  PUT  /admin/config/modules      → sauvegarder modules.yaml
  GET  /admin/config/{module}     → config.yaml d'un module
  PUT  /admin/config/{module}     → sauvegarder config.yaml d'un module

Toutes les routes PUT/POST exigent le rôle admin.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_role, get_current_user
from database import get_db
from modules.admin.engine import AdminEngine
import yaml


class YamlPayload(BaseModel):
    content: str


class TogglePayload(BaseModel):
    enabled: bool


def get_router(config: dict) -> APIRouter:
    router = APIRouter()
    editable = set(config.get("editable_modules", []))

    def _engine(db: AsyncSession = Depends(get_db)) -> AdminEngine:
        return AdminEngine(db=db, config=config)

    # ── UI ───────────────────────────────────────────────────────

    @router.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def config_ui():
        from modules.admin.ui import render_html
        return HTMLResponse(render_html())

    # ── API JSON ─────────────────────────────────────────────────

    @router.get("/modules")
    async def list_modules(
        _=Depends(require_role("admin", "moe")),
        engine: AdminEngine = Depends(_engine),
    ):
        return engine.list_modules()

    @router.post("/modules/{name}/toggle")
    async def toggle_module(
        name: str,
        payload: TogglePayload,
        _=Depends(require_role("admin")),
        engine: AdminEngine = Depends(_engine),
    ):
        try:
            engine.toggle_module(name, payload.enabled)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"ok": True, "module": name, "enabled": payload.enabled}

    @router.get("/config/modules")
    async def get_modules_yaml(
        _=Depends(require_role("admin", "moe")),
        engine: AdminEngine = Depends(_engine),
    ):
        data = engine.read_modules_yaml()
        return {"content": data["raw"]}

    @router.put("/config/modules")
    async def save_modules_yaml(
        payload: YamlPayload,
        _=Depends(require_role("admin")),
        engine: AdminEngine = Depends(_engine),
    ):
        try:
            engine.write_modules_yaml(payload.content)
        except (ValueError, yaml.YAMLError) as e:
            raise HTTPException(status_code=422, detail=str(e))
        return {"ok": True}

    @router.get("/config/{module}")
    async def get_module_config(
        module: str,
        _=Depends(require_role("admin", "moe")),
        engine: AdminEngine = Depends(_engine),
    ):
        if editable and module not in editable:
            raise HTTPException(status_code=403, detail="Module non autorisé")
        content = engine.read_module_config(module)
        return {"content": content}

    @router.put("/config/{module}")
    async def save_module_config(
        module: str,
        payload: YamlPayload,
        _=Depends(require_role("admin")),
        engine: AdminEngine = Depends(_engine),
    ):
        if editable and module not in editable:
            raise HTTPException(status_code=403, detail="Module non autorisé")
        try:
            engine.write_module_config(module, payload.content)
        except yaml.YAMLError as e:
            raise HTTPException(status_code=422, detail=f"YAML invalide : {e}")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"ok": True}

    return router
