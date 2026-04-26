# V2 only — requires Redis + ARQ. Enable by renaming to worker.py.
"""
ARQ Worker — exécute les jobs orchestra et agent en arrière-plan.

Démarrage :
  python worker.py           (en dev, dans le container api)
  docker compose up worker   (en prod)

Jobs disponibles :
  orchestra_job   → run_orchestra()
  agent_job       → run_agent()
"""

import asyncio
import functools
import json
import logging
import time
from uuid import UUID

from arq import create_pool, cron
from arq.connections import RedisSettings

from core.settings import settings
from database import AsyncSessionLocal

log = logging.getLogger("arq.worker")

_DLQ_KEY = "arq:dlq"
_DLQ_MAX = 1000


def _dlq_wrap(func):
    """Décore un job ARQ pour pousser les échecs dans la Dead-Letter Queue Redis."""

    @functools.wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        try:
            return await func(ctx, *args, **kwargs)
        except Exception as exc:
            try:
                redis = ctx.get("redis")
                if redis:
                    entry = json.dumps(
                        {
                            "job_id": ctx.get("job_id", "unknown"),
                            "function": func.__name__,
                            "error": str(exc)[:500],
                            "failed_at": time.time(),
                        }
                    )
                    await redis.lpush(_DLQ_KEY, entry)
                    await redis.ltrim(_DLQ_KEY, 0, _DLQ_MAX - 1)
            except Exception:
                pass
            raise

    return wrapper


# ── Jobs ──────────────────────────────────────────────────────────────────────


async def orchestra_job(
    ctx,
    run_id: str,
    instruction: str,
    affaire_id: str,
    user_id: str | None,
    agents: list[str] | None,
    criticite: str | None = None,
):
    """
    Exécute une orchestration Zeus pour un OrchestraRun déjà créé en DB (status=queued).
    Met à jour le run avec les résultats une fois terminé.
    Le paramètre criticite est optionnel pour rester compatible avec les jobs déjà en queue.
    """
    from apps.orchestra.service import run_orchestra_from_run_id

    log.info(f"[orchestra_job] start run_id={run_id}")
    async with AsyncSessionLocal() as db:
        await run_orchestra_from_run_id(
            db=db,
            run_id=UUID(run_id),
            instruction=instruction,
            affaire_id=UUID(affaire_id),
            user_id=UUID(user_id) if user_id else None,
            agents=agents,
            criticite=criticite,
        )
    log.info(f"[orchestra_job] done run_id={run_id}")


async def agent_job(
    ctx,
    run_id: str,
    instruction: str,
    affaire_id: str,
    user_id: str | None,
    agent_name: str,
    max_iterations: int,
):
    """
    Exécute un run agent pour un AgentRun déjà créé en DB (status=queued).
    """
    from apps.agent.service import run_agent_from_run_id

    log.info(f"[agent_job] start run_id={run_id}")
    async with AsyncSessionLocal() as db:
        await run_agent_from_run_id(
            db=db,
            run_id=UUID(run_id),
            instruction=instruction,
            affaire_id=UUID(affaire_id),
            user_id=UUID(user_id) if user_id else None,
            agent_name=agent_name,
            max_iterations=max_iterations,
        )
    log.info(f"[agent_job] done run_id={run_id}")


