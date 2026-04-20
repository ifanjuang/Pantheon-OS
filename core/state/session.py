"""SessionState — per-run in-memory state container."""
from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SessionState:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    thread_id: str = ""
    user_id: str = ""
    intent: str = ""
    workflow: str = ""
    agents_used: list[str] = field(default_factory=list)
    artifacts: dict = field(default_factory=dict)
    final_answer: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 0.0
    uncertainty_score: float = 0.0

    def add_artifact(self, key: str, value: object) -> None:
        self.artifacts[key] = value

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "thread_id": self.thread_id,
            "workflow": self.workflow,
            "agents_used": self.agents_used,
            "confidence": self.confidence,
        }
