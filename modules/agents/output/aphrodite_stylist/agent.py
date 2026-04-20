from pathlib import Path
from core.contracts.agent import AgentBase


class Aphrodite(AgentBase):
    agent = "@Aphrodite"
    role = "stylist"
    layer = "output"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
