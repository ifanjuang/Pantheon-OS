"""Unit tests for Hera."""
from agents.meta.hera_supervisor.agent import Hera


def test_identity():
    assert Hera.agent == "@HERA"
    assert Hera.role == "supervisor"
    assert Hera.layer == "meta"


def test_soul_method():
    soul = Hera.soul()
    assert isinstance(soul, str)
