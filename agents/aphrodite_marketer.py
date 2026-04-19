from pathlib import Path
from core._base import AgentBase

class AphroditeMarketer(AgentBase):
    agent = "APHRODITE"; role = "marketer"; layer = "communication"; veto = False
    triggers = []
    _soul_dir = Path(__file__).parent / "aphrodite"
