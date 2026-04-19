from pathlib import Path
from .._base import AgentBase


class Hestia(AgentBase):
    """Short-term memory / session context — keeps immediate context, stores user clarifications."""

    agent = "@Hestia"
    role = "session_memory"
    layer = "memory"
    veto = False
    _soul_dir = Path(__file__).parent / "hestia"
