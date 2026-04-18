"""
Bus inter-modules via PostgreSQL LISTEN/NOTIFY (§1b).
Découple les modules sans import croisé.

Usage :
    # S'abonner (dans le startup d'un module) :
    await events.subscribe("planning_channel", handler, pool)

    # Publier (depuis n'importe quel engine) :
    await events.publish("planning_channel", {"event_type": "retard", ...}, pool)

Channels standard :
    planning_channel      → lots validés, jalons dépassés, chemin critique changé
    budget_channel        → seuil atteint, situation déposée
    chantier_channel      → blocage ouvert, avancement mis à jour
    finance_channel       → dépassement budget, retard paiement
    meeting_channel       → action créée, décision extraite
    communication_channel → email urgent reçu
    notifications_channel → demande d'envoi de notification (→ module notifications)
    rag_channel           → document importé (→ module memory)
"""
import asyncpg
import json
from typing import Callable, Any
from collections import defaultdict
from core.logging import get_logger

log = get_logger("events")

_handlers: dict[str, list[Callable]] = defaultdict(list)
_pool: asyncpg.Pool | None = None
# Connexions dédiées aux listeners — conservées pour éviter les fuites de pool
_listener_conns: list[asyncpg.Connection] = []


async def init_pool(dsn: str) -> asyncpg.Pool:
    """Initialise le pool asyncpg partagé. Appelé dans main.py au startup."""
    global _pool
    _pool = await asyncpg.create_pool(dsn, min_size=2, max_size=5)
    log.info("events.pool_ready", dsn=dsn.split("@")[-1])
    return _pool


async def close_pool() -> None:
    global _pool
    # Fermer les connexions listeners dédiées
    for conn in _listener_conns:
        try:
            await conn.close()
        except Exception:
            pass
    _listener_conns.clear()
    if _pool:
        await _pool.close()
        _pool = None


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Event pool non initialisé — appeler events.init_pool() au startup")
    return _pool


async def subscribe(channel: str, handler: Callable, pool: asyncpg.Pool | None = None) -> None:
    """
    Abonne un handler à un channel PostgreSQL.
    handler(payload: dict) sera appelé à chaque NOTIFY.
    La connexion est conservée dans _listener_conns et libérée proprement dans close_pool().
    """
    pool = pool or get_pool()
    _handlers[channel].append(handler)
    conn = await pool.acquire()
    _listener_conns.append(conn)
    await conn.add_listener(channel, _dispatch)
    log.info("events.subscribed", channel=channel, handler=handler.__qualname__)


async def publish(channel: str, payload: dict, pool: asyncpg.Pool | None = None) -> None:
    """Envoie un NOTIFY sur un channel PostgreSQL."""
    pool = pool or get_pool()
    async with pool.acquire() as conn:
        await conn.execute("SELECT pg_notify($1, $2)", channel, json.dumps(payload))
    log.debug("events.published", channel=channel, event_type=payload.get("event_type"))


async def _dispatch(conn: asyncpg.Connection, pid: int, channel: str, payload_str: str) -> None:
    """Callback interne asyncpg — distribue le payload aux handlers abonnés."""
    try:
        payload = json.loads(payload_str)
    except json.JSONDecodeError:
        log.error("events.invalid_payload", channel=channel, raw=payload_str[:200])
        return

    handlers = _handlers.get(channel, [])
    for handler in handlers:
        try:
            await handler(payload)
        except Exception as e:
            log.error("events.handler_error", channel=channel, handler=handler.__qualname__, error=str(e))
