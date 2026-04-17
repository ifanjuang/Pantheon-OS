"""
Tests modules/guards — guards purs (criticality, loop) + veto séquentiel
+ criticality_guard_hybrid (couche AI).

Les fonctions pures (criticality_guard, loop_guard) sont testées sans DB ni LLM.
Les tests hybrid et veto utilisent des mocks LLM pour tester la logique de routing.
"""
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from modules.guards.schemas import CriticalityImpacts, CriticalityVerdict
from modules.guards.service import GuardsService, MAX_COMPLEMENTS_BY_CRITICITE


# ── criticality_guard (règle pure, 0 LLM) ───────────────────────────────────

class TestCriticalityGuard:
    def test_default_no_impact_returns_c1(self):
        verdict = GuardsService.criticality_guard(CriticalityImpacts())
        assert verdict.criticite == "C1"
        assert "default=C1" in verdict.triggers

    def test_cost_above_50k_returns_c5(self):
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(impact_cout=60_000)
        )
        assert verdict.criticite == "C5"
        assert any("cout>" in t for t in verdict.triggers)

    def test_cost_above_10k_returns_c4(self):
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(impact_cout=15_000)
        )
        assert verdict.criticite == "C4"

    def test_cost_above_2k_returns_c3(self):
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(impact_cout=3_000)
        )
        assert verdict.criticite == "C3"

    def test_delay_above_30j_returns_c5(self):
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(impact_delai=45)
        )
        assert verdict.criticite == "C5"

    def test_delay_above_10j_returns_c4(self):
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(impact_delai=15)
        )
        assert verdict.criticite == "C4"

    def test_delay_above_3j_returns_c3(self):
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(impact_delai=5)
        )
        assert verdict.criticite == "C3"

    def test_severity_litige_returns_c5(self):
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(severity="litige")
        )
        assert verdict.criticite == "C5"

    def test_severity_contrat_returns_c4(self):
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(severity="contrat")
        )
        assert verdict.criticite == "C4"

    def test_irreversible_forces_min_c4(self):
        # Impact faible mais irréversible → au moins C4
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(impact_cout=500, reversible=False)
        )
        assert verdict.criticite in ("C4", "C5")
        assert "irreversible" in verdict.triggers

    def test_max_rule_wins(self):
        # Coût C3 mais délai C5 → C5
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(impact_cout=3_000, impact_delai=45)
        )
        assert verdict.criticite == "C5"

    def test_intent_decision_engageante_returns_c4(self):
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(intent="decision_engageante")
        )
        assert verdict.criticite == "C4"

    def test_intent_question_returns_c2(self):
        verdict = GuardsService.criticality_guard(
            CriticalityImpacts(intent="question")
        )
        assert verdict.criticite == "C2"

    def test_verdict_source_is_rules_by_default(self):
        verdict = GuardsService.criticality_guard(CriticalityImpacts(impact_cout=3_000))
        assert verdict.source == "rules"
        assert verdict.ai_reasoning == ""


# ── criticality_guard_hybrid (couche 0+1 règles + couche 2 AI) ───────────────

