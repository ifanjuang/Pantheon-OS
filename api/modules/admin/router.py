"""
Router admin — config YAML + assistant d'installation.

Routes config :
  GET  /admin/                          → UI HTML (navigateur)
  GET  /admin/modules                   → liste modules + statut
  POST /admin/modules/{n}/toggle        → activer/désactiver
  GET  /admin/config/modules            → modules.yaml brut
  PUT  /admin/config/modules            → sauvegarder modules.yaml
  GET  /admin/schema/{module}           → config + manifest + prompt_files
  GET  /admin/config/{module}           → config.yaml brut
  PUT  /admin/config/{module}           → sauvegarder config.yaml
  GET  /admin/manifest/{module}         → manifest.yaml (lecture seule)
  GET  /admin/prompt/{module}/{file}    → contenu fichier prompt
  PUT  /admin/prompt/{module}/{file}    → sauvegarder fichier prompt

Routes setup/installation :
  GET  /admin/setup/status              → statut global tous services
  GET  /admin/setup/schema              → schéma formulaire .env
  PUT  /admin/setup/env                 → sauvegarder valeurs .env
  POST /admin/setup/test/{service}      → tester un service (db/minio/llm/smtp/telegram/whatsapp)
  GET  /admin/setup/ollama/models       → modèles Ollama disponibles
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import require_role
from database import get_db
from modules.admin.engine import AdminEngine
from modules.admin.setup_engine import SetupEngine
import yaml


class YamlPayload(BaseModel):
    content: str


class TogglePayload(BaseModel):
    enabled: bool


class PromptPayload(BaseModel):
    content: str


class EnvPayload(BaseModel):
    values: dict[str, str]


def get_router(config: dict) -> APIRouter:
    router = APIRouter()
    editable = set(config.get("editable_modules", []))

    def _engine(db: AsyncSession = Depends(get_db)) -> AdminEngine:
        return AdminEngine(db=db, config=config)

    def _check_editable(module: str):
        if editable and module not in editable:
            raise HTTPException(status_code=403, detail=f"Module '{module}' non autorisé")

    # ── UI HTML ──────────────────────────────────────────────────

    @router.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def config_ui():
        from modules.admin.ui import render_html
        return HTMLResponse(render_html())

    # ── Modules ──────────────────────────────────────────────────

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

    # ── modules.yaml ─────────────────────────────────────────────

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

    # ── Schéma complet pour formulaire ───────────────────────────

    @router.get("/schema/{module}")
    async def get_module_schema(
        module: str,
        _=Depends(require_role("admin", "moe")),
        engine: AdminEngine = Depends(_engine),
    ):
        """Retourne config + manifest + liste prompt_files pour alimenter le formulaire UI."""
        _check_editable(module)
        return engine.get_form_schema(module)

    # ── config.yaml ──────────────────────────────────────────────

    @router.get("/config/{module}")
    async def get_module_config(
        module: str,
        _=Depends(require_role("admin", "moe")),
        engine: AdminEngine = Depends(_engine),
    ):
        _check_editable(module)
        return {"content": engine.read_module_config(module)}

    @router.put("/config/{module}")
    async def save_module_config(
        module: str,
        payload: YamlPayload,
        _=Depends(require_role("admin")),
        engine: AdminEngine = Depends(_engine),
    ):
        _check_editable(module)
        try:
            engine.write_module_config(module, payload.content)
        except yaml.YAMLError as e:
            raise HTTPException(status_code=422, detail=f"YAML invalide : {e}")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"ok": True}

    # ── manifest.yaml (lecture seule) ────────────────────────────

    @router.get("/manifest/{module}")
    async def get_module_manifest(
        module: str,
        _=Depends(require_role("admin", "moe")),
        engine: AdminEngine = Depends(_engine),
    ):
        manifest = engine.read_module_manifest(module)
        return {"manifest": manifest}

    # ── Fichiers prompt ───────────────────────────────────────────

    @router.get("/prompt/{module}/{filename}")
    async def get_prompt_file(
        module: str,
        filename: str,
        _=Depends(require_role("admin", "moe")),
        engine: AdminEngine = Depends(_engine),
    ):
        _check_editable(module)
        try:
            content = engine.read_prompt_file(module, filename)
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        return {"content": content}

    @router.put("/prompt/{module}/{filename}")
    async def save_prompt_file(
        module: str,
        filename: str,
        payload: PromptPayload,
        _=Depends(require_role("admin")),
        engine: AdminEngine = Depends(_engine),
    ):
        _check_editable(module)
        try:
            engine.write_prompt_file(module, filename, payload.content)
        except (ValueError, FileNotFoundError) as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"ok": True}

    # ── Setup / Installation ─────────────────────────────────────

    @router.get("/setup/status")
    async def setup_status(_=Depends(require_role("admin", "moe"))):
        engine = SetupEngine()
        return await engine.full_status()

    @router.get("/setup/schema")
    async def setup_schema(_=Depends(require_role("admin"))):
        engine = SetupEngine()
        return {"groups": engine.get_schema()}

    @router.put("/setup/env")
    async def save_env(
        payload: EnvPayload,
        _=Depends(require_role("admin")),
    ):
        engine = SetupEngine()
        try:
            engine.save_env(payload.values)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"ok": True, "saved": list(payload.values.keys())}

    @router.post("/setup/test/{service}")
    async def test_service(
        service: str,
        _=Depends(require_role("admin", "moe")),
    ):
        engine = SetupEngine()
        testers = {
            "db": engine.test_db,
            "minio": engine.test_minio,
            "llm": engine.test_llm,
            "smtp": engine.test_smtp,
            "telegram": engine.test_telegram,
            "whatsapp": engine.test_whatsapp,
        }
        if service not in testers:
            raise HTTPException(status_code=404, detail=f"Service inconnu : {service}. Valides : {list(testers)}")
        result = await testers[service]()
        return result

    @router.get("/setup/ollama/models")
    async def ollama_models(_=Depends(require_role("admin", "moe"))):
        engine = SetupEngine()
        models = await engine.ollama_list_models()
        return {"models": models}

    return router
