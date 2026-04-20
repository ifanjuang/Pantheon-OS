"""VetoEngine — checks outputs against registered veto policies."""
from __future__ import annotations
import yaml
from pathlib import Path


class VetoEngine:
    def __init__(self, policies_path: Path = Path("config/policies.yaml")):
        self._path = policies_path
        self._rules: list[dict] = []
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            data = yaml.safe_load(self._path.read_text(encoding="utf-8")) or {}
            self._rules = data.get("veto_patterns", [])

    def check(self, output: str, agent: str) -> tuple[bool, str]:
        for rule in self._rules:
            pattern = rule.get("pattern", "")
            if pattern and pattern in output:
                return (False, rule.get("message", "Veto triggered"))
        return (True, "")
