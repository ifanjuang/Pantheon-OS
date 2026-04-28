from pathlib import Path
from core.contracts.agent import AgentBase


class Chronos(AgentBase):
    agent = "@Chronos"
    role = "scheduler"
    layer = "meta"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
