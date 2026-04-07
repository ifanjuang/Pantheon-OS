"""
AgentService — boucle agentique ReAct (Reason + Act).

Fonctionnement :
  1. Reçoit une instruction + contexte affaire
  2. Envoie au LLM avec les outils disponibles (function calling)
  3. Si le LLM appelle un outil → exécute → réinjecte le résultat
  4. Répète jusqu'à réponse finale ou max_iterations atteint
  5. Persiste l'historique complet dans agent_runs
"""
import asyncio
import functools
import json
import time
from pathlib import Path
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from core.logging import get_logger
from core.services.llm_service import LlmService
from core.settings import settings
from database import AsyncSessionLocal
from modules.agent.models import AgentRun
from modules.agent.tools import DEFINITIONS, execute_tool

log = get_logger("agent.service")

AGENTS_DIR = Path(settings.AGENTS_DIR) if hasattr(settings, "AGENTS_DIR") else Path(__file__).parent.parent.parent.parent / "agents"
VALID_AGENTS = {
    # Perception
    "hermes", "argos",
    # Analyse
    "athena", "hephaistos", "promethee", "apollon", "dionysos",
    # Cadrage
    "themis", "chronos", "ares",
    # Continuité
    "hestia", "mnemosyne",
    # Communication
    "iris", "aphrodite",
    # Production
    "dedale",
}

_DEFAULT_PROMPT = """Tu es un assistant copilote pour une agence d'architecture (MOE).
Tu aides les chargés de projet à trouver des informations, analyser des documents
et prendre des décisions sur leurs projets de construction.

Règles :
- Utilise les outils disponibles pour chercher les informations avant de répondre.
- Cite tes sources (nom du document, score de pertinence).
- Réponds en français, de manière concise et structurée.
- Si une information est introuvable, dis-le clairement.
- N'invente jamais de données chiffrées (délais, coûts, surfaces).
"""

AGENTS_COMMON = (AGENTS_DIR / "AGENTS.md").read_text(encoding="utf-8") if (AGENTS_DIR / "AGENTS.md").exists() else ""


@functools.lru_cache(maxsize=32)
def _build_system_prompt(agent_name: str) -> str:
    """Charge SOUL.md + MEMORY.md de l'agent demandé. Résultat mis en cache (process lifetime).
    Fallback sur prompt par défaut si fichier absent."""
    name = agent_name.lower() if agent_name else "athena"
    if name not in VALID_AGENTS:
        name = "athena"

    soul_path = AGENTS_DIR / name / "SOUL.md"
    memory_path = AGENTS_DIR / name / "MEMORY.md"

    soul = soul_path.read_text(encoding="utf-8") if soul_path.exists() else _DEFAULT_PROMPT
    memory_raw = memory_path.read_text(encoding="utf-8").strip() if memory_path.exists() else ""

    has_memory = any(
        line.strip() and not line.strip().startswith("#") and not line.strip().startswith("<!--")
        for line in memory_raw.splitlines()
    )
    memory_section = f"\n\n## Mémoire permanente\n{memory_raw}" if has_memory else ""
    common_section = f"\n\n## Règles communes\n{AGENTS_COMMON}" if AGENTS_COMMON else ""
    return f"{soul}{memory_section}{common_section}"


async def _build_affaire_context(db: AsyncSession, affaire_id: UUID) -> str:
    """Charge les métadonnées de l'affaire et les formate pour injection dans le prompt."""
    try:
        from modules.affaires.models import Affaire
        from sqlalchemy import select
        result = await db.execute(select(Affaire).where(Affaire.id == affaire_id))
        affaire = result.scalar_one_or_none()
        if not affaire:
            return ""
        parts = [f"Affaire : {affaire.code} — {affaire.nom}"]
        if affaire.typology:
            parts.append(f"Typologie : {affaire.typology}")
        if affaire.region:
            parts.append(f"Région : {affaire.region}")
        if affaire.budget_moa:
            parts.append(f"Budget MOA : {affaire.budget_moa:,.0f} € HT")
        if affaire.honoraires:
            parts.append(f"Honoraires MOE : {affaire.honoraires:,.0f} € HT")
        if affaire.phase_courante:
            parts.append(f"Phase courante : {affaire.phase_courante}")
        if affaire.date_fin_prevue:
            parts.append(f"Fin prévisionnelle : {affaire.date_fin_prevue.isoformat()}")
        if affaire.abf:
            parts.append("Secteur ABF : OUI — prescriptions architecturales obligatoires")
        if affaire.zone_risque:
            risques = [k for k, v in affaire.zone_risque.items() if v]
            if risques:
                parts.append(f"Zones à risque : {', '.join(risques)}")
        return "\n".join(parts)
    except Exception:
        return ""


