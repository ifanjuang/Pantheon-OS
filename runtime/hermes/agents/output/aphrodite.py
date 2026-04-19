from pathlib import Path
from .._base import AgentBase


class Aphrodite(AgentBase):
    """Polish and impact — improves presentation, gives more impact to form, beautifies external outputs."""

    agent = "@Aphrodite"
    role = "stylist"
    layer = "output"
    veto = False
    _soul_dir = Path(__file__).parent / "aphrodite"
