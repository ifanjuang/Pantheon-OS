from pathlib import Path
from core._base import AgentBase

class HestiaMemory(AgentBase):
    agent = "HESTIA"; role = "memory_project"; layer = "continuity"; veto = False
    triggers = ["C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "hestia"
