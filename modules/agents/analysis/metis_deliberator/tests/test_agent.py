from modules.agents.analysis.metis_deliberator.agent import Metis


def test_identity():
    assert Metis.agent == "@Metis"
    assert Metis.role == "deliberator"
    assert Metis.layer == "analysis"


def test_soul_method():
    assert isinstance(Metis.soul(), str)
