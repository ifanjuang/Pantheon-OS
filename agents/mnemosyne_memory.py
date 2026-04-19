from pathlib import Path
from core._base import AgentBase

class MnemosyneMemory(AgentBase):
    agent = "MNEMOSYNE"; role = "memory_agency"; layer = "continuity"; veto = False
    triggers = ["C4", "C5"]
    _soul_dir = Path(__file__).parent / "mnemosyne"
