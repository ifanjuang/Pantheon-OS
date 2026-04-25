from modules.agents.memory.hades_retrieval.agent import Hades


def test_identity():
    assert Hades.agent == "@Hades"
    assert Hades.role == "deep_retrieval"
    assert Hades.layer == "memory"


def test_soul_method():
    assert isinstance(Hades.soul(), str)
