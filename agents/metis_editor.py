from pathlib import Path
from core._base import AgentBase


class MetisEditor(AgentBase):
    agent = "METIS"; role = "editor"; layer = "communication"; veto = False
    triggers = ["C2", "C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "metis"
