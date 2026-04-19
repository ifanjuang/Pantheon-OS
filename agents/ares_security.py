from pathlib import Path
from core._base import AgentBase

class AresSecurity(AgentBase):
    agent = "ARES"; role = "security_guard"; layer = "system"; veto = True
    triggers = ["C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "ares"
