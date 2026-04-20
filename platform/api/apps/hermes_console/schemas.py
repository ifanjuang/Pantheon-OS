from pydantic import BaseModel
from typing import Optional


class AgentOut(BaseModel):
    name: str
    layer: str
    role: str
    enabled: bool
    veto: bool = False
    description: str = ""


class SkillOut(BaseModel):
    id: str
    name: str
    category: str
    enabled: bool
    description: str = ""
    agents: list[str] = []


class WorkflowOut(BaseModel):
    id: str
    name: str
    enabled: bool
    description: str = ""
    steps: list[str] = []


class ToggleIn(BaseModel):
    enabled: bool


class SettingsOut(BaseModel):
    mode: str
    max_agents_per_run: int
    language: str
    uncertainty_threshold: float
    confidence_threshold: float
    llm_provider: str


class SettingsIn(BaseModel):
    mode: Optional[str] = None
    max_agents_per_run: Optional[int] = None
    uncertainty_threshold: Optional[float] = None
    confidence_threshold: Optional[float] = None


class LogEntry(BaseModel):
    timestamp: str
    level: str
    component: str
    message: str
    extra: dict = {}
