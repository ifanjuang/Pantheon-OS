"""
telegram.py — service bot Telegram pour ARCEUS.

Routing entrant :
  /start                   → message de bienvenue
  /affaire <code>          → lier ce chat à une affaire
  /agents                  → liste des agents disponibles
  /help                    → aide
  @<agent> <texte>         → déclencher un agent spécifique
  photo (+ légende)        → cascade Argos → Héphaïstos
  texte libre              → Hermès qualifie et route

Sécurité :
  TELEGRAM_ALLOWED_CHAT_IDS — seuls ces chat_id sont autorisés (vide = tous)
  X-Telegram-Bot-Api-Secret-Token — header envoyé par Telegram si WEBHOOK_SECRET défini
"""

import re
from uuid import UUID

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.settings import settings
from apps.affaires.models import Affaire
from apps.webhooks.models import WebhookSession

log = get_logger("webhooks.telegram")

# ── Agents disponibles pour @mention ────────────────────────────────────────
MENTIONABLE_AGENTS = {
    "hermes",
    "argos",
    "athena",
    "hephaistos",
    "promethee",
    "apollon",
    "dionysos",
    "themis",
    "chronos",
    "ares",
    "hestia",
    "mnemosyne",
    "iris",
    "aphrodite",
    "dedale",
    "zeus",
}

_MENTION_RE = re.compile(r"^@(\w+)\s*", re.IGNORECASE)

# ── Telegram Bot API ─────────────────────────────────────────────────────────


def _tg_url(method: str) -> str:
    return f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/{method}"


async def tg_send(chat_id: str | int, text: str, parse_mode: str = "Markdown") -> None:
    """Envoie un message Telegram. Silencieux en cas d'erreur réseau."""
    if not settings.TELEGRAM_TOKEN:
        log.warning("telegram.send_skipped", reason="TELEGRAM_TOKEN non configuré")
        return
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(
                _tg_url("sendMessage"),
                json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
            )
    except Exception as exc:
        log.error("telegram.send_failed", chat_id=str(chat_id), error=str(exc))


async def tg_send_typing(chat_id: str | int) -> None:
    """Envoie l'indicateur 'en train de taper...'."""
    if not settings.TELEGRAM_TOKEN:
        return
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            await client.post(
                _tg_url("sendChatAction"),
                json={"chat_id": chat_id, "action": "typing"},
            )
    except Exception:
        pass


async def tg_download_file(file_id: str) -> bytes | None:
    """Télécharge un fichier Telegram (photo, document) par file_id."""
    if not settings.TELEGRAM_TOKEN:
        return None
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # 1. Obtenir le file_path
            r = await client.get(_tg_url("getFile"), params={"file_id": file_id})
            r.raise_for_status()
            file_path = r.json()["result"]["file_path"]

            # 2. Télécharger
            url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_TOKEN}/{file_path}"
            r2 = await client.get(url)
            r2.raise_for_status()
            return r2.content
    except Exception as exc:
        log.error("telegram.download_failed", file_id=file_id, error=str(exc))
        return None


# ── Auth chat ────────────────────────────────────────────────────────────────


def is_chat_allowed(chat_id: str | int) -> bool:
    """Vérifie si le chat_id est autorisé (vide = tous autorisés)."""
    allowed_raw = getattr(settings, "TELEGRAM_ALLOWED_CHAT_IDS", "") or ""
    if not allowed_raw.strip():
        return True
    allowed = {c.strip() for c in allowed_raw.split(",") if c.strip()}
    return str(chat_id) in allowed


# ── Session ──────────────────────────────────────────────────────────────────


