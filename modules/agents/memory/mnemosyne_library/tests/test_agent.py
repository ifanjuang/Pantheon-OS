from modules.agents.memory.mnemosyne_library.agent import Mnemosyne


def test_identity():
    assert Mnemosyne.agent == "@Mnemosyne"
    assert Mnemosyne.role == "knowledge_library"
    assert Mnemosyne.layer == "memory"


def test_soul_method():
    assert isinstance(Mnemosyne.soul(), str)
