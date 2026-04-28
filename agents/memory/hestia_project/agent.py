from pathlib import Path
from core.contracts.agent import AgentBase


class Hestia(AgentBase):
    agent = "@Hestia"
    role = "project_memory"
    layer = "memory"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
