"""
Embedding model — singleton lazy-loaded.

Supporte Ollama (via l'API OpenAI-compat) et OpenAI.
Le modèle est initialisé au premier appel et réutilisé pour tout le process.
"""

from core.settings import settings

_embed_model = None


def get_embed_model():
    global _embed_model
    if _embed_model is None:
        from llama_index.embeddings.openai import OpenAIEmbedding

        if settings.EMBEDDING_PROVIDER == "ollama":
            _embed_model = OpenAIEmbedding(
                model=settings.OLLAMA_EMBEDDING_MODEL,
                api_base=f"{settings.OLLAMA_BASE_URL}/v1",
                api_key="ollama",
                embed_batch_size=10,
            )
        else:
            _embed_model = OpenAIEmbedding(
                model=settings.effective_embedding_model,
                api_key=settings.OPENAI_API_KEY,
            )
    return _embed_model


async def embed(text_input: str) -> list[float]:
    """Génère un vecteur d'embedding pour un texte."""
    return await get_embed_model().aget_text_embedding(text_input)
