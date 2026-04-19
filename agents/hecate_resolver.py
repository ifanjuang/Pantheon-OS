from pathlib import Path
from core._base import AgentBase


class HecateResolver(AgentBase):
    agent = "HECATE"; role = "uncertainty_resolver"; layer = "analysis"; veto = False
    triggers = ["C1", "C2", "C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "hecate"
