from pathlib import Path
from core._base import AgentBase

class HadesMemory(AgentBase):
    agent = "HADES"; role = "memory_longterm"; layer = "continuity"; veto = False
    triggers = ["C4", "C5"]
    _soul_dir = Path(__file__).parent / "hades"
