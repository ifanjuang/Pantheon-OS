from pathlib import Path
from core._base import AgentBase

class HephaistosBuilder(AgentBase):
    agent = "HEPHAISTOS"; role = "diagram_builder"; layer = "production"; veto = False
    triggers = ["C1", "C2", "C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "hephaistos"
