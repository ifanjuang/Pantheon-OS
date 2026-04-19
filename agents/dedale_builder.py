from pathlib import Path
from core._base import AgentBase

class DedaleBuilder(AgentBase):
    agent = "DEDALE"; role = "builder"; layer = "production"; veto = False
    triggers = ["C4", "C5"]
    _soul_dir = Path(__file__).parent / "dedale"
