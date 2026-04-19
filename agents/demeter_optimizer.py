from pathlib import Path
from core._base import AgentBase

class DemeterOptimizer(AgentBase):
    agent = "DEMETER"; role = "optimizer"; layer = "framing"; veto = False
    triggers = ["C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "demeter"