async def telegram_message_job(
    ctx,
    chat_id: str,
    message: dict,
):
    """
    Traite un message Telegram entrant : commande, mention @agent, photo ou texte libre.
    Délégué depuis le webhook POST /webhooks/telegram via ARQ.
    """
    from apps.webhooks.telegram import (
        build_photo_instruction,
        get_or_create_session,
        handle_command,
        route_message,
        tg_send,
        tg_send_typing,
        tg_download_file,
    )
    from apps.agent.service import run_agent
    from apps.orchestra.service import run_orchestra

    log.info(f"[telegram_job] start chat_id={chat_id}")

    async with AsyncSessionLocal() as db:
        text: str = message.get("text") or message.get("caption") or ""
        photos: list = message.get("photo") or []

        # ── Commandes /start /help /affaire /agents ────────────────────────
        if text.startswith("/"):
            parts = text.lstrip("/").split(None, 1)
            command = parts[0].lower().split("@")[0]  # /start@BotName → start
            args = parts[1] if len(parts) > 1 else ""
            reply = await handle_command(db=db, chat_id=chat_id, command=command, args=args)
            await tg_send(chat_id, reply)
            return

        # ── Session & affaire active ───────────────────────────────────────
        session = await get_or_create_session(db, chat_id)
        affaire_id = session.affaire_id

        await tg_send_typing(chat_id)

        # ── Photo → cascade Argos ──────────────────────────────────────────
        if photos:
            # Prendre la photo de meilleure résolution (dernier élément)
            best = photos[-1]
            file_id = best.get("file_id")
            caption = message.get("caption")
            instruction = await build_photo_instruction(caption=caption, filename=f"photo_{file_id}.jpg")

            if not affaire_id:
                await tg_send(chat_id, "⚠️ Aucune affaire définie. Utilise `/affaire <CODE>` d'abord.")
                return

            run = await run_agent(
                db=db,
                instruction=instruction,
                affaire_id=UUID(affaire_id),
                user_id=None,
                agent_name="argos",
                max_iterations=5,
            )
            result_text = run.result or "Analyse terminée (pas de résultat textuel)."
            await tg_send(chat_id, f"*Argos — analyse photo :*\n\n{result_text}")
            return

        # ── Texte libre / @mention ─────────────────────────────────────────
        if not text.strip():
            return

        agent, instruction = await route_message(db=db, chat_id=chat_id, text=text, affaire_id=affaire_id)

        if not instruction:
            await tg_send(chat_id, "Je n'ai pas compris. Envoie une question ou `/help`.")
            return

        if not affaire_id:
            await tg_send(chat_id, "⚠️ Aucune affaire définie. Utilise `/affaire <CODE>` d'abord.")
            return

        # Zeus → orchestration complète ; autres → agent direct
        if agent == "zeus":
            run = await run_orchestra(
                db=db,
                instruction=instruction,
                affaire_id=UUID(affaire_id),
                user_id=None,
            )
            result_text = (run.final_answer or run.result or "Orchestration terminée.").strip()
        else:
            run = await run_agent(
                db=db,
                instruction=instruction,
                affaire_id=UUID(affaire_id),
                user_id=None,
                agent_name=agent,
                max_iterations=8,
            )
            result_text = (run.result or "Pas de réponse.").strip()

        # Truncate à 4000 chars (limite Telegram)
        if len(result_text) > 4000:
            result_text = result_text[:3950] + "\n\n_(réponse tronquée)_"

        agent_label = agent.capitalize()
        await tg_send(chat_id, f"*{agent_label} :*\n\n{result_text}")

    log.info(f"[telegram_job] done chat_id={chat_id} agent={agent}")


async def memory_job(
    ctx,
    agent_name: str,
    instruction: str,
    result: str,
    affaire_id: str,
    run_id: str,
):
    """
    Extrait et stocke les leçons d'un run agent terminé.
    Planifié par agent/service.py après chaque run complété.
    """
    from apps.agent.memory import extract_and_store_memories

    async with AsyncSessionLocal() as db:
        count = await extract_and_store_memories(
            agent_name=agent_name,
            instruction=instruction,
            result=result,
            affaire_id=UUID(affaire_id),
            run_id=UUID(run_id),
            db=db,
        )
    log.info(f"[memory_job] done agent={agent_name} lessons={count} run_id={run_id}")


