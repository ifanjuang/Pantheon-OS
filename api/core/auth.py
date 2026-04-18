"""
Auth JWT — 4 rôles : admin | moe | collaborateur | lecteur
Dépendances FastAPI utilisables dans tous les routers.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import settings
from database import get_db

bearer = HTTPBearer()

ROLE_HIERARCHY = ["lecteur", "collaborateur", "moe", "admin"]


# ── Helpers JWT ──────────────────────────────────────────────────


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.JWT_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalide : {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# ── Dépendances FastAPI ──────────────────────────────────────────


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db),
):
    """Décode le JWT et retourne l'utilisateur. 401 si invalide ou expiré."""
    from modules.auth.models import User  # import tardif pour éviter les imports circulaires

    payload = decode_token(credentials.credentials)
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token sans sujet")

    user = await db.get(User, UUID(user_id))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable ou désactivé")
    return user


def require_role(*roles: str):
    """
    Dépendance : vérifie que l'utilisateur a l'un des rôles spécifiés.
    Usage : user = Depends(require_role("admin", "moe"))
    """

    async def checker(user=Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Rôle insuffisant. Requis : {roles}, actuel : {user.role}",
            )
        return user

    return checker


async def require_affaire_access(
    affaire_id: UUID,
    min_role: str = "lecteur",
    user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Vérifie l'accès à une affaire.
    Admin : accès total. Autres : rôle global ou override par affaire.
    """
    from modules.auth.models import AffairePermission  # import tardif

    if user.role == "admin":
        return user

    perm = await db.execute(
        select(AffairePermission).where(
            AffairePermission.user_id == user.id,
            AffairePermission.affaire_id == affaire_id,
        )
    )
    perm = perm.scalar_one_or_none()
    effective_role = perm.role_override if perm and perm.role_override else user.role

    if not _has_access(effective_role, min_role):
        raise HTTPException(status_code=403, detail="Accès refusé à cette affaire")
    return user


def _has_access(effective_role: str, min_role: str) -> bool:
    try:
        return ROLE_HIERARCHY.index(effective_role) >= ROLE_HIERARCHY.index(min_role)
    except ValueError:
        return False
