# V2 only — ARQ job queue. Requires redis.
"""
queue.py — pool Redis ARQ partagé (singleton lazy).

Usage :
  from core.queue import get_queue
  pool = await get_queue()
  await pool.enqueue_job("orchestra_job", ...)
"""

from arq.connections import ArqRedis, RedisSettings, create_pool as _create_pool

from core.settings import settings

_pool: ArqRedis | None = None


async def get_queue() -> ArqRedis:
    global _pool
    if _pool is None:
        _pool = await _create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
    return _pool


async def close_queue() -> None:
    global _pool
    if _pool is not None:
        await _pool.aclose()
        _pool = None
