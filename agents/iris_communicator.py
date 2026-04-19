from pathlib import Path
from core._base import AgentBase

class IrisCommunicator(AgentBase):
    agent = "IRIS"; role = "communicator"; layer = "communication"; veto = False
    triggers = ["C4", "C5"]
    _soul_dir = Path(__file__).parent / "iris"
