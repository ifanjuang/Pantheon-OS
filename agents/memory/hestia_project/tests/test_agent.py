from agents.memory.hestia_project.agent import Hestia


def test_identity():
    assert Hestia.agent == "@Hestia"
    assert Hestia.role == "project_memory"
    assert Hestia.layer == "memory"


def test_soul_method():
    assert isinstance(Hestia.soul(), str)
