from agents.analysis.hermes_router.agent import Hermes


def test_identity():
    assert Hermes.agent == "@Hermes"
    assert Hermes.role == "router"
    assert Hermes.layer == "analysis"


def test_soul_method():
    assert isinstance(Hermes.soul(), str)
