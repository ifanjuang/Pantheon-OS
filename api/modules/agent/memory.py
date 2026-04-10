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

MEMORY_CATEGORIES = ("technique", "planning", "budget", "contractuel", "general")

_EXTRACT_PROMPT = """\
Tu es un assistant qui extrait des leçons d'apprentissage d'un run d'agent.

Agent : {agent_name}
Instruction initiale : {instruction}
Résultat produit : {result}

Extrait 1 à 3 leçons CONCRÈTES et RÉUTILISABLES pour de futurs runs du même agent
sur la même affaire. Chaque leçon doit être une phrase courte et actionnable.

Pour chaque leçon, indique sa catégorie :
- "technique"    : matériaux, DTU, faisabilité, détails constructifs
- "planning"     : délais, retards, jalons, ordonnancement
- "budget"       : coûts, dépassements, honoraires, situations
- "contractuel"  : obligations MOE, loi MOP, CCAG, marchés, ABF
- "general"      : tout le reste

Exemples de bonnes leçons :
- {{"lesson": "Le lot gros œuvre est systématiquement en retard de 3 semaines.", "category": "planning"}}
- {{"lesson": "Les documents CCTP sont fragmentés — chercher aussi dans le lot VRD.", "category": "technique"}}
- {{"lesson": "Le maître d'ouvrage demande des bilans hebdomadaires chaque lundi.", "category": "contractuel"}}

Réponds en JSON strict :
{{"lessons": [{{"lesson": "...", "category": "..."}}]}}

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
        # Parse JSON robuste par accolades équilibrées
        parsed: dict = {}
        depth, start = 0, None
        for i, ch in enumerate(content):
            if ch == "{":
                if start is None:
                    start = i
                depth += 1
            elif ch == "}" and start is not None:
                depth -= 1
                if depth == 0:
                    try:
                        parsed = json.loads(content[start:i + 1])
                    except json.JSONDecodeError:
                        start = None
                    break
        raw_lessons = parsed.get("lessons", [])

        # Normaliser : accepter l'ancien format (list[str]) et le nouveau (list[dict])
        lessons: list[dict] = []
        for item in raw_lessons[:3]:
            if isinstance(item, str):
                lessons.append({"lesson": item.strip(), "category": "general"})
            elif isinstance(item, dict) and item.get("lesson"):
                cat = item.get("category", "general")
                if cat not in MEMORY_CATEGORIES:
                    cat = "general"
                lessons.append({"lesson": item["lesson"].strip(), "category": cat})

        # Charger les leçons existantes valides pour dédoublonnage
        existing_rows: list[AgentMemory] = []
        if affaire_id:
            rows = await db.execute(
                select(AgentMemory).where(
                    AgentMemory.agent_name == agent_name,
                    AgentMemory.affaire_id == affaire_id,
                    AgentMemory.valid_until.is_(None),
                )
            )
            existing_rows = list(rows.scalars().all())
        existing_texts = {m.lesson.strip().lower() for m in existing_rows}

        count = 0
        for item in lessons:
            text = item["lesson"]
            if len(text) < 10 or text.lower() in existing_texts:
                continue
            new_memory = AgentMemory(
                agent_name=agent_name,
                affaire_id=affaire_id,
                source_run_id=run_id,
                lesson=text,
                category=item["category"],
            )
            db.add(new_memory)
            existing_texts.add(text.lower())
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
    category: str | None = None,
) -> list[str]:
    """
    Retourne les N leçons **valides** les plus récentes pour cet agent sur cette affaire.
    Filtre optionnel par catégorie (technique, planning, budget, contractuel, general).
    Retourne une liste vide si aucun souvenir ou en cas d'erreur.
    """
    if not affaire_id:
        return []
    try:
        stmt = (
            select(AgentMemory.lesson)
            .where(
                AgentMemory.agent_name == agent_name,
                AgentMemory.affaire_id == affaire_id,
                AgentMemory.valid_until.is_(None),  # ne retourner que les faits valides
            )
            .order_by(AgentMemory.created_at.desc())
            .limit(limit)
        )
        if category and category in MEMORY_CATEGORIES:
            stmt = stmt.where(AgentMemory.category == category)
        result = await db.execute(stmt)
        lessons = [row[0] for row in result.all()]
        return list(reversed(lessons))  # chronologique : plus ancien en premier
    except Exception as exc:
        log.warning("agent.memory.get_failed", agent=agent_name, error=str(exc))
        return []


async def consolidate_memories(
    db: AsyncSession,
    agent_name: str | None = None,
    min_lessons: int = 5,
) -> int:
    """
    Consolide les leçons brutes en patterns de plus haut niveau.

    Pour chaque couple (agent, affaire) ayant >= min_lessons leçons valides :
      1. Regroupe les leçons par catégorie
      2. Demande au LLM de fusionner en 1-2 patterns synthétiques
      3. Crée les nouveaux patterns et marque les anciens comme superseded

    Retourne le nombre total de consolidations effectuées.
    Appelé périodiquement via ARQ cron (1x/jour).
    """
    from sqlalchemy import func

    # Trouver les couples (agent, affaire) avec assez de leçons
    stmt = (
        select(
            AgentMemory.agent_name,
            AgentMemory.affaire_id,
            AgentMemory.category,
            func.count(AgentMemory.id).label("cnt"),
        )
        .where(
            AgentMemory.valid_until.is_(None),
            AgentMemory.superseded_by.is_(None),
        )
        .group_by(AgentMemory.agent_name, AgentMemory.affaire_id, AgentMemory.category)
        .having(func.count(AgentMemory.id) >= min_lessons)
    )
    if agent_name:
        stmt = stmt.where(AgentMemory.agent_name == agent_name)

    groups = (await db.execute(stmt)).all()
    total_consolidated = 0

    for group in groups:
        a_name, a_id, category, count = group.agent_name, group.affaire_id, group.category, group.cnt
        try:
            # Charger les leçons de ce groupe
            lessons_rows = await db.execute(
                select(AgentMemory)
                .where(
                    AgentMemory.agent_name == a_name,
                    AgentMemory.affaire_id == a_id,
                    AgentMemory.category == category,
                    AgentMemory.valid_until.is_(None),
                    AgentMemory.superseded_by.is_(None),
                )
                .order_by(AgentMemory.created_at)
            )
            lessons = list(lessons_rows.scalars().all())
            if len(lessons) < min_lessons:
                continue

            lessons_text = "\n".join(f"- {m.lesson}" for m in lessons)

            consolidation_prompt = (
                f"Agent : {a_name}\n"
                f"Catégorie : {category or 'general'}\n"
                f"Nombre de leçons : {len(lessons)}\n\n"
                f"Leçons brutes :\n{lessons_text}\n\n"
                "Fusionne ces leçons en 1 ou 2 patterns synthétiques de haut niveau.\n"
                "Chaque pattern doit capturer l'essence de plusieurs leçons.\n"
                "Réponds en JSON strict :\n"
                '{"patterns": [{"lesson": "...", "category": "..."}]}'
            )

            response = await LlmService._get_client().chat.completions.create(
                model=settings.effective_llm_model,
                messages=[{"role": "user", "content": consolidation_prompt}],
                temperature=0.1,
                max_tokens=400,
            )
            content = response.choices[0].message.content or "{}"

            # Parse JSON
            parsed: dict = {}
            depth, start = 0, None
            for i, ch in enumerate(content):
                if ch == "{":
                    if start is None:
                        start = i
                    depth += 1
                elif ch == "}" and start is not None:
                    depth -= 1
                    if depth == 0:
                        try:
                            parsed = json.loads(content[start:i + 1])
                        except json.JSONDecodeError:
                            start = None
                        break

            patterns = parsed.get("patterns", [])
            if not patterns:
                continue

            # Créer les nouveaux patterns et marquer les anciens
            from datetime import datetime, timezone
            now = datetime.now(timezone.utc)

            for pattern_data in patterns[:2]:
                p_text = pattern_data.get("lesson", "").strip()
                p_cat = pattern_data.get("category", category)
                if not p_text or len(p_text) < 10:
                    continue
                if p_cat not in MEMORY_CATEGORIES:
                    p_cat = category or "general"

                new_memory = AgentMemory(
                    agent_name=a_name,
                    affaire_id=a_id,
                    lesson=p_text,
                    scope="projet" if a_id else "agence",
                    category=p_cat,
                )
                db.add(new_memory)
                await db.flush()

                # Marquer les anciennes leçons comme superseded
                for old in lessons:
                    old.valid_until = now
                    old.superseded_by = new_memory.id

                total_consolidated += len(lessons)

            await db.commit()
            log.info(
                "agent.memory.consolidated",
                agent=a_name,
                affaire_id=str(a_id),
                category=category,
                old_count=len(lessons),
                new_patterns=len(patterns),
            )

        except Exception as exc:
            log.warning(
                "agent.memory.consolidation_failed",
                agent=a_name,
                category=category,
                error=str(exc),
            )
            await db.rollback()
            continue

    return total_consolidated


async def invalidate_memory(
    db: AsyncSession,
    memory_id: UUID,
    superseded_by_id: UUID | None = None,
) -> bool:
    """
    Marque une leçon comme obsolète (valid_until = now).
    Si superseded_by_id est fourni, crée le lien vers la leçon de remplacement.
    """
    from datetime import datetime, timezone
    memory = await db.get(AgentMemory, memory_id)
    if not memory or memory.valid_until is not None:
        return False
    memory.valid_until = datetime.now(timezone.utc)
    if superseded_by_id:
        memory.superseded_by = superseded_by_id
    await db.commit()
    log.info("agent.memory.invalidated", memory_id=str(memory_id), superseded_by=str(superseded_by_id))
    return True
