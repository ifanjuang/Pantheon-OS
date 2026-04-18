"""
HybridSearcher — recherche hybride sémantique + full-text + RRF.

Trois modes :
  search()          : dispatcher (hybrid par défaut)
  search_hybrid()   : cosine pgvector + FTS PostgreSQL fusionnés via RRF SQL natif
  search_semantic() : cosine pgvector seul
  _search_fts()     : full-text PostgreSQL seul

_rrf_fusion() : fusion Python de deux listes de hits (fallback + tests unitaires).
"""

import re
import time
from typing import Optional
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.rag._embed import embed
from core.services.rag._rerank import _rerank
from core.settings import settings

log = get_logger("rag.search")

_RRF_K = 60


def _rrf_fusion(
    semantic: list[dict],
    fts: list[dict],
    top_k: int,
    k: int = _RRF_K,
) -> list[dict]:
    """Fusion Python RRF de deux listes de hits (fallback / tests).

    La production utilise la CTE SQL dans search_hybrid() pour éviter
    deux allers-retours DB. Cette version Python sert de fallback et
    est utilisée directement dans les tests unitaires.
    """
    scores: dict[str, float] = {}
    hits_by_id: dict[str, dict] = {}

    for rank, hit in enumerate(semantic, 1):
        cid = hit["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
        hits_by_id[cid] = hit

    for rank, hit in enumerate(fts, 1):
        cid = hit["chunk_id"]
        scores[cid] = scores.get(cid, 0.0) + 1.0 / (k + rank)
        hits_by_id[cid] = hit

    sorted_ids = sorted(scores, key=lambda x: scores[x], reverse=True)[:top_k]
    result = []
    for cid in sorted_ids:
        h = dict(hits_by_id[cid])
        h["score"] = scores[cid]
        h["score_type"] = "rrf"
        result.append(h)
    return result


class HybridSearcher:
    @classmethod
    async def search(
        cls,
        db: AsyncSession,
        query: str,
        affaire_id: UUID,
        top_k: int = 5,
        source_type: Optional[str] = None,
        couche: Optional[str] = None,
        mode: str = "hybrid",
    ) -> list[dict]:
        """Dispatcher : hybrid (défaut) | semantic | fts."""
        if mode == "semantic":
            return await cls.search_semantic(db, query, affaire_id, top_k, source_type)
        if mode == "fts":
            return await cls._search_fts(db, query, affaire_id, top_k * 2, source_type)
        return await cls.search_hybrid(db, query, affaire_id, top_k, source_type)

    @classmethod
    async def search_hybrid(
        cls,
        db: AsyncSession,
        query: str,
        affaire_id: UUID,
        top_k: int = 5,
        source_type: Optional[str] = None,
    ) -> list[dict]:
        """Recherche hybride via CTE + RRF SQL natif (un seul aller-retour DB).

        Les CTEs sem_raw et fts_raw calculent les candidats de chaque branche.
        La CTE rrf fusionne via FULL OUTER JOIN avec le scoring 1/(k+rank).
        Fallback silencieux vers search_semantic() si la CTE échoue.
        """
        t0 = time.monotonic()

        sanitized_fts = re.sub(r"[^\w\s\-àâäéèêëïîôùûüÿçœæ]", " ", query)
        sanitized_fts = " ".join(sanitized_fts.split())

        if not sanitized_fts:
            return await cls.search_semantic(db, query, affaire_id, top_k, source_type)

        query_emb = await embed(query)
        fetch_k = top_k * 3
        rrf_candidates = top_k * 2 if getattr(settings, "RERANK_ENABLED", False) else top_k

        extra_filter = ""
        params: dict = {
            "qvec": str(query_emb),
            "fts_query": sanitized_fts,
            "affaire_id": str(affaire_id),
            "fetch_k": fetch_k,
            "top_k": rrf_candidates,
            "rrf_k": float(_RRF_K),
        }
        if source_type:
            extra_filter = "AND meta->>'source_type' = :source_type"
            params["source_type"] = source_type

        try:
            rows = await db.execute(
                text(f"""
                    WITH
                    sem_raw AS (
                        SELECT id, document_id, contenu, meta,
                               embedding <=> :qvec::vector AS sem_dist
                        FROM   chunks
                        WHERE  affaire_id = :affaire_id
                               {extra_filter}
                        ORDER  BY embedding <=> :qvec::vector
                        LIMIT  :fetch_k
                    ),
                    semantic AS (
                        SELECT id, document_id, contenu, meta,
                               row_number() OVER (ORDER BY sem_dist) AS rank
                        FROM   sem_raw
                    ),
                    fts_raw AS (
                        SELECT id, document_id, contenu, meta,
                               ts_rank_cd(tsv, plainto_tsquery('french', :fts_query)) AS fts_score
                        FROM   chunks
                        WHERE  affaire_id = :affaire_id
                               AND tsv @@ plainto_tsquery('french', :fts_query)
                               {extra_filter}
                        ORDER  BY fts_score DESC
                        LIMIT  :fetch_k
                    ),
                    fts AS (
                        SELECT id, document_id, contenu, meta,
                               row_number() OVER (ORDER BY fts_score DESC) AS rank
                        FROM   fts_raw
                    ),
                    rrf AS (
                        SELECT
                            COALESCE(s.id,          f.id)          AS id,
                            COALESCE(s.document_id, f.document_id) AS document_id,
                            COALESCE(s.contenu,     f.contenu)     AS contenu,
                            COALESCE(s.meta,        f.meta)        AS meta,
                            COALESCE(1.0 / (:rrf_k + s.rank), 0.0)
                          + COALESCE(1.0 / (:rrf_k + f.rank), 0.0) AS rrf_score
                        FROM      semantic s
                        FULL OUTER JOIN fts f ON s.id = f.id
                    )
                    SELECT id, document_id, contenu, meta, rrf_score
                    FROM   rrf
                    ORDER  BY rrf_score DESC
                    LIMIT  :top_k
                """),
                params,
            )
            results = [
                {
                    "chunk_id": str(row.id),
                    "document_id": str(row.document_id),
                    "contenu": row.contenu,
                    "meta": row.meta,
                    "score": float(row.rrf_score),
                    "score_type": "rrf",
                }
                for row in rows
            ]
        except Exception as exc:
            log.warning("rag.hybrid_sql_failed", error=str(exc), fallback="semantic")
            results = await cls.search_semantic(db, query, affaire_id, top_k, source_type)

        results = _rerank(query, results, top_k)

        log.info(
            "rag.search_hybrid",
            affaire_id=str(affaire_id),
            query=query[:60],
            results=len(results),
            duration_ms=int((time.monotonic() - t0) * 1000),
        )
        return results

    @classmethod
    async def search_semantic(
        cls,
        db: AsyncSession,
        query: str,
        affaire_id: UUID,
        top_k: int = 5,
        source_type: Optional[str] = None,
    ) -> list[dict]:
        """Recherche par cosine similarity pgvector (index HNSW)."""
        query_emb = await embed(query)
        extra_filter = ""
        params: dict = {"qvec": str(query_emb), "affaire_id": str(affaire_id), "top_k": top_k}
        if source_type:
            extra_filter = " AND meta->>'source_type' = :source_type"
            params["source_type"] = source_type

        rows = await db.execute(
            text(f"""
                SELECT id, document_id, contenu, meta,
                       1 - (embedding <=> :qvec::vector) AS score
                FROM   chunks
                WHERE  affaire_id = :affaire_id
                {extra_filter}
                ORDER  BY embedding <=> :qvec::vector
                LIMIT  :top_k
            """),
            params,
        )
        return [
            {
                "chunk_id": str(row.id),
                "document_id": str(row.document_id),
                "contenu": row.contenu,
                "meta": row.meta,
                "score": float(row.score),
                "score_type": "semantic",
            }
            for row in rows
        ]

    @classmethod
    async def _search_fts(
        cls,
        db: AsyncSession,
        query: str,
        affaire_id: UUID,
        top_k: int = 15,
        source_type: Optional[str] = None,
    ) -> list[dict]:
        """Recherche full-text via colonne tsv pré-calculée (index GIN)."""
        sanitized = re.sub(r"[^\w\s\-àâäéèêëïîôùûüÿçœæ]", " ", query)
        sanitized = " ".join(sanitized.split())
        if not sanitized.strip():
            return []

        extra_filter = ""
        params: dict = {"query": sanitized, "affaire_id": str(affaire_id), "top_k": top_k}
        if source_type:
            extra_filter = " AND meta->>'source_type' = :source_type"
            params["source_type"] = source_type

        try:
            rows = await db.execute(
                text(f"""
                    SELECT id, document_id, contenu, meta,
                           ts_rank_cd(tsv, plainto_tsquery('french', :query)) AS score
                    FROM   chunks
                    WHERE  affaire_id = :affaire_id
                      AND  tsv @@ plainto_tsquery('french', :query)
                    {extra_filter}
                    ORDER  BY score DESC
                    LIMIT  :top_k
                """),
                params,
            )
            return [
                {
                    "chunk_id": str(row.id),
                    "document_id": str(row.document_id),
                    "contenu": row.contenu,
                    "meta": row.meta,
                    "score": float(row.score),
                    "score_type": "fts",
                }
                for row in rows
            ]
        except Exception as exc:
            log.warning("rag.fts_failed", query=query[:60], error=str(exc))
            return []
