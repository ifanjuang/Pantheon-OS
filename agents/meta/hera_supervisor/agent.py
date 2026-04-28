from pathlib import Path
from core.contracts.agent import AgentBase


class Hera(AgentBase):
    agent = "@HERA"
    role = "supervisor"
    layer = "meta"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
