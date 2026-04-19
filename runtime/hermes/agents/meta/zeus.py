from pathlib import Path
from .._base import AgentBase


class Zeus(AgentBase):
    """Global orchestration — chooses execution order, arbitrates agents, decides merge/fork/child workflows."""

    agent = "@ZEUS"
    role = "orchestrator"
    layer = "meta"
    veto = False
    _soul_dir = Path(__file__).parent / "zeus"