async def memory_consolidation_job(ctx):
    """
    Consolide les leçons brutes en patterns de haut niveau.
    Exécuté périodiquement (cron 1x/jour) via ARQ.
    """
    from apps.agent.memory import consolidate_memories

    log.info("[memory_consolidation_job] start")
    async with AsyncSessionLocal() as db:
        total = await consolidate_memories(db=db)
    log.info(f"[memory_consolidation_job] done consolidated={total}")


async def ingest_courrier_job(ctx, courrier_id: str):
    """
    Indexe le contenu textuel d'un courrier dans le RAG (source_type='courrier').
    Enfilé automatiquement à la création/mise à jour d'un courrier avec résumé.
    Idempotent : réindexe complètement si appelé plusieurs fois.
    """
    from apps.communications.service import ingest_courrier

    log.info(f"[ingest_courrier_job] start courrier_id={courrier_id}")
    async with AsyncSessionLocal() as db:
        count = await ingest_courrier(db=db, courrier_id=UUID(courrier_id))
    log.info(f"[ingest_courrier_job] done courrier_id={courrier_id} chunks={count}")


async def draft_courrier_job(ctx, courrier_id: str):
    """
    Rédige un brouillon de réponse à un courrier entrant avec l'agent Iris.
    Enfilé par POST /communications/courriers/{id}/draft-response.
    """
    from apps.communications.service import process_draft_response

    log.info(f"[draft_courrier_job] start courrier_id={courrier_id}")
    async with AsyncSessionLocal() as db:
        await process_draft_response(db=db, courrier_id=UUID(courrier_id))
        await db.commit()
    log.info(f"[draft_courrier_job] done courrier_id={courrier_id}")


async def analyze_chantier_obs_job(ctx, obs_id: str):
    """
    Analyse une observation chantier avec l'agent Argos.
    Enfilé par POST /chantier/observations/{id}/analyze.
    """
    from apps.chantier.service import process_observation_analysis

    log.info(f"[analyze_chantier_obs_job] start obs_id={obs_id}")
    async with AsyncSessionLocal() as db:
        await process_observation_analysis(db=db, obs_id=UUID(obs_id))
        await db.commit()
    log.info(f"[analyze_chantier_obs_job] done obs_id={obs_id}")


async def qualify_nc_job(ctx, nc_id: str):
    """
    Qualifie une non-conformité chantier avec l'agent Héphaïstos.
    Enfilé par POST /chantier/nonconformites/{id}/qualify.
    """
    from apps.chantier.service import process_nc_qualification

    log.info(f"[qualify_nc_job] start nc_id={nc_id}")
    async with AsyncSessionLocal() as db:
        await process_nc_qualification(db=db, nc_id=UUID(nc_id))
        await db.commit()
    log.info(f"[qualify_nc_job] done nc_id={nc_id}")


async def capture_job(
    ctx,
    capture_id: str,
    affaire_id: str,
    user_id: str | None,
):
    """
    Traite une session de capture vocale NoobScribe :
      1. Transcription audio (Whisper)
      2. Passage par le pipeline agent
    """
    from apps.capture.service import process_capture

    log.info(f"[capture_job] start capture_id={capture_id}")
    async with AsyncSessionLocal() as db:
        await process_capture(
            db=db,
            capture_id=UUID(capture_id),
            affaire_id=UUID(affaire_id),
            user_id=UUID(user_id) if user_id else None,
        )
    log.info(f"[capture_job] done capture_id={capture_id}")


