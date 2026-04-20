from pathlib import Path
from core.contracts.agent import AgentBase


class Daedalus(AgentBase):
    agent = "@Daedalus"
    role = "builder"
    layer = "output"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
