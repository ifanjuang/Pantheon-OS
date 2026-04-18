"""
Service auth — hash, vérification, création utilisateur, seed admin.
"""

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.settings import settings
from modules.auth.models import User

log = get_logger("auth.service")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


async def create_user(
    db: AsyncSession,
    email: str,
    password: str,
    full_name: str = "",
    role: str = "lecteur",
) -> User:
    user = User(
        email=email,
        hashed_password=hash_password(password),
        full_name=full_name,
        role=role,
    )
    db.add(user)
    await db.flush()
    return user


async def seed_admin(db: AsyncSession) -> None:
    """Crée l'utilisateur admin par défaut s'il n'existe pas encore."""
    existing = await get_user_by_email(db, settings.ADMIN_EMAIL)
    if existing:
        return
    await create_user(
        db,
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
        full_name="Administrateur",
        role="admin",
    )
    await db.commit()
    log.info("auth.admin_seeded", email=settings.ADMIN_EMAIL)
