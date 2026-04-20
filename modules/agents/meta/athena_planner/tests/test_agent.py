"""Unit tests for Athena."""
from modules.agents.meta.athena_planner.agent import Athena


def test_identity():
    assert Athena.agent == "@ATHENA"
    assert Athena.role == "planner"
    assert Athena.layer == "meta"


def test_soul_method():
    soul = Athena.soul()
    assert isinstance(soul, str)
