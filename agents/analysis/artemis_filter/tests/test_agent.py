from agents.analysis.artemis_filter.agent import Artemis


def test_identity():
    assert Artemis.agent == "@Artemis"
    assert Artemis.role == "filter"
    assert Artemis.layer == "analysis"


def test_soul_method():
    assert isinstance(Artemis.soul(), str)
