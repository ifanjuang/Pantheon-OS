from agents.analysis.hecate_uncertainty.agent import Hecate


def test_identity():
    assert Hecate.agent == "@Hecate"
    assert Hecate.role == "uncertainty_resolver"
    assert Hecate.layer == "analysis"


def test_soul_method():
    assert isinstance(Hecate.soul(), str)
