"""Unit tests for Themis."""
from modules.agents.meta.themis_guardian.agent import Themis


def test_identity():
    assert Themis.agent == "@THEMIS"
    assert Themis.role == "process_guardian"
    assert Themis.layer == "meta"


def test_soul_method():
    soul = Themis.soul()
    assert isinstance(soul, str)