async def run_agent(
    db: AsyncSession,
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    agent_name: str = "athena",
    max_iterations: int = 10,
) -> AgentRun:
    """Exécute la boucle agentique et persiste le résultat."""
    from modules.agent.memory import extract_and_store_memories, get_agent_memories

    t_start = time.monotonic()

    # Construire le system prompt
    system_prompt = _build_system_prompt(agent_name)

    # Injecter le contexte projet (typology, region, budget, phase, ABF, zones)
    affaire_context = await _build_affaire_context(db, affaire_id)
    if affaire_context:
        system_prompt += f"\n\n## Contexte projet\n{affaire_context}"

    # Injecter la mémoire dynamique (leçons apprises sur cette affaire)
    memories = await get_agent_memories(db, agent_name, affaire_id)
    if memories:
        memories_text = "\n".join(f"- {m}" for m in memories)
        system_prompt += f"\n\n## Mémoire dynamique — ce que tu as appris sur cette affaire\n{memories_text}"

    log.info("agent.start", agent=agent_name, affaire_id=str(affaire_id))

    run = AgentRun(
        affaire_id=affaire_id,
        user_id=user_id,
        instruction=instruction,
        status="running",
        steps=[],
    )
    db.add(run)
    await db.flush()  # obtenir l'id sans commit

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": instruction},
    ]

    steps: list[dict] = []
    all_sources: list[dict] = []   # sources RAG collectées sur tous les appels d'outils
    final_answer: str | None = None
    model = settings.effective_llm_model

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    async def _llm_react_call(msgs: list) -> object:
        return await LlmService._get_client().chat.completions.create(
            model=model,
            messages=msgs,
            tools=DEFINITIONS,
            tool_choice="auto",
            temperature=0.3,
            max_tokens=2048,
        )

    try:
        for iteration in range(max_iterations):
            t_iter = time.monotonic()

            response = await _llm_react_call(messages)

            choice = response.choices[0]
            msg = choice.message

            # Ajouter la réponse du LLM aux messages
            messages.append(msg.model_dump(exclude_none=True))

            # Pas d'appel d'outil → réponse finale
            if not msg.tool_calls:
                final_answer = msg.content or ""
                break

            # Exécuter tous les appels d'outils demandés
            for tc in msg.tool_calls:
                t_tool = time.monotonic()
                tool_name = tc.function.name
                tool_args = json.loads(tc.function.arguments or "{}")

                log.info(
                    "agent.tool_call",
                    run_id=str(run.id),
                    iteration=iteration,
                    tool=tool_name,
                    args=tool_args,
                )

                tool_output, tool_sources = await execute_tool(
                    name=tool_name,
                    args=tool_args,
                    affaire_id=affaire_id,
                    db=db,
                )

                # Dédupliquer les sources par chunk_id
                seen_chunks = {s["chunk_id"] for s in all_sources}
                for src in tool_sources:
                    if src["chunk_id"] not in seen_chunks:
                        all_sources.append(src)
                        seen_chunks.add(src["chunk_id"])

                duration_tool = int((time.monotonic() - t_tool) * 1000)
                steps.append({
                    "tool": tool_name,
                    "args": tool_args,
                    "output": tool_output[:1000],  # tronqué pour le stockage
                    "sources_count": len(tool_sources),
                    "duration_ms": duration_tool,
                })

                # Réinjecter le résultat dans les messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": tool_output,
                })

        else:
            # max_iterations atteint sans réponse finale
            final_answer = (
                "Limite d'itérations atteinte. Voici ce que j'ai trouvé jusqu'ici :\n"
                + (steps[-1]["output"] if steps else "Aucune information collectée.")
            )

        run.status = "completed"
        run.result = final_answer

    except Exception as exc:
        log.error("agent.run_failed", run_id=str(run.id), error=str(exc))
        run.status = "failed"
        run.result = f"Erreur lors de l'exécution : {exc}"

    finally:
        run.steps = steps
        run.sources = all_sources
        run.iterations = len([s for s in steps]) // max(len(DEFINITIONS), 1) + 1
        run.duration_ms = int((time.monotonic() - t_start) * 1000)
        await db.commit()
        await db.refresh(run)

    log.info(
        "agent.run_complete",
        run_id=str(run.id),
        status=run.status,
        steps=len(steps),
        duration_ms=run.duration_ms,
    )

    # Extraire et stocker les leçons via ARQ (job tracé, pas fire-and-forget)
    if run.status == "completed" and run.result:
        try:
            from core.queue import get_queue
            pool = await get_queue()
            await pool.enqueue_job(
                "memory_job",
                agent_name=agent_name,
                instruction=instruction,
                result=run.result,
                affaire_id=str(affaire_id),
                run_id=str(run.id),
            )
        except Exception as exc:
            # Queue indisponible → fallback tâche locale tracée
            log.warning("agent.memory.queue_failed", error=str(exc))
            async def _store_memories_fallback():
                try:
                    async with AsyncSessionLocal() as bg_db:
                        await extract_and_store_memories(
                            agent_name=agent_name,
                            instruction=instruction,
                            result=run.result,
                            affaire_id=affaire_id,
                            run_id=run.id,
                            db=bg_db,
                        )
                except Exception as e:
                    log.error("agent.memory.fallback_failed", agent=agent_name, error=str(e))
            asyncio.ensure_future(_store_memories_fallback())

    return run


async def run_agent_from_run_id(
    db: AsyncSession,
    run_id,
    instruction: str,
    affaire_id: UUID,
    user_id: UUID | None,
    agent_name: str = "athena",
    max_iterations: int = 10,
) -> AgentRun:
    """
    Variante worker ARQ : le run AgentRun existe déjà en DB (status=queued).
    Met à jour son statut puis exécute la boucle ReAct.
    """
    run = await db.get(AgentRun, run_id)
    if not run:
        raise ValueError(f"AgentRun {run_id} introuvable")
    run.status = "running"
    await db.commit()
    return await run_agent(
        db=db,
        instruction=instruction,
        affaire_id=affaire_id,
        user_id=user_id,
        agent_name=agent_name,
        max_iterations=max_iterations,
    )
