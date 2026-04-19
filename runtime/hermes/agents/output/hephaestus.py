from pathlib import Path
from .._base import AgentBase


class Hephaestus(AgentBase):
    """Technical production and diagrams — produces schemas, diagrams, Mermaid; prepares figures and legends."""

    agent = "@Hephaestus"
    role = "diagram_builder"
    layer = "output"
    veto = False
    _soul_dir = Path(__file__).parent / "hephaestus"
