from modules.agents.analysis.metis_optimizer.agent import Metis


def test_identity():
    assert Metis.agent == "@Metis"
    assert Metis.role == "optimizer"
    assert Metis.layer == "analysis"


def test_soul_method():
    assert isinstance(Metis.soul(), str)
