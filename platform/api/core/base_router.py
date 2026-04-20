from abc import ABC
from fastapi import APIRouter


class BaseRouter(ABC):
    """Chaque module expose un router FastAPI via get_router(config)."""

    prefix: str = ""
    tags: list[str] = []

    def get_router(self) -> APIRouter:
        raise NotImplementedError
