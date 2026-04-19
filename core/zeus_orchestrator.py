from pathlib import Path
from ._base import AgentBase


class ZeusOrchestrator(AgentBase):
    agent = "ZEUS"
    role = "orchestrator"
    layer = "meta"
    veto = False
    triggers = ["C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "zeus"
