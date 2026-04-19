from pathlib import Path
from .._base import AgentBase


class Mnemosyne(AgentBase):
    """Library and structured memory — organizes internal references, links dossier types, exposes reusable memory."""

    agent = "@Mnemosyne"
    role = "knowledge_library"
    layer = "memory"
    veto = False
    _soul_dir = Path(__file__).parent / "mnemosyne"
