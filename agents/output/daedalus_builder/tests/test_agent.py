from agents.output.daedalus_builder.agent import Daedalus


def test_identity():
    assert Daedalus.agent == "@Daedalus"
    assert Daedalus.role == "builder"
    assert Daedalus.layer == "output"


def test_soul_method():
    assert isinstance(Daedalus.soul(), str)
