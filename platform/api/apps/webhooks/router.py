"""
Router webhooks — endpoints pour orchestrateurs externes (Paperclip, n8n, cron, Telegram)

POST /webhooks/heartbeat
    Déclenche l'agent Argos (vigie) sur toutes les affaires actives.
    Conçu pour être appelé quotidiennement par Paperclip.

POST /webhooks/document-uploaded
    Déclenche l'agent Thémis (rigueur) sur un document nouvellement uploadé.
    Appelé automatiquement après chaque upload (ou par Paperclip sur événement).

POST /webhooks/agent/{agent_name}
    Déclenche un agent spécifique sur une affaire donnée.
    Endpoint générique pour Paperclip.

POST /webhooks/telegram
    Webhook Telegram — reçoit les mises à jour du bot et les route via ARQ.

GET  /webhooks/health
    Healthcheck pour Paperclip (vérifie que ARCEUS répond).

Auth : Bearer = WEBHOOK_SECRET (distinct du JWT_SECRET_KEY, configurable dans .env)
"""

import uuid
from typing import Annotated, Any

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.queue import get_queue
from core.settings import settings
from database import get_db
from apps.affaires.models import Affaire
from apps.agent.service import run_agent
from apps.orchestra.service import run_orchestra
from apps.webhooks.telegram import is_chat_allowed, tg_send

log = get_logger("webhooks.router")


# ── Auth webhook ─────────────────────────────────────────────────────────────


def _check_webhook_secret(authorization: Annotated[str | None, Header()] = None):
    """
    Valide le header Authorization: Bearer <WEBHOOK_SECRET>.
    Accepte aussi JWT_SECRET_KEY pour compatibilité si WEBHOOK_SECRET non défini.
    """
    valid_secrets = {settings.JWT_SECRET_KEY}
    webhook_secret = getattr(settings, "WEBHOOK_SECRET", None)
    if webhook_secret:
        valid_secrets.add(webhook_secret)

    token = (authorization or "").removeprefix("Bearer ").strip()
    if token not in valid_secrets:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Webhook secret invalide",
        )


# ── Schémas ──────────────────────────────────────────────────────────────────


class HeartbeatResponse(BaseModel):
    runs_triggered: int
    affaires: list[str]


class DocumentEventPayload(BaseModel):
    document_id: uuid.UUID
    affaire_id: uuid.UUID
    nom: str


class AgentWebhookPayload(BaseModel):
    affaire_id: uuid.UUID
    instruction: str
    max_iterations: int = 8


class AgentWebhookResponse(BaseModel):
    run_id: uuid.UUID
    agent: str
    status: str
    result: str | None


