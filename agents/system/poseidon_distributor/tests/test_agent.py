from agents.system.poseidon_distributor.agent import Poseidon


def test_identity():
    assert Poseidon.agent == "@Poseidon"
    assert Poseidon.role == "distributor"
    assert Poseidon.layer == "system"


def test_soul_method():
    assert isinstance(Poseidon.soul(), str)
