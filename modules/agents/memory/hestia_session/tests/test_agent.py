from modules.agents.memory.hestia_session.agent import Hestia


def test_identity():
    assert Hestia.agent == "@Hestia"
    assert Hestia.role == "session_memory"
    assert Hestia.layer == "memory"


def test_soul_method():
    assert isinstance(Hestia.soul(), str)
