from pathlib import Path
from ._base import AgentBase


class HeraSupervisor(AgentBase):
    agent = "HERA"
    role = "supervisor"
    layer = "meta"
    veto = False
    triggers = ["C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "hera"
