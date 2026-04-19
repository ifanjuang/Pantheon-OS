from pathlib import Path
from core._base import AgentBase

class ChronosPlanner(AgentBase):
    agent = "CHRONOS"; role = "time_planner"; layer = "framing"; veto = False
    triggers = ["C1", "C2", "C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "chronos"
