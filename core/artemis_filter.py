from pathlib import Path
from ._base import AgentBase


class ArtemisFilter(AgentBase):
    agent = "ARTEMIS"
    role = "filter"
    layer = "meta"
    veto = False
    triggers = ["C1", "C2", "C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "artemis"
