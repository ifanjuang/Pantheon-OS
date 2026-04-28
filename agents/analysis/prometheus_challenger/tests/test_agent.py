from agents.analysis.prometheus_challenger.agent import Prometheus


def test_identity():
    assert Prometheus.agent == "@Prometheus"
    assert Prometheus.role == "challenger"
    assert Prometheus.layer == "analysis"


def test_soul_method():
    assert isinstance(Prometheus.soul(), str)
