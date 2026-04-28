from pathlib import Path
from core.contracts.agent import AgentBase


class Hephaestus(AgentBase):
    agent = "@Hephaestus"
    role = "diagram_builder"
    layer = "output"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
