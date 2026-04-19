from pathlib import Path
from core._base import AgentBase

class DionysosCreative(AgentBase):
    agent = "DIONYSOS"; role = "creative"; layer = "analysis"; veto = False
    triggers = ["C4", "C5"]
    _soul_dir = Path(__file__).parent / "dionysos"
