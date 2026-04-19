from pathlib import Path
from core._base import AgentBase

class HephaistosValidator(AgentBase):
    agent = "HEPHAISTOS"; role = "technical_validator"; layer = "analysis"; veto = True
    triggers = ["C1", "C2", "C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "hephaistos"
