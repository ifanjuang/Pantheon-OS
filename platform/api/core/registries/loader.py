"""Filesystem manifest loader for Hermes runtime modules.

This loader is intentionally tolerant for the MVP: missing folders or invalid
entries are logged and skipped instead of crashing the API startup. Strict
schema validation belongs to the next manifest-hardening step.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from core.logging import get_logger

log = get_logger("manifest_loader")


@dataclass(frozen=True)
class RuntimeManifest:
    """Loaded runtime manifest.

    The loader keeps the raw manifest to stay backward-compatible while the
    manifest schema is still being hardened.
    """

    id: str
    type: str
    path: str
    manifest: dict[str, Any]


class ManifestLoader:
    """Loads agents, skills and workflows from the filesystem.

    Expected MVP layout:

    - /modules/agents/**/manifest.yaml
    - /modules/skills/**/manifest.yaml
    - /modules/workflows/**/manifest.yaml

    The current implementation does not instantiate Python classes. It only
    indexes manifests safely so startup, health checks and the console can see
    what is present on disk.
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

        manifest_id = str(raw.get("id") or raw.get("name") or manifest_path.parent.name).strip()
        if not manifest_id:
            log.error("manifest_loader.missing_id", path=str(manifest_path))
            return None

        if raw.get("enabled") is False:
            log.info("manifest_loader.disabled", id=manifest_id, type=manifest_type, path=str(manifest_path))
            return None

        return RuntimeManifest(
            id=manifest_id,
            type=str(raw.get("type") or manifest_type),
            path=str(manifest_path.parent),
            manifest=raw,
        )
