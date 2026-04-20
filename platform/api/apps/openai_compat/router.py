"""
Couche de compatibilité OpenAI — permet à Open WebUI de se connecter à ARCEUS.

Routes exposées sous /v1 (prefix du manifest) :
  GET  /v1/models                  → liste des affaires comme "modèles"
  POST /v1/chat/completions        → RAG sur l'affaire choisie + réponse LLM streamée

Fonctionnement :
  - Open WebUI affiche chaque affaire dans le dropdown "modèle"
  - L'utilisateur sélectionne une affaire → toute la conversation est
    contextualisée par les documents de ce projet via RAG pgvector
  - La réponse est streamée en SSE (format OpenAI chunks)

Auth :
  - Open WebUI envoie JWT_SECRET_KEY comme Bearer token (cf. docker-compose)
  - La dépendance _check_api_key valide ce token
"""

import json
import time
import uuid
from typing import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.llm_service import LlmService
from core.services.rag_service import RagService
from core.settings import settings
from database import get_db
from apps.affaires.models import Affaire

log = get_logger("openai_compat")
bearer = HTTPBearer(auto_error=False)

# ── Schémas OpenAI ───────────────────────────────────────────────────────────


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str  # UUID de l'affaire ou "hermes-mvp"
    messages: list[ChatMessage]
    stream: bool = True
    temperature: float = 0.3
    max_tokens: int = 2048


# ── Auth interne ─────────────────────────────────────────────────────────────


async def _check_api_key(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
):
    """Valide le Bearer token envoyé par Open WebUI (= JWT_SECRET_KEY)."""
    if credentials and credentials.credentials == settings.JWT_SECRET_KEY:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API key invalide",
        headers={"WWW-Authenticate": "Bearer"},
    )


# ── Helpers streaming ────────────────────────────────────────────────────────


def _chunk(run_id: str, model_id: str, content: str) -> str:
    data = {
        "id": run_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model_id,
        "choices": [{"index": 0, "delta": {"content": content}, "finish_reason": None}],
    }
    return f"data: {json.dumps(data)}\n\n"


def _chunk_stop(run_id: str, model_id: str) -> str:
    data = {
        "id": run_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model_id,
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
    }
    return f"data: {json.dumps(data)}\n\n"


