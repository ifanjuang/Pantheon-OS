from pathlib import Path
from core.contracts.agent import AgentBase


class Apollo(AgentBase):
    agent = "@APOLLO"
    role = "validator"
    layer = "meta"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
