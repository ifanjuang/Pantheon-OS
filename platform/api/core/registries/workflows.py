"""Workflow definition loader.

Loads workflow.yaml and tasks.yaml files from modules/workflows/** directories and
validates them through the Task/Workflow contracts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from core.contracts.tasks import WorkflowDefinition, load_workflow_definition
from core.logging import get_logger

log = get_logger("workflow_registry")


class WorkflowDefinitionLoader:
    """Loads explicit workflow definitions from the filesystem."""

    def __init__(self, base_path: Path | str):
        self.base_path = Path(base_path)

    def load_all(self) -> list[WorkflowDefinition]:
        root = self.base_path / "workflows"
        if not root.exists():
            log.warning("workflow_loader.folder_missing", path=str(root))
            return []

        workflows: list[WorkflowDefinition] = []
        for workflow_yaml in sorted(root.rglob("workflow.yaml")):
            loaded = self.load_one(workflow_yaml.parent)
            if loaded is not None:
                workflows.append(loaded)

        log.info("workflow_loader.loaded", count=len(workflows), root=str(root))
        return workflows

    def load_one(self, workflow_dir: Path | str) -> WorkflowDefinition | None:
        workflow_dir = Path(workflow_dir)
        workflow_path = workflow_dir / "workflow.yaml"
        tasks_path = workflow_dir / "tasks.yaml"

        if not workflow_path.exists():
            log.warning("workflow_loader.workflow_yaml_missing", path=str(workflow_path))
            return None

        try:
            workflow_raw = self._read_yaml_object(workflow_path)
            tasks_raw = self._read_optional_tasks(tasks_path)
            merged = self._merge_workflow_and_tasks(workflow_raw, tasks_raw)
            return load_workflow_definition(merged)
        except (TypeError, ValidationError, ValueError) as exc:
            log.error("workflow_loader.invalid", path=str(workflow_dir), error=str(exc))
            return None

    def _read_optional_tasks(self, tasks_path: Path) -> list[dict[str, Any]]:
        if not tasks_path.exists():
            return []

        raw = self._read_yaml_object(tasks_path)
        if "tasks" in raw:
            tasks = raw["tasks"]
        else:
            tasks = raw

        if not isinstance(tasks, list):
            raise TypeError("tasks.yaml must contain a list or an object with a 'tasks' list")
        if not all(isinstance(task, dict) for task in tasks):
            raise TypeError("each task must be an object")
        return tasks

    @staticmethod
    def _read_yaml_object(path: Path) -> dict[str, Any]:
        try:
            raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception as exc:  # noqa: BLE001 - caller logs contextual error
            raise ValueError(f"failed to read {path}: {exc}") from exc

        if not isinstance(raw, dict):
            raise TypeError(f"{path.name} must be a YAML object")
        return raw

    @staticmethod
    def _merge_workflow_and_tasks(workflow_raw: dict[str, Any], tasks_raw: list[dict[str, Any]]) -> dict[str, Any]:
        merged = dict(workflow_raw)
        if tasks_raw:
            if "tasks" in merged and merged["tasks"]:
                raise ValueError("workflow.yaml and tasks.yaml both define tasks; keep tasks in one place")
            merged["tasks"] = tasks_raw
        else:
            merged.setdefault("tasks", [])
        return merged
