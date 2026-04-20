from pathlib import Path
from core.contracts.agent import AgentBase


class Demeter(AgentBase):
    agent = "@Demeter"
    role = "collector"
    layer = "analysis"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
