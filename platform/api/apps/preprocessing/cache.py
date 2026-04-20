"""
Cache sémantique des prétraitements Hermès++ (O4).

Pour une même affaire, des questions proches (cosine similarity > 0.92
sur l'embedding nomic-embed-text) retournent le même PreprocessedInput
depuis Redis sans appel LLM.

Structure Redis :
  preprocess:sem:{affaire_id}  →  LIST de JSON {emb: [...], result: {...}}
  TTL : 3600 s (renouvelé à chaque écriture)
  MAX_ENTRIES : 20 entrées par affaire (FIFO, les plus vieilles droppées)

Gains :
  - 0 appel LLM sur cache hit (économie Instructor + 1-2 tokens/req)
  - Latence réduite de ~500-2000 ms → < 5 ms sur hit Redis local
  - Transparent : fallback silencieux si Redis down ou embed raté
"""

import json
import math
from typing import Optional

from core.logging import get_logger

log = get_logger("preprocessing.cache")

_NAMESPACE = "preprocess:sem"
_TTL = 3600  # secondes — aligne sur la mémoire fonctionnelle
_MAX_ENTRIES = 20  # max entrées par affaire (LIFO push + LTRIM)
_THRESHOLD = 0.92  # similarité cosine minimale pour un cache hit


def _cosine(a: list[float], b: list[float]) -> float:
    """Similarité cosine entre deux vecteurs de même dimension."""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


async def _get_redis():
    """Retourne le client Redis de FunctionalMemoryService (singleton partagé)."""
    from apps.memory.service import FunctionalMemoryService

    return await FunctionalMemoryService._get_client()


class SemanticPreprocessCache:
    @classmethod
    async def get(
        cls,
        affaire_id: str,
        embedding: list[float],
    ) -> Optional[dict]:
        """Cherche un PreprocessedInput.model_dump() similaire dans Redis.

        Retourne le dict résultat si un vecteur stocké a une similarité
        cosine ≥ _THRESHOLD avec l'embedding fourni. None sinon.
        """
        redis = await _get_redis()
        if redis is None:
            return None

        key = f"{_NAMESPACE}:{affaire_id}"
        try:
            entries_raw = await redis.lrange(key, 0, _MAX_ENTRIES - 1)
        except Exception as exc:
            log.debug("preprocess_cache.lrange_failed", error=str(exc))
            return None

        best_score = 0.0
        best_result = None

        for raw in entries_raw:
            try:
                entry = json.loads(raw)
                stored_emb = entry["emb"]
                sim = _cosine(embedding, stored_emb)
                if sim > best_score:
                    best_score = sim
                    best_result = entry["result"]
            except Exception:
                continue  # entrée corrompue — on ignore

        if best_score >= _THRESHOLD and best_result is not None:
            log.info(
                "preprocess_cache.hit",
                affaire_id=affaire_id,
                similarity=round(best_score, 4),
            )
            return best_result

        return None

    @classmethod
    async def set(
        cls,
        affaire_id: str,
        embedding: list[float],
        result: dict,
    ) -> None:
        """Stocke un résultat avec son embedding dans Redis.

        Push en tête de liste + LTRIM pour ne conserver que _MAX_ENTRIES.
        Renouvelle le TTL de la clé.
        """
        redis = await _get_redis()
        if redis is None:
            return

        key = f"{_NAMESPACE}:{affaire_id}"
        entry = json.dumps({"emb": embedding, "result": result}, ensure_ascii=False)

        try:
            pipe = redis.pipeline()
            pipe.lpush(key, entry)
            pipe.ltrim(key, 0, _MAX_ENTRIES - 1)
            pipe.expire(key, _TTL)
            await pipe.execute()
            log.debug("preprocess_cache.stored", affaire_id=affaire_id)
        except Exception as exc:
            log.debug("preprocess_cache.store_failed", error=str(exc))
