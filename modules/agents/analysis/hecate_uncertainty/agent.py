from pathlib import Path
from core.contracts.agent import AgentBase


class Hecate(AgentBase):
    agent = "@Hecate"
    role = "uncertainty_resolver"
    layer = "analysis"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
