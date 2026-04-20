"""
IngestPipeline — ingestion de fichiers et de texte brut dans le RAG.

Deux méthodes publiques :
  ingest()             : fichier binaire → chunks → embeddings → chunks table
  ingest_text_direct() : texte brut → chunks → embeddings → chunks table
  delete_document()    : supprime les chunks d'un document
  delete_source()      : supprime les chunks d'une source générique

Chunking :
  - SentenceWindowNodeParser (window=3) pour cctp/dtu (contexte enrichi)
  - SentenceSplitter standard pour les autres types

Contextual Retrieval (Anthropic pattern) :
  Génère un court contexte par chunk pour améliorer la précision sémantique.
  Désactivable via CONTEXTUAL_RETRIEVAL=false.
"""

import asyncio
import json
import tempfile
import time
from pathlib import Path
from typing import Optional
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.rag._embed import get_embed_model
from core.settings import settings

log = get_logger("rag.ingest")

# Types utilisant SentenceWindowNodeParser
_WINDOW_TYPES = {"cctp", "dtu"}

# Configuration chunking adaptatif par type de document
CHUNK_CONFIG: dict[str, dict] = {
    "cctp": {"chunk_size": 512, "chunk_overlap": 64},
    "dtu": {"chunk_size": 256, "chunk_overlap": 32},
    "email": {"chunk_size": 128, "chunk_overlap": 16},
    "cr": {"chunk_size": 256, "chunk_overlap": 32},
    "note": {"chunk_size": 256, "chunk_overlap": 32},
}
DEFAULT_CHUNK = {"chunk_size": 256, "chunk_overlap": 32}

_CTX_PROMPT = (
    "Document source : {filename} (type: {source_type})\n"
    "Début du document : {doc_summary}\n\n"
    "Pour le fragment suivant, écris UNE phrase de contexte (max 50 mots) "
    "qui situe ce fragment dans son document source. "
    "Commence par 'Ce fragment...' ou 'Cet extrait...'\n\n"
    "Fragment :\n{chunk}\n\nContexte :"
)


async def _contextual_retrieval(
    texts: list[str],
    filename: str,
    source_type: str,
) -> list[str]:
    """Génère un court contexte par chunk (Anthropic Contextual Retrieval).

    Batch de 10 appels LLM parallèles. Retourne une liste de même longueur,
    vide-string si le contexte n'a pas pu être généré pour un chunk donné.
    Silencieux sur erreur — l'ingestion continue sans contexte.
    """
    from core.services.llm_service import LlmService

    contexts: list[str] = [""] * len(texts)
    doc_summary = texts[0][:500] if texts else ""

    for batch_start in range(0, len(texts), 10):
        batch = texts[batch_start : batch_start + 10]
        tasks = [
            LlmService.chat(
                messages=[
                    {
                        "role": "user",
                        "content": _CTX_PROMPT.format(
                            filename=filename,
                            source_type=source_type,
                            doc_summary=doc_summary,
                            chunk=t[:800],
                        ),
                    }
                ],
                temperature=0.0,
                max_tokens=80,
            )
            for t in batch
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, str) and len(result.strip()) > 10:
                contexts[batch_start + i] = result.strip()

    generated = sum(1 for c in contexts if c)
    log.info("rag.contextual_retrieval", chunks=len(texts), contexts_generated=generated)
    return contexts


