from pathlib import Path
from core._base import AgentBase

class AresExecutor(AgentBase):
    agent = "ARES"; role = "executor"; layer = "framing"; veto = False
    triggers = ["C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "ares"
