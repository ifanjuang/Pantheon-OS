from pathlib import Path
from .._base import AgentBase


class Poseidon(AgentBase):
    """Load management and flow control — monitors load, helps regulate parallelism, avoids unstable cascades."""

    agent = "@Poseidon"
    role = "distributor"
    layer = "system"
    veto = False
    _soul_dir = Path(__file__).parent / "poseidon"
