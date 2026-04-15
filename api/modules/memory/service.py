"""
FunctionalMemoryService — mémoire de session Redis TTL.

Comble le chaînon manquant entre :
  - mémoire agence    (Mnémosyne, agent_memory scope='agence')
  - mémoire projet    (Hestia,    agent_memory scope='projet')
  - mémoire fonctionnelle (ici)  → Redis TTL, session uniquement

API :

  set_context(thread_id, key, value, ttl=3600)
    Écrit une entrée dans la session. TTL par défaut 1h.

  get_context(thread_id) → dict
    Lit toutes les entrées actives d'un thread (retourne {} si vide).

  delete_context(thread_id, key=None)
    Supprime une clé ou tout le thread.

  promote_to_project(thread_id, affaire_id, lesson, category, agent)
    Pousse une leçon extraite de la session vers agent_memory
    (scope='projet'). Utilisé par write_memories après une décision
    validée pour capitaliser le contexte session en mémoire projet.

Fallback : si Redis est inaccessible, les opérations sont no-op
(on ne bloque pas l'orchestration sur une mémoire volatile).
"""
import json
from typing import Any, Optional
from uuid import UUID

import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.settings import settings

log = get_logger("memory.functional")


_KEY_PREFIX = "memory:fn"
_THREAD_INDEX = "memory:fn:threads"  # set de tous les thread_ids actifs


class FunctionalMemoryService:

    _client: Optional[aioredis.Redis] = None

    # ── Connexion Redis (singleton lazy) ─────────────────────────────

    @classmethod
    async def _get_client(cls) -> Optional[aioredis.Redis]:
        if cls._client is None:
            try:
                cls._client = aioredis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                )
                await cls._client.ping()
            except Exception as exc:
                log.warning("memory.redis_unavailable", error=str(exc))
                cls._client = None
        return cls._client

    @classmethod
    async def close(cls) -> None:
        if cls._client is not None:
            try:
                await cls._client.aclose()
            except Exception:
                pass
            cls._client = None

    # ── Helpers clés ─────────────────────────────────────────────────

    @staticmethod
    def _thread_key(thread_id: str, key: str) -> str:
        return f"{_KEY_PREFIX}:{thread_id}:{key}"

    @staticmethod
    def _thread_pattern(thread_id: str) -> str:
        return f"{_KEY_PREFIX}:{thread_id}:*"

    # ── set_context ──────────────────────────────────────────────────

    @classmethod
    async def set_context(
        cls,
        thread_id: str,
        key: str,
        value: Any,
        ttl: int = 3600,
    ) -> bool:
        """Écrit une entrée. TTL par défaut 1h, max 24h.

        Retourne True si écrit, False si Redis indisponible.
        """
        client = await cls._get_client()
        if client is None:
            return False
        try:
            payload = json.dumps(value, ensure_ascii=False, default=str)
            await client.set(
                cls._thread_key(thread_id, key),
                payload,
                ex=max(1, min(ttl, 86400)),
            )
            # Index light pour debug/promotion (même TTL étendu)
            await client.sadd(_THREAD_INDEX, thread_id)
            log.debug("memory.set", thread_id=thread_id, key=key, ttl=ttl)
            return True
        except Exception as exc:
            log.warning("memory.set_failed", error=str(exc))
            return False

    # ── get_context ──────────────────────────────────────────────────

    @classmethod
    async def get_context(cls, thread_id: str) -> dict[str, Any]:
        """Lit toutes les entrées actives d'un thread."""
        client = await cls._get_client()
        if client is None:
            return {}
        try:
            keys = [k async for k in client.scan_iter(match=cls._thread_pattern(thread_id))]
            if not keys:
                return {}
            values = await client.mget(keys)
            context: dict[str, Any] = {}
            prefix_len = len(f"{_KEY_PREFIX}:{thread_id}:")
            for full_key, raw in zip(keys, values):
                if raw is None:
                    continue
                short = full_key[prefix_len:]
                try:
                    context[short] = json.loads(raw)
                except json.JSONDecodeError:
                    context[short] = raw
            return context
        except Exception as exc:
            log.warning("memory.get_failed", error=str(exc))
            return {}

    # ── delete_context ───────────────────────────────────────────────

    @classmethod
    async def delete_context(
        cls,
        thread_id: str,
        key: Optional[str] = None,
    ) -> int:
        """Supprime une clé (si spécifiée) ou tout le thread."""
        client = await cls._get_client()
        if client is None:
            return 0
        try:
            if key is not None:
                return await client.delete(cls._thread_key(thread_id, key))
            keys = [k async for k in client.scan_iter(match=cls._thread_pattern(thread_id))]
            if not keys:
                return 0
            deleted = await client.delete(*keys)
            await client.srem(_THREAD_INDEX, thread_id)
            return deleted
        except Exception as exc:
            log.warning("memory.delete_failed", error=str(exc))
            return 0

    # ── promote_to_project ───────────────────────────────────────────

    @classmethod
    async def promote_to_project(
        cls,
        db: AsyncSession,
        *,
        thread_id: str,
        affaire_id: UUID | str,
        lesson: str,
        category: str = "general",
        agent: str = "hermes",
    ) -> tuple[bool, Optional[str]]:
        """Promeut une leçon de la mémoire fonctionnelle → agent_memory.

        Retourne (promoted, memory_id). Ne consomme pas la mémoire
        fonctionnelle (laisse Redis expirer par TTL).
        """
        from modules.agent.models import AgentMemory

        try:
            aid = affaire_id if isinstance(affaire_id, UUID) else UUID(str(affaire_id))
            mem = AgentMemory(
                agent_name=agent,
                scope="projet",
                affaire_id=aid,
                category=category or "general",
                lesson=lesson.strip()[:4000],
            )
            db.add(mem)
            await db.flush()
            memory_id = str(mem.id)
            log.info(
                "memory.promoted",
                thread_id=thread_id,
                affaire_id=str(aid),
                memory_id=memory_id,
            )
            return True, memory_id
        except Exception as exc:
            log.warning("memory.promote_failed", error=str(exc))
            return False, None
