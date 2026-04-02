"""
memory.py — extraction et récupération de la mémoire dynamique des agents.

Après chaque run d'agent :
  extract_and_store_memories() demande au LLM d'extraire 1-3 leçons clés
  puis les stocke dans agent_memory (agent_name, affaire_id, lesson).

Avant chaque run :
  get_agent_memories() retourne les N dernières leçons pour injecter
  dans le system prompt.
"""
import asyncio
import json
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.llm_service import LlmService
from core.settings import settings
from modules.agent.models import AgentMemory

log = get_logger("agent.memory")

_EXTRACT_PROMPT = """\
Tu es un assistant qui extrait des leçons d'apprentissage d'un run d'agent.

Agent : {agent_name}
Instruction initiale : {instruction}
Résultat produit : {result}

Extrait 1 à 3 leçons CONCRÈTES et RÉUTILISABLES pour de futurs runs du même agent
sur la même affaire. Chaque leçon doit être une phrase courte et actionnable.

Exemples de bonnes leçons :
- "Le lot gros œuvre est systématiquement en retard de 3 semaines sur cette affaire."
- "Les documents CCTP sont fragmentés — chercher aussi dans le lot 'VRD'."
- "Le maître d'ouvrage demande des bilans hebdomadaires chaque lundi."

Réponds en JSON strict :
{{"lessons": ["leçon 1", "leçon 2"]}}

Si le run ne contient aucune leçon réutilisable, réponds :
{{"lessons": []}}
"""


async def extract_and_store_memories(
    agent_name: str,
    instruction: str,
    result: str,
    affaire_id: UUID | None,
    run_id: UUID,
    db: AsyncSession,
) -> int:
    """
    Appelle le LLM pour extraire des leçons du run et les stocke en DB.
    Retourne le nombre de leçons créées.
    Silencieux en cas d'erreur — ne doit jamais bloquer le run principal.
    """
    if not result or len(result.strip()) < 50:
        return 0

    try:
        prompt = _EXTRACT_PROMPT.format(
            agent_name=agent_name,
            instruction=instruction[:500],
            result=result[:1500],
        )
        response = await LlmService._get_client().chat.completions.create(
            model=settings.effective_llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=512,
        )
        content = response.choices[0].message.content or "{}"
        # Extraction JSON robuste
        start = content.find("{")
        end = content.rfind("}") + 1
        parsed = json.loads(content[start:end]) if start >= 0 and end > start else {}
        lessons = parsed.get("lessons", [])

        count = 0
        for lesson in lessons[:3]:  # maximum 3 leçons par run
            if lesson and len(lesson.strip()) > 10:
                db.add(AgentMemory(
                    agent_name=agent_name,
                    affaire_id=affaire_id,
                    source_run_id=run_id,
                    lesson=lesson.strip(),
                ))
                count += 1

        if count:
            await db.commit()
            log.info("agent.memory.stored", agent=agent_name, lessons=count, run_id=str(run_id))

        return count

    except Exception as exc:
        log.warning("agent.memory.extract_failed", agent=agent_name, error=str(exc))
        return 0


async def get_agent_memories(
    db: AsyncSession,
    agent_name: str,
    affaire_id: UUID | None,
    limit: int = 6,
) -> list[str]:
    """
    Retourne les N leçons les plus récentes pour cet agent sur cette affaire.
    Retourne une liste vide si aucun souvenir ou en cas d'erreur.
    """
    if not affaire_id:
        return []
    try:
        result = await db.execute(
            select(AgentMemory.lesson)
            .where(
                AgentMemory.agent_name == agent_name,
                AgentMemory.affaire_id == affaire_id,
            )
            .order_by(AgentMemory.created_at.desc())
            .limit(limit)
        )
        lessons = [row[0] for row in result.all()]
        return list(reversed(lessons))  # chronologique : plus ancien en premier
    except Exception as exc:
        log.warning("agent.memory.get_failed", agent=agent_name, error=str(exc))
        return []
