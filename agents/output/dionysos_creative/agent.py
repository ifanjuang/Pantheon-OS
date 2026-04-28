from pathlib import Path
from core.contracts.agent import AgentBase


class Dionysos(AgentBase):
    agent = "@Dionysos"
    role = "creative"
    layer = "output"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
