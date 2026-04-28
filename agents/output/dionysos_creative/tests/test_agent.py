"""Unit tests for Dionysos."""
from agents.output.dionysos_creative.agent import Dionysos


def test_identity():
    assert Dionysos.agent == "@Dionysos"
    assert Dionysos.role == "creative"
    assert Dionysos.layer == "output"


def test_soul_method():
    soul = Dionysos.soul()
    assert isinstance(soul, str)
