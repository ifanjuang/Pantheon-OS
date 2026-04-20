"""
Package RAG — pipeline hybride sémantique + full-text + reranking.

Exporte RagService (facade) qui conserve la même API publique que
l'ancien rag_service.py monolithique. Les sous-modules internes sont :
  _embed.py   : singleton modèle d'embedding
  _rerank.py  : Reranker cross-encoder (lazy-loaded)
  _ingest.py  : IngestPipeline (fichiers + texte brut)
  _search.py  : HybridSearcher (hybrid / semantic / fts)
"""

from core.services.rag._embed import embed as _embed_fn, get_embed_model
from core.services.rag._ingest import (
    CHUNK_CONFIG,
    DEFAULT_CHUNK,
    IngestPipeline,
    _WINDOW_TYPES,
)
from core.services.rag._rerank import _rerank, reranker
from core.services.rag._search import HybridSearcher, _rrf_fusion


class RagService:
    """Facade publique — délègue aux sous-composants RAG.

    Tous les appels existants (RagService.search, RagService.ingest, …)
    continuent de fonctionner sans modification.
    """

    # ── Embedding ─────────────────────────────────────────────────────

    @classmethod
    async def embed(cls, text_input: str) -> list[float]:
        return await _embed_fn(text_input)

    @classmethod
    def _get_embed_model(cls):
        return get_embed_model()

    # ── Ingestion ─────────────────────────────────────────────────────

    ingest = IngestPipeline.ingest
    ingest_text_direct = IngestPipeline.ingest_text_direct
    delete_document = IngestPipeline.delete_document
    delete_source = IngestPipeline.delete_source

    # ── Recherche ─────────────────────────────────────────────────────

    search = HybridSearcher.search
    search_hybrid = HybridSearcher.search_hybrid
    search_semantic = HybridSearcher.search_semantic
    _search_fts = HybridSearcher._search_fts


__all__ = [
    "RagService",
    "CHUNK_CONFIG",
    "DEFAULT_CHUNK",
    "_WINDOW_TYPES",
    "_rerank",
    "_rrf_fusion",
    "reranker",
    "IngestPipeline",
    "HybridSearcher",
]
