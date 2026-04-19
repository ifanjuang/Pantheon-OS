from pathlib import Path
from .._base import AgentBase


class Argos(AgentBase):
    """Factual extraction — extracts facts, figures, citations, references; structures verifiable evidence."""

    agent = "@Argos"
    role = "extractor"
    layer = "analysis"
    veto = False
    _soul_dir = Path(__file__).parent / "argos"
