from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import yaml
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from .models import WorkflowDefinition
from .schemas import WorkflowDefinitionCreate, WorkflowDefinitionUpdate, WorkflowStep

log = get_logger("flowmanager.service")

_WORKFLOWS_DIR = Path(__file__).parents[4] / "config" / "workflows"


def _normalize_steps(steps: list[str | list[str]]) -> list[dict]:
    """Convertit la liste steps YAML → liste de WorkflowStep normalisés."""
    result = []
    for step in steps:
        if isinstance(step, list):
            result.append({"agents": [a.upper() for a in step], "parallel": True})
        else:
            result.append({"agents": [step.upper()], "parallel": False})
    return result


class FlowManagerService:

    @staticmethod
    async def list_workflows(db: AsyncSession, active_only: bool = False) -> list[WorkflowDefinition]:
        stmt = select(WorkflowDefinition).order_by(WorkflowDefinition.name)
        if active_only:
            stmt = stmt.where(WorkflowDefinition.is_active.is_(True))
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str) -> WorkflowDefinition | None:
        result = await db.execute(
            select(WorkflowDefinition).where(WorkflowDefinition.name == name)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: WorkflowDefinitionCreate) -> WorkflowDefinition:
        wf = WorkflowDefinition(
            id=str(uuid4()),
            name=data.name,
            version=data.version,
            description=data.description,
            definition={"steps": _normalize_steps(data.steps)},
            source=data.source,
        )
        db.add(wf)
        await db.commit()
        await db.refresh(wf)
        log.info("flowmanager.created", name=wf.name, version=wf.version)
        return wf

    @staticmethod
    async def update(
        db: AsyncSession, wf: WorkflowDefinition, data: WorkflowDefinitionUpdate
    ) -> WorkflowDefinition:
        if data.version is not None:
            wf.version = data.version
        if data.description is not None:
            wf.description = data.description
        if data.steps is not None:
            wf.definition = {"steps": _normalize_steps(data.steps)}
        if data.is_active is not None:
            wf.is_active = data.is_active
        await db.commit()
        await db.refresh(wf)
        log.info("flowmanager.updated", name=wf.name, version=wf.version)
        return wf

    @staticmethod
    async def deactivate(db: AsyncSession, wf: WorkflowDefinition) -> WorkflowDefinition:
        wf.is_active = False
        await db.commit()
        await db.refresh(wf)
        log.info("flowmanager.deactivated", name=wf.name)
        return wf

    @staticmethod
    async def create_from_yaml(db: AsyncSession, yaml_content: str) -> WorkflowDefinition:
        """Parse un YAML de workflow et crée l'entrée en DB."""
        data = yaml.safe_load(yaml_content)
        flow = data.get("flow", data)
        create = WorkflowDefinitionCreate(
            name=flow["name"],
            version=flow.get("version", "1.0.0"),
            description=flow.get("description"),
            steps=flow.get("steps", []),
            source=yaml_content,
        )
        return await FlowManagerService.create(db, create)

    @staticmethod
    async def seed_from_disk(db: AsyncSession) -> int:
        """Charge les workflows YAML de config/workflows/ absents de la DB."""
        if not _WORKFLOWS_DIR.exists():
            return 0
        loaded = 0
        for yaml_file in sorted(_WORKFLOWS_DIR.glob("*.yaml")):
            content = yaml_file.read_text(encoding="utf-8")
            try:
                data = yaml.safe_load(content)
                flow = data.get("flow", data)
                name = flow.get("name")
                if not name:
                    continue
                existing = await FlowManagerService.get_by_name(db, name)
                if existing:
                    continue
                await FlowManagerService.create_from_yaml(db, content)
                loaded += 1
                log.info("flowmanager.seeded", file=yaml_file.name, name=name)
            except Exception as exc:
                log.warning("flowmanager.seed_failed", file=yaml_file.name, error=str(exc))
        return loaded
