"""Unit tests for Apollo."""
from agents.meta.apollo_validator.agent import Apollo


def test_identity():
    assert Apollo.agent == "@APOLLO"
    assert Apollo.role == "validator"
    assert Apollo.layer == "meta"


def test_soul_method():
    soul = Apollo.soul()
    assert isinstance(soul, str)
