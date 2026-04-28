"""Unit tests for Chronos."""
from agents.meta.chronos_scheduler.agent import Chronos


def test_identity():
    assert Chronos.agent == "@Chronos"
    assert Chronos.role == "scheduler"
    assert Chronos.layer == "meta"


def test_soul_method():
    soul = Chronos.soul()
    assert isinstance(soul, str)
