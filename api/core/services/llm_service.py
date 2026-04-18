"""
LlmService — wrapper unifié Ollama / OpenAI via Instructor (§1b).
- chat()    : réponse texte libre
- extract() : extraction structurée Pydantic garantie (via Instructor, auto-retry)
- embed()   : vecteur d'embedding (délègue à RagService)
- ping()    : healthcheck
"""

import time
from typing import Any, Optional, Type, TypeVar
from pydantic import BaseModel

import instructor
from openai import AsyncOpenAI

from core.settings import settings
from core.logging import get_logger

log = get_logger("llm_service")
T = TypeVar("T", bound=BaseModel)


def _build_openai_client() -> AsyncOpenAI:
    """Construit le client OpenAI ou Ollama (compatible OpenAI API)."""
    if settings.LLM_PROVIDER == "ollama":
        return AsyncOpenAI(
            base_url=f"{settings.OLLAMA_BASE_URL}/v1",
            api_key="ollama",  # Ollama n'exige pas de clé
        )
    return AsyncOpenAI(
        base_url=settings.OPENAI_API_BASE_URL,
        api_key=settings.OPENAI_API_KEY or "no-key",
    )


class LlmService:
    _client: Optional[AsyncOpenAI] = None
    _instructor_client: Optional[Any] = None

    @classmethod
    def _get_client(cls) -> AsyncOpenAI:
        if cls._client is None:
            cls._client = _build_openai_client()
        return cls._client

    @classmethod
    def _get_instructor(cls) -> Any:
        if cls._instructor_client is None:
            cls._instructor_client = instructor.from_openai(cls._get_client())
        return cls._instructor_client

    @classmethod
    async def chat(
        cls,
        messages: list[dict],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Réponse texte libre. Protégé par circuit breaker."""
        from core.circuit_breaker import llm_breaker

        llm_breaker.check()  # fail-fast si Ollama est down

        t0 = time.monotonic()
        model = model or settings.effective_llm_model
        try:
            response = await cls._get_client().chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            llm_breaker.record_success()
        except Exception:
            llm_breaker.record_failure()
            raise

        content = response.choices[0].message.content or ""
        log.info(
            "llm.chat",
            model=model,
            tokens=response.usage.total_tokens if response.usage else 0,
            duration_ms=int((time.monotonic() - t0) * 1000),
        )
        return content

    @classmethod
    async def extract(
        cls,
        messages: list[dict],
        response_model: Type[T],
        model: Optional[str] = None,
        temperature: float = 0.1,
        max_retries: int = 3,
    ) -> T:
        """
        Extraction structurée Pydantic garantie via Instructor.
        Retry automatique si la sortie LLM ne valide pas le schema.
        """
        t0 = time.monotonic()
        model = model or settings.effective_llm_model
        result = await cls._get_instructor().chat.completions.create(
            model=model,
            messages=messages,
            response_model=response_model,
            temperature=temperature,
            max_retries=max_retries,
        )
        log.info(
            "llm.extract",
            model=model,
            response_model=response_model.__name__,
            duration_ms=int((time.monotonic() - t0) * 1000),
        )
        return result

    @classmethod
    async def embed(cls, text: str) -> list[float]:
        """Délègue à RagService pour cohérence des embeddings."""
        from core.services.rag_service import RagService

        return await RagService.embed(text)

    @classmethod
    async def ping(cls) -> bool:
        """Vérifie que le LLM est accessible. Réinitialise le circuit breaker si OK."""
        try:
            await cls._get_client().models.list()
            from core.circuit_breaker import llm_breaker

            llm_breaker.record_success()
            return True
        except Exception as e:
            log.warning("llm.ping_failed", error=str(e))
            return False
