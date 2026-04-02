"""
checkpointer.py — PostgreSQL checkpointer LangGraph (HITL).

Permet de suspendre un graphe Zeus après la phase de distribution
et de le reprendre après validation humaine.

Les tables LangGraph (checkpoints, checkpoint_blobs, checkpoint_migrations,
checkpoint_writes) sont créées automatiquement par checkpointer.setup().
"""
from contextlib import asynccontextmanager

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from core.settings import settings


@asynccontextmanager
async def get_checkpointer():
    """
    Context manager qui fournit un AsyncPostgresSaver initialisé.

    Usage :
        async with get_checkpointer() as cp:
            graph = build_graph(...).compile(checkpointer=cp)
    """
    async with await AsyncPostgresSaver.from_conn_string(
        settings.DATABASE_URL_SYNC
    ) as checkpointer:
        yield checkpointer


async def setup_checkpointer() -> None:
    """
    Crée les tables LangGraph dans la DB si elles n'existent pas encore.
    Appelé au démarrage de l'application (lifespan FastAPI).
    """
    async with get_checkpointer() as cp:
        await cp.setup()
