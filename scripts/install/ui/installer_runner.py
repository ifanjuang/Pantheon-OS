"""Installer runner for Pantheon OS local installer UI.

This module intentionally runs local shell commands. It is meant for a trusted
LAN/NAS administrator, not for public exposure.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

import httpx

from installer_state import load_state, update_config, update_step

TARGETED_TESTS = [
    "tests/test_manifest_loader.py",
    "tests/test_manifest_contract.py",
    "tests/test_task_contracts.py",
    "tests/test_workflow_definition_loader.py",
    "tests/test_document_analysis_workflow.py",
    "tests/test_approval_contracts.py",
]


def run_command(command: list[str], *, timeout: int = 120) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = "\n".join(part for part in [completed.stdout, completed.stderr] if part)
        return completed.returncode, output.strip()
    except FileNotFoundError:
        return 127, f"Command not found: {command[0]}"
    except subprocess.TimeoutExpired:
        return 124, f"Command timed out: {' '.join(command)}"


async def check_docker() -> dict[str, Any]:
    code, output = run_command(["docker", "--version"], timeout=15)
    if code == 0:
        return update_step("docker", "ok", output)
    return update_step("docker", "error", output)


async def check_docker_compose() -> dict[str, Any]:
    code, output = run_command(["docker", "compose", "version"], timeout=15)
    if code == 0:
        return update_step("docker_compose", "ok", output)
    return update_step("docker_compose", "error", output)


async def check_ollama(ollama_host: str | None = None, chat_model: str | None = None, embedding_model: str | None = None) -> dict[str, Any]:
    state = load_state()
    config = state.get("config", {})
    ollama_host = ollama_host or config.get("ollama_host")
    chat_model = chat_model or config.get("chat_model") or "qwen2.5:7b"
    embedding_model = embedding_model or config.get("embedding_model") or "nomic-embed-text"

    if not ollama_host:
        return update_step("ollama", "error", "Missing Ollama host")

    if not ollama_host.startswith("http"):
        ollama_base_url = f"http://{ollama_host}:11434"
    else:
        ollama_base_url = ollama_host.rstrip("/")

    update_config({"ollama_host": ollama_host, "chat_model": chat_model, "embedding_model": embedding_model})

    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(f"{ollama_base_url}/api/tags")
            response.raise_for_status()
            payload = response.json()
    except Exception as exc:  # noqa: BLE001
        return update_step("ollama", "error", f"Ollama not reachable at {ollama_base_url}: {exc}")

    model_names = {item.get("name") for item in payload.get("models", []) if isinstance(item, dict)}
    missing = [model for model in [chat_model, embedding_model] if model and model not in model_names]
    if missing:
        return update_step(
            "ollama",
            "warning",
            f"Ollama reachable, but missing models: {', '.join(missing)}",
            {"base_url": ollama_base_url, "models": sorted(model_names)},
        )

    return update_step(
        "ollama",
        "ok",
        f"Ollama reachable with required models at {ollama_base_url}",
        {"base_url": ollama_base_url, "models": sorted(model_names)},
    )


def ensure_env_value(lines: list[str], key: str, value: str) -> list[str]:
    prefix = f"{key}="
    if any(line.startswith(prefix) for line in lines):
        return [f"{prefix}{value}" if line.startswith(prefix) else line for line in lines]
    lines.append(f"{prefix}{value}")
    return lines


async def check_env(ollama_host: str | None = None, chat_model: str | None = None, embedding_model: str | None = None) -> dict[str, Any]:
    state = load_state()
    config = state.get("config", {})
    ollama_host = ollama_host or config.get("ollama_host")
    chat_model = chat_model or config.get("chat_model") or "qwen2.5:7b"
    embedding_model = embedding_model or config.get("embedding_model") or "nomic-embed-text"

    env_path = Path(".env")
    if not env_path.exists():
        example = Path(".env.example")
        if example.exists():
            env_path.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            env_path.write_text("", encoding="utf-8")

    lines = env_path.read_text(encoding="utf-8").splitlines()

    if ollama_host:
        base_url = ollama_host if ollama_host.startswith("http") else f"http://{ollama_host}:11434"
        lines = ensure_env_value(lines, "OLLAMA_BASE_URL", base_url)
    lines = ensure_env_value(lines, "LLM_PROVIDER", "ollama")
    lines = ensure_env_value(lines, "DEFAULT_MODEL", chat_model)
    lines = ensure_env_value(lines, "EMBEDDING_MODEL", embedding_model)

    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    update_config({"ollama_host": ollama_host, "chat_model": chat_model, "embedding_model": embedding_model})
    return update_step("env", "ok", ".env checked and updated for Ollama")


async def start_containers() -> dict[str, Any]:
    update_step("containers", "running", "docker compose up -d --build started")
    code, output = run_command(["docker", "compose", "up", "-d", "--build"], timeout=900)
    if code == 0:
        return update_step("containers", "ok", "Containers started", {"output": output[-4000:]})
    return update_step("containers", "error", "Container startup failed", {"output": output[-4000:]})


async def run_migrations() -> dict[str, Any]:
    update_step("migrations", "running", "Running Alembic migrations")
    code, output = run_command(["docker", "compose", "exec", "-T", "api", "alembic", "upgrade", "head"], timeout=240)
    if code == 0:
        return update_step("migrations", "ok", "Migrations applied", {"output": output[-4000:]})
    return update_step("migrations", "warning", "Migrations failed or need manual Alembic verification", {"output": output[-4000:]})


async def run_tests() -> dict[str, Any]:
    update_step("tests", "running", "Running targeted tests")
    code, output = run_command(["docker", "compose", "exec", "-T", "api", "pytest", *TARGETED_TESTS], timeout=600)
    if code == 0:
        return update_step("tests", "ok", "Targeted tests passed", {"output": output[-4000:]})
    return update_step("tests", "warning", "Targeted tests failed", {"output": output[-4000:]})


async def check_health(api_base_url: str | None = None) -> dict[str, Any]:
    state = load_state()
    api_base_url = api_base_url or state.get("config", {}).get("api_base_url") or "http://localhost:8000"
    update_config({"api_base_url": api_base_url})
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(f"{api_base_url.rstrip('/')}/health")
            response.raise_for_status()
            payload = response.json()
        status = "ok" if payload.get("db") == "ok" else "warning"
        return update_step("health", status, f"/health returned {payload.get('status', 'unknown')}", payload)
    except Exception as exc:  # noqa: BLE001
        return update_step("health", "error", f"Health check failed: {exc}")


async def check_runtime_registry(api_base_url: str | None = None) -> dict[str, Any]:
    state = load_state()
    api_base_url = api_base_url or state.get("config", {}).get("api_base_url") or "http://localhost:8000"
    update_config({"api_base_url": api_base_url})
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(f"{api_base_url.rstrip('/')}/debug/runtime-registry")
            response.raise_for_status()
            payload = response.json()
        counts = payload.get("counts", {})
        return update_step("runtime_registry", "ok", "Runtime registry reachable", counts)
    except Exception as exc:  # noqa: BLE001
        return update_step("runtime_registry", "warning", f"Runtime registry check failed: {exc}")


async def run_all(ollama_host: str, chat_model: str, embedding_model: str, api_base_url: str = "http://localhost:8000") -> dict[str, Any]:
    update_config({
        "ollama_host": ollama_host,
        "chat_model": chat_model,
        "embedding_model": embedding_model,
        "api_base_url": api_base_url,
    })
    await check_docker()
    await check_docker_compose()
    await check_ollama(ollama_host, chat_model, embedding_model)
    await check_env(ollama_host, chat_model, embedding_model)
    await start_containers()
    await run_migrations()
    await run_tests()
    await check_health(api_base_url)
    await check_runtime_registry(api_base_url)
    return load_state()
