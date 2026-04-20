"""Hermes Console — REST API for agents/skills/workflows/logs/settings management."""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from core.auth import get_current_user, require_role
from .schemas import AgentOut, SkillOut, WorkflowOut, ToggleIn, SettingsOut, SettingsIn, LogEntry
from . import service


def get_router(config: dict) -> APIRouter:
    router = APIRouter(prefix="/console", tags=["Hermes Console"])

    # ── Agents ──────────────────────────────────────────────────────

    @router.get("/agents", response_model=list[AgentOut])
    async def list_agents(_=Depends(get_current_user)):
        return service.list_agents()

    @router.post("/agents/{name}/toggle", response_model=AgentOut)
    async def toggle_agent(
        name: str,
        body: ToggleIn,
        _=Depends(require_role("admin", "moe")),
    ):
        result = service.toggle_agent(name, body.enabled)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return service.list_agents()[0]  # return updated agent

    @router.get("/agents/{name}", response_model=AgentOut)
    async def get_agent(name: str, _=Depends(get_current_user)):
        agents = [a for a in service.list_agents() if a["name"].upper() == name.upper()]
        if not agents:
            raise HTTPException(status_code=404, detail=f"Agent {name} not found")
        return agents[0]

    # ── Skills ──────────────────────────────────────────────────────

    @router.get("/skills", response_model=list[SkillOut])
    async def list_skills(_=Depends(get_current_user)):
        return service.list_skills()

    @router.post("/skills/{skill_id}/toggle", response_model=dict)
    async def toggle_skill(
        skill_id: str,
        body: ToggleIn,
        _=Depends(require_role("admin", "moe")),
    ):
        result = service.toggle_skill(skill_id, body.enabled)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result

    # ── Workflows ────────────────────────────────────────────────────

    @router.get("/workflows", response_model=list[WorkflowOut])
    async def list_workflows(_=Depends(get_current_user)):
        return service.list_workflows()

    @router.post("/workflows/{workflow_id}/toggle", response_model=dict)
    async def toggle_workflow(
        workflow_id: str,
        body: ToggleIn,
        _=Depends(require_role("admin", "moe")),
    ):
        result = service.toggle_workflow(workflow_id, body.enabled)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result

    # ── Settings ─────────────────────────────────────────────────────

    @router.get("/settings", response_model=SettingsOut)
    async def get_settings(_=Depends(get_current_user)):
        return service.get_settings()

    @router.post("/settings", response_model=SettingsOut)
    async def update_settings(
        body: SettingsIn,
        _=Depends(require_role("admin")),
    ):
        return service.update_settings(body.model_dump(exclude_none=True))

    # ── Logs ─────────────────────────────────────────────────────────

    @router.get("/logs", response_model=list[LogEntry])
    async def get_logs(
        level: Optional[str] = Query(None, description="Filter by level: debug|info|warning|error"),
        component: Optional[str] = Query(None, description="Filter by component name"),
        limit: int = Query(100, ge=1, le=500),
        _=Depends(get_current_user),
    ):
        return service.get_logs(level=level, component=component, limit=limit)

    # ── Dashboard ─────────────────────────────────────────────────────

    @router.get("/dashboard")
    async def dashboard(_=Depends(get_current_user)):
        agents = service.list_agents()
        skills = service.list_skills()
        workflows = service.list_workflows()
        return {
            "agents": {
                "total": len(agents),
                "enabled": sum(1 for a in agents if a["enabled"]),
                "veto_count": sum(1 for a in agents if a.get("veto")),
            },
            "skills": {
                "total": len(skills),
                "enabled": sum(1 for s in skills if s.get("enabled")),
            },
            "workflows": {
                "total": len(workflows),
                "enabled": sum(1 for w in workflows if w.get("enabled")),
            },
            "recent_logs": service.get_logs(limit=5),
        }

    return router
