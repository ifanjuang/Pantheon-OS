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

import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from core.logging import get_logger
from core.services.llm_service import LlmService
from core.settings import settings
from database import AsyncSessionLocal
from apps.agent.models import AgentRun
from apps.agent.memory import extract_and_store_memories, get_agent_memories, get_unified_memory
from apps.agent.tools import DEFINITIONS, execute_tool, _DB_TOOLS

log = get_logger("agent.service")

_ROOT = Path(__file__).parent.parent.parent.parent
AGENTS_DIR = Path(settings.AGENTS_DIR) if hasattr(settings, "AGENTS_DIR") else _ROOT / "agents"
CORE_DIR = _ROOT / "core"  # meta-agents
VALID_AGENTS = {
    # Perception
    "hermes",
    "argos",
    # Analyse
    "athena",
    "hephaistos",
    "promethee",
    "apollon",
    "dionysos",
    # Cadrage
    "themis",
    "chronos",
    "ares",
    # Continuité
    "hestia",
    "mnemosyne",
    # Communication
    "iris",
    "aphrodite",
    # Production
    "dedale",
    # Pantheon OS — nouveaux agents
    "hera",
    "artemis",
    "hades",
    "demeter",
    "poseidon",
    "kairos",
}

_DEFAULT_PROMPT = """Tu es un assistant expert au service d'une organisation professionnelle.
Tu aides les équipes à trouver des informations, analyser des documents
et prendre des décisions éclairées dans leur domaine d'expertise.

Règles :
- Utilise les outils disponibles pour chercher les informations avant de répondre.
- Cite tes sources (nom du document, score de pertinence).
- Réponds en français, de manière concise et structurée.
- Si une information est introuvable, dis-le clairement.
- N'invente jamais de données chiffrées (délais, coûts, quantités).
"""

AGENTS_COMMON = (AGENTS_DIR / "AGENTS.md").read_text(encoding="utf-8") if (AGENTS_DIR / "AGENTS.md").exists() else ""


def _resolve_soul_path(agent_name: str) -> Path | None:
    """Résout le chemin SOUL.md — core/ en priorité, agents/ en fallback."""
    name = agent_name.lower()
    core_path = CORE_DIR / name / "SOUL.md"
    if core_path.exists():
        return core_path
    agents_path = AGENTS_DIR / name / "SOUL.md"
    if agents_path.exists():
        return agents_path
    return None


@functools.lru_cache(maxsize=1)
def _get_domain_context_for_agent() -> str:
    """Charge le contexte domaine depuis agents/domains/{DOMAIN}.yaml (LRU cached)."""
    try:
        import yaml  # type: ignore[import]
    except ImportError:
        return ""
    domain = getattr(settings, "DOMAIN", "btp")
    overlay_path = AGENTS_DIR / "domains" / f"{domain}.yaml"
    if not overlay_path.exists():
        return ""
    try:
        data = yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
        return data.get("context_injection", "") if isinstance(data, dict) else ""
    except Exception:
        return ""


@functools.lru_cache(maxsize=32)
def _build_system_prompt(agent_name: str) -> str:
    """Charge SOUL.md + MEMORY.md + contexte domaine de l'agent. Mis en cache (process lifetime).
    Fallback sur prompt par défaut si fichier absent."""
    name = agent_name.lower() if agent_name else "athena"
    if name not in VALID_AGENTS:
        name = "athena"

    soul_path = _resolve_soul_path(name)
    memory_path = (
        (CORE_DIR / name / "MEMORY.md")
        if (CORE_DIR / name / "MEMORY.md").exists()
        else (AGENTS_DIR / name / "MEMORY.md")
    )

    soul = soul_path.read_text(encoding="utf-8") if soul_path else _DEFAULT_PROMPT
    memory_raw = memory_path.read_text(encoding="utf-8").strip() if memory_path.exists() else ""

    has_memory = any(
        line.strip() and not line.strip().startswith("#") and not line.strip().startswith("<!--")
        for line in memory_raw.splitlines()
    )
    memory_section = f"\n\n## Mémoire permanente\n{memory_raw}" if has_memory else ""
    common_section = f"\n\n## Règles communes\n{AGENTS_COMMON}" if AGENTS_COMMON else ""
    domain_ctx = _get_domain_context_for_agent()
    domain_section = f"\n\n{domain_ctx}" if domain_ctx else ""
    return f"{soul}{memory_section}{common_section}{domain_section}"


