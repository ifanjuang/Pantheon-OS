from pathlib import Path
from .._base import AgentBase


class Hera(AgentBase):
    """Global coherence — verifies final alignment, detects internal contradictions."""

    agent = "@HERA"
    role = "supervisor"
    layer = "meta"
    veto = False
    _soul_dir = Path(__file__).parent / "hera"
