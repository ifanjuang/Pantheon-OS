from agents.analysis.demeter_collector.agent import Demeter


def test_identity():
    assert Demeter.agent == "@Demeter"
    assert Demeter.role == "collector"
    assert Demeter.layer == "analysis"


def test_soul_method():
    assert isinstance(Demeter.soul(), str)
