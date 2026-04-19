from __future__ import annotations
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class WorkflowStep(BaseModel):
    """Un pas dans un workflow — un ou plusieurs agents, avec flag parallèle."""
    agents: list[str]
    parallel: bool = False


class WorkflowDefinitionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128, pattern=r"^[a-z0-9_\-]+$")
    version: str = "1.0.0"
    description: str | None = None
    # steps : str = agent unique, list[str] = groupe parallèle
    steps: list[str | list[str]]
    source: str | None = None  # YAML/JSON brut pour archivage


class WorkflowDefinitionUpdate(BaseModel):
    version: str | None = None
    description: str | None = None
    steps: list[str | list[str]] | None = None
    is_active: bool | None = None


class WorkflowDefinitionOut(BaseModel):
    id: str
    name: str
    version: str
    description: str | None
    definition: dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WorkflowTrigger(BaseModel):
    """Déclenche un run d'orchestration avec le workflow nommé."""
    instruction: str = Field(min_length=1)
    affaire_id: str | None = None
    criticite: str | None = None  # forcer la criticité (sinon détectée par Hermès)


class WorkflowTriggerOut(BaseModel):
    run_id: str
    workflow_name: str
    status: str = "queued"
