from modules.agents.system.ares_executor.agent import Ares


def test_identity():
    assert Ares.agent == "@Ares"
    assert Ares.role == "fast_executor"
    assert Ares.layer == "system"


def test_soul_method():
    assert isinstance(Ares.soul(), str)
