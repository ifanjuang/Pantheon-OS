from agents.analysis.argos_extractor.agent import Argos


def test_identity():
    assert Argos.agent == "@Argos"
    assert Argos.role == "extractor"
    assert Argos.layer == "analysis"


def test_soul_method():
    assert isinstance(Argos.soul(), str)
