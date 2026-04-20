"""
Rate limiting via slowapi.
Décorer les endpoints LLM avec @limiter.limit(settings.RATE_LIMIT_LLM).

Usage :
    from core.rate_limit import limiter
    from fastapi import Request

    @router.post("/analyse")
    @limiter.limit("10/minute")
    async def analyse(request: Request, ...):
        ...
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from core.settings import settings

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMIT_STANDARD],
)
