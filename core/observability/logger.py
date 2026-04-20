"""HermesLogger — structured run logging for agent steps."""
from __future__ import annotations
import logging

logger = logging.getLogger("hermes")


class HermesLogger:
    def agent_start(self, agent: str, step: str, session_id: str) -> None:
        logger.info("agent_start", extra={"agent": agent, "step": step, "session": session_id})

    def agent_end(self, agent: str, step: str, session_id: str, duration_ms: int) -> None:
        logger.info("agent_end", extra={"agent": agent, "step": step, "session": session_id, "ms": duration_ms})

    def workflow_start(self, workflow: str, session_id: str) -> None:
        logger.info("workflow_start", extra={"workflow": workflow, "session": session_id})

    def workflow_end(self, workflow: str, session_id: str, confidence: float) -> None:
        logger.info("workflow_end", extra={"workflow": workflow, "session": session_id, "confidence": confidence})
