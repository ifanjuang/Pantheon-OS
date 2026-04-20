"""ToolBase — contract for all shared tools."""
from typing import ClassVar


class ToolBase:
    tool_id: ClassVar[str] = ""
    name: ClassVar[str] = ""

    async def execute(self, **kwargs) -> dict:
        raise NotImplementedError
