from agents.memory.mnemosyne_agency.agent import Mnemosyne


def test_identity():
    assert Mnemosyne.agent == "@Mnemosyne"
    assert Mnemosyne.role == "agency_memory"
    assert Mnemosyne.layer == "memory"


def test_soul_method():
    assert isinstance(Mnemosyne.soul(), str)
