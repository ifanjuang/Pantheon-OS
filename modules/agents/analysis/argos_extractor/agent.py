from pathlib import Path
from core.contracts.agent import AgentBase


class Argos(AgentBase):
    agent = "@Argos"
    role = "extractor"
    layer = "analysis"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
