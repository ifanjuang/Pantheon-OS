from pathlib import Path
from core.contracts.agent import AgentBase


class Iris(AgentBase):
    agent = "@Iris"
    role = "communicator"
    layer = "output"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
