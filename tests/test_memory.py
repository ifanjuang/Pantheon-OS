"""
Tests mémoire dynamique des agents — extraction, consolidation, invalidation.
LLM mocké pour tester la logique sans appels réels.
"""
import uuid
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from modules.agent.models import AgentMemory


def _mock_llm_response(content: str):
    """Crée un mock de réponse OpenAI chat completion."""
    mock = MagicMock()
    mock.choices = [MagicMock()]
    mock.choices[0].message.content = content
    return mock


class TestExtractAndStoreMemories:
    async def test_extracts_lessons(self, db, affaire):
        """L'extraction stocke des leçons en DB."""
        llm_response = json.dumps({
            "lessons": [
                {"lesson": "Le lot CVC est systématiquement livré en retard.", "category": "planning"},
                {"lesson": "Les DTU béton sont dans le CCTP lot gros oeuvre.", "category": "technique"},
            ]
        })

        with patch("modules.agent.memory.LlmService") as MockLlm:
            mock_client = MagicMock()
            mock_client.chat.completions.create = AsyncMock(
                return_value=_mock_llm_response(llm_response)
            )
            MockLlm._get_client.return_value = mock_client

            from modules.agent.memory import extract_and_store_memories
            run_id = uuid.uuid4()
            count = await extract_and_store_memories(
                agent_name="athena",
                instruction="Analyse les risques du projet",
                result="Le lot CVC est en retard. Les DTU béton sont dans le CCTP." * 5,
                affaire_id=affaire.id,
                run_id=run_id,
                db=db,
            )

            assert count == 2
            from sqlalchemy import select
            rows = await db.execute(
                select(AgentMemory).where(AgentMemory.source_run_id == run_id)
            )
            memories = rows.scalars().all()
            assert len(memories) == 2
            categories = {m.category for m in memories}
            assert "planning" in categories
            assert "technique" in categories

    async def test_deduplicates_existing(self, db, affaire):
        """Les leçons identiques ne sont pas stockées en double."""
        existing = AgentMemory(
            agent_name="athena",
            affaire_id=affaire.id,
            source_run_id=uuid.uuid4(),
            lesson="Le lot CVC est en retard.",
            category="planning",
        )
        db.add(existing)
        await db.flush()

        llm_response = json.dumps({
            "lessons": [
                {"lesson": "Le lot CVC est en retard.", "category": "planning"},
                {"lesson": "Nouvelle leçon unique.", "category": "general"},
            ]
        })

        with patch("modules.agent.memory.LlmService") as MockLlm:
            mock_client = MagicMock()
            mock_client.chat.completions.create = AsyncMock(
                return_value=_mock_llm_response(llm_response)
            )
            MockLlm._get_client.return_value = mock_client

            from modules.agent.memory import extract_and_store_memories
            count = await extract_and_store_memories(
                agent_name="athena",
                instruction="Test dédup",
                result="Contenu suffisamment long pour passer le seuil de 50 caractères minimum.",
                affaire_id=affaire.id,
                run_id=uuid.uuid4(),
                db=db,
            )
            assert count == 1  # seule la nouvelle leçon est ajoutée

    async def test_skips_short_result(self, db, affaire):
        """Résultat trop court -> pas d'extraction."""
        from modules.agent.memory import extract_and_store_memories
        count = await extract_and_store_memories(
            agent_name="athena",
            instruction="Test",
            result="Court",
            affaire_id=affaire.id,
            run_id=uuid.uuid4(),
            db=db,
        )
        assert count == 0


class TestGetAgentMemories:
    async def test_returns_recent_lessons(self, db, affaire):
        for i in range(3):
            db.add(AgentMemory(
                agent_name="themis",
                affaire_id=affaire.id,
                source_run_id=uuid.uuid4(),
                lesson=f"Leçon numéro {i}",
                category="contractuel",
            ))
        await db.flush()

        from modules.agent.memory import get_agent_memories
        lessons = await get_agent_memories(db, "themis", affaire.id, limit=10)
        assert len(lessons) == 3
        assert "Leçon numéro 0" in lessons[0]

    async def test_filters_invalidated(self, db, affaire):
        """Les leçons avec valid_until ne sont pas retournées."""
        valid = AgentMemory(
            agent_name="athena", affaire_id=affaire.id,
            source_run_id=uuid.uuid4(), lesson="Valide",
        )
        invalid = AgentMemory(
            agent_name="athena", affaire_id=affaire.id,
            source_run_id=uuid.uuid4(), lesson="Obsolète",
            valid_until=datetime.now(timezone.utc),
        )
        db.add_all([valid, invalid])
        await db.flush()

        from modules.agent.memory import get_agent_memories
        lessons = await get_agent_memories(db, "athena", affaire.id)
        assert len(lessons) == 1
        assert "Valide" in lessons[0]

    async def test_returns_empty_without_affaire(self, db):
        from modules.agent.memory import get_agent_memories
        lessons = await get_agent_memories(db, "athena", None)
        assert lessons == []


