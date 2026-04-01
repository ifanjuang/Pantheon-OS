"""
RagService — pipeline RAG (§1b).

- embed()   : génère un vecteur pour un texte
- ingest()  : fichier → chunks → embeddings → INSERT dans la table chunks
- search()  : embed query → SELECT cosine distance (pgvector) → résultats triés
- delete_document() : supprime tous les chunks d'un document

Stockage : table `chunks` gérée par SQLAlchemy (pas la table interne LlamaIndex).
Recherche : requête SQL directe avec l'opérateur <=> de pgvector.
"""
import json
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

# Configuration chunking adaptatif par type de document (§23.6 + §21.4)
CHUNK_CONFIG: dict[str, dict] = {
    "cctp":  {"chunk_size": 512, "chunk_overlap": 64},
    "dtu":   {"chunk_size": 256, "chunk_overlap": 32},
    "email": {"chunk_size": 128, "chunk_overlap": 16},
    "cr":    {"chunk_size": 256, "chunk_overlap": 32},
    "note":  {"chunk_size": 256, "chunk_overlap": 32},
}
DEFAULT_CHUNK = {"chunk_size": 256, "chunk_overlap": 32}


def _db_params() -> dict:
    """Extrait host/port/user/password/dbname depuis DATABASE_URL_SYNC."""
    parsed = urlparse(settings.DATABASE_URL_SYNC)
    return {
        "host": parsed.hostname or "db",
        "port": parsed.port or 5432,
        "user": parsed.username or "arceus",
        "password": parsed.password or "",
        "database": (parsed.path or "/arceus").lstrip("/"),
    }


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
          2. Découpe en chunks (SentenceSplitter, config par source_type)
          3. Calcule l'embedding de chaque chunk
          4. INSERT dans la table chunks

        Retourne le nombre de chunks créés.
        """
        from llama_index.core import SimpleDirectoryReader
        from llama_index.core.node_parser import SentenceSplitter

        t0 = time.monotonic()
        chunk_cfg = CHUNK_CONFIG.get(source_type, DEFAULT_CHUNK)
        extra_meta = extra_meta or {}

        # Écrire dans un fichier temporaire pour SimpleDirectoryReader
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

        splitter = SentenceSplitter(
            chunk_size=chunk_cfg["chunk_size"],
            chunk_overlap=chunk_cfg["chunk_overlap"],
        )
        nodes = splitter.get_nodes_from_documents(documents)

        # Embedding en batch
        texts = [node.get_content() for node in nodes]
        embeddings = await cls._get_embed_model().aget_text_embedding_batch(texts)

        # INSERT dans la table chunks
        for idx, (node, embedding) in enumerate(zip(nodes, embeddings)):
            meta = {
                "source_type": source_type,
                "filename": filename,
                **extra_meta,
                **node.metadata,
            }
            await db.execute(
                text("""
                    INSERT INTO chunks
                        (id, document_id, affaire_id, contenu, embedding,
                         chunk_index, meta, created_at)
                    VALUES
                        (uuid_generate_v4(), :doc_id, :aff_id, :contenu,
                         :embedding::vector, :idx, :meta, now())
                """),
                {
                    "doc_id": str(document_id),
                    "aff_id": str(affaire_id),
                    "contenu": node.get_content(),
                    "embedding": str(embedding),
                    "idx": idx,
                    "meta": json.dumps(meta),
                },
            )

        await db.commit()
        log.info(
            "rag.ingest",
            document_id=str(document_id),
            affaire_id=str(affaire_id),
            source_type=source_type,
            chunks=len(nodes),
            duration_ms=int((time.monotonic() - t0) * 1000),
        )
        return len(nodes)

    @classmethod
    async def search(
        cls,
        db: AsyncSession,
        query: str,
        affaire_id: UUID,
        top_k: int = 5,
        source_type: Optional[str] = None,
        couche: Optional[str] = None,
    ) -> list[dict]:
        """
        Recherche sémantique via pgvector (<=> cosine distance).
        Retourne [{chunk_id, document_id, contenu, score, meta}]
        """
        t0 = time.monotonic()
        query_emb = await cls.embed(query)
        emb_str = str(query_emb)

        # Filtre optionnel sur source_type (stocké dans meta JSONB)
        extra_filter = ""
        params: dict = {
            "qvec": emb_str,
            "affaire_id": str(affaire_id),
            "top_k": top_k,
        }
        if source_type:
            extra_filter += " AND meta->>'source_type' = :source_type"
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

        results = [
            {
                "chunk_id": str(row.id),
                "document_id": str(row.document_id),
                "contenu": row.contenu,
                "meta": row.meta,
                "score": float(row.score),
            }
            for row in rows
        ]

        log.info(
            "rag.search",
            affaire_id=str(affaire_id),
            query=query[:60],
            hits=len(results),
            duration_ms=int((time.monotonic() - t0) * 1000),
        )
        return results

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
