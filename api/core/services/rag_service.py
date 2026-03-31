"""
RagService — pipeline RAG via LlamaIndex (§1b).
- ingest()        : chunking + embedding + stockage pgvector
- search()        : recherche sémantique cosine avec cache (§23.6)
- embed()         : embedding d'un texte
- delete_source() : supprime les chunks d'une source
"""
import time
from pathlib import Path
from typing import Optional
from uuid import UUID

from core.settings import settings
from core.logging import get_logger

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

# Seuil cache sémantique (§23.6)
CACHE_SIMILARITY_THRESHOLD = 0.90


class RagService:
    """
    Toutes les méthodes sont des classmethods — pas d'instance à instancier.
    LlamaIndex est initialisé en lazy loading au premier appel.
    """
    _vector_store = None
    _embed_model = None

    @classmethod
    def _get_embed_model(cls):
        if cls._embed_model is None:
            from llama_index.embeddings.openai import OpenAIEmbedding

            if settings.EMBEDDING_PROVIDER == "ollama":
                from llama_index.embeddings.openai import OpenAIEmbedding
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
    def _get_vector_store(cls):
        if cls._vector_store is None:
            from llama_index.vector_stores.postgres import PGVectorStore
            cls._vector_store = PGVectorStore.from_params(
                database="arceus",
                host=settings.DATABASE_URL_SYNC.split("@")[-1].split("/")[0].split(":")[0],
                password=settings.DATABASE_URL_SYNC.split(":")[2].split("@")[0],
                port=5432,
                user="arceus",
                table_name="notion_chunks",
                embed_dim=settings.EMBEDDING_DIM,
            )
        return cls._vector_store

    @classmethod
    async def embed(cls, text: str) -> list[float]:
        """Génère un vecteur d'embedding pour un texte."""
        embed_model = cls._get_embed_model()
        result = await embed_model.aget_text_embedding(text)
        return result

    @classmethod
    async def ingest(
        cls,
        file_path: str,
        source_type: str,
        affaire_id: UUID,
        metadata: dict,
    ) -> list[str]:
        """
        Ingère un fichier : lecture → chunking → embedding → stockage pgvector.
        Retourne les IDs des chunks créés.
        """
        from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
        from llama_index.core.node_parser import SentenceSplitter

        t0 = time.monotonic()
        chunk_cfg = CHUNK_CONFIG.get(source_type, DEFAULT_CHUNK)

        reader = SimpleDirectoryReader(input_files=[file_path])
        documents = reader.load_data()

        # Enrichir les métadonnées
        for doc in documents:
            doc.metadata.update({
                "affaire_id": str(affaire_id),
                "source_type": source_type,
                **metadata,
            })

        splitter = SentenceSplitter(
            chunk_size=chunk_cfg["chunk_size"],
            chunk_overlap=chunk_cfg["chunk_overlap"],
        )

        storage_context = StorageContext.from_defaults(vector_store=cls._get_vector_store())
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            transformations=[splitter],
            embed_model=cls._get_embed_model(),
            show_progress=False,
        )

        node_ids = [node.node_id for node in splitter.get_nodes_from_documents(documents)]
        log.info("rag.ingest", affaire_id=str(affaire_id), source_type=source_type,
                 chunks=len(node_ids), duration_ms=int((time.monotonic() - t0) * 1000))
        return node_ids

    @classmethod
    async def search(
        cls,
        query: str,
        affaire_id: UUID,
        top_k: int = 5,
        source_type: Optional[str] = None,
    ) -> list[dict]:
        """
        Recherche sémantique. Vérifie le cache avant d'appeler LlamaIndex.
        Retourne [{text, score, metadata}]
        """
        from llama_index.core import VectorStoreIndex, StorageContext

        t0 = time.monotonic()
        query_emb = await cls.embed(query)

        # Vérifier le cache sémantique (§23.6) — implémenté dans le module rag
        # (le cache nécessite une session DB, délégué au router du module rag)

        storage_context = StorageContext.from_defaults(vector_store=cls._get_vector_store())
        index = VectorStoreIndex.from_vector_store(
            cls._get_vector_store(),
            embed_model=cls._get_embed_model(),
        )

        filters_dict = {"affaire_id": str(affaire_id)}
        if source_type:
            filters_dict["source_type"] = source_type

        from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter
        filters = MetadataFilters(filters=[
            ExactMatchFilter(key=k, value=v) for k, v in filters_dict.items()
        ])

        retriever = index.as_retriever(similarity_top_k=top_k, filters=filters)
        nodes = await retriever.aretrieve(query)

        results = [
            {
                "text": node.text,
                "score": node.score,
                "metadata": node.metadata,
            }
            for node in nodes
        ]

        log.info("rag.search", affaire_id=str(affaire_id), query=query[:60],
                 hits=len(results), duration_ms=int((time.monotonic() - t0) * 1000))
        return results

    @classmethod
    async def delete_source(cls, affaire_id: UUID, source_ref: str) -> None:
        """Supprime tous les chunks liés à une source."""
        # LlamaIndex PGVectorStore supporte la suppression par métadonnée
        cls._get_vector_store().delete(
            ref_doc_id=source_ref,
        )
        log.info("rag.delete_source", affaire_id=str(affaire_id), source_ref=source_ref)
