"""Approval Gate service layer."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.approvals.models import ApprovalRequest
from apps.approvals.schemas import ApprovalCreate, ApprovalDecision


async def create_approval_request(db: AsyncSession, payload: ApprovalCreate) -> ApprovalRequest:
    approval = ApprovalRequest(**payload.model_dump())
    db.add(approval)
    await db.flush()
    await db.refresh(approval)
    return approval


async def get_approval_request(db: AsyncSession, approval_id: UUID) -> ApprovalRequest | None:
    return await db.get(ApprovalRequest, approval_id)


async def list_approval_requests(
    db: AsyncSession,
    *,
    status: str | None = None,
    limit: int = 50,
) -> list[ApprovalRequest]:
    stmt = select(ApprovalRequest).order_by(ApprovalRequest.created_at.desc()).limit(limit)
    if status:
        stmt = stmt.where(ApprovalRequest.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def decide_approval_request(
    db: AsyncSession,
    *,
    approval_id: UUID,
    decision: ApprovalDecision,
    decided_by: str,
    decision_note: str | None = None,
) -> ApprovalRequest | None:
    """Approve or reject a request if it is still decidable.

    The update is guarded by status IN (pending, escalated), which prevents
    double decisions from overwriting an already resolved approval.
    """
    now = datetime.now(timezone.utc)
    stmt = (
        update(ApprovalRequest)
        .where(ApprovalRequest.id == approval_id)
        .where(ApprovalRequest.status.in_(["pending", "escalated"]))
        .values(
            status=decision.value,
            decided_by=decided_by,
            decision_note=decision_note,
            decided_at=now,
        )
        .returning(ApprovalRequest)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def expire_approval_request(db: AsyncSession, *, approval_id: UUID) -> ApprovalRequest | None:
    now = datetime.now(timezone.utc)
    stmt = (
        update(ApprovalRequest)
        .where(ApprovalRequest.id == approval_id)
        .where(ApprovalRequest.status.in_(["pending", "escalated"]))
        .values(status="expired", decided_at=now)
        .returning(ApprovalRequest)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def escalate_approval_request(db: AsyncSession, *, approval_id: UUID) -> ApprovalRequest | None:
    stmt = (
        update(ApprovalRequest)
        .where(ApprovalRequest.id == approval_id)
        .where(ApprovalRequest.status == "pending")
        .values(status="escalated")
        .returning(ApprovalRequest)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()
