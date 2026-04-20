"""SkillBase — contract for all Hermes skills."""
from typing import ClassVar


class SkillBase:
    skill_id: ClassVar[str] = ""
    name: ClassVar[str] = ""
    enabled: ClassVar[bool] = True
    agents: ClassVar[list[str]] = []

    async def run(self, context: dict) -> dict:
        raise NotImplementedError
