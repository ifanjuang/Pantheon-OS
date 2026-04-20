"""
Pagination cursor-based (§23.8).
Plus stable que l'offset sur les listings avec insertions fréquentes.

Usage :
    from core.pagination import CursorPage, cursor_params

    @router.get("/", response_model=CursorPage[LotRead])
    async def list_lots(affaire_id: UUID, p: dict = Depends(cursor_params), db=Depends(get_db)):
        stmt = (
            select(PlanningLot)
            .where(PlanningLot.affaire_id == affaire_id, PlanningLot.deleted_at.is_(None))
            .order_by(PlanningLot.created_at.asc(), PlanningLot.id.asc())
            .limit(p["limit"] + 1)
        )
        if p["after"]:
            cursor_row = await db.get(PlanningLot, p["after"])
            if cursor_row:
                stmt = stmt.where(
                    (PlanningLot.created_at > cursor_row.created_at) |
                    ((PlanningLot.created_at == cursor_row.created_at) & (PlanningLot.id > p["after"]))
                )
        rows = (await db.execute(stmt)).scalars().all()
        has_more = len(rows) > p["limit"]
        return CursorPage(
            items=rows[:p["limit"]],
            next_cursor=str(rows[p["limit"] - 1].id) if has_more else None,
        )
"""

from typing import TypeVar, Generic, Optional
from pydantic import BaseModel
from fastapi import Query
from uuid import UUID

T = TypeVar("T")


class CursorPage(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: Optional[str] = None  # UUID du dernier item, None si dernière page


def cursor_params(
    after: Optional[UUID] = Query(default=None, description="Cursor : UUID du dernier item reçu"),
    limit: int = Query(default=50, ge=1, le=200, description="Nombre d'items par page"),
) -> dict:
    return {"after": after, "limit": limit}
