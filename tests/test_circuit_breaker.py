"""
Tests circuit breaker — pattern disjoncteur pour LLM local (Ollama).
Tests unitaires purs, pas de dépendance externe.
"""

import time
import pytest
from core.circuit_breaker import CircuitBreaker, CircuitOpenError


class TestCircuitBreakerClosed:
    def test_initial_state_is_closed(self):
        cb = CircuitBreaker("test", failure_threshold=3, recovery_timeout=10)
        assert cb.state == "closed"

    def test_check_passes_when_closed(self):
        cb = CircuitBreaker("test", failure_threshold=3, recovery_timeout=10)
        cb.check()  # ne doit pas lever d'exception

    def test_success_resets_failure_count(self):
        cb = CircuitBreaker("test", failure_threshold=3, recovery_timeout=10)
        cb.record_failure()
        cb.record_failure()
        assert cb._failures == 2
        cb.record_success()
        assert cb._failures == 0
        assert cb.state == "closed"


class TestCircuitBreakerOpen:
    def test_opens_after_threshold(self):
        cb = CircuitBreaker("test", failure_threshold=3, recovery_timeout=10)
        for _ in range(3):
            cb.record_failure()
        assert cb.state == "open"

    def test_check_raises_when_open(self):
        cb = CircuitBreaker("test", failure_threshold=3, recovery_timeout=10)
        for _ in range(3):
            cb.record_failure()
        with pytest.raises(CircuitOpenError):
            cb.check()

    def test_error_message_contains_name(self):
        cb = CircuitBreaker("ollama_llm", failure_threshold=2, recovery_timeout=10)
        cb.record_failure()
        cb.record_failure()
        with pytest.raises(CircuitOpenError, match="ollama_llm"):
            cb.check()


class TestCircuitBreakerHalfOpen:
    def test_transitions_to_half_open_after_recovery(self):
        cb = CircuitBreaker("test", failure_threshold=2, recovery_timeout=0.1)
        cb.record_failure()
        cb.record_failure()
        assert cb.state == "open"
        time.sleep(0.15)
        assert cb.state == "half_open"

    def test_half_open_allows_one_check(self):
        cb = CircuitBreaker("test", failure_threshold=2, recovery_timeout=0.1)
        cb.record_failure()
        cb.record_failure()
        time.sleep(0.15)
        cb.check()  # ne doit pas lever

    def test_success_in_half_open_closes(self):
        cb = CircuitBreaker("test", failure_threshold=2, recovery_timeout=0.1)
        cb.record_failure()
        cb.record_failure()
        time.sleep(0.15)
        assert cb.state == "half_open"
        cb.record_success()
        assert cb.state == "closed"
        assert cb._failures == 0

    def test_failure_in_half_open_reopens(self):
        cb = CircuitBreaker("test", failure_threshold=2, recovery_timeout=0.1)
        cb.record_failure()
        cb.record_failure()
        time.sleep(0.15)
        assert cb.state == "half_open"
        cb.record_failure()
        assert cb.state == "open"


class TestCircuitBreakerGlobalInstances:
    def test_llm_breaker_exists(self):
        from core.circuit_breaker import llm_breaker

        assert llm_breaker.name == "llm"
        assert llm_breaker.failure_threshold == 5

    def test_embed_breaker_exists(self):
        from core.circuit_breaker import embed_breaker

        assert embed_breaker.name == "embed"
        assert embed_breaker.failure_threshold == 3
