from pathlib import Path
from core.contracts.agent import AgentBase


class Ares(AgentBase):
    agent = "@Ares"
    role = "fast_executor"
    layer = "system"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
