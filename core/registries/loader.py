"""Manifest loader — auto-discovers agents/skills/workflows by scanning modules/."""
from __future__ import annotations
import yaml
from pathlib import Path


class ManifestLoader:
    """Scans a module root for manifest.yaml files and builds a registry dict."""

    def __init__(self, modules_root: Path):
        self._root = Path(modules_root)

    def load_all(self) -> dict[str, dict]:
        registry: dict[str, dict] = {}
        for manifest_path in self._root.rglob("manifest.yaml"):
            try:
                data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
                if data and "id" in data:
                    data["_path"] = str(manifest_path.parent)
                    registry[data["id"]] = data
            except Exception:
                pass
        return registry

    def load_agents(self) -> dict[str, dict]:
        agents_root = self._root / "agents"
        return ManifestLoader(agents_root).load_all()

    def load_skills(self) -> dict[str, dict]:
        skills_root = self._root / "skills"
        return ManifestLoader(skills_root).load_all()

    def load_workflows(self) -> dict[str, dict]:
        workflows_root = self._root / "workflows"
        return ManifestLoader(workflows_root).load_all()