async def _build_affaire_context(db: AsyncSession, affaire_id: UUID) -> str:
    """Charge les métadonnées de l'affaire et les formate pour injection dans le prompt."""
    try:
        from apps.affaires.models import Affaire
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
        if getattr(affaire, "domain", None) and affaire.domain != "btp":
            parts.append(f"Domaine : {affaire.domain}")
        if getattr(affaire, "domain_metadata", None):
            for k, v in affaire.domain_metadata.items():
                parts.append(f"{k} : {v}")
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
    thread_id: str = "",
) -> AgentRun:
    """Exécute la boucle agentique et persiste le résultat."""
    t_start = time.monotonic()

    # Construire le system prompt
    system_prompt = _build_system_prompt(agent_name)

    # Injecter le contexte projet (typology, region, budget, phase, ABF, zones)
    affaire_context = await _build_affaire_context(db, affaire_id)
    if affaire_context:
        system_prompt += f"\n\n## Contexte projet\n{affaire_context}"

    # C5 — mémoire unifiée : projet + agence + session
    mem = await get_unified_memory(db, agent_name, affaire_id, thread_id=thread_id)
    if mem["projet"]:
        system_prompt += "\n\n## Mémoire projet — leçons apprises sur cette affaire\n" + "\n".join(
            f"- {m}" for m in mem["projet"]
        )
    if mem["agence"]:
        system_prompt += "\n\n## Patterns agence — bonnes pratiques réutilisables\n" + "\n".join(
            f"- {m}" for m in mem["agence"]
        )
    if mem["session"]:
        bits = []
        if mem["session"].get("last_answer_excerpt"):
            bits.append(f"Dernière réponse : {mem['session']['last_answer_excerpt'][:200]}")
        if mem["session"].get("phase_projet"):
            bits.append(f"Phase projet : {mem['session']['phase_projet']}")
        if mem["session"].get("domaine"):
            bits.append(f"Domaine : {mem['session']['domaine']}")
        if bits:
            system_prompt += "\n\n## Contexte session\n" + "\n".join(bits)

    run = AgentRun(
        affaire_id=affaire_id,
        user_id=user_id,
        instruction=instruction,
        status="running",
        steps=[],
    )
    db.add(run)
    await db.flush()  # obtenir l'id sans commit

    structlog.contextvars.bind_contextvars(run_id=str(run.id), run_type="agent", agent=agent_name)
    log.info("agent.start", affaire_id=str(affaire_id))

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": instruction},
    ]

    steps: list[dict] = []
    all_sources: list[dict] = []  # sources RAG collectées sur tous les appels d'outils
    final_answer: str | None = None
    llm_iterations: int = 0
    model = settings.effective_llm_model

    _LLM_AGENT_TIMEOUT = 90  # secondes — empêche un Ollama pendu de figer la boucle

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    async def _llm_react_call(msgs: list) -> object:
        from core.circuit_breaker import llm_breaker

        llm_breaker.check()  # fail-fast si Ollama est down
        try:
            result = await asyncio.wait_for(
                LlmService._get_client().chat.completions.create(
                    model=model,
                    messages=msgs,
                    tools=DEFINITIONS,
                    tool_choice="auto",
                    temperature=0.3,
                    max_tokens=2048,
                ),
                timeout=_LLM_AGENT_TIMEOUT,
            )
            llm_breaker.record_success()
            return result
        except Exception:
            llm_breaker.record_failure()
            raise

    try:
        for iteration in range(max_iterations):
            llm_iterations += 1
            time.monotonic()

            response = await _llm_react_call(messages)

            choice = response.choices[0]
            msg = choice.message

            # Ajouter la réponse du LLM aux messages
            messages.append(msg.model_dump(exclude_none=True))

            # Pas d'appel d'outil → réponse finale
            if not msg.tool_calls:
                final_answer = msg.content or ""
                break

            # Exécuter les appels d'outils en parallèle (asyncio.gather).
            # Les tools DB utilisent une session isolée quand le batch en contient
            # plusieurs, pour éviter les accès concurrents sur la même AsyncSession.
            async def _call_tool(tc) -> tuple:
                t_tool = time.monotonic()
                t_name = tc.function.name
                t_args = json.loads(tc.function.arguments or "{}")
                log.info(
                    "agent.tool_call",
                    run_id=str(run.id),
                    iteration=iteration,
                    tool=t_name,
                    parallel=len(msg.tool_calls) > 1,
                )
                if t_name in _DB_TOOLS and len(msg.tool_calls) > 1:
                    async with AsyncSessionLocal() as _iso_db:
                        out, srcs = await execute_tool(t_name, t_args, affaire_id, _iso_db)
                else:
                    out, srcs = await execute_tool(t_name, t_args, affaire_id, db)
                return tc, t_name, t_args, out, srcs, int((time.monotonic() - t_tool) * 1000)

            t_batch = time.monotonic()
            batch_results = await asyncio.gather(*[_call_tool(tc) for tc in msg.tool_calls], return_exceptions=True)

            for br in batch_results:
                if isinstance(br, Exception):
                    log.error("agent.tool_failed", error=str(br))
                    continue
                tc_r, tool_name, tool_args, tool_output, tool_sources, dur_ms = br

                # Dédupliquer les sources par chunk_id
                seen_chunks = {s["chunk_id"] for s in all_sources}
                for src in tool_sources:
                    if src["chunk_id"] not in seen_chunks:
                        all_sources.append(src)
                        seen_chunks.add(src["chunk_id"])

                steps.append(
                    {
                        "tool": tool_name,
                        "args": tool_args,
                        "output": tool_output[:1000],
                        "sources_count": len(tool_sources),
                        "duration_ms": dur_ms,
                    }
                )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc_r.id,
                        "content": tool_output,
                    }
                )

            if len(msg.tool_calls) > 1:
                log.info(
                    "agent.tools_parallel_done",
                    count=len(msg.tool_calls),
                    batch_ms=int((time.monotonic() - t_batch) * 1000),
                )

        else:
            # max_iterations atteint sans réponse finale
            final_answer = "Limite d'itérations atteinte. Voici ce que j'ai trouvé jusqu'ici :\n" + (
                steps[-1]["output"] if steps else "Aucune information collectée."
            )

        run.status = "completed"
        run.result = final_answer

    except Exception as exc:
        log.error("agent.run_failed", error=str(exc))
        run.status = "failed"
        run.error_message = str(exc)
        run.result = f"Erreur lors de l'exécution : {exc}"

    finally:
        run.steps = steps
        run.sources = all_sources
        run.iterations = llm_iterations
        run.duration_ms = int((time.monotonic() - t_start) * 1000)
        await db.commit()
        await db.refresh(run)
        structlog.contextvars.unbind_contextvars("run_id", "run_type", "agent")

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

            # create_task conserve une référence forte (évite le garbage-collect de ensure_future)
            task = asyncio.create_task(_store_memories_fallback())
            task.add_done_callback(lambda t: t.exception() if not t.cancelled() else None)

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
