"""Pantheon OS local installer UI.

Run from repository root:

    python scripts/install/ui/installer_api.py

Then open:

    http://NAS_IP:8090

This mini-app is intentionally standalone and should only be exposed on a
trusted local network.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks, FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
import uvicorn

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from installer_runner import (  # noqa: E402
    check_docker,
    check_docker_compose,
    check_env,
    check_health,
    check_ollama,
    check_runtime_registry,
    run_all,
    run_migrations,
    run_tests,
    start_containers,
)
from installer_state import load_state, update_config  # noqa: E402

app = FastAPI(title="Pantheon OS Installer", version="0.1.0")

static_dir = CURRENT_DIR / "static"
templates_dir = CURRENT_DIR / "templates"
static_dir.mkdir(parents=True, exist_ok=True)
templates_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))


class InstallerConfig(BaseModel):
    ollama_host: str
    chat_model: str = "qwen2.5:7b"
    embedding_model: str = "nomic-embed-text"
    api_base_url: str = "http://localhost:8000"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "state": load_state()})


@app.get("/api/status")
async def status():
    return JSONResponse(load_state())


@app.post("/api/config")
async def save_config(config: InstallerConfig):
    return JSONResponse(update_config(config.model_dump()))


@app.post("/api/config-form")
async def save_config_form(
    ollama_host: str = Form(...),
    chat_model: str = Form("qwen2.5:7b"),
    embedding_model: str = Form("nomic-embed-text"),
    api_base_url: str = Form("http://localhost:8000"),
):
    state = update_config(
        {
            "ollama_host": ollama_host,
            "chat_model": chat_model,
            "embedding_model": embedding_model,
            "api_base_url": api_base_url,
        }
    )
    return JSONResponse(state)


@app.post("/api/check/docker")
async def api_check_docker():
    return JSONResponse(await check_docker())


@app.post("/api/check/docker-compose")
async def api_check_docker_compose():
    return JSONResponse(await check_docker_compose())


@app.post("/api/check/ollama")
async def api_check_ollama(config: InstallerConfig):
    return JSONResponse(await check_ollama(config.ollama_host, config.chat_model, config.embedding_model))


@app.post("/api/check/env")
async def api_check_env(config: InstallerConfig):
    return JSONResponse(await check_env(config.ollama_host, config.chat_model, config.embedding_model))


@app.post("/api/containers/start")
async def api_start_containers():
    return JSONResponse(await start_containers())


@app.post("/api/migrations/run")
async def api_run_migrations():
    return JSONResponse(await run_migrations())


@app.post("/api/tests/run")
async def api_run_tests():
    return JSONResponse(await run_tests())


@app.post("/api/check/health")
async def api_check_health(config: InstallerConfig):
    return JSONResponse(await check_health(config.api_base_url))


@app.post("/api/check/runtime-registry")
async def api_check_runtime_registry(config: InstallerConfig):
    return JSONResponse(await check_runtime_registry(config.api_base_url))


@app.post("/api/run-all")
async def api_run_all(config: InstallerConfig, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_all, config.ollama_host, config.chat_model, config.embedding_model, config.api_base_url)
    update_config(config.model_dump())
    return JSONResponse({"status": "started", "message": "Installer run started in background"})


@app.post("/run-all-form")
async def run_all_form(
    background_tasks: BackgroundTasks,
    ollama_host: str = Form(...),
    chat_model: str = Form("qwen2.5:7b"),
    embedding_model: str = Form("nomic-embed-text"),
    api_base_url: str = Form("http://localhost:8000"),
):
    update_config(
        {
            "ollama_host": ollama_host,
            "chat_model": chat_model,
            "embedding_model": embedding_model,
            "api_base_url": api_base_url,
        }
    )
    background_tasks.add_task(run_all, ollama_host, chat_model, embedding_model, api_base_url)
    return JSONResponse({"status": "started"})


if __name__ == "__main__":
    uvicorn.run("installer_api:app", host="0.0.0.0", port=8090, reload=False)
