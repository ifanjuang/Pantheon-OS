from pathlib import Path
from core.contracts.agent import AgentBase


class Hades(AgentBase):
    agent = "@Hades"
    role = "vector_retrieval"
    layer = "memory"
    veto = False
    enabled = True
    _soul_dir = Path(__file__).parent
