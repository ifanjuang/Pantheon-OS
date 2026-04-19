from pathlib import Path
from .._base import AgentBase


class Ares(AgentBase):
    """Fast execution — handles simple tasks quickly; serves as fast degraded mode/fallback."""

    agent = "@Ares"
    role = "fast_executor"
    layer = "system"
    veto = False
    _soul_dir = Path(__file__).parent / "ares"
