from pathlib import Path
from core.contracts.agent import AgentBase


class Artemis(AgentBase):
    agent = "@Artemis"
    role = "filter"
    layer = "analysis"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
