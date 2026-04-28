from pathlib import Path
from core.contracts.agent import AgentBase


class Kairos(AgentBase):
    agent = "@Kairos"
    role = "synthesizer"
    layer = "output"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
