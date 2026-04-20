from modules.agents.output.kairos_synthesizer.agent import Kairos


def test_identity():
    assert Kairos.agent == "@Kairos"
    assert Kairos.role == "synthesizer"
    assert Kairos.layer == "output"


def test_soul_method():
    assert isinstance(Kairos.soul(), str)