@pytest.mark.asyncio
class TestCriticalityGuardHybrid:
    """La couche AI ne s'active que sur les cas ambigus (C2/C3/C4) + contexte."""

    async def test_c5_from_rules_skips_ai(self):
        """C5 déterministe → pas d'appel LLM, source=rules."""
        impacts = CriticalityImpacts(impact_cout=60_000)
        with patch("modules.guards.service.LlmService.extract") as mock_extract:
            verdict = await GuardsService.criticality_guard_hybrid(impacts, context="quelque chose")
        mock_extract.assert_not_called()
        assert verdict.criticite == "C5"
        assert verdict.source == "rules"

    async def test_no_context_skips_ai(self):
        """Sans contexte → pas d'appel LLM même si c'est C3."""
        impacts = CriticalityImpacts(impact_cout=3_000)
        with patch("modules.guards.service.LlmService.extract") as mock_extract:
            verdict = await GuardsService.criticality_guard_hybrid(impacts, context="")
        mock_extract.assert_not_called()
        assert verdict.criticite == "C3"
        assert verdict.source == "rules"

    async def test_c1_no_context_skips_ai(self):
        """C1 sans contexte → source=rules."""
        impacts = CriticalityImpacts()
        with patch("modules.guards.service.LlmService.extract") as mock_extract:
            verdict = await GuardsService.criticality_guard_hybrid(impacts)
        mock_extract.assert_not_called()
        assert verdict.criticite == "C1"

    async def test_ai_upgrades_c3_to_c4(self):
        """Règles donnent C3, AI détecte litige → upgrade C4."""
        impacts = CriticalityImpacts(impact_cout=3_000)

        mock_ai = MagicMock()
        mock_ai.criticite = "C4"
        mock_ai.reasoning = "Risque de litige contractuel non capturé par les règles financières."

        with patch("modules.guards.service.LlmService.extract", new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_ai
            verdict = await GuardsService.criticality_guard_hybrid(
                impacts,
                context="L'entreprise refuse de signer le PV de réception. Le MOA menace d'un litige.",
            )

        assert verdict.criticite == "C4"
        assert verdict.source == "hybrid"
        assert "ai_upgrade:C3→C4" in verdict.triggers
        assert verdict.ai_reasoning != ""

    async def test_ai_never_downgrades(self):
        """AI propose C2 mais règles donnent C3 → on garde C3."""
        impacts = CriticalityImpacts(impact_cout=3_000)

        mock_ai = MagicMock()
        mock_ai.criticite = "C2"
        mock_ai.reasoning = "Situation banale."

        with patch("modules.guards.service.LlmService.extract", new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_ai
            verdict = await GuardsService.criticality_guard_hybrid(
                impacts,
                context="Situation standard de chantier.",
            )

        assert verdict.criticite == "C3"
        assert "ai_upgrade" not in " ".join(verdict.triggers)

    async def test_ai_failure_falls_back_to_rules(self):
        """Erreur LLM → fallback sur résultat des règles, pas d'exception."""
        impacts = CriticalityImpacts(impact_delai=15)  # C4 par les règles

        with patch(
            "modules.guards.service.LlmService.extract",
            new_callable=AsyncMock,
            side_effect=RuntimeError("LLM timeout"),
        ):
            verdict = await GuardsService.criticality_guard_hybrid(
                impacts,
                context="Contexte complexe avec retard critique.",
            )

        assert verdict.criticite == "C4"
        assert verdict.source == "rules"

    async def test_ai_upgrades_c2_to_c5_on_safety(self):
        """Règles donnent C2, AI détecte danger structurel → C5."""
        impacts = CriticalityImpacts(intent="question")

        mock_ai = MagicMock()
        mock_ai.criticite = "C5"
        mock_ai.reasoning = "Danger structurel identifié : ferraillage non conforme sous charge."

        with patch("modules.guards.service.LlmService.extract", new_callable=AsyncMock) as mock_extract:
            mock_extract.return_value = mock_ai
            verdict = await GuardsService.criticality_guard_hybrid(
                impacts,
                context="Le BE structure signale un risque d'effondrement sur le lot charpente.",
            )

        assert verdict.criticite == "C5"
        assert verdict.source == "hybrid"


# ── loop_guard (règle pure, 0 LLM) ──────────────────────────────────────────

class TestLoopGuard:
    def test_first_iteration_should_continue(self):
        verdict = GuardsService.loop_guard({}, max_complements=1)
        assert verdict.should_continue is True
        assert verdict.iteration == 0

    def test_complement_done_stops(self):
        verdict = GuardsService.loop_guard({"complement_done": True}, max_complements=1)
        assert verdict.should_continue is False

    def test_complement_count_respected(self):
        verdict = GuardsService.loop_guard({"complement_count": 2}, max_complements=2)
        assert verdict.should_continue is False

    def test_below_max_continues(self):
        verdict = GuardsService.loop_guard({"complement_count": 1}, max_complements=3)
        assert verdict.should_continue is True

    def test_zero_max_always_stops(self):
        verdict = GuardsService.loop_guard({}, max_complements=0)
        assert verdict.should_continue is False


# ── MAX_COMPLEMENTS_BY_CRITICITE ─────────────────────────────────────────────

class TestMaxComplements:
    def test_c1_c2_zero(self):
        assert MAX_COMPLEMENTS_BY_CRITICITE["C1"] == 0
        assert MAX_COMPLEMENTS_BY_CRITICITE["C2"] == 0

    def test_c3_one(self):
        assert MAX_COMPLEMENTS_BY_CRITICITE["C3"] == 1

    def test_c4_two(self):
        assert MAX_COMPLEMENTS_BY_CRITICITE["C4"] == 2

    def test_c5_three(self):
        assert MAX_COMPLEMENTS_BY_CRITICITE["C5"] == 3


# ── veto_patterns (couche 0 — regex, 0 LLM) ─────────────────────────────────

class TestVetoPatterns:
    def test_themis_hors_mission_detected(self):
        from modules.guards.veto_patterns import fast_veto_check
        output = "Cette demande est clairement hors mission MOE. Je m'oppose formellement."
        result = fast_veto_check("themis", output)
        assert result is not None
        assert result.veto is True
        assert result.severity == "bloquant"

    def test_hephaistos_infaisable_detected(self):
        from modules.guards.veto_patterns import fast_veto_check
        output = "Ce montage est techniquement infaisable selon les DTU en vigueur."
        result = fast_veto_check("hephaistos", output)
        assert result is not None
        assert result.veto is True

    def test_no_veto_returns_none(self):
        from modules.guards.veto_patterns import fast_veto_check
        output = "L'analyse indique quelques points d'attention mais rien de bloquant."
        result = fast_veto_check("themis", output)
        assert result is None

    def test_short_output_returns_none(self):
        from modules.guards.veto_patterns import fast_veto_check
        result = fast_veto_check("themis", "ok")
        assert result is None


# ── extract_and_store_memories — scope + promotable ──────────────────────────

class TestMemoryPromotion:
    async def test_promotable_lesson_creates_agence_memory(self, db, affaire):
        """Une leçon promotable crée aussi une entrée scope=agence pour Mnémosyne."""
        import uuid, json
        from unittest.mock import AsyncMock, MagicMock, patch
        from modules.agent.models import AgentMemory
        from sqlalchemy import select

        llm_response = json.dumps({
            "lessons": [
                {
                    "lesson": "En zone ABF, tout changement de façade exige un avis préalable.",
                    "category": "contractuel",
                    "promotable": True,
                },
                {
                    "lesson": "Le lot CVC de ce projet est livré en retard.",
                    "category": "planning",
                    "promotable": False,
                },
            ]
        })

        with patch("modules.agent.memory.LlmService") as MockLlm:
            mock_client = MagicMock()
            mock_client.chat.completions.create = AsyncMock(
                return_value=MagicMock(
                    choices=[MagicMock(message=MagicMock(content=llm_response))]
                )
            )
            MockLlm._get_client.return_value = mock_client

            from modules.agent.memory import extract_and_store_memories
            run_id = uuid.uuid4()
            await extract_and_store_memories(
                agent_name="themis",
                instruction="Vérifie la conformité réglementaire",
                result="Zone ABF confirmée. Le lot CVC est en retard de 3 semaines." * 4,
                affaire_id=affaire.id,
                run_id=run_id,
                db=db,
            )

        # Vérifier les mémoires projet (2 leçons)
        projet_rows = await db.execute(
            select(AgentMemory).where(
                AgentMemory.source_run_id == run_id,
                AgentMemory.scope == "projet",
            )
        )
        projet_mems = projet_rows.scalars().all()
        assert len(projet_mems) == 2

        # Vérifier la promotion agence (1 seule leçon promotable)
        agence_rows = await db.execute(
            select(AgentMemory).where(
                AgentMemory.source_run_id == run_id,
                AgentMemory.scope == "agence",
                AgentMemory.agent_name == "mnemosyne",
            )
        )
        agence_mems = agence_rows.scalars().all()
        assert len(agence_mems) == 1
        assert "ABF" in agence_mems[0].lesson

    async def test_non_promotable_lesson_no_agence_memory(self, db, affaire):
        """Une leçon non-promotable ne crée pas d'entrée agence."""
        import uuid, json
        from unittest.mock import AsyncMock, MagicMock, patch
        from modules.agent.models import AgentMemory
        from sqlalchemy import select

        llm_response = json.dumps({
            "lessons": [
                {
                    "lesson": "Le MOA appelle tous les vendredis pour un point.",
                    "category": "general",
                    "promotable": False,
                }
            ]
        })

        with patch("modules.agent.memory.LlmService") as MockLlm:
            mock_client = MagicMock()
            mock_client.chat.completions.create = AsyncMock(
                return_value=MagicMock(
                    choices=[MagicMock(message=MagicMock(content=llm_response))]
                )
            )
            MockLlm._get_client.return_value = mock_client

            from modules.agent.memory import extract_and_store_memories
            run_id = uuid.uuid4()
            await extract_and_store_memories(
                agent_name="hestia",
                instruction="Capitalise",
                result="Le MOA appelle tous les vendredis." * 5,
                affaire_id=affaire.id,
                run_id=run_id,
                db=db,
            )

        agence_rows = await db.execute(
            select(AgentMemory).where(
                AgentMemory.source_run_id == run_id,
                AgentMemory.scope == "agence",
            )
        )
        assert len(agence_rows.scalars().all()) == 0
