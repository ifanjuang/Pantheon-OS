from pathlib import Path
from .._base import AgentBase


class Metis(AgentBase):
    """Optimization and tactical refinement — improves plans, proposes intelligent shortcuts, refines existing solutions."""

    agent = "@Metis"
    role = "optimizer"
    layer = "analysis"
    veto = False
    _soul_dir = Path(__file__).parent / "metis"
