"""Manifest schema — common metadata descriptor for discoverable modules."""
from dataclasses import dataclass, field


@dataclass
class AgentManifest:
    id: str
    name: str
    layer: str
    role: str
    enabled: bool = True
    veto: bool = False
    description: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class SkillManifest:
    id: str
    name: str
    enabled: bool = True
    agents: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class WorkflowManifest:
    id: str
    name: str
    enabled: bool = True
    steps: list[str] = field(default_factory=list)
    fallback: str | None = None
    description: str = ""
