from pathlib import Path
from core.contracts.agent import AgentBase


class Poseidon(AgentBase):
    agent = "@Poseidon"
    role = "distributor"
    layer = "system"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
