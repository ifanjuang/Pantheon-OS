from agents.output.hephaestus_diagrams.agent import Hephaestus


def test_identity():
    assert Hephaestus.agent == "@Hephaestus"
    assert Hephaestus.role == "diagram_builder"
    assert Hephaestus.layer == "output"


def test_soul_method():
    assert isinstance(Hephaestus.soul(), str)
