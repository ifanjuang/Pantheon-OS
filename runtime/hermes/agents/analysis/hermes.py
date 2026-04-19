from pathlib import Path
from .._base import AgentBase


class Hermes(AgentBase):
    """Router and research orchestrator — chooses where to search, activates skills, distributes to local/web/DB/NAS."""

    agent = "@Hermes"
    role = "router"
    layer = "analysis"
    veto = False
    _soul_dir = Path(__file__).parent / "hermes"
