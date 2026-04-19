from pathlib import Path
from .._base import AgentBase


class Themis(AgentBase):
    """Process integrity — verifies workflow follows rules, blocks non-conformant outputs."""

    agent = "@THEMIS"
    role = "process_guardian"
    layer = "meta"
    veto = True
    _soul_dir = Path(__file__).parent / "themis"
