from pathlib import Path
from core._base import AgentBase

class AphroditeStylist(AgentBase):
    agent = "APHRODITE"; role = "stylist"; layer = "production"; veto = False
    triggers = []
    _soul_dir = Path(__file__).parent / "aphrodite"
