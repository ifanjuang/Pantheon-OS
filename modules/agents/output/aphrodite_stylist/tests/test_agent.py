from modules.agents.output.aphrodite_stylist.agent import Aphrodite


def test_identity():
    assert Aphrodite.agent == "@Aphrodite"
    assert Aphrodite.role == "stylist"
    assert Aphrodite.layer == "output"


def test_soul_method():
    assert isinstance(Aphrodite.soul(), str)
