"""Unit tests for Zeus."""
from modules.agents.meta.zeus_orchestrator.agent import Zeus


def test_identity():
    assert Zeus.agent == "@ZEUS"
    assert Zeus.role == "orchestrator"
    assert Zeus.layer == "meta"


def test_soul_method():
    soul = Zeus.soul()
    assert isinstance(soul, str)
