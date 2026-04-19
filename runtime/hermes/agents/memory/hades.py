from pathlib import Path
from .._base import AgentBase


class Hades(AgentBase):
    """Deep memory / vector store — semantic retrieval, access to chunks and embeddings, long-term search."""

    agent = "@Hades"
    role = "vector_retrieval"
    layer = "memory"
    veto = False
    _soul_dir = Path(__file__).parent / "hades"
