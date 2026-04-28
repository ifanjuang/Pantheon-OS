from pathlib import Path
from core.contracts.agent import AgentBase


class Zeus(AgentBase):
    agent = "@ZEUS"
    role = "orchestrator"
    layer = "meta"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
