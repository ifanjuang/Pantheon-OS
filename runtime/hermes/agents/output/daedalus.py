from pathlib import Path
from .._base import AgentBase


class Daedalus(AgentBase):
    """Deliverable construction — builds dossiers, briefs, reports; creates intro/sections/subsections with citations."""

    agent = "@Daedalus"
    role = "builder"
    layer = "output"
    veto = False
    _soul_dir = Path(__file__).parent / "daedalus"
