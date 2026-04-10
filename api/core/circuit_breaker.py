"""
Circuit breaker pour appels LLM (Ollama/OpenAI).

Empêche les appels répétés à un service down — fail-fast au lieu de timeout 90s par appel.
Essentiel en local avec Ollama qui peut crasher ou saturer.

États :
  CLOSED     → tout passe normalement
  OPEN       → échecs consécutifs atteints, tous les appels échouent immédiatement
  HALF_OPEN  → cooldown expiré, un seul appel de test autorisé

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


# ── Instances globales ──────────────────────────────────────────────

# LLM principal (Ollama en local, OpenAI en cloud)
llm_breaker = CircuitBreaker(name="llm", failure_threshold=5, recovery_timeout=30.0)

# Embedding (peut être un service séparé)
embed_breaker = CircuitBreaker(name="embed", failure_threshold=3, recovery_timeout=20.0)
