from pathlib import Path
from .._base import AgentBase


class Artemis(AgentBase):
    """Filtering and focus — cuts noise, keeps most relevant, adapts depth to context."""

    agent = "@Artemis"
    role = "filter"
    layer = "analysis"
    veto = False
    _soul_dir = Path(__file__).parent / "artemis"