async def _stream_rag_response(
    affaire: Affaire,
    messages: list[ChatMessage],
    db: AsyncSession,
) -> AsyncIterator[str]:
    """
    Pipeline : dernière question → RAG search → LLM stream avec contexte injecté.
    """
    run_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    model_id = str(affaire.id)

    # Extraire la dernière question utilisateur pour la recherche RAG
    user_messages = [m for m in messages if m.role == "user"]
    query = user_messages[-1].content if user_messages else ""

    # RAG search — top 4 chunks les plus pertinents
    rag_results = []
    if query:
        try:
            rag_results = await RagService.search(
                db=db,
                query=query,
                affaire_id=affaire.id,
                top_k=4,
            )
        except Exception as e:
            log.warning("openai_compat.rag_failed", error=str(e))

    # Construire le contexte documentaire
    if rag_results:
        context_parts = []
        for i, r in enumerate(rag_results, 1):
            score_pct = int(r["score"] * 100)
            source = r["meta"].get("filename", "document")
            context_parts.append(f"[Source {i} — {source}, pertinence {score_pct}%]\n{r['contenu'][:600]}")
        context_block = "\n\n---\n\n".join(context_parts)
        context_section = f"\n\n## Extraits documentaires pertinents\n\n{context_block}"
    else:
        context_section = "\n\n(Aucun document trouvé pour cette question dans le projet.)"

    system_prompt = (
        f"Tu es le copilote du projet **{affaire.nom}** (code : {affaire.code}).\n"
        f"Statut du projet : {affaire.statut}.\n\n"
        "Tu aides le chargé de projet MOE à trouver des informations dans les documents "
        "du projet. Réponds en français, de manière concise et structurée. "
        "Cite toujours tes sources (numéro et nom du document). "
        "Ne spécule jamais sur des données chiffrées (délais, coûts, surfaces) "
        "si elles ne sont pas dans les extraits fournis."
        f"{context_section}"
    )

    # Construire les messages pour le LLM (historique complet + contexte)
    llm_messages = [{"role": "system", "content": system_prompt}]
    # Limiter l'historique aux 10 derniers échanges pour ne pas saturer le contexte
    for m in messages[-10:]:
        llm_messages.append({"role": m.role, "content": m.content})

    # Stream LLM
    try:
        stream = await LlmService._get_client().chat.completions.create(
            model=settings.effective_llm_model,
            messages=llm_messages,
            stream=True,
            temperature=0.3,
            max_tokens=2048,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield _chunk(run_id, model_id, delta.content)

    except Exception as e:
        log.error("openai_compat.llm_failed", error=str(e))
        yield _chunk(run_id, model_id, f"\n\n[Erreur LLM : {e}]")

    yield _chunk_stop(run_id, model_id)
    yield "data: [DONE]\n\n"


async def _full_rag_response(
    affaire: Affaire,
    messages: list[ChatMessage],
    db: AsyncSession,
) -> dict:
    """Version non-streamée (pour les clients qui ne supportent pas SSE)."""
    full_text = ""
    async for chunk in _stream_rag_response(affaire, messages, db):
        if chunk.startswith("data: {"):
            data = json.loads(chunk[6:])
            content = data["choices"][0]["delta"].get("content", "")
            full_text += content

    run_id = f"chatcmpl-{uuid.uuid4().hex[:12]}"
    return {
        "id": run_id,
        "object": "chat.completion",
        "created": int(time.time()),
        "model": str(affaire.id),
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": full_text},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }


# ── Router ───────────────────────────────────────────────────────────────────


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.get("/models")
    async def list_models(
        db: AsyncSession = Depends(get_db),
        _auth=Depends(_check_api_key),
    ):
        """
        Retourne les affaires actives comme modèles disponibles.
        Open WebUI les affiche dans le dropdown de sélection de modèle.
        """
        result = await db.execute(select(Affaire).where(Affaire.statut == "actif").order_by(Affaire.nom))
        affaires = result.scalars().all()

        models = [
            {
                "id": str(a.id),
                "object": "model",
                "created": int(a.created_at.timestamp()),
                "owned_by": "pantheon",
                "display_name": f"{a.nom} [{a.code}]",
            }
            for a in affaires
        ]

        # Modèle générique si aucune affaire
        if not models:
            models.append(
                {
                    "id": "hermes-mvp",
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "pantheon",
                    "display_name": "ARCEUS — Copilote MOE",
                }
            )

        return {"object": "list", "data": models}

    @router.post("/chat/completions")
    async def chat_completions(
        payload: ChatCompletionRequest,
        db: AsyncSession = Depends(get_db),
        _auth=Depends(_check_api_key),
    ):
        """
        Entrée principale Open WebUI.
        model = UUID affaire → RAG scopé sur les documents de ce projet.
        """
        # Résoudre l'affaire depuis le model ID
        affaire = None
        try:
            affaire_id = uuid.UUID(payload.model)
            affaire = await db.get(Affaire, affaire_id)
        except (ValueError, AttributeError):
            pass

        if affaire is None:
            # Fallback : affaire générique sans contexte documentaire
            affaire = Affaire(
                id=uuid.uuid4(),
                code="ARCEUS",
                nom="ARCEUS — Copilote MOE",
                statut="actif",
            )

        log.info(
            "openai_compat.chat",
            affaire=affaire.code,
            messages=len(payload.messages),
            stream=payload.stream,
        )

        if payload.stream:
            return StreamingResponse(
                _stream_rag_response(affaire, payload.messages, db),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                },
            )

        return await _full_rag_response(affaire, payload.messages, db)

    return router
