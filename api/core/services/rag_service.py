"""
RagService — pipeline RAG hybride (sémantique + full-text + RRF).

Méthodes publiques :
  embed()          : génère un vecteur pour un texte
  ingest()         : fichier → chunks → embeddings → bulk INSERT chunks
  search()         : recherche hybride par défaut (délègue à search_hybrid)
  search_hybrid()  : cosine pgvector + FTS PostgreSQL fusionnés via RRF
  search_semantic(): cosine pgvector seul (pour cas spécifiques)
  delete_document(): supprime tous les chunks d'un document

Chunking :
  - SentenceWindowNodeParser pour cctp/dtu (window=3 phrases, contexte enrichi)
  - SentenceSplitter standard pour les autres types

Hybrid search :
  - Sémantique : cosine similarity pgvector (HNSW index)
  - Full-text   : ts_rank_cd PostgreSQL, colonne tsv pré-calculée (GIN)
  - Fusion      : Reciprocal Rank Fusion (RRF, k=60) — SQL natif via CTE
                  FULL OUTER JOIN (1 round-trip DB au lieu de 2)
"""
import asyncio
import json
import re
import tempfile
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.settings import settings

log = get_logger("rag_service")

# Types de documents utilisant le SentenceWindowNodeParser (context enrichi)
_WINDOW_TYPES = {"cctp", "dtu"}

# Configuration chunking adaptatif par type de document
CHUNK_CONFIG: dict[str, dict] = {
    "cctp":  {"chunk_size": 512, "chunk_overlap": 64},
    "dtu":   {"chunk_size": 256, "chunk_overlap": 32},
    "email": {"chunk_size": 128, "chunk_overlap": 16},
    "cr":    {"chunk_size": 256, "chunk_overlap": 32},
    "note":  {"chunk_size": 256, "chunk_overlap": 32},
}
DEFAULT_CHUNK = {"chunk_size": 256, "chunk_overlap": 32}

# Constante RRF (standard = 60)
_RRF_K = 60


def _db_params() -> dict:
    parsed = urlparse(settings.DATABASE_URL_SYNC)
    return {
        "host": parsed.hostname or "db",
        "port": parsed.port or 5432,
        "user": parsed.username or "arceus",
        "password": parsed.password or "",
        "database": (parsed.path or "/arceus").lstrip("/"),
    }


