"""Base class pour tous les agents Pantheon OS."""
from pathlib import Path
from typing import ClassVar


class AgentBase:
    """Contrat d'identité d'un agent — agent ≠ role."""

    agent: ClassVar[str] = ""     # identité (ZEUS, ATHENA, …)
    role: ClassVar[str] = ""      # fonction stable (orchestrator, planner, …)
    layer: ClassVar[str] = ""     # couche architecturale
    veto: ClassVar[bool] = False  # peut émettre un veto bloquant
    triggers: ClassVar[list[str]] = []  # criticités activant l'agent ([] = jamais auto)

    _soul_dir: ClassVar[Path] = Path()

    @classmethod
    def soul(cls) -> str:
        """Charge le SOUL.md de l'agent (prompt système)."""
        path = cls._soul_dir / "SOUL.md"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    @classmethod
    def identity(cls) -> dict:
        """Retourne {agent, role} — clé JSON standard Pantheon OS."""
        return {"agent": cls.agent, "role": cls.role}
