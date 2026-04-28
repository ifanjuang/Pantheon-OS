from pathlib import Path
from core.contracts.agent import AgentBase


class Athena(AgentBase):
    agent = "@ATHENA"
    role = "planner"
    layer = "meta"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
