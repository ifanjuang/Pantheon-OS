from pathlib import Path
from core._base import AgentBase

class PoseidonDistributor(AgentBase):
    agent = "POSEIDON"; role = "distributor"; layer = "system"; veto = False
    triggers = ["C4", "C5"]
    _soul_dir = Path(__file__).parent / "poseidon"
