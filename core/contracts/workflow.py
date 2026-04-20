"""WorkflowBase — contract for all workflow definitions."""
from dataclasses import dataclass, field
from typing import ClassVar


class WorkflowBase:
    workflow_id: ClassVar[str] = ""
    name: ClassVar[str] = ""
    enabled: ClassVar[bool] = True
    steps: ClassVar[list[str]] = []
    fallback: ClassVar[str | None] = None

    async def run(self, context: dict) -> dict:
        raise NotImplementedError
