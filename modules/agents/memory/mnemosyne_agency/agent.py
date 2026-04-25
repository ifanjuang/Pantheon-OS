from pathlib import Path
from core.contracts.agent import AgentBase


class Mnemosyne(AgentBase):
    agent = "@Mnemosyne"
    role = "agency_memory"
    layer = "memory"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
