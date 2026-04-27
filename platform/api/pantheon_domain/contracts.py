"""Contracts for the Pantheon OS Domain Operating Layer.

These contracts deliberately model the post-pivot architecture documented in
README.md, ARCHITECTURE.md, AGENTS.md, MODULES.md, ROADMAP.md and STATUS.md.
They do not try to re-create an autonomous agent runtime. They expose the
Pantheon definitions that Hermes Agent can execute and OpenWebUI can surface.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ComponentStatus(str, Enum):
    """Lifecycle status for a Pantheon component."""

    DRAFT = "draft"
    CANDIDATE = "candidate"
    ACTIVE = "active"
    ARCHIVED = "archived"
    LEGACY = "legacy"
    TO_AUDIT = "to_audit"


class Layer(str, Enum):
    """System layer owning a responsibility."""

    PANTHEON = "pantheon"
    HERMES = "hermes"
    OPENWEBUI = "openwebui"
    LEGACY_RUNTIME = "legacy_runtime"


class ActionKind(str, Enum):
    """Action classes used by the approval classifier."""

    DIAGNOSTIC = "diagnostic"
    READ = "read"
    DRAFT = "draft"
    MEMORY_PROMOTION = "memory_promotion"
    FILE_MUTATION = "file_mutation"
    EXTERNAL_COMMUNICATION = "external_communication"
    DESTRUCTIVE = "destructive"
    SHELL = "shell"
    WEB_SIDE_EFFECT = "web_side_effect"
    SECRET_OR_VOLUME_ACCESS = "secret_or_volume_access"


class ApprovalDecision(str, Enum):
    """Approval requirement level before execution."""

    NOT_REQUIRED = "not_required"
    REQUIRED = "required"
    FORBIDDEN_UNTIL_POLICY_EXISTS = "forbidden_until_policy_exists"


class AgentDefinition(BaseModel):
    id: str
    name: str
    role: str
    status: ComponentStatus = ComponentStatus.ACTIVE
    layer: Layer = Layer.PANTHEON
    responsibilities: list[str] = Field(default_factory=list)
    limits: list[str] = Field(default_factory=list)
    activation_triggers: list[str] = Field(default_factory=list)
    output_contract: list[str] = Field(default_factory=list)


class SkillDefinition(BaseModel):
    id: str
    name: str
    domain: str
    status: ComponentStatus = ComponentStatus.CANDIDATE
    purpose: str
    agents: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    knowledge_sources: list[str] = Field(default_factory=list)
    approval_required_if: list[ActionKind] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)


class WorkflowDefinition(BaseModel):
    id: str
    name: str
    domain: str
    status: ComponentStatus = ComponentStatus.CANDIDATE
    purpose: str
    steps: list[str] = Field(default_factory=list)
    agents: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    approval_points: list[ActionKind] = Field(default_factory=list)
    memory_targets: list[str] = Field(default_factory=list)
    fallback: str | None = None


class MemoryStoreDefinition(BaseModel):
    id: str
    name: str
    status: ComponentStatus = ComponentStatus.CANDIDATE
    owner: str
    purpose: str
    accepted_entries: list[str] = Field(default_factory=list)
    promotion_rule: str
    rejection_rule: str


class KnowledgeCollectionDefinition(BaseModel):
    id: str
    name: str
    status: ComponentStatus = ComponentStatus.CANDIDATE
    owner_layer: Layer = Layer.OPENWEBUI
    purpose: str
    accepted_documents: list[str] = Field(default_factory=list)
    excluded_documents: list[str] = Field(default_factory=list)
    reliability_rule: str


class LegacyComponentDefinition(BaseModel):
    id: str
    name: str
    status: ComponentStatus = ComponentStatus.TO_AUDIT
    path: str
    previous_role: str
    proposed_decision: str
    risk: str


class DomainLayerSnapshot(BaseModel):
    mode: str = "hermes_backed_domain_layer"
    doctrine: str = "Pantheon defines. Hermes executes. OpenWebUI exposes and retrieves."
    status: ComponentStatus = ComponentStatus.CANDIDATE
    layers: dict[str, str]
    agents: list[AgentDefinition]
    skills: list[SkillDefinition]
    workflows: list[WorkflowDefinition]
    memory_stores: list[MemoryStoreDefinition]
    knowledge_collections: list[KnowledgeCollectionDefinition]
    legacy_components: list[LegacyComponentDefinition]


class ApprovalClassificationRequest(BaseModel):
    action_kind: ActionKind
    description: str = Field(min_length=3)
    target: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ApprovalClassification(BaseModel):
    action_kind: ActionKind
    decision: ApprovalDecision
    reason: str
    required_human_validation: bool
    blocked_until_policy_exists: bool = False
