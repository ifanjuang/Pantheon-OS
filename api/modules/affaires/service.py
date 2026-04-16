from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from modules.affaires.models import Affaire


async def get_affaire(db: AsyncSession, affaire_id: UUID) -> Affaire | None:
    return await db.get(Affaire, affaire_id)


async def get_affaire_by_code(db: AsyncSession, code: str) -> Affaire | None:
    result = await db.execute(select(Affaire).where(Affaire.code == code))
    return result.scalar_one_or_none()


async def list_affaires(
    db: AsyncSession,
    statut: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Affaire]:
    q = select(Affaire).order_by(Affaire.created_at.desc()).limit(limit).offset(offset)
    if statut:
        q = q.where(Affaire.statut == statut)
    result = await db.execute(q)
    return result.scalars().all()


async def create_affaire(
    db: AsyncSession,
    code: str,
    nom: str,
    description: str | None,
    statut: str,
    created_by: UUID | None,
    **context_fields,
) -> Affaire:
    affaire = Affaire(
        code=code,
        nom=nom,
        description=description,
        statut=statut,
        created_by=created_by,
        **{k: v for k, v in context_fields.items() if v is not None},
    )
    db.add(affaire)
    await db.flush()
    return affaire


async def update_affaire(
    db: AsyncSession,
    affaire: Affaire,
    data: dict,
) -> Affaire:
    for field, value in data.items():
        if value is not None:
            setattr(affaire, field, value)
    await db.flush()
    return affaire


async def delete_affaire(db: AsyncSession, affaire: Affaire) -> None:
    await db.delete(affaire)
