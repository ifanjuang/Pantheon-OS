from pathlib import Path
from core.contracts.agent import AgentBase


class Mnemosyne(AgentBase):
    agent = "@Mnemosyne"
    role = "knowledge_library"
    layer = "memory"
    veto = False
    enabled = False
    _soul_dir = Path(__file__).parent
