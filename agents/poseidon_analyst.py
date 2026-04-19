from pathlib import Path
from core._base import AgentBase

class PoseidonAnalyst(AgentBase):
    agent = "POSEIDON"; role = "cascade_analyst"; layer = "analysis"; veto = False
    triggers = ["C4", "C5"]
    _soul_dir = Path(__file__).parent / "poseidon"
