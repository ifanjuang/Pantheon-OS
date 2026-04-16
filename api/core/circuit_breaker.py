"""
Circuit breaker pour appels LLM (Ollama/OpenAI).

Empêche les appels répétés à un service down — fail-fast au lieu de timeout 90s par appel.
Essentiel en local avec Ollama qui peut crasher ou saturer.

États :
  CLOSED     → tout passe normalement
  OPEN       → échecs consécutifs atteints, tous les appels échouent immédiatement
  HALF_OPEN  → cooldown expiré, un seul appel de test autorisé

Deux classes disponibles :

  CircuitBreaker      — in-process uniquement (adapté mono-worker)
  RedisCircuitBreaker — état partagé via Redis (C4 — multi-process API + ARQ worker)
    • record_failure/success → fire-and-forget write Redis (non-bloquant)
    • state property → rafraîchit depuis Redis en arrière-plan toutes les
      _REFRESH_INTERVAL secondes ; in-process si Redis down
    • Utilise le client Redis de FunctionalMemoryService (singleton partagé)

Usage :
    from core.circuit_breaker import llm_breaker

    async def my_llm_call():
        llm_breaker.check()  # lève CircuitOpenError si ouvert
        try:
            result = await llm_client.create(...)
            llm_breaker.record_success()
            return result
        except Exception as e:
            llm_breaker.record_failure()
            raise
"""
import asyncio
import time
from core.logging import get_logger

log = get_logger("circuit_breaker")


class CircuitOpenError(Exception):
    """Le circuit est ouvert — service LLM indisponible."""

    def __init__(self, service: str, retry_after: float):
        self.service = service
        self.retry_after = retry_after
        super().__init__(
            f"Circuit ouvert pour {service} — réessayer dans {retry_after:.0f}s"
        )


