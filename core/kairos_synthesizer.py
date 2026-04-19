from pathlib import Path
from ._base import AgentBase


class KairosSynthesizer(AgentBase):
    agent = "KAIROS"
    role = "synthesizer"
    layer = "meta"
    veto = False
    triggers = ["C1", "C2", "C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "kairos"