# ── Router ───────────────────────────────────────────────────────────────────


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    async def health(_auth=Depends(_check_webhook_secret)):
        """Healthcheck pour Paperclip."""
        return {"status": "ok", "service": "pantheon"}

    @router.post("/heartbeat", response_model=HeartbeatResponse)
    async def heartbeat(
        db: AsyncSession = Depends(get_db),
        _auth=Depends(_check_webhook_secret),
    ):
        """
        Heartbeat quotidien : Argus analyse toutes les affaires actives.
        Paperclip appelle cet endpoint selon son schedule (ex : tous les matins à 8h).
        """
        result = await db.execute(select(Affaire).where(Affaire.statut == "actif"))
        affaires = result.scalars().all()

        if not affaires:
            log.info("webhooks.heartbeat", affaires=0)
            return HeartbeatResponse(runs_triggered=0, affaires=[])

        triggered = []
        for affaire in affaires:
            await run_agent(
                db=db,
                instruction=(
                    "Analyse l'état de ce projet. "
                    "Identifie les risques actifs, les documents manquants, "
                    "et les points de vigilance. "
                    "Donne une liste priorisée CRITIQUE / ALERTE / INFO."
                ),
                affaire_id=affaire.id,
                user_id=None,
                agent_name="argus",
                max_iterations=6,
            )
            triggered.append(affaire.code)
            log.info("webhooks.heartbeat_run", affaire=affaire.code)

        return HeartbeatResponse(runs_triggered=len(triggered), affaires=triggered)

    @router.post("/document-uploaded")
    async def document_uploaded(
        payload: DocumentEventPayload,
        db: AsyncSession = Depends(get_db),
        _auth=Depends(_check_webhook_secret),
    ):
        """
        Déclenché après l'upload d'un document.
        Thémis vérifie la conformité réglementaire du document.
        """
        run = await run_agent(
            db=db,
            instruction=(
                f"Un nouveau document vient d'être uploadé : '{payload.nom}'. "
                "Analyse son contenu pour identifier : "
                "1. Les obligations réglementaires mentionnées (DTU, normes, RE2020). "
                "2. Les points de conformité à vérifier. "
                "3. Les clauses ou engagements contractuels à retenir."
            ),
            affaire_id=payload.affaire_id,
            user_id=None,
            agent_name="themis",
            max_iterations=5,
        )
        log.info(
            "webhooks.document_uploaded",
            document_id=str(payload.document_id),
            affaire_id=str(payload.affaire_id),
            run_id=str(run.id),
        )
        return {"run_id": str(run.id), "status": run.status}

    @router.post("/orchestra")
    async def trigger_orchestra(
        payload: AgentWebhookPayload,
        db: AsyncSession = Depends(get_db),
        _auth=Depends(_check_webhook_secret),
    ):
        """
        Déclenche une orchestration Zeus complète depuis Paperclip.
        Zeus coordonne automatiquement les agents nécessaires.
        """
        run = await run_orchestra(
            db=db,
            instruction=payload.instruction,
            affaire_id=payload.affaire_id,
            user_id=None,
        )
        log.info("webhooks.orchestra", run_id=str(run.id), status=run.status)
        return {
            "run_id": str(run.id),
            "status": run.status,
            "agents": list(run.agent_results.keys()),
        }

    @router.post("/agent/{agent_name}", response_model=AgentWebhookResponse)
    async def trigger_agent(
        agent_name: str,
        payload: AgentWebhookPayload,
        db: AsyncSession = Depends(get_db),
        _auth=Depends(_check_webhook_secret),
    ):
        """
        Endpoint générique : Paperclip déclenche n'importe quel agent
        avec une instruction personnalisée.
        """
        valid = {"themis", "argus", "hermes", "mnemosyne", "athena", "apollon"}
        if agent_name not in valid:
            raise HTTPException(
                status_code=400,
                detail=f"Agent inconnu. Valeurs acceptées : {valid}",
            )

        run = await run_agent(
            db=db,
            instruction=payload.instruction,
            affaire_id=payload.affaire_id,
            user_id=None,
            agent_name=agent_name,
            max_iterations=payload.max_iterations,
        )
        return AgentWebhookResponse(
            run_id=run.id,
            agent=agent_name,
            status=run.status,
            result=run.result,
        )

    @router.post("/telegram", status_code=200)
    async def telegram_webhook(
        request: Request,
        db: AsyncSession = Depends(get_db),
    ):
        """
        Reçoit les updates Telegram et les délègue à telegram_message_job via ARQ.
        Valide l'en-tête X-Telegram-Bot-Api-Secret-Token si WEBHOOK_SECRET est défini.
        """
        # Validation du secret Telegram (optionnelle mais recommandée)
        webhook_secret = getattr(settings, "WEBHOOK_SECRET", None)
        if webhook_secret:
            tg_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
            if tg_secret != webhook_secret:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")

        if not settings.TELEGRAM_TOKEN:
            raise HTTPException(status_code=503, detail="Telegram non configuré")

        update: dict[str, Any] = await request.json()

        # Extraire message ou callback_query
        message = update.get("message") or update.get("edited_message")
        if not message:
            return {"ok": True}  # update non géré (inline query, etc.)

        chat_id = str(message.get("chat", {}).get("id", ""))
        if not chat_id:
            return {"ok": True}

        # Vérification de l'autorisation du chat
        if not is_chat_allowed(chat_id):
            log.warning("telegram.chat_not_allowed", chat_id=chat_id)
            return {"ok": True}

        # Déléguer le traitement à ARQ (non bloquant)
        try:
            pool = await get_queue()
            await pool.enqueue_job(
                "telegram_message_job",
                chat_id=chat_id,
                message=message,
            )
        except Exception as exc:
            log.error("telegram.enqueue_failed", chat_id=chat_id, error=str(exc))
            # Répondre quand même OK à Telegram pour éviter les retries
            await tg_send(chat_id, "Désolé, une erreur interne s'est produite. Réessaie dans un instant.")

        return {"ok": True}

    return router
