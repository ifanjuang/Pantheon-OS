"""
Orchestra — nœuds de synthèse et mémoire (M4).

  synthesize    : un agent produit la réponse finale consolidée
  write_memories: persiste les mémoires projet/agence/wiki/fonctionnelle
"""
from uuid import UUID

from ._shared import (
    OrchestraState,
    _run_agent_isolated,
    log,
)

# ── Prompt synthèse ──────────────────────────────────────────────────

_SYNTHESIS_PROMPT_TEMPLATE = """\
{synthesis_instruction}

## Demande originale
{instruction}

## Analyses des agents
{results}

Produis une réponse finale construite, structurée, en français.
"""


# ── Nœuds LangGraph ──────────────────────────────────────────────────

async def synthesize(state: OrchestraState) -> dict:
    """Phase 4b — un agent produit la synthèse finale."""
    affaire_uuid = UUID(state["affaire_id"])
    user_uuid = UUID(state["user_id"]) if state.get("user_id") else None

    synthesis_agent = state.get("synthesis_agent", "mnemosyne")
    results_text = "\n\n".join(
        f"### {agent}\n{result}"
        for agent, result in state["agent_results"].items()
    )
    synthesis_instruction = _SYNTHESIS_PROMPT_TEMPLATE.format(
        synthesis_instruction=state.get("instruction", "Synthétise les analyses."),
        instruction=state["instruction"],
        results=results_text,
    )
    log.info("orchestra.synthesize", agent=synthesis_agent)

    _, final_answer, run_id = await _run_agent_isolated(
        agent=synthesis_agent,
        instruction=synthesis_instruction,
        affaire_id=affaire_uuid,
        user_id=user_uuid,
    )
    agent_run_ids = list(state["agent_run_ids"]) + [run_id]
    return {"final_answer": final_answer, "agent_run_ids": agent_run_ids}


async def write_memories(state: OrchestraState) -> dict:
    """Écrit la mémoire orchestre (Hestia/Mnémosyne) et promeut en wiki pour C4/C5.

    Les mémoires par agent sont déjà extraites par run_agent() —
    ce nœud se concentre sur la mémoire de synthèse globale.
    """
    from modules.agent.models import AgentMemory
    from database import AsyncSessionLocal

    affaire_id_val = UUID(state["affaire_id"]) if state.get("affaire_id") else None
    final_answer = state.get("final_answer", "")
    criticite = state.get("criticite", "C2")
    memories_count = 0
    wiki_page_id = ""

    if not final_answer or len(final_answer.strip()) < 50:
        return {"memories_written": 0, "wiki_page_id": ""}

    # ── 1. Mémoire de synthèse orchestre ──────────────────────────────
    # Hestia (projet) stocke la leçon liée à cette affaire
    # Mnémosyne (agence) stocke un pattern réutilisable si C4/C5
    try:
        async with AsyncSessionLocal() as db:
            lesson_text = (
                f"Orchestration {criticite} — "
                f"{state['instruction'][:200]} → "
                f"Verdict agents : {state.get('score_verdict', 'non scoré')}. "
                f"Agents impliqués : {', '.join(state.get('agent_results', {}).keys())}."
            )
            hestia_mem = AgentMemory(
                agent_name="hestia",
                affaire_id=affaire_id_val,
                lesson=lesson_text[:500],
                scope="projet",
                category="general",
            )
            db.add(hestia_mem)
            memories_count += 1

            if criticite in ("C4", "C5"):
                pattern_text = (
                    f"Pattern {criticite} : {state['instruction'][:150]}. "
                    f"Score : {state.get('score_total', '?')}/100 "
                    f"({state.get('score_verdict', 'non scoré')}). "
                    f"Agents : {', '.join(state.get('agent_results', {}).keys())}."
                )
                mnemosyne_mem = AgentMemory(
                    agent_name="mnemosyne",
                    affaire_id=None,
                    lesson=pattern_text[:500],
                    scope="agence",
                    category="general",
                )
                db.add(mnemosyne_mem)
                memories_count += 1

            await db.commit()
    except Exception as exc:
        log.error("orchestra.memories_failed", error=str(exc))

    # ── 2. Promotion wiki pour C4/C5 ──────────────────────────────────
    if criticite in ("C4", "C5") and affaire_id_val:
        try:
            from modules.wiki.service import WikiService

            async with AsyncSessionLocal() as db:
                page = await WikiService.create_page(
                    db,
                    titre=state["instruction"][:512],
                    contenu_md=final_answer,
                    scope="projet",
                    affaire_id=affaire_id_val,
                    tags=[criticite, f"score:{state.get('score_total', '?')}"],
                    criticite=criticite,
                    score=state.get("score_total"),
                    auto_validate=False,
                )
                wiki_page_id = str(page.id)
            log.info("orchestra.wiki_promoted", page_id=wiki_page_id, criticite=criticite)
        except Exception as exc:
            log.error("orchestra.wiki_promote_failed", error=str(exc))

    # ── 3. Mémoire fonctionnelle (M3) ─────────────────────────────────
    thread_id = state.get("thread_id") or ""
    if thread_id:
        try:
            from modules.memory.service import FunctionalMemoryService
            await FunctionalMemoryService.set_context(
                thread_id,
                "last_verdict",
                {
                    "criticite": criticite,
                    "score_verdict": state.get("score_verdict", ""),
                    "score_total": state.get("score_total"),
                    "veto_severity": state.get("veto_severity", ""),
                },
                ttl=3600,
            )
            await FunctionalMemoryService.set_context(
                thread_id,
                "last_answer_excerpt",
                final_answer[:400],
                ttl=3600,
            )
        except Exception as exc:
            log.debug("orchestra.functional_memory_skipped", error=str(exc))

    log.info("orchestra.memories_written", count=memories_count, wiki=bool(wiki_page_id))
    return {"memories_written": memories_count, "wiki_page_id": wiki_page_id}
