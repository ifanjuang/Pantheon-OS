from pathlib import Path
from core._base import AgentBase


class IrisClarifier(AgentBase):
    agent = "IRIS"; role = "clarifier"; layer = "communication"; veto = False
    triggers = ["C1", "C2", "C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "iris_clarifier"