class IngestPipeline:
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
        """Ingère un fichier binaire dans le RAG. Retourne le nombre de chunks créés."""
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
            documents = SimpleDirectoryReader(input_files=[tmp_path]).load_data()
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        # OCR fallback — scanned PDFs / images with little native text
        ocr_endpoint = getattr(settings, "GLM_OCR_ENDPOINT", None)
        ocr_min = getattr(settings, "GLM_OCR_MIN_CHARS", 100)
        if ocr_endpoint and documents:
            native_text = " ".join(doc.get_content() for doc in documents)
            if len(native_text.strip()) < ocr_min:
                try:
                    from core.services.ocr_service import OcrService

                    ocr_result = await OcrService.extract_text(file_bytes, filename)
                    if ocr_result["text"].strip():
                        from llama_index.core import Document as LIDocument

                        documents = [LIDocument(text=ocr_result["text"])]
                        extra_meta = {
                            **extra_meta,
                            "ocr_provider": ocr_result.get("ocr_provider", ""),
                            "extraction_mode": "ocr",
                        }
                        log.info("rag.ocr_fallback_used", filename=filename, chars=len(ocr_result["text"]))
                except Exception as exc:
                    log.warning("rag.ocr_fallback_failed", filename=filename, error=str(exc))

        if not documents:
            log.warning("rag.ingest_empty", document_id=str(document_id), filename=filename)
            return 0

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
            nodes = SentenceSplitter(
                chunk_size=chunk_cfg["chunk_size"],
                chunk_overlap=chunk_cfg["chunk_overlap"],
            ).get_nodes_from_documents(documents)

        texts = [node.get_content() for node in nodes]

        # Contextual Retrieval — enrichit chaque chunk d'une phrase de situalisation
        contextual_enabled = getattr(settings, "CONTEXTUAL_RETRIEVAL", True)
        contexts: list[str] = [""] * len(texts)
        if contextual_enabled and len(texts) <= 200:
            try:
                contexts = await _contextual_retrieval(texts, filename, source_type)
            except Exception as exc:
                log.warning("rag.contextual_retrieval_failed", error=str(exc))

        embed_texts = [f"{ctx}\n\n{t}" if ctx else t for ctx, t in zip(contexts, texts)]
        embeddings = await get_embed_model().aget_text_embedding_batch(embed_texts)

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
            rows.append(
                {
                    "doc_id": str(document_id),
                    "aff_id": str(affaire_id),
                    "contenu": node.get_content(),
                    "embedding": str(embedding),
                    "idx": idx,
                    "meta": json.dumps(meta),
                }
            )

        await db.execute(
            text("""
                INSERT INTO chunks
                    (id, document_id, affaire_id, contenu, embedding,
                     chunk_index, meta, created_at)
                VALUES
                    (uuid_generate_v4(), :doc_id, :aff_id, :contenu,
                     :embedding::vector, :idx, :meta, now())
            """),
            rows,
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
        """Ingère du texte brut sans fichier source. Retourne le nombre de chunks créés.

        Idempotent : les chunks existants pour (source_type, source_id) sont supprimés
        avant l'insertion.
        """
        from llama_index.core import Document as LIDocument
        from llama_index.core.node_parser import SentenceSplitter

        t0 = time.monotonic()
        extra_meta = extra_meta or {}

        if not text_content or not text_content.strip():
            log.warning("rag.ingest_text_empty", source_type=source_type, source_id=str(source_id))
            return 0

        await db.execute(
            text("DELETE FROM chunks WHERE source_type = :st AND source_id = :sid"),
            {"st": source_type, "sid": str(source_id)},
        )

        chunk_cfg = CHUNK_CONFIG.get(source_type, DEFAULT_CHUNK)
        nodes = SentenceSplitter(
            chunk_size=chunk_cfg["chunk_size"],
            chunk_overlap=chunk_cfg["chunk_overlap"],
        ).get_nodes_from_documents([LIDocument(text=text_content)])

        if not nodes:
            return 0

        texts = [node.get_content() for node in nodes]
        embeddings = await get_embed_model().aget_text_embedding_batch(texts)

        rows = []
        for idx, (node, embedding) in enumerate(zip(nodes, embeddings)):
            meta = {"source_type": source_type, "source_id": str(source_id), **extra_meta}
            rows.append(
                {
                    "src_type": source_type,
                    "src_id": str(source_id),
                    "aff_id": str(affaire_id),
                    "contenu": node.get_content(),
                    "embedding": str(embedding),
                    "idx": idx,
                    "meta": json.dumps(meta),
                }
            )

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
    async def delete_document(cls, db: AsyncSession, document_id: UUID) -> int:
        """Supprime tous les chunks d'un document. Retourne le nombre supprimé."""
        result = await db.execute(
            text("DELETE FROM chunks WHERE document_id = :doc_id"),
            {"doc_id": str(document_id)},
        )
        await db.commit()
        deleted = result.rowcount
        log.info("rag.delete_document", document_id=str(document_id), chunks_deleted=deleted)
        return deleted

    @classmethod
    async def delete_source(cls, db: AsyncSession, source_type: str, source_id: UUID) -> int:
        """Supprime tous les chunks d'une source générique. Retourne le nombre supprimé."""
        result = await db.execute(
            text("DELETE FROM chunks WHERE source_type = :st AND source_id = :sid"),
            {"st": source_type, "sid": str(source_id)},
        )
        await db.commit()
        deleted = result.rowcount
        log.info("rag.delete_source", source_type=source_type, source_id=str(source_id), chunks_deleted=deleted)
        return deleted
