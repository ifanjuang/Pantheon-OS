from pathlib import Path
from .._base import AgentBase


class Hecate(AgentBase):
    """Information gap and uncertainty detection — detects ambiguities, lists missing info, decides if clarification needed."""

    agent = "@Hecate"
    role = "uncertainty_resolver"
    layer = "analysis"
    veto = False
    _soul_dir = Path(__file__).parent / "hecate"