async def daily_alerts_job(ctx):
    """
    Parcourt toutes les affaires actives, détecte les alertes métier critiques
    et les logge en WARNING pour les remonter dans les outils d'observabilité.

    Cron : 1x/jour à 06:00 UTC (avant la journée de travail).
    """
    from apps.affaires.service import list_affaires
    from apps.affaires.cockpit import get_alertes

    log.info("[daily_alerts_job] start")
    nb_affaires = 0
    nb_critical = 0

    async with AsyncSessionLocal() as db:
        affaires = await list_affaires(db, statut="actif", limit=500, offset=0)
        nb_affaires = len(affaires)
        for affaire in affaires:
            try:
                alertes = await get_alertes(db, affaire.id)
                for alerte in alertes:
                    if alerte["niveau"] == "critical":
                        log.warning(
                            "[daily_alerts] alerte_critique",
                            affaire=affaire.code,
                            module=alerte["module"],
                            message=alerte["message"],
                        )
                        nb_critical += 1
                    elif alerte["niveau"] == "warning":
                        log.info(
                            "[daily_alerts] alerte_warning",
                            affaire=affaire.code,
                            module=alerte["module"],
                            message=alerte["message"],
                        )
            except Exception as exc:
                log.error(f"[daily_alerts_job] failed affaire={affaire.code} error={exc}")

    log.info(f"[daily_alerts_job] done affaires={nb_affaires} critical={nb_critical}")


async def weekly_summary_job(ctx):
    """
    Génère un résumé hebdomadaire de chaque affaire active via l'agent Hestia.
    Hestia capitalise les points clés : décisions récentes, avancement planning,
    NC ouvertes, courriers en attente, situation financière.

    Cron : 1x/semaine le lundi à 07:00 UTC.
    """
    from apps.affaires.service import list_affaires
    from apps.agent.service import run_agent

    log.info("[weekly_summary_job] start")
    async with AsyncSessionLocal() as db:
        affaires = await list_affaires(db, statut="actif", limit=500, offset=0)
        for affaire in affaires:
            instruction = (
                f"Génère le résumé hebdomadaire de l'affaire {affaire.code} — {affaire.nom}.\n"
                "Synthétise : décisions D2/D3 ouvertes, avancement planning (jalons, tâches critiques), "
                "non-conformités chantier ouvertes, courriers en attente de réponse, "
                "situation financière (avenants, situations à valider, dérive budgétaire). "
                "Formule en 5 à 10 points clés actionnables pour l'équipe MOE."
            )
            try:
                await run_agent(
                    db=db,
                    instruction=instruction,
                    affaire_id=affaire.id,
                    user_id=None,
                    agent_name="hestia",
                    max_iterations=5,
                )
                log.info(f"[weekly_summary_job] done affaire={affaire.code}")
            except Exception as exc:
                log.error(f"[weekly_summary_job] failed affaire={affaire.code} error={exc}")

    log.info("[weekly_summary_job] done")


# ── Configuration worker ──────────────────────────────────────────────────────


class WorkerSettings:
    functions = [
        _dlq_wrap(orchestra_job),
        _dlq_wrap(agent_job),
        _dlq_wrap(memory_job),
        _dlq_wrap(telegram_message_job),
        _dlq_wrap(capture_job),
        memory_consolidation_job,
        _dlq_wrap(analyze_chantier_obs_job),
        _dlq_wrap(qualify_nc_job),
        _dlq_wrap(ingest_courrier_job),
        _dlq_wrap(draft_courrier_job),
        daily_alerts_job,
        weekly_summary_job,
    ]
    cron_jobs = [
        # Consolidation mémoire : 1x/jour à 03:00 UTC
        cron(memory_consolidation_job, hour=3, minute=0, run_at_startup=False),
        # Alertes métier : 1x/jour à 06:00 UTC
        cron(daily_alerts_job, hour=6, minute=0, run_at_startup=False),
        # Résumé hebdo Hestia : lundi à 07:00 UTC
        cron(weekly_summary_job, weekday=0, hour=7, minute=0, run_at_startup=False),
    ]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    max_jobs = 10
    job_timeout = 600  # 10 min max par job
    keep_result = 3600  # conserver le résultat 1h
    retry_jobs = False  # ne pas relancer automatiquement (les runs sont idempotents)
    log_results = True


# ── Entrée principale ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import arq

    logging.basicConfig(level=logging.INFO)
    arq.run_worker(WorkerSettings)
