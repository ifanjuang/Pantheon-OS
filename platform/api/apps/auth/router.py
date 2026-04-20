"""
Router auth

POST /auth/login        → JWT (public)
POST /auth/register     → créer utilisateur (admin only)
GET  /auth/me           → profil courant
GET  /auth/users        → liste utilisateurs (admin only)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import create_access_token, get_current_user, require_role
from core.logging import get_logger
from database import get_db
from apps.auth.models import User
from apps.auth.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from apps.auth.service import authenticate_user, create_user, get_user_by_email

log = get_logger("auth.router")


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.post("/login", response_model=TokenResponse)
    async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
        user = await authenticate_user(db, payload.email, payload.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Identifiants invalides",
            )
        token = create_access_token({"sub": str(user.id), "role": user.role})
        log.info("auth.login", email=user.email)
        return TokenResponse(access_token=token)

    @router.post("/register", response_model=UserResponse, status_code=201)
    async def register(
        payload: RegisterRequest,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        if await get_user_by_email(db, payload.email):
            raise HTTPException(status_code=409, detail="Email déjà utilisé")
        user = await create_user(db, payload.email, payload.password, payload.full_name, payload.role)
        await db.commit()
        await db.refresh(user)
        log.info("auth.register", email=user.email, role=user.role)
        return user

    @router.get("/me", response_model=UserResponse)
    async def me(user: User = Depends(get_current_user)):
        return user

    @router.get("/users", response_model=list[UserResponse])
    async def list_users(
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin")),
    ):
        result = await db.execute(select(User).order_by(User.created_at))
        return result.scalars().all()

    return router
