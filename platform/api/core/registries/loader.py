"""Filesystem manifest loader for Hermes runtime modules.

This loader is tolerant enough for the MVP while already normalizing manifests
through the shared ComponentManifest contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from core.contracts.manifest import ComponentManifest, normalize_manifest
from core.logging import get_logger

log = get_logger("manifest_loader")


@dataclass(frozen=True)
class RuntimeManifest:
    """Loaded runtime manifest."""

    id: str
    type: str
    path: str
    manifest: dict[str, Any]
    model: ComponentManifest


class ManifestLoader:
    """Loads agents, skills and workflows from the filesystem.

    Expected layout (top-level, per MODULES.md):

    - /agents/**/manifest.yaml
    - /skills/**/manifest.yaml
    - /workflows/**/manifest.yaml

    The current implementation does not instantiate Python classes. It indexes
    normalized manifests safely so startup, health checks and the console can
    see what is present on disk.
    """

    def __init__(self, base_path: Path | str):
        self.base_path = Path(base_path)

    def load_agents(self) -> list[RuntimeManifest]:
        return self._load_kind("agents", "agent")

    def load_skills(self) -> list[RuntimeManifest]:
        return self._load_kind("skills", "skill")

    def load_workflows(self) -> list[RuntimeManifest]:
        return self._load_kind("workflows", "workflow")

    def _load_kind(self, folder: str, manifest_type: str) -> list[RuntimeManifest]:
        root = self.base_path / folder
        if not root.exists():
            log.warning("manifest_loader.folder_missing", type=manifest_type, path=str(root))
            return []

        manifests: list[RuntimeManifest] = []
        for manifest_path in sorted(root.rglob("manifest.yaml")):
            loaded = self._load_manifest(manifest_path, manifest_type)
            if loaded is not None:
                manifests.append(loaded)

        log.info("manifest_loader.loaded", type=manifest_type, count=len(manifests), root=str(root))
        return manifests

    def _load_manifest(self, manifest_path: Path, manifest_type: str) -> RuntimeManifest | None:
        try:
            raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
        except Exception as exc:  # noqa: BLE001 - startup must remain tolerant in MVP
            log.error("manifest_loader.read_failed", path=str(manifest_path), error=str(exc))
            return None

        if not isinstance(raw, dict):
            log.error("manifest_loader.invalid_yaml", path=str(manifest_path), reason="manifest is not an object")
            return None

        try:
            model = normalize_manifest(raw, fallback_id=manifest_path.parent.name, default_type=manifest_type)
        except (TypeError, ValidationError) as exc:
            log.error("manifest_loader.manifest_invalid", path=str(manifest_path), error=str(exc))
            return None

        if not model.enabled:
            log.info("manifest_loader.disabled", id=model.id, type=model.type, path=str(manifest_path))
            return None

        for issue in model.issues():
            log.warning(
                "manifest_loader.quality_issue",
                id=model.id,
                type=model.type,
                field=issue.field,
                severity=issue.severity,
                message=issue.message,
            )

        return RuntimeManifest(
            id=model.id,
            type=str(model.type),
            path=str(manifest_path.parent),
            manifest=model.model_dump(mode="json"),
            model=model,
        )
