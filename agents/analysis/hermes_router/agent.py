from pathlib import Path
from core.contracts.agent import AgentBase


class Hermes(AgentBase):
    agent = "@Hermes"
    role = "router"
    layer = "analysis"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
