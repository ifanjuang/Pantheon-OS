from pathlib import Path
from .._base import AgentBase


class Athena(AgentBase):
    """Planning and decomposition — analyzes request, identifies task type, decomposes into sub-tasks."""

    agent = "@ATHENA"
    role = "planner"
    layer = "meta"
    veto = False
    _soul_dir = Path(__file__).parent / "athena"
