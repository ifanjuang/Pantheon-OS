from pathlib import Path
from core.contracts.agent import AgentBase


class Metis(AgentBase):
    agent = "@Metis"
    role = "optimizer"
    layer = "analysis"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
