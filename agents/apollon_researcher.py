from pathlib import Path
from core._base import AgentBase

class ApollonResearcher(AgentBase):
    agent = "APOLLON"; role = "researcher"; layer = "analysis"; veto = False
    triggers = ["C1", "C2", "C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "apollon"