def _rerank(query: str, hits: list[dict], top_k: int) -> list[dict]:
    """
    Rerank post-RRF via cross-encoder (sentence-transformers).
    Modèle léger (~80 Mo) compatible CPU/local.
    Fallback silencieux : retourne les hits tels quels si le modèle n'est pas disponible.
    """
    if not hits or len(hits) <= 1:
        return hits

    rerank_enabled = getattr(settings, "RERANK_ENABLED", False)
    if not rerank_enabled:
        return hits

    try:
        from sentence_transformers import CrossEncoder
        _model_name = getattr(settings, "RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

        if not hasattr(_rerank, "_model") or _rerank._model is None:
            _rerank._model = CrossEncoder(_model_name)

        pairs = [(query, h["contenu"][:512]) for h in hits]
        scores = _rerank._model.predict(pairs)

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

_rerank._model = None  # lazy-loaded singleton


class RagService:
    _embed_model = None

    @classmethod
    def _get_embed_model(cls):
        if cls._embed_model is None:
            from llama_index.embeddings.openai import OpenAIEmbedding

            if settings.EMBEDDING_PROVIDER == "ollama":
                cls._embed_model = OpenAIEmbedding(
                    model=settings.OLLAMA_EMBEDDING_MODEL,
                    api_base=f"{settings.OLLAMA_BASE_URL}/v1",
                    api_key="ollama",
                    embed_batch_size=10,
                )
            else:
                cls._embed_model = OpenAIEmbedding(
                    model=settings.effective_embedding_model,
                    api_key=settings.OPENAI_API_KEY,
                )
        return cls._embed_model

    @classmethod
    async def embed(cls, text_input: str) -> list[float]:
        """Génère un vecteur d'embedding pour un texte."""
        return await cls._get_embed_model().aget_text_embedding(text_input)

    @classmethod
    async def ingest(
        cls,
        db: AsyncSession,
        document_id: UUID,
        file_bytes: bytes,
        filename: str,
        source_type: str,
        affaire_id: UUID,
        extra_meta: Optional[dict] = None,
    ) -> int:
        """
        Ingère un fichier :
          1. Extrait le texte via LlamaIndex SimpleDirectoryReader
          2. Découpe en chunks :
             - SentenceWindowNodeParser (window=3) pour cctp/dtu
             - SentenceSplitter standard pour les autres types
          3. Calcule l'embedding de chaque chunk
          4. INSERT dans la table chunks (contenu + window dans meta si applicable)

        Retourne le nombre de chunks créés.
        """
        from llama_index.core import SimpleDirectoryReader
        from llama_index.core.node_parser import SentenceSplitter

        t0 = time.monotonic()
        chunk_cfg = CHUNK_CONFIG.get(source_type, DEFAULT_CHUNK)
        extra_meta = extra_meta or {}

        suffix = Path(filename).suffix or ".txt"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            reader = SimpleDirectoryReader(input_files=[tmp_path])
            documents = reader.load_data()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        if not documents:
            log.warning("rag.ingest_empty", document_id=str(document_id), filename=filename)
            return 0

        # ── OCR fallback (GLM-4V) ───────────────────────────────────────
        # Déclenché quand le texte natif est trop court (PDF scanné / image).
        native_text = " ".join(doc.get_content() for doc in documents)
        ocr_min = getattr(settings, "GLM_OCR_MIN_CHARS", 100)
        ocr_endpoint = getattr(settings, "GLM_OCR_ENDPOINT", None)

        if ocr_endpoint and len(native_text.strip()) < ocr_min:
            try:
                from core.services.ocr_service import OcrService
                ocr_result = await OcrService.extract_text(file_bytes, filename)
                if ocr_result["text"].strip():
                    from llama_index.core import Document as LIDocument
                    documents = [LIDocument(text=ocr_result["text"])]
                    extra_meta = {
                        **extra_meta,
                        "ocr_provider": ocr_result["ocr_provider"],
                        "ocr_confidence": ocr_result["confidence"],
                        "layout_blocks_count": ocr_result["layout_blocks_count"],
                        "extraction_mode": ocr_result["extraction_mode"],
                    }
                    log.info(
                        "rag.ocr_fallback_used",
                        document_id=str(document_id),
                        filename=filename,
                        native_chars=len(native_text.strip()),
                        ocr_chars=len(ocr_result["text"]),
                    )
            except Exception as exc:
                log.warning("rag.ocr_fallback_failed", filename=filename, error=str(exc))

        # Chunking adaptatif selon le type de document
        if source_type in _WINDOW_TYPES:
            from llama_index.core.node_parser import SentenceWindowNodeParser
            parser = SentenceWindowNodeParser.from_defaults(
                window_size=3,
                window_metadata_key="window",
                original_text_metadata_key="original_text",
            )
            nodes = parser.get_nodes_from_documents(documents)
            log.debug("rag.ingest_window", source_type=source_type, nodes=len(nodes))
        else:
            splitter = SentenceSplitter(
                chunk_size=chunk_cfg["chunk_size"],
                chunk_overlap=chunk_cfg["chunk_overlap"],
            )
            nodes = splitter.get_nodes_from_documents(documents)

        # Embedding en batch sur le contenu principal (pas la window)
        texts = [node.get_content() for node in nodes]

        # ── Contextual Retrieval (Anthropic pattern) ────────────────────
        # Génère un court contexte par chunk situant le fragment dans son document source.
        # Améliore la précision de la recherche sémantique de ~49% (Anthropic, 2024).
        # Désactivable via CONTEXTUAL_RETRIEVAL=false dans .env.
        contextual_enabled = getattr(settings, "CONTEXTUAL_RETRIEVAL", True)
        contexts: list[str] = [""] * len(texts)

        if contextual_enabled and len(texts) <= 200:  # skip pour très gros documents
            try:
                doc_summary = texts[0][:500] if texts else ""
                _CTX_PROMPT = (
                    f"Document source : {filename} (type: {source_type})\n"
                    f"Début du document : {doc_summary}\n\n"
                    "Pour le fragment suivant, écris UNE phrase de contexte (max 50 mots) "
                    "qui situe ce fragment dans son document source. "
                    "Commence par 'Ce fragment...' ou 'Cet extrait...'\n\n"
                    "Fragment :\n{chunk}\n\nContexte :"
                )
                # Batch : on traite par lots de 10 pour ne pas saturer Ollama
                from core.services.llm_service import LlmService
                for batch_start in range(0, len(texts), 10):
                    batch = texts[batch_start:batch_start + 10]
                    ctx_tasks = [
                        LlmService.chat(
                            messages=[{"role": "user", "content": _CTX_PROMPT.format(chunk=t[:800])}],
                            temperature=0.0,
                            max_tokens=80,
                        )
                        for t in batch
                    ]
                    batch_results = await asyncio.gather(*ctx_tasks, return_exceptions=True)
                    for i, result in enumerate(batch_results):
                        if isinstance(result, str) and len(result.strip()) > 10:
                            contexts[batch_start + i] = result.strip()

                log.info("rag.contextual_retrieval", chunks=len(texts),
                         contexts_generated=sum(1 for c in contexts if c))
            except Exception as exc:
                log.warning("rag.contextual_retrieval_failed", error=str(exc))
                # Continuer sans contexte — pas bloquant

        # Préparer le texte pour embedding : contexte + contenu
        embed_texts = [
            f"{ctx}\n\n{t}" if ctx else t
            for ctx, t in zip(contexts, texts)
        ]
        embeddings = await cls._get_embed_model().aget_text_embedding_batch(embed_texts)

        # Bulk INSERT — un seul aller-retour DB pour tous les chunks
        rows = []
        for idx, (node, embedding) in enumerate(zip(nodes, embeddings)):
            meta = {
                "source_type": source_type,
                "filename": filename,
                **extra_meta,
                **{k: v for k, v in node.metadata.items() if k != "window"},
            }
            if "window" in node.metadata:
                meta["window"] = node.metadata["window"]
            rows.append({
                "doc_id": str(document_id),
                "aff_id": str(affaire_id),
                "contenu": node.get_content(),
                "embedding": str(embedding),
                "idx": idx,
                "meta": json.dumps(meta),
            })

        await db.execute(
            text("""
                INSERT INTO chunks
                    (id, document_id, affaire_id, contenu, embedding,
                     chunk_index, meta, created_at)
                VALUES
                    (uuid_generate_v4(), :doc_id, :aff_id, :contenu,
                     :embedding::vector, :idx, :meta, now())
            """),
            rows,  # executemany — un seul aller-retour pour tous les chunks
        )
        await db.commit()
        log.info(
            "rag.ingest",
            document_id=str(document_id),
            affaire_id=str(affaire_id),
            source_type=source_type,
            chunks=len(nodes),
            window=source_type in _WINDOW_TYPES,
            duration_ms=int((time.monotonic() - t0) * 1000),
        )
        return len(nodes)

    # ── Recherche ───────────────────────────────────────────────────

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
        """
        Recherche dans les chunks.
        mode="hybrid"   (défaut) : sémantique + FTS fusionnés via RRF
        mode="semantic" : cosine pgvector seul
        mode="fts"      : full-text PostgreSQL seul
        """
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
        """
        Recherche hybride via une seule requête CTE + RRF SQL natif.

        Remplace les 2 requêtes parallèles + fusion Python par un unique
        aller-retour DB : les CTEs `sem_raw` et `fts_raw` calculent les
        candidats de chaque branche, `rrf` les fusionne via FULL OUTER JOIN
        avec le scoring 1/(k+rank), et la requête externe trie et limite.

        Fallback : si la CTE échoue (pgvector absent, query invalide, etc.),
        bascule silencieusement sur la recherche sémantique seule.
        """
        t0 = time.monotonic()

        # Sanitize FTS (identique à l'ancienne _search_fts)
        sanitized_fts = re.sub(r'[^\w\s\-àâäéèêëïîôùûüÿçœæ]', ' ', query)
        sanitized_fts = ' '.join(sanitized_fts.split())

        # Si la query FTS est vide après nettoyage → sémantique seule
        if not sanitized_fts:
            return await cls.search_semantic(db, query, affaire_id, top_k, source_type)

        query_emb = await cls.embed(query)
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
        """Recherche par cosine similarity pgvector (HNSW index)."""
        query_emb = await cls.embed(query)
        emb_str = str(query_emb)

        extra_filter = ""
        params: dict = {
            "qvec": emb_str,
            "affaire_id": str(affaire_id),
            "top_k": top_k,
        }
        if source_type:
            extra_filter = " AND meta->>'source_type' = :source_type"
            params["source_type"] = source_type

        rows = await db.execute(
            text(f"""
                SELECT
                    id,
                    document_id,
                    contenu,
                    meta,
                    1 - (embedding <=> :qvec::vector) AS score
                FROM chunks
                WHERE affaire_id = :affaire_id
                {extra_filter}
                ORDER BY embedding <=> :qvec::vector
                LIMIT :top_k
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
        """Recherche full-text via to_tsvector PostgreSQL (GIN index)."""
        extra_filter = ""
        params: dict = {
            "query": query,
            "affaire_id": str(affaire_id),
            "top_k": top_k,
        }
        if source_type:
            extra_filter = " AND meta->>'source_type' = :source_type"
            params["source_type"] = source_type

        try:
            # Sanitiser la query FTS : supprimer les caractères spéciaux qui cassent plainto_tsquery
            sanitized_query = re.sub(r'[^\w\s\-àâäéèêëïîôùûüÿçœæ]', ' ', query)
            sanitized_query = ' '.join(sanitized_query.split())  # normaliser les espaces
            if not sanitized_query.strip():
                return []
            params["query"] = sanitized_query

            # Utilise la colonne pré-calculée tsv (migration 0013) avec index GIN
            # au lieu du LATERAL to_tsvector() coûteux à chaque requête
            rows = await db.execute(
                text(f"""
                    SELECT id, document_id, contenu, meta,
                           ts_rank_cd(tsv, plainto_tsquery('french', :query)) AS score
                    FROM chunks
                    WHERE affaire_id = :affaire_id
                      AND tsv @@ plainto_tsquery('french', :query)
                    {extra_filter}
                    ORDER BY score DESC
                    LIMIT :top_k
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
            # FTS peut échouer si la query contient des caractères spéciaux
            log.warning("rag.fts_failed", query=query[:60], error=str(exc))
            return []

    @classmethod
    async def ingest_text_direct(
        cls,
        db: AsyncSession,
        text_content: str,
        affaire_id: UUID,
        source_type: str,
        source_id: UUID,
        extra_meta: Optional[dict] = None,
    ) -> int:
        """
        Ingère du texte brut sans fichier source (courrier, observation, note, etc.).

        Découpe le texte en chunks via SentenceSplitter, calcule les embeddings
        et insère dans `chunks` avec source_type/source_id au lieu de document_id.

        Les chunks existants pour ce (source_type, source_id) sont supprimés
        au préalable pour garantir l'idempotence (réindexation à la mise à jour).

        Retourne le nombre de chunks créés.
        """
        from llama_index.core.node_parser import SentenceSplitter

        t0 = time.monotonic()
        extra_meta = extra_meta or {}

        if not text_content or not text_content.strip():
            log.warning(
                "rag.ingest_text_direct_empty",
                source_type=source_type,
                source_id=str(source_id),
            )
            return 0

        # Supprimer les chunks existants pour cet objet (idempotence)
        await db.execute(
            text(
                "DELETE FROM chunks WHERE source_type = :st AND source_id = :sid"
            ),
            {"st": source_type, "sid": str(source_id)},
        )

        chunk_cfg = CHUNK_CONFIG.get(source_type, DEFAULT_CHUNK)
        splitter = SentenceSplitter(
            chunk_size=chunk_cfg["chunk_size"],
            chunk_overlap=chunk_cfg["chunk_overlap"],
        )

        from llama_index.core import Document as LIDocument
        li_doc = LIDocument(text=text_content)
        nodes = splitter.get_nodes_from_documents([li_doc])

        if not nodes:
            return 0

        texts = [node.get_content() for node in nodes]
        embeddings = await cls._get_embed_model().aget_text_embedding_batch(texts)

        rows = []
        for idx, (node, embedding) in enumerate(zip(nodes, embeddings)):
            meta = {
                "source_type": source_type,
                "source_id": str(source_id),
                **extra_meta,
            }
            rows.append({
                "src_type": source_type,
                "src_id": str(source_id),
                "aff_id": str(affaire_id),
                "contenu": node.get_content(),
                "embedding": str(embedding),
                "idx": idx,
                "meta": json.dumps(meta),
            })

        await db.execute(
            text("""
                INSERT INTO chunks
                    (id, source_type, source_id, affaire_id, contenu, embedding,
                     chunk_index, meta, created_at)
                VALUES
                    (uuid_generate_v4(), :src_type, :src_id::uuid, :aff_id,
                     :contenu, :embedding::vector, :idx, :meta, now())
            """),
            rows,
        )
        await db.commit()
        log.info(
            "rag.ingest_text_direct",
            source_type=source_type,
            source_id=str(source_id),
            affaire_id=str(affaire_id),
            chunks=len(rows),
            duration_ms=int((time.monotonic() - t0) * 1000),
        )
        return len(rows)

    @classmethod
    async def delete_source(cls, db: AsyncSession, source_type: str, source_id: UUID) -> int:
        """Supprime tous les chunks liés à une source générique. Retourne le nombre supprimé."""
        result = await db.execute(
            text("DELETE FROM chunks WHERE source_type = :st AND source_id = :sid"),
            {"st": source_type, "sid": str(source_id)},
        )
        await db.commit()
        deleted = result.rowcount
        log.info(
            "rag.delete_source",
            source_type=source_type,
            source_id=str(source_id),
            chunks_deleted=deleted,
        )
        return deleted

    @classmethod
    async def delete_document(cls, db: AsyncSession, document_id: UUID) -> int:
        """Supprime tous les chunks liés à un document. Retourne le nombre supprimé."""
        result = await db.execute(
            text("DELETE FROM chunks WHERE document_id = :doc_id"),
            {"doc_id": str(document_id)},
        )
        await db.commit()
        deleted = result.rowcount
        log.info("rag.delete_document", document_id=str(document_id), chunks_deleted=deleted)
        return deleted
