"""
SetupEngine — assistant d'installation.
Diagnostic des services, lecture/écriture du .env, tests de connexion en live.
"""
import os
import re
import asyncio
from pathlib import Path
from typing import Any

from core.logging import get_logger
from core.settings import settings

log = get_logger("admin.setup")

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.resolve()
ENV_FILE = PROJECT_ROOT / ".env"

# ── Définition des champs .env — groupes + types ─────────────────

ENV_SCHEMA: list[dict] = [
    {
        "group": "Base de données",
        "icon": "🗄",
        "fields": [
            {"key": "DB_PASSWORD", "label": "Mot de passe PostgreSQL", "type": "password", "required": True},
        ],
    },
    {
        "group": "Authentification JWT",
        "icon": "🔐",
        "fields": [
            {"key": "JWT_SECRET_KEY", "label": "Secret JWT (min 32 car.)", "type": "password", "required": True},
            {"key": "JWT_EXPIRE_MINUTES", "label": "Expiration du token (minutes)", "type": "number"},
            {"key": "ADMIN_EMAIL", "label": "Email administrateur", "type": "email", "required": True},
            {"key": "ADMIN_PASSWORD", "label": "Mot de passe admin (1er démarrage)", "type": "password", "required": True},
        ],
    },
    {
        "group": "Fournisseur IA",
        "icon": "🤖",
        "fields": [
            {"key": "LLM_PROVIDER", "label": "Provider LLM", "type": "select",
             "options": ["ollama", "openai"], "required": True},
            {"key": "OLLAMA_BASE_URL", "label": "URL Ollama (ex: http://192.168.1.50:11434)",
             "type": "url", "show_if": {"LLM_PROVIDER": "ollama"}},
            {"key": "OLLAMA_MODEL", "label": "Modèle Ollama", "type": "ollama_model",
             "show_if": {"LLM_PROVIDER": "ollama"}},
            {"key": "EMBEDDING_PROVIDER", "label": "Provider embeddings", "type": "select",
             "options": ["ollama", "openai"]},
            {"key": "OLLAMA_EMBEDDING_MODEL", "label": "Modèle embeddings Ollama",
             "type": "text", "show_if": {"EMBEDDING_PROVIDER": "ollama"}},
            {"key": "EMBEDDING_DIM", "label": "Dimension embeddings", "type": "number"},
            {"key": "OPENAI_API_KEY", "label": "Clé API OpenAI", "type": "password",
             "show_if": {"LLM_PROVIDER": "openai"}},
            {"key": "OPENAI_API_BASE_URL", "label": "URL base OpenAI", "type": "url",
             "show_if": {"LLM_PROVIDER": "openai"}},
            {"key": "LLM_MODEL", "label": "Modèle (ex: gpt-4o)", "type": "text",
             "show_if": {"LLM_PROVIDER": "openai"}},
        ],
    },
    {
        "group": "Stockage MinIO",
        "icon": "📦",
        "fields": [
            {"key": "MINIO_ENDPOINT", "label": "Endpoint MinIO (host:port)", "type": "text", "required": True},
            {"key": "MINIO_ROOT_USER", "label": "Utilisateur MinIO", "type": "text", "required": True},
            {"key": "MINIO_ROOT_PASSWORD", "label": "Mot de passe MinIO", "type": "password", "required": True},
            {"key": "MINIO_BUCKET", "label": "Nom du bucket", "type": "text"},
            {"key": "MINIO_SECURE", "label": "TLS activé", "type": "bool"},
        ],
    },
    {
        "group": "Notifications — Email",
        "icon": "📧",
        "fields": [
            {"key": "SMTP_HOST", "label": "Serveur SMTP", "type": "text"},
            {"key": "SMTP_PORT", "label": "Port SMTP", "type": "number"},
            {"key": "SMTP_USER", "label": "Utilisateur SMTP", "type": "email"},
            {"key": "SMTP_PASSWORD", "label": "Mot de passe SMTP", "type": "password"},
            {"key": "SMTP_FROM", "label": "Expéditeur", "type": "text"},
        ],
    },
    {
        "group": "Notifications — Telegram",
        "icon": "✈️",
        "fields": [
            {"key": "TELEGRAM_TOKEN", "label": "Token bot Telegram", "type": "password"},
            {"key": "TELEGRAM_DEFAULT_CHAT_ID", "label": "Chat ID par défaut", "type": "text"},
        ],
    },
    {
        "group": "Notifications — WhatsApp",
        "icon": "💬",
        "fields": [
            {"key": "WHATSAPP_ENABLED", "label": "WhatsApp activé", "type": "bool"},
            {"key": "WHATSAPP_MODE", "label": "Mode", "type": "select", "options": ["meta", "evolution"]},
            {"key": "WA_PHONE_ID", "label": "Phone Number ID (Meta)", "type": "text",
             "show_if": {"WHATSAPP_MODE": "meta"}},
            {"key": "WA_TOKEN", "label": "Token Meta", "type": "password",
             "show_if": {"WHATSAPP_MODE": "meta"}},
            {"key": "WA_TEMPLATE_NAME", "label": "Nom du template Meta", "type": "text",
             "show_if": {"WHATSAPP_MODE": "meta"}},
            {"key": "EVOLUTION_API_KEY", "label": "Clé Evolution API", "type": "password",
             "show_if": {"WHATSAPP_MODE": "evolution"}},
        ],
    },
    {
        "group": "Intégrations",
        "icon": "🔗",
        "fields": [
            {"key": "NOTION_TOKEN", "label": "Token Notion", "type": "password"},
            {"key": "NOTION_DATABASE_AFFAIRES", "label": "ID DB Affaires (Notion)", "type": "text"},
            {"key": "NOTION_DATABASE_ACTIONS", "label": "ID DB Actions (Notion)", "type": "text"},
        ],
    },
]

