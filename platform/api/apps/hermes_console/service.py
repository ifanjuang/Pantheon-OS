"""Hermes Console — service layer bridging YAML registries to the API."""
import sys
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

_CONFIG_DIR = Path("/config")
_AGENTS_FILE = _CONFIG_DIR / "agents.yaml"
_SKILLS_FILE = _CONFIG_DIR / "skills.yaml"
_WORKFLOWS_FILE = _CONFIG_DIR / "workflows.yaml"
_SETTINGS_FILE = _CONFIG_DIR / "settings.yaml"

_runtime_logs: list[dict] = []


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text()) or {}


def _save_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.dump(data, allow_unicode=True, default_flow_style=False))


# ── Agents ────────────────────────────────────────────────────────

def list_agents() -> list[dict]:
    data = _load_yaml(_AGENTS_FILE)
    agents = data.get("agents", {})
    return [
        {
            "name": name,
            "layer": cfg.get("layer", ""),
            "role": cfg.get("role", ""),
            "enabled": cfg.get("enabled", True),
            "veto": cfg.get("veto", False),
            "description": cfg.get("description", ""),
        }
        for name, cfg in agents.items()
    ]


def toggle_agent(name: str, enabled: bool) -> dict:
    data = _load_yaml(_AGENTS_FILE)
    agents = data.get("agents", {})
    key = name.upper()
    if key not in agents:
        return {"error": f"Agent {key} not found"}
    agents[key]["enabled"] = enabled
    data["agents"] = agents
    _save_yaml(_AGENTS_FILE, data)
    _log("hermes_console", f"Agent {key} {'enabled' if enabled else 'disabled'}")
    return {"name": key, "enabled": enabled}


# ── Skills ────────────────────────────────────────────────────────

def list_skills() -> list[dict]:
    data = _load_yaml(_SKILLS_FILE)
    return data.get("skills", [])


def toggle_skill(skill_id: str, enabled: bool) -> dict:
    data = _load_yaml(_SKILLS_FILE)
    skills = data.get("skills", [])
    for skill in skills:
        if skill.get("id") == skill_id:
            skill["enabled"] = enabled
            data["skills"] = skills
            _save_yaml(_SKILLS_FILE, data)
            _log("hermes_console", f"Skill {skill_id} {'enabled' if enabled else 'disabled'}")
            return {"id": skill_id, "enabled": enabled}
    return {"error": f"Skill {skill_id} not found"}


# ── Workflows ─────────────────────────────────────────────────────

def list_workflows() -> list[dict]:
    data = _load_yaml(_WORKFLOWS_FILE)
    return data.get("workflows", [])


def toggle_workflow(workflow_id: str, enabled: bool) -> dict:
    data = _load_yaml(_WORKFLOWS_FILE)
    workflows = data.get("workflows", [])
    for wf in workflows:
        if wf.get("id") == workflow_id:
            wf["enabled"] = enabled
            data["workflows"] = workflows
            _save_yaml(_WORKFLOWS_FILE, data)
            _log("hermes_console", f"Workflow {workflow_id} {'enabled' if enabled else 'disabled'}")
            return {"id": workflow_id, "enabled": enabled}
    return {"error": f"Workflow {workflow_id} not found"}


# ── Settings ──────────────────────────────────────────────────────

def get_settings() -> dict:
    from core.settings import settings
    data = _load_yaml(_SETTINGS_FILE)
    runtime = data.get("runtime", {})
    return {
        "mode": runtime.get("mode", "balanced"),
        "max_agents_per_run": runtime.get("max_agents_per_run", 8),
        "language": runtime.get("language", "fr"),
        "uncertainty_threshold": runtime.get("uncertainty_threshold", 0.7),
        "confidence_threshold": runtime.get("confidence_threshold", 0.6),
        "llm_provider": settings.LLM_PROVIDER,
    }


def update_settings(updates: dict) -> dict:
    data = _load_yaml(_SETTINGS_FILE)
    runtime = data.get("runtime", {})
    for key, value in updates.items():
        if value is not None:
            runtime[key] = value
    data["runtime"] = runtime
    _save_yaml(_SETTINGS_FILE, data)
    _log("hermes_console", f"Settings updated: {list(updates.keys())}")
    return get_settings()


# ── Logs ──────────────────────────────────────────────────────────

def _log(component: str, message: str, level: str = "info", extra: Optional[dict] = None) -> None:
    _runtime_logs.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "component": component,
        "message": message,
        "extra": extra or {},
    })
    # Keep last 500 entries in memory
    if len(_runtime_logs) > 500:
        _runtime_logs.pop(0)


def get_logs(level: Optional[str] = None, component: Optional[str] = None, limit: int = 100) -> list[dict]:
    logs = _runtime_logs[-limit:]
    if level:
        logs = [l for l in logs if l["level"] == level]
    if component:
        logs = [l for l in logs if l["component"] == component]
    return list(reversed(logs))