async def get_or_create_session(db: AsyncSession, chat_id: str) -> WebhookSession:
    """Retourne la session existante ou en crée une nouvelle."""
    result = await db.execute(
        select(WebhookSession).where(
            WebhookSession.platform == "telegram",
            WebhookSession.chat_id == chat_id,
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        session = WebhookSession(platform="telegram", chat_id=chat_id)
        db.add(session)
        await db.flush()
    return session


# ── Commandes ────────────────────────────────────────────────────────────────


async def handle_command(
    db: AsyncSession,
    chat_id: str,
    command: str,
    args: str,
) -> str:
    """Traite les commandes /start, /affaire, /agents, /help."""
    session = await get_or_create_session(db, chat_id)

    if command == "start":
        return (
            "👋 *Bienvenue sur ARCEUS*\n\n"
            "Je suis ton assistant MOE. Pour commencer :\n"
            "• `/affaire <code>` — lier ce chat à une affaire\n"
            "• `@agent <question>` — interroger un agent spécifique\n"
            "• Envoie une *photo* pour une analyse terrain\n"
            "• Texte libre → Hermès qualifie et route automatiquement\n\n"
            "Tape `/help` pour plus d'infos."
        )

    if command == "help":
        return (
            "*Commandes disponibles :*\n"
            "• `/affaire <code>` — définir l'affaire active\n"
            "• `/agents` — liste des agents\n\n"
            "*Mentions agents :*\n"
            "`@themis`, `@chronos`, `@hephaistos`, `@apollon`, `@zeus`...\n\n"
            "*Photos :*\n"
            "Envoie une photo (avec ou sans légende) → analyse Argos + Héphaïstos\n\n"
            "*Texte libre :*\n"
            "Hermès qualifie ta demande (C1-C5) et route vers le bon agent."
        )

    if command == "agents":
        agents_list = "\n".join(f"• `@{a}`" for a in sorted(MENTIONABLE_AGENTS))
        return f"*Agents disponibles :*\n{agents_list}"

    if command == "affaire":
        code = args.strip().upper()
        if not code:
            current = f"Affaire active : `{session.affaire_id}`" if session.affaire_id else "Aucune affaire définie."
            return f"{current}\n\nUtilise `/affaire <CODE>` pour en définir une."

        result = await db.execute(select(Affaire).where(Affaire.code == code))
        affaire = result.scalar_one_or_none()
        if not affaire:
            return f"❌ Affaire `{code}` introuvable. Vérifie le code dans ARCEUS."

        session.affaire_id = str(affaire.id)
        await db.commit()
        return (
            f"✅ Affaire définie : *{affaire.code} — {affaire.nom}*\n"
            f"Tous tes messages seront maintenant contextualisés sur cette affaire."
        )

    return f"Commande inconnue : `/{command}`"


# ── Parsing des mentions ─────────────────────────────────────────────────────


def parse_mention(text: str) -> tuple[str | None, str]:
    """
    Extrait la mention @agent du début du message.
    Retourne (agent_name, texte_nettoyé) ou (None, texte_original).
    """
    m = _MENTION_RE.match(text.strip())
    if not m:
        return None, text.strip()
    name = m.group(1).lower()
    cleaned = text[m.end() :].strip()
    if name in MENTIONABLE_AGENTS:
        return name, cleaned
    return None, text.strip()


# ── Routing message ──────────────────────────────────────────────────────────


async def route_message(
    db: AsyncSession,
    chat_id: str,
    text: str,
    affaire_id: str | None,
) -> tuple[str, str | None]:
    """
    Détermine l'agent et l'instruction à partir du texte.
    Retourne (agent_name, instruction) — agent="zeus" → orchestration complète.
    """
    agent, instruction = parse_mention(text)

    if not instruction:
        instruction = text.strip()

    if not agent:
        agent = "hermes"  # Hermès qualifie par défaut

    if not instruction:
        return agent, None

    return agent, instruction


# ── Photo pipeline ───────────────────────────────────────────────────────────


async def build_photo_instruction(caption: str | None, filename: str) -> str:
    """Construit l'instruction pour la cascade Argos → Héphaïstos."""
    context = f"\nContexte fourni : {caption}" if caption else ""
    return (
        f"Une photo a été partagée depuis le chantier ({filename}).{context}\n\n"
        "Effectue un constat visuel objectif : describe ce que tu vois "
        "(géométrie, matériaux visibles, anomalies, localisation dans l'image). "
        "Ne conclus pas sur les causes — décris uniquement les faits observables."
    )
