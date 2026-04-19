from pathlib import Path
from .._base import AgentBase


class Prometheus(AgentBase):
    """Contradiction and cross-referencing — compares sources, detects inconsistencies, flags weak hypotheses."""

    agent = "@Prometheus"
    role = "challenger"
    layer = "analysis"
    veto = False
    _soul_dir = Path(__file__).parent / "prometheus"