class TestInvalidateMemory:
    async def test_invalidate_sets_valid_until(self, db, affaire):
        memory = AgentMemory(
            agent_name="athena", affaire_id=affaire.id,
            source_run_id=uuid.uuid4(), lesson="Ancienne leçon",
        )
        db.add(memory)
        await db.flush()

        from modules.agent.memory import invalidate_memory
        result = await invalidate_memory(db, memory.id)
        assert result is True
        await db.refresh(memory)
        assert memory.valid_until is not None

    async def test_invalidate_with_superseded_by(self, db, affaire):
        old = AgentMemory(
            agent_name="athena", affaire_id=affaire.id,
            source_run_id=uuid.uuid4(), lesson="Ancienne",
        )
        new = AgentMemory(
            agent_name="athena", affaire_id=affaire.id,
            source_run_id=uuid.uuid4(), lesson="Nouvelle",
        )
        db.add_all([old, new])
        await db.flush()

        from modules.agent.memory import invalidate_memory
        result = await invalidate_memory(db, old.id, superseded_by_id=new.id)
        assert result is True
        await db.refresh(old)
        assert old.superseded_by == new.id

    async def test_invalidate_already_invalid_returns_false(self, db, affaire):
        memory = AgentMemory(
            agent_name="athena", affaire_id=affaire.id,
            source_run_id=uuid.uuid4(), lesson="Déjà obsolète",
            valid_until=datetime.now(timezone.utc),
        )
        db.add(memory)
        await db.flush()

        from modules.agent.memory import invalidate_memory
        result = await invalidate_memory(db, memory.id)
        assert result is False


class TestConsolidateMemories:
    async def test_consolidation_merges_lessons(self, db, affaire):
        """5+ leçons d'un même groupe -> consolidation en patterns."""
        for i in range(6):
            db.add(AgentMemory(
                agent_name="chronos",
                affaire_id=affaire.id,
                source_run_id=uuid.uuid4(),
                lesson=f"Le lot {i} a un retard de {i} jours.",
                category="planning",
            ))
        await db.flush()

        consolidation_response = json.dumps({
            "patterns": [
                {"lesson": "Les lots du projet ont des retards systématiques croissants.", "category": "planning"},
            ]
        })

        with patch("modules.agent.memory.LlmService") as MockLlm:
            mock_client = MagicMock()
            mock_client.chat.completions.create = AsyncMock(
                return_value=_mock_llm_response(consolidation_response)
            )
            MockLlm._get_client.return_value = mock_client

            from modules.agent.memory import consolidate_memories
            total = await consolidate_memories(db, agent_name="chronos", min_lessons=5)

            assert total == 6  # 6 anciennes leçons consolidées

            # Vérifier qu'un nouveau pattern existe
            from sqlalchemy import select
            valid = await db.execute(
                select(AgentMemory).where(
                    AgentMemory.agent_name == "chronos",
                    AgentMemory.affaire_id == affaire.id,
                    AgentMemory.valid_until.is_(None),
                    AgentMemory.superseded_by.is_(None),
                )
            )
            active = valid.scalars().all()
            assert len(active) == 1
            assert "systématiques" in active[0].lesson

    async def test_consolidation_skips_below_threshold(self, db, affaire):
        """Moins de min_lessons -> pas de consolidation."""
        for i in range(3):
            db.add(AgentMemory(
                agent_name="athena",
                affaire_id=affaire.id,
                source_run_id=uuid.uuid4(),
                lesson=f"Leçon courte {i}",
                category="general",
            ))
        await db.flush()

        from modules.agent.memory import consolidate_memories
        total = await consolidate_memories(db, agent_name="athena", min_lessons=5)
        assert total == 0
