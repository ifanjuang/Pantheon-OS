from pathlib import Path
from .._base import AgentBase


class Iris(AgentBase):
    """Communication and tone adaptation — reformulates by context, adapts to recipient, asks clear questions."""

    agent = "@Iris"
    role = "communicator"
    layer = "output"
    veto = False
    _soul_dir = Path(__file__).parent / "iris"