class CircuitBreaker:
    """Circuit breaker in-process (sans Redis — adapté au mode local/single-worker)."""

    def __init__(
        self,
        name: str = "llm",
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        # State
        self._failures: int = 0
        self._last_failure_time: float = 0.0
        self._state: str = "closed"  # closed | open | half_open

    @property
    def state(self) -> str:
        if self._state == "open":
            elapsed = time.monotonic() - self._last_failure_time
            if elapsed >= self.recovery_timeout:
                self._state = "half_open"
        return self._state

    def check(self) -> None:
        """Vérifie si un appel est autorisé. Lève CircuitOpenError si non."""
        current = self.state
        if current == "open":
            retry_after = self.recovery_timeout - (time.monotonic() - self._last_failure_time)
            raise CircuitOpenError(self.name, max(0, retry_after))
        # half_open et closed : laisser passer

    def record_success(self) -> None:
        """Un appel a réussi — fermer le circuit."""
        if self._state in ("half_open", "open"):
            log.info("circuit_breaker.recovered", service=self.name, prior_failures=self._failures)
        self._failures = 0
        self._state = "closed"

    def record_failure(self) -> None:
        """Un appel a échoué — incrémenter ou ouvrir."""
        self._failures += 1
        self._last_failure_time = time.monotonic()
        if self._failures >= self.failure_threshold:
            if self._state != "open":
                log.warning(
                    "circuit_breaker.opened",
                    service=self.name,
                    failures=self._failures,
                    recovery_timeout=self.recovery_timeout,
                )
            self._state = "open"

    def reset(self) -> None:
        """Reset manuel (utile en test)."""
        self._failures = 0
        self._state = "closed"
        self._last_failure_time = 0.0


class RedisCircuitBreaker(CircuitBreaker):
    """Circuit breaker avec synchronisation Redis — partage d'état multi-process.

    L'état in-process reste la source de vérité pour `check()` (0 latence réseau).
    Redis est utilisé pour propager les changements d'état vers les autres workers :
      - record_failure/success() → fire-and-forget write Redis (via create_task)
      - state property → planifie un refresh en arrière-plan toutes les
        _REFRESH_INTERVAL s ; ne jamais bloquer le hot path

    Le refresh ne met à jour l'état in-process que si Redis indique un état
    plus dégradé (évite d'effacer une recovery locale prématurément).

    Fallback silencieux si Redis est down — se comporte comme CircuitBreaker.
    """

    _REFRESH_INTERVAL = 5.0     # secondes entre deux lectures Redis
    _REDIS_KEY_PREFIX  = "circuit"

    def __init__(self, name: str, failure_threshold: int = 5,
                 recovery_timeout: float = 30.0):
        super().__init__(name, failure_threshold, recovery_timeout)
        self._last_redis_refresh: float = 0.0
        self._redis_refresh_pending: bool = False

    def _redis_key(self) -> str:
        return f"{self._REDIS_KEY_PREFIX}:{self.name}"

    # ── state : planifie un refresh non-bloquant ──────────────────────

    @property
    def state(self) -> str:
        now = time.monotonic()
        if (now - self._last_redis_refresh > self._REFRESH_INTERVAL
                and not self._redis_refresh_pending):
            self._redis_refresh_pending = True
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self._refresh_from_redis())
            except RuntimeError:
                # Pas de boucle en cours (tests sync) — skip
                self._redis_refresh_pending = False
        return super().state

    # ── record_failure / record_success : write fire-and-forget ──────

    def record_failure(self) -> None:
        super().record_failure()
        self._schedule_write()

    def record_success(self) -> None:
        super().record_success()
        self._schedule_write()

    def _schedule_write(self) -> None:
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._write_to_redis())
        except RuntimeError:
            pass  # contexte sync — Redis write ignoré

    # ── Redis I/O ─────────────────────────────────────────────────────

    async def _refresh_from_redis(self) -> None:
        """Lit l'état Redis et met à jour in-process si Redis est plus dégradé."""
        try:
            from modules.memory.service import FunctionalMemoryService
            redis = await FunctionalMemoryService._get_client()
            if redis is None:
                return
            data = await redis.hgetall(self._redis_key())
            if not data:
                return
            r_failures = int(data.get("failures", 0))
            r_state    = data.get("state", "closed")
            r_last     = float(data.get("last_failure", 0.0))

            # Ne mettre à jour que si Redis signale un état PLUS dégradé
            if r_failures > self._failures:
                self._failures = r_failures
                self._last_failure_time = max(self._last_failure_time, r_last)
            if r_state == "open" and self._state == "closed":
                self._state = "open"
                self._last_failure_time = max(self._last_failure_time, r_last)
                log.warning(
                    "circuit_breaker.synced_open",
                    service=self.name,
                    source="redis",
                )
        except Exception as exc:
            log.debug("circuit_breaker.redis_refresh_failed", service=self.name, error=str(exc))
        finally:
            self._last_redis_refresh = time.monotonic()
            self._redis_refresh_pending = False

    async def _write_to_redis(self) -> None:
        """Persiste l'état courant dans Redis (TTL = recovery_timeout × 4)."""
        try:
            from modules.memory.service import FunctionalMemoryService
            redis = await FunctionalMemoryService._get_client()
            if redis is None:
                return
            ttl = int(self.recovery_timeout * 4)
            pipe = redis.pipeline()
            pipe.hset(self._redis_key(), mapping={
                "state":        self._state,
                "failures":     self._failures,
                "last_failure": self._last_failure_time,
            })
            pipe.expire(self._redis_key(), ttl)
            await pipe.execute()
            log.debug(
                "circuit_breaker.redis_written",
                service=self.name,
                state=self._state,
                failures=self._failures,
            )
        except Exception as exc:
            log.debug("circuit_breaker.redis_write_failed", service=self.name, error=str(exc))


# ── Instances globales ──────────────────────────────────────────────

# LLM principal (Ollama en local, OpenAI en cloud)
llm_breaker = RedisCircuitBreaker(name="llm", failure_threshold=5, recovery_timeout=30.0)

# Embedding (peut être un service séparé)
embed_breaker = RedisCircuitBreaker(name="embed", failure_threshold=3, recovery_timeout=20.0)
