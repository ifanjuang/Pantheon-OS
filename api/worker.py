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
import logging
from uuid import UUID

from arq import create_pool, cron
from arq.connections import RedisSettings

from core.settings import settings
from database import AsyncSessionLocal

log = logging.getLogger("arq.worker")


# ── Jobs ──────────────────────────────────────────────────────────────────────

async def orchestra_job(
    ctx,
    run_id: str,
    instruction: str,
    affaire_id: str,
    user_id: str | None,
    agents: list[str] | None,
):
    """
    Exécute une orchestration Zeus pour un OrchestraRun déjà créé en DB (status=queued).
    Met à jour le run avec les résultats une fois terminé.
    """
    from modules.orchestra.models import OrchestraRun
    from modules.orchestra.service import run_orchestra_from_run_id

    log.info(f"[orchestra_job] start run_id={run_id}")
    async with AsyncSessionLocal() as db:
        await run_orchestra_from_run_id(
            db=db,
            run_id=UUID(run_id),
            instruction=instruction,
            affaire_id=UUID(affaire_id),
            user_id=UUID(user_id) if user_id else None,
            agents=agents,
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
    from modules.agent.service import run_agent_from_run_id

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
    from modules.agent.memory import extract_and_store_memories

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


# ── Configuration worker ──────────────────────────────────────────────────────

class WorkerSettings:
    functions = [orchestra_job, agent_job, memory_job]
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    max_jobs = 10
    job_timeout = 600           # 10 min max par job
    keep_result = 3600          # conserver le résultat 1h
    retry_jobs = False          # ne pas relancer automatiquement (les runs sont idempotents)
    log_results = True


# ── Entrée principale ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import arq

    logging.basicConfig(level=logging.INFO)
    arq.run_worker(WorkerSettings)
