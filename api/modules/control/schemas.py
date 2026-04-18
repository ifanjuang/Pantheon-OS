from __future__ import annotations
from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel


class ModuleStatus(BaseModel):
    name: str
    status: Literal["loaded", "disabled"]
    version: str
    prefix: str
    description: str
    depends_on: list[str]


class RunSummary(BaseModel):
    run_id: str
    criticite: str
    status: str
    instruction_excerpt: str
    agents_involved: list[str]
    started_at: datetime
    duration_ms: int | None
    veto_severity: str | None
    affaire_id: str | None
    error_message: str | None


class TraceEvent(BaseModel):
    type: str
    run_id: str
    timestamp: datetime
    agent: str | None
    payload: dict[str, Any]


class ErrorEntry(BaseModel):
    severity: Literal["error", "warning", "info"]
    source: str
    message: str
    run_id: str | None
    timestamp: datetime


class ControlSnapshot(BaseModel):
    modules: list[ModuleStatus]
    runs: list[RunSummary]
    errors: list[ErrorEntry]
    computed_at: datetime
