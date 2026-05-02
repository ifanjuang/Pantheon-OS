"""Router approvals.

POST /approvals              → create approval request
GET  /approvals              → list approval requests
GET  /approvals/{id}         → read one approval request
POST /approvals/{id}/decide  → approve or reject
POST /approvals/{id}/expire  → expire pending/escalated request
POST /approvals/{id}/escalate→ escalate pending request
"""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.approvals.schemas import ApprovalCreate, ApprovalDecisionRequest, ApprovalResponse
from apps.approvals.service import (
    create_approval_request,
    decide_approval_request,
    escalate_approval_request,
    expire_approval_request,
    get_approval_request,
    list_approval_requests,
)
from apps.auth.models import User
from core.auth import get_current_user, require_role
from core.logging import get_logger
from database import get_db

log = get_logger("approvals.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.post("", response_model=ApprovalResponse, status_code=status.HTTP_201_CREATED)
    async def create(
        payload: ApprovalCreate,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        approval = await create_approval_request(db, payload)
        await db.commit()
        await db.refresh(approval)
        log.info("approvals.created", id=str(approval.id), user=str(user.id), action_type=approval.action_type)
        return approval

    @router.get("", response_model=list[ApprovalResponse])
    async def list_requests(
        status_filter: str | None = Query(default=None, alias="status"),
        limit: int = Query(default=50, ge=1, le=200),
        db: AsyncSession = Depends(get_db),
        _user: User = Depends(get_current_user),
    ):
        return await list_approval_requests(db, status=status_filter, limit=limit)

    @router.get("/{approval_id}", response_model=ApprovalResponse)
    async def read(
        approval_id: UUID,
        db: AsyncSession = Depends(get_db),
        _user: User = Depends(get_current_user),
    ):
        approval = await get_approval_request(db, approval_id)
        if approval is None:
            raise HTTPException(status_code=404, detail="Approval request not found")
        return approval

    @router.post("/{approval_id}/decide", response_model=ApprovalResponse)
    async def decide(
        approval_id: UUID,
        payload: ApprovalDecisionRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        approval = await decide_approval_request(
            db,
            approval_id=approval_id,
            decision=payload.decision,
            decided_by=str(user.id),
            decision_note=payload.decision_note,
        )
        if approval is None:
            existing = await get_approval_request(db, approval_id)
            if existing is None:
                raise HTTPException(status_code=404, detail="Approval request not found")
            raise HTTPException(status_code=409, detail=f"Approval request already resolved: {existing.status}")

        await db.commit()
        await db.refresh(approval)
        log.info("approvals.decided", id=str(approval.id), status=approval.status, user=str(user.id))
        return approval

    @router.post("/{approval_id}/expire", response_model=ApprovalResponse)
    async def expire(
        approval_id: UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        approval = await expire_approval_request(db, approval_id=approval_id)
        if approval is None:
            existing = await get_approval_request(db, approval_id)
            if existing is None:
                raise HTTPException(status_code=404, detail="Approval request not found")
            raise HTTPException(
                status_code=409, detail=f"Approval request cannot expire from status: {existing.status}"
            )

        await db.commit()
        await db.refresh(approval)
        log.info("approvals.expired", id=str(approval.id))
        return approval

    @router.post("/{approval_id}/escalate", response_model=ApprovalResponse)
    async def escalate(
        approval_id: UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        approval = await escalate_approval_request(db, approval_id=approval_id)
        if approval is None:
            existing = await get_approval_request(db, approval_id)
            if existing is None:
                raise HTTPException(status_code=404, detail="Approval request not found")
            raise HTTPException(
                status_code=409, detail=f"Approval request cannot escalate from status: {existing.status}"
            )

        await db.commit()
        await db.refresh(approval)
        log.info("approvals.escalated", id=str(approval.id))
        return approval

    return router