# ── Lecture/écriture .env ────────────────────────────────────────

def _parse_env_file() -> dict[str, str]:
    if not ENV_FILE.exists():
        return {}
    env: dict[str, str] = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip()
    return env


def _write_env_file(values: dict[str, str]) -> None:
    """Met à jour les clés dans .env en préservant les commentaires et l'ordre."""
    if not ENV_FILE.exists():
        # Créer depuis .env.example
        example = PROJECT_ROOT / ".env.example"
        if example.exists():
            ENV_FILE.write_text(example.read_text(encoding="utf-8"), encoding="utf-8")

    lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
    updated_keys: set[str] = set()
    new_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            key = stripped.partition("=")[0].strip()
            if key in values:
                new_lines.append(f"{key}={values[key]}")
                updated_keys.add(key)
                continue
        new_lines.append(line)

    # Ajouter les clés nouvelles à la fin
    for key, val in values.items():
        if key not in updated_keys:
            new_lines.append(f"{key}={val}")

    ENV_FILE.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    log.info("setup.env_updated", keys=list(values.keys()))


# ── SetupEngine ──────────────────────────────────────────────────

class SetupEngine:

    def get_schema(self) -> list[dict]:
        """Retourne le schéma de formulaire enrichi avec les valeurs actuelles."""
        current = _parse_env_file()
        schema = []
        for group in ENV_SCHEMA:
            fields = []
            for f in group["fields"]:
                field = dict(f)
                raw_val = current.get(f["key"], "")
                field["value"] = raw_val
                fields.append(field)
            schema.append({**group, "fields": fields})
        return schema

    def save_env(self, values: dict[str, str]) -> None:
        """Sauvegarde les valeurs dans le .env."""
        # Sécurité : n'autoriser que les clés connues dans le schéma
        allowed = {f["key"] for g in ENV_SCHEMA for f in g["fields"]}
        filtered = {k: v for k, v in values.items() if k in allowed}
        _write_env_file(filtered)

    # ── Tests de connexion ────────────────────────────────────────

    async def test_db(self) -> dict:
        try:
            import asyncpg
            conn = await asyncio.wait_for(
                asyncpg.connect(settings.ASYNCPG_URL), timeout=5
            )
            version = await conn.fetchval("SELECT version()")
            await conn.close()
            return {"ok": True, "detail": version.split(",")[0]}
        except Exception as e:
            return {"ok": False, "detail": str(e)}

    async def test_minio(self) -> dict:
        try:
            from core.services.storage_service import StorageService
            ok = await StorageService.ping()
            return {"ok": ok, "detail": "Bucket accessible" if ok else "Connexion échouée"}
        except Exception as e:
            return {"ok": False, "detail": str(e)}

    async def test_llm(self) -> dict:
        try:
            from core.services.llm_service import LlmService
            ok = await LlmService.ping()
            if ok:
                # Test rapide : 1 token
                response = await LlmService.chat(
                    [{"role": "user", "content": "Dis uniquement 'ok'"}],
                    max_tokens=5,
                )
                return {"ok": True, "detail": f"Modèle : {settings.effective_llm_model} — réponse : {response.strip()[:40]}"}
            return {"ok": False, "detail": "LLM inaccessible"}
        except Exception as e:
            return {"ok": False, "detail": str(e)}

    async def test_smtp(self) -> dict:
        if not settings.SMTP_HOST:
            return {"ok": False, "detail": "SMTP_HOST non configuré"}
        try:
            import smtplib
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=5) as s:
                s.ehlo()
                if settings.SMTP_PORT == 587:
                    s.starttls()
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    s.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            return {"ok": True, "detail": f"Connexion SMTP réussie ({settings.SMTP_HOST}:{settings.SMTP_PORT})"}
        except Exception as e:
            return {"ok": False, "detail": str(e)}

    async def test_telegram(self) -> dict:
        if not settings.TELEGRAM_TOKEN:
            return {"ok": False, "detail": "TELEGRAM_TOKEN non configuré"}
        try:
            import httpx
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/getMe")
            data = r.json()
            if data.get("ok"):
                name = data["result"].get("username", "?")
                return {"ok": True, "detail": f"Bot : @{name}"}
            return {"ok": False, "detail": data.get("description", "Erreur Telegram")}
        except Exception as e:
            return {"ok": False, "detail": str(e)}

    async def test_whatsapp(self) -> dict:
        if not settings.WHATSAPP_ENABLED:
            return {"ok": False, "detail": "WhatsApp désactivé"}
        try:
            import httpx
            if settings.WHATSAPP_MODE == "meta":
                if not settings.WA_TOKEN or not settings.WA_PHONE_ID:
                    return {"ok": False, "detail": "WA_TOKEN ou WA_PHONE_ID manquant"}
                async with httpx.AsyncClient(timeout=5) as client:
                    r = await client.get(
                        f"https://graph.facebook.com/v19.0/{settings.WA_PHONE_ID}",
                        headers={"Authorization": f"Bearer {settings.WA_TOKEN}"},
                    )
                if r.status_code == 200:
                    return {"ok": True, "detail": f"Phone ID {settings.WA_PHONE_ID} valide"}
                return {"ok": False, "detail": f"HTTP {r.status_code} — {r.text[:80]}"}
            return {"ok": False, "detail": "Mode evolution : test manuel requis"}
        except Exception as e:
            return {"ok": False, "detail": str(e)}

    async def ollama_list_models(self) -> list[str]:
        """Retourne les modèles disponibles sur le serveur Ollama."""
        try:
            import httpx
            base = settings.OLLAMA_BASE_URL.rstrip("/")
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{base}/api/tags")
            if r.status_code == 200:
                return [m["name"] for m in r.json().get("models", [])]
        except Exception:
            pass
        return []

    async def full_status(self) -> dict:
        """Statut global de tous les services — utilisé pour le dashboard."""
        db, minio, llm = await asyncio.gather(
            self.test_db(), self.test_minio(), self.test_llm()
        )
        return {
            "db": db,
            "minio": minio,
            "llm": llm,
            "config": {
                "llm_provider": settings.LLM_PROVIDER,
                "llm_model": settings.effective_llm_model,
                "embedding_model": settings.effective_embedding_model,
                "whatsapp_enabled": settings.WHATSAPP_ENABLED,
                "whatsapp_mode": settings.WHATSAPP_MODE if settings.WHATSAPP_ENABLED else None,
                "smtp_configured": bool(settings.SMTP_HOST),
                "telegram_configured": bool(settings.TELEGRAM_TOKEN),
                "notion_configured": bool(settings.NOTION_TOKEN),
            },
        }
