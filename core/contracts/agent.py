"""AgentBase — common contract for all Hermes agents."""
from pathlib import Path
from typing import ClassVar


class AgentBase:
    """Identity + responsibility contract. Every agent inherits from this."""

    agent: ClassVar[str] = ""
    role: ClassVar[str] = ""
    layer: ClassVar[str] = ""
    veto: ClassVar[bool] = False
    enabled: ClassVar[bool] = True
    triggers: ClassVar[list[str]] = []
    _soul_dir: ClassVar[Path] = Path()

    @classmethod
    def soul(cls) -> str:
        # SOUL location: <repo>/agents/{layer}/{name}.md
        # _soul_dir = modules/agents/{layer}/{name}/  → repo_root = parents[3]
        repo_root = cls._soul_dir.parents[3]
        name = cls._soul_dir.name
        path = repo_root / "agents" / cls.layer / f"{name}.md"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    @classmethod
    def identity(cls) -> dict:
        return {"agent": cls.agent, "role": cls.role, "layer": cls.layer}
