from pathlib import Path
from core._base import AgentBase

class HadesAnalyst(AgentBase):
    agent = "HADES"; role = "risk_analyst"; layer = "analysis"; veto = False
    triggers = ["C4", "C5"]
    _soul_dir = Path(__file__).parent / "hades"
