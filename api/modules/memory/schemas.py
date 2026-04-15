"""
Schémas memory — mémoire fonctionnelle TTL (session).

La mémoire fonctionnelle (M3) comble le chaînon manquant entre :
  - la mémoire agence (Mnémosyne, scope='agence', permanente)
  - la mémoire projet (Hestia,   scope='projet',  durée affaire)
  - la mémoire fonctionnelle (Hermès, Chronos, session) ← ce module

Stockage : Redis TTL par défaut 1h (configurable par appel).
Clé      : memory:fn:{thread_id}:{key}

Usage typique : thread_id = checkpoint_thread_id LangGraph ou
session_id Telegram, persiste le cleaned_question, le dernier
preprocessed_input, la dernière réponse agent pour retrouver le
contexte sur N appels consécutifs.
"""
from typing import Any, Optional

from pydantic import BaseModel, Field


# ── Requête / réponse API ────────────────────────────────────────────

class MemoryEntry(BaseModel):
    """Une entrée de mémoire fonctionnelle."""
    key: str = Field(..., min_length=1, max_length=128)
    value: Any = Field(..., description="Valeur JSON-sérialisable")
    ttl: int = Field(3600, ge=1, le=86400, description="TTL en secondes (max 24h)")


class SetContextRequest(BaseModel):
    thread_id: str = Field(..., min_length=1, max_length=128)
    entries: list[MemoryEntry] = Field(..., min_length=1, max_length=32)


class GetContextResponse(BaseModel):
    thread_id: str
    context: dict[str, Any] = Field(default_factory=dict)
    keys_count: int = 0


class PromoteRequest(BaseModel):
    """Promotion du contexte fonctionnel → mémoire projet (Hestia)."""
    thread_id: str = Field(..., min_length=1, max_length=128)
    affaire_id: str = Field(..., description="UUID de l'affaire cible")
    lesson: str = Field(
        ..., min_length=3, max_length=4000,
        description="Leçon à écrire dans agent_memory scope=projet",
    )
    category: Optional[str] = Field(
        "general",
        description="technique | planning | budget | contractuel | general",
    )
    agent: str = Field(
        "hermes",
        description="Agent émetteur (par défaut hermes pour la fonctionnelle)",
    )


class PromoteResponse(BaseModel):
    promoted: bool
    memory_id: Optional[str] = None
    reason: str = ""
