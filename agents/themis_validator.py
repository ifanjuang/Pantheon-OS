from pathlib import Path
from core._base import AgentBase

class ThemisValidator(AgentBase):
    agent = "THEMIS"; role = "legal_validator"; layer = "framing"; veto = True
    triggers = ["C4", "C5"]
    _soul_dir = Path(__file__).parent / "themis"
