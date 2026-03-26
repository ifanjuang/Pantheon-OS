"""
AdminEngine — lecture / écriture des fichiers YAML de configuration.
Toutes les opérations sont restreintes à l'arborescence du projet (path traversal impossible).
"""
from pathlib import Path
import yaml

from core.base_engine import BaseEngine
from core.logging import get_logger

log = get_logger("admin.engine")

# Racine du projet (remontée depuis api/modules/admin/)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
MODULES_YAML = PROJECT_ROOT / "modules.yaml"
MODULES_DIR = PROJECT_ROOT / "api" / "modules"


def _safe_path(base: Path, target: Path) -> Path:
    """Lève ValueError si target sort de base (path traversal)."""
    resolved = target.resolve()
    if not resolved.is_relative_to(base):
        raise ValueError(f"Chemin non autorisé : {target}")
    return resolved


class AdminEngine(BaseEngine):

    @classmethod
    def name(cls) -> str:
        return "admin"

    # ── modules.yaml ────────────────────────────────────────────

    def read_modules_yaml(self) -> dict:
        content = MODULES_YAML.read_text(encoding="utf-8")
        return {"raw": content, "parsed": yaml.safe_load(content)}

    def write_modules_yaml(self, raw_yaml: str) -> None:
        # Valider le YAML avant d'écrire
        parsed = yaml.safe_load(raw_yaml)
        if not isinstance(parsed, dict) or "modules" not in parsed:
            raise ValueError("modules.yaml invalide : clé 'modules' manquante")
        MODULES_YAML.write_text(raw_yaml, encoding="utf-8")
        log.info("admin.modules_yaml_saved")

    def toggle_module(self, name: str, enabled: bool) -> None:
        """Active ou désactive un module dans modules.yaml sans écraser les autres champs."""
        data = yaml.safe_load(MODULES_YAML.read_text(encoding="utf-8"))
        for entry in data["modules"]:
            if entry["name"] == name:
                entry["enabled"] = enabled
                break
        else:
            raise ValueError(f"Module '{name}' introuvable dans modules.yaml")
        MODULES_YAML.write_text(yaml.dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        log.info("admin.module_toggled", module=name, enabled=enabled)

    # ── config.yaml des modules ──────────────────────────────────

    def list_modules(self) -> list[dict]:
        """Retourne la liste des modules avec leur statut enabled et présence d'un config.yaml."""
        data = yaml.safe_load(MODULES_YAML.read_text(encoding="utf-8"))
        result = []
        for entry in data.get("modules", []):
            mod_dir = MODULES_DIR / entry["name"]
            has_config = (mod_dir / "config.yaml").exists()
            manifest_path = mod_dir / "manifest.yaml"
            description = ""
            if manifest_path.exists():
                m = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
                description = m.get("description", "")
            result.append({
                "name": entry["name"],
                "enabled": entry.get("enabled", True),
                "has_config": has_config,
                "description": description,
            })
        return result

    def read_module_config(self, module: str) -> str:
        config_path = _safe_path(PROJECT_ROOT, MODULES_DIR / module / "config.yaml")
        if not config_path.exists():
            return ""
        return config_path.read_text(encoding="utf-8")

    def write_module_config(self, module: str, raw_yaml: str) -> None:
        config_path = _safe_path(PROJECT_ROOT, MODULES_DIR / module / "config.yaml")
        # Valider le YAML
        yaml.safe_load(raw_yaml)  # lève yaml.YAMLError si invalide
        config_path.write_text(raw_yaml, encoding="utf-8")
        log.info("admin.module_config_saved", module=module)

    # ── manifest.yaml (lecture seule) ───────────────────────────

    def read_module_manifest(self, module: str) -> dict:
        manifest_path = _safe_path(PROJECT_ROOT, MODULES_DIR / module / "manifest.yaml")
        if not manifest_path.exists():
            return {}
        return yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

    # ── Fichiers prompt (agent_system.txt, etc.) ─────────────────

    def list_prompt_files(self, module: str) -> list[str]:
        """Retourne les fichiers texte du module (prompts, templates)."""
        mod_dir = _safe_path(PROJECT_ROOT, MODULES_DIR / module)
        if not mod_dir.exists():
            return []
        extensions = {".txt", ".md", ".j2"}
        return [
            f.name for f in sorted(mod_dir.iterdir())
            if f.is_file() and f.suffix in extensions
        ]

    def read_prompt_file(self, module: str, filename: str) -> str:
        file_path = _safe_path(PROJECT_ROOT, MODULES_DIR / module / filename)
        if not file_path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {filename}")
        return file_path.read_text(encoding="utf-8")

    def write_prompt_file(self, module: str, filename: str, content: str) -> None:
        file_path = _safe_path(PROJECT_ROOT, MODULES_DIR / module / filename)
        # N'autoriser que les extensions texte
        if file_path.suffix not in {".txt", ".md", ".j2"}:
            raise ValueError(f"Extension non autorisée : {file_path.suffix}")
        file_path.write_text(content, encoding="utf-8")
        log.info("admin.prompt_file_saved", module=module, filename=filename)

    # ── Schéma de formulaire ─────────────────────────────────────

    def get_form_schema(self, module: str) -> dict:
        """
        Retourne {config_parsed, manifest_parsed, prompt_files}
        pour que l'UI puisse générer le formulaire complet.
        """
        config_raw = self.read_module_config(module)
        config_parsed = yaml.safe_load(config_raw) or {} if config_raw else {}
        manifest = self.read_module_manifest(module)
        prompt_files = self.list_prompt_files(module)
        return {
            "config": config_parsed,
            "config_raw": config_raw,
            "manifest": manifest,
            "prompt_files": prompt_files,
            "available_modules": [m["name"] for m in self.list_modules()],
        }
