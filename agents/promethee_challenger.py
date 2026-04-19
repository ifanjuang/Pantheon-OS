from pathlib import Path
from core._base import AgentBase

class PrometheeChallenger(AgentBase):
    agent = "PROMETHEE"; role = "challenger"; layer = "analysis"; veto = False
    triggers = ["C4", "C5"]
    _soul_dir = Path(__file__).parent / "promethee"
