from pathlib import Path
from .._base import AgentBase


class Apollo(AgentBase):
    """Final validation and credibility — evaluates reliability, assigns confidence score, decides if response can exit."""

    agent = "@APOLLO"
    role = "validator"
    layer = "meta"
    veto = False
    _soul_dir = Path(__file__).parent / "apollo"
