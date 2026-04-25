"""Approval Gate models."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

APPROVAL_STATUSES = ("pending", "approved", "rejected", "expired", "escalated", "cancelled")


def _now() -> datetime:
    return datetime.now(timezone.utc)


class ApprovalRequest(Base):
    """Human approval request for a sensitive runtime action."""

    __tablename__ = "approval_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    workflow_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    agent_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)

    action_type: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    action_description: Mapped[str] = mapped_column(Text, nullable=False)
    agent_reasoning: Mapped[str] = mapped_column(Text, nullable=False, default="")
    criticity: Mapped[str] = mapped_column(String(8), nullable=False, default="C3")
    reversibility: Mapped[str] = mapped_column(String(64), nullable=False, default="unknown")

    assignee: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    assignee_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    escalate_to: Mapped[str | None] = mapped_column(String(255), nullable=True)

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending", index=True)
    decided_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    decision_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now, index=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    timeout_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    def is_decidable(self) -> bool:
        return self.status in {"pending", "escalated"}
