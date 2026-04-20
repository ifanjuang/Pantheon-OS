from pathlib import Path
from core.contracts.agent import AgentBase


class Themis(AgentBase):
    agent = "@THEMIS"
    role = "process_guardian"
    layer = "meta"
    veto = True
    enabled = False
    _soul_dir = Path(__file__).parent
