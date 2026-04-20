"""
Reranker — cross-encoder post-RRF.

Classe singleton avec chargement lazy du modèle (sentence-transformers).
Modèle par défaut : cross-encoder/ms-marco-MiniLM-L-6-v2 (~80 Mo, CPU-compatible).

Activé via RERANK_ENABLED=true dans .env.
Fallback silencieux si le paquet n'est pas installé ou si le modèle échoue.
"""

from core.logging import get_logger
from core.settings import settings

log = get_logger("rag.rerank")


class Reranker:
    """Singleton de reranking cross-encoder.

    Usage :
        hits = reranker.rerank(query, hits, top_k=5)
    """

    def __init__(self) -> None:
        self._model = None

    def _load_model(self):
        if self._model is None:
            from sentence_transformers import CrossEncoder

            model_name = getattr(settings, "RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
            self._model = CrossEncoder(model_name)
            log.info("rag.rerank_model_loaded", model=model_name)
        return self._model

    def rerank(self, query: str, hits: list[dict], top_k: int) -> list[dict]:
        """Rerank post-RRF via cross-encoder.

        Ne fait rien si RERANK_ENABLED=false ou si hits <= 1.
        Fallback silencieux sur toute erreur (modèle absent, OOM, etc.).
        """
        if not hits or len(hits) <= 1:
            return hits

        if not getattr(settings, "RERANK_ENABLED", False):
            return hits

        try:
            model = self._load_model()
            pairs = [(query, h["contenu"][:512]) for h in hits]
            scores = model.predict(pairs)

            for hit, score in zip(hits, scores):
                hit["rerank_score"] = float(score)

            reranked = sorted(hits, key=lambda h: h["rerank_score"], reverse=True)[:top_k]
            for h in reranked:
                h["score_type"] = "rerank"
                h["score"] = h.pop("rerank_score")
            return reranked

        except ImportError:
            log.debug("rag.rerank_unavailable", reason="sentence-transformers not installed")
            return hits[:top_k]
        except Exception as exc:
            log.warning("rag.rerank_failed", error=str(exc))
            return hits[:top_k]


# Singleton process-level
reranker = Reranker()


def _rerank(query: str, hits: list[dict], top_k: int) -> list[dict]:
    """Compatibilité : wrapper fonctionnel sur le singleton Reranker."""
    return reranker.rerank(query, hits, top_k)
