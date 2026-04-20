"""
ModuleRegistry — auto-discovery et chargement des modules (§1b).
main.py ne connaît aucun module : tout passe par registry.load_all().
"""

import importlib
import yaml
from pathlib import Path
from fastapi import FastAPI

from core.logging import get_logger

log = get_logger("registry")

# Instance globale accessible depuis health.py et les modules
registry: "ModuleRegistry | None" = None


class ModuleRegistry:
    def __init__(self, app: FastAPI):
        self.app = app
        self._modules: dict[str, dict] = {}

    def load_all(self, modules_yaml: str = "modules.yaml") -> None:
        """Charge tous les modules activés dans modules.yaml."""
        global registry
        registry = self

        config_path = Path(modules_yaml)
        if not config_path.exists():
            log.warning("registry.modules_yaml_not_found", path=modules_yaml)
            return

        config = yaml.safe_load(config_path.read_text())
        for entry in config.get("modules", []):
            if entry.get("enabled", True):
                try:
                    self._load_module(entry["name"])
                except Exception as e:
                    log.error("registry.load_failed", module=entry["name"], error=str(e))

    def _load_module(self, name: str) -> None:
        base = Path(f"apps/{name}")
        if not base.exists():
            log.warning("registry.module_dir_missing", module=name, path=str(base))
            return

        manifest_path = base / "manifest.yaml"
        if not manifest_path.exists():
            log.warning("registry.manifest_missing", module=name)
            return

        manifest = yaml.safe_load(manifest_path.read_text())
        config_path = base / "config.yaml"
        config = yaml.safe_load(config_path.read_text()) if config_path.exists() else {}

        # Vérifier que les dépendances sont chargées
        for dep in manifest.get("depends_on", []):
            if dep not in self._modules:
                raise RuntimeError(
                    f"Module '{name}' requiert '{dep}' qui n'est pas encore chargé. Vérifier l'ordre dans modules.yaml."
                )

        # Charger le router du module
        try:
            mod = importlib.import_module(f"apps.{name}.router")
            router = mod.get_router(config)
            self.app.include_router(
                router,
                prefix=manifest["prefix"],
                tags=[name],
            )
        except (ImportError, AttributeError) as e:
            log.error("registry.router_load_failed", module=name, error=str(e))
            return

        self._modules[name] = {"manifest": manifest, "config": config}
        log.info("registry.module_loaded", module=name, prefix=manifest["prefix"])

    def is_enabled(self, name: str) -> bool:
        return name in self._modules

    def get_config(self, name: str) -> dict:
        return self._modules.get(name, {}).get("config", {})

    def get_manifest(self, name: str) -> dict:
        return self._modules.get(name, {}).get("manifest", {})

    def get_all_behaviors(self) -> str:
        """Retourne les behaviors de tous les modules chargés, concaténés.

        Utilisé par Zeus pour injecter les contraintes métier actives dans son
        contexte de planification sans modifier les SOUL.md des agents.
        """
        parts = []
        for name, data in self._modules.items():
            behavior = data["manifest"].get("behavior", "").strip()
            if behavior:
                parts.append(f"[{name}]\n{behavior}")
        return "\n\n".join(parts)

    @property
    def loaded_modules(self) -> list[str]:
        return list(self._modules.keys())
