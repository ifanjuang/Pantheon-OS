from agents.output.iris_communicator.agent import Iris


def test_identity():
    assert Iris.agent == "@Iris"
    assert Iris.role == "communicator"
    assert Iris.layer == "output"


def test_soul_method():
    assert isinstance(Iris.soul(), str)
