"""Manifest contracts for API apps and runtime modules.

The schema is intentionally backward-compatible with existing MVP manifests.
It normalizes legacy fields while exposing the richer contract required by the
Pantheon OS documentation.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator


class ManifestType(StrEnum):
    API_APP = "api_app"
    AGENT = "agent"
    SKILL = "skill"
    TOOL = "tool"
    WORKFLOW = "workflow"
    ACTION = "action"
    PROVIDER = "provider"
    EVALUATOR = "evaluator"
    SERVICE = "service"
    TEMPLATE = "template"


class RiskProfile(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SideEffectProfile(StrEnum):
    NONE = "none"
    READ_ONLY = "read_only"
    INTERNAL = "internal"
    MEMORY_WRITE = "memory_write"
    EXTERNAL = "external"
    IRREVERSIBLE = "irreversible"


class ManifestValidationIssue(BaseModel):
    field: str
    message: str
    severity: Literal["warning", "error"] = "warning"


class ComponentManifest(BaseModel):
    """Normalized manifest used by registries and future console views."""

    model_config = ConfigDict(extra="allow", use_enum_values=True)

    id: str
    name: str | None = None
    type: ManifestType = ManifestType.API_APP
    version: str = "0.1.0"
    description: str = ""
    enabled: bool = True
    priority: int = 0

    # Existing API-app fields
    prefix: str | None = None
    depends_on: list[str] = Field(default_factory=list)

    # New generic contract fields
    dependencies: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    risk_profile: RiskProfile = RiskProfile.LOW
    side_effect_profile: SideEffectProfile = SideEffectProfile.NONE
    approval_required_if: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    agent: str | None = None
    behavior: str = ""

    @field_validator("id", "version")
    @classmethod
    def _not_empty(cls, value: str) -> str:
        value = str(value).strip()
        if not value:
            raise ValueError("must not be empty")
        return value

    @field_validator("prefix")
    @classmethod
    def _prefix_format(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if value and not value.startswith("/"):
            raise ValueError("prefix must start with '/'")
        return value

    @model_validator(mode="after")
    def _merge_legacy_dependencies(self) -> "ComponentManifest":
        merged = list(dict.fromkeys([*self.dependencies, *self.depends_on]))
        self.dependencies = merged
        self.depends_on = merged
        return self

    def issues(self) -> list[ManifestValidationIssue]:
        """Return non-blocking quality issues for progressive hardening."""
        issues: list[ManifestValidationIssue] = []

        if not self.description:
            issues.append(ManifestValidationIssue(field="description", message="description is recommended"))

        if self.type == ManifestType.API_APP and not self.prefix:
            issues.append(ManifestValidationIssue(field="prefix", message="api_app manifests should declare a prefix"))

        if self.type != ManifestType.API_APP and self.side_effect_profile == SideEffectProfile.NONE:
            issues.append(
                ManifestValidationIssue(
                    field="side_effect_profile",
                    message="non-api runtime components should declare an explicit side_effect_profile",
                )
            )

        if self.type in {ManifestType.ACTION, ManifestType.TOOL} and not self.outputs:
            issues.append(ManifestValidationIssue(field="outputs", message="actions and tools should declare outputs"))

        return issues


def normalize_manifest(raw: dict[str, Any], *, fallback_id: str, default_type: str = "api_app") -> ComponentManifest:
    """Normalize a raw manifest into the progressive V2 contract.

    Legacy manifests often use `name` as the identifier and `depends_on` for
    dependencies. Both remain supported.
    """
    if not isinstance(raw, dict):
        raise TypeError("manifest must be an object")

    data = dict(raw)
    data.setdefault("id", data.get("name") or fallback_id)
    data.setdefault("name", data.get("id"))
    data.setdefault("type", data.get("component_type") or default_type)
    data.setdefault("enabled", True)
    data.setdefault("priority", 0)

    try:
        return ComponentManifest.model_validate(data)
    except ValidationError:
        raise
