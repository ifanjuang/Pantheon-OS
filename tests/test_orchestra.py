"""
Tests module orchestra — orchestration multi-agents Zeus via LangGraph.
run_orchestra est mocké pour éviter d'appeler le vrai LLM.
"""

import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from tests.conftest import auth_headers


def _make_mock_run(**overrides):
    """Fabrique un mock OrchestraRun avec tous les champs nécessaires."""
    run = MagicMock()
    run.id = overrides.get("id", uuid.uuid4())
    run.status = overrides.get("status", "completed")
    run.instruction = overrides.get("instruction", "Quels sont les risques sur ce projet ?")
    run.initial_agents = overrides.get("initial_agents", ["themis", "argus"])
    run.zeus_reasoning = overrides.get("zeus_reasoning", "Thémis pour la conformité, Argus pour les risques.")
    run.assignments = overrides.get(
        "assignments",
        [
            {"agent": "themis", "instruction": "Analyse la conformité.", "priority": 1},
            {"agent": "argus", "instruction": "Analyse les risques.", "priority": 1},
        ],
    )
    run.agent_results = overrides.get(
        "agent_results",
        {
            "themis": "Aucune non-conformité détectée.",
            "argus": "Risque de retard sur lot 3.",
        },
    )
    run.agent_run_ids = overrides.get("agent_run_ids", [str(uuid.uuid4()), str(uuid.uuid4())])
    run.synthesis_agent = overrides.get("synthesis_agent", "mnemosyne")
    run.final_answer = overrides.get("final_answer", "Synthèse : projet globalement conforme, vigilance sur le lot 3.")
    run.duration_ms = overrides.get("duration_ms", 1200)
    # Champs traçabilité 0012
    run.subtasks = overrides.get("subtasks", [])
    run.subtask_results = overrides.get("subtask_results", {})
    run.veto_agent = overrides.get("veto_agent", None)
    run.veto_motif = overrides.get("veto_motif", None)
    run.error_message = overrides.get("error_message", None)
    run.criticite = overrides.get("criticite", "C2")
    run.hitl_enabled = overrides.get("hitl_enabled", False)
    run.hitl_payload = overrides.get("hitl_payload", None)
    return run


@pytest.fixture
def mock_orchestra_run(mocker):
    """Mock de run_orchestra pour éviter d'appeler LangGraph + LLM."""
    run = _make_mock_run()
    mocker.patch(
        "modules.orchestra.router.run_orchestra",
        new_callable=AsyncMock,
        return_value=run,
    )
    return run


@pytest.fixture
def mock_queue(mocker):
    """Mock get_queue pour ne pas toucher Redis."""
    mock_pool = AsyncMock()
    mock_pool.enqueue_job = AsyncMock()
    mocker.patch(
        "modules.orchestra.router.get_queue",
        new_callable=AsyncMock,
        return_value=mock_pool,
    )
    return mock_pool


class TestOrchestraRun:
    async def test_run_requires_auth(self, client, affaire):
        r = await client.post(
            "/orchestra/run",
            json={
                "instruction": "Quels sont les risques ?",
                "affaire_id": str(affaire.id),
            },
        )
        assert r.status_code == 403

    async def test_run_enqueued(self, client, moe_token, affaire, mock_queue):
        """POST /orchestra/run retourne 202 (queued) quand Redis est disponible."""
        r = await client.post(
            "/orchestra/run",
            json={
                "instruction": "Quels sont les risques sur ce projet ?",
                "affaire_id": str(affaire.id),
            },
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 202
        data = r.json()
        assert data["status"] == "queued"
        assert data["criticite"] == "C2"
        mock_queue.enqueue_job.assert_awaited_once()

    async def test_run_with_criticite(self, client, moe_token, affaire, mock_queue):
        """La criticité est persistée sur le run."""
        r = await client.post(
            "/orchestra/run",
            json={
                "instruction": "Décision engageante sur le lot 5",
                "affaire_id": str(affaire.id),
                "criticite": "C4",
            },
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 202
        assert r.json()["criticite"] == "C4"

    async def test_run_fallback_sync(self, client, moe_token, affaire, mock_orchestra_run, mocker):
        """Si Redis indisponible, fallback sync via run_orchestra."""
        mocker.patch(
            "modules.orchestra.router.get_queue",
            new_callable=AsyncMock,
            side_effect=Exception("Redis down"),
        )
        r = await client.post(
            "/orchestra/run",
            json={
                "instruction": "Quels sont les risques sur ce projet ?",
                "affaire_id": str(affaire.id),
            },
            headers=auth_headers(moe_token),
        )
        # Fallback sync retourne le résultat du mock (status 202 mais completed)
        assert r.status_code == 202
        assert r.json()["status"] == "completed"

    async def test_run_with_specific_agents(self, client, moe_token, affaire, mock_queue):
        r = await client.post(
            "/orchestra/run",
            json={
                "instruction": "Analyse de conformité.",
                "affaire_id": str(affaire.id),
                "agents": ["themis", "mnemosyne"],
            },
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 202

    async def test_run_forbidden_for_lecteur(self, client, lecteur_token, affaire):
        r = await client.post(
            "/orchestra/run",
            json={
                "instruction": "Test interdit",
                "affaire_id": str(affaire.id),
            },
            headers=auth_headers(lecteur_token),
        )
        assert r.status_code == 403

    async def test_run_instruction_too_short(self, client, moe_token, affaire):
        r = await client.post(
            "/orchestra/run",
            json={"instruction": "Test", "affaire_id": str(affaire.id)},
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 422


class TestOrchestraResponse:
    async def test_response_includes_traceability_fields(self, client, moe_token, affaire, mock_queue):
        """Les champs 0012 (subtasks, veto, error_message) sont présents dans la réponse."""
        r = await client.post(
            "/orchestra/run",
            json={
                "instruction": "Quels sont les risques ?",
                "affaire_id": str(affaire.id),
            },
            headers=auth_headers(moe_token),
        )
        data = r.json()
        assert "subtasks" in data
        assert "subtask_results" in data
        assert "veto_agent" in data
        assert "error_message" in data
        assert "criticite" in data


class TestOrchestraHistory:
    async def test_list_runs_empty(self, client, moe_token, affaire):
        r = await client.get(
            f"/orchestra/runs/{affaire.id}",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        assert r.json() == []

    async def test_get_run_not_found(self, client, moe_token):
        r = await client.get(
            f"/orchestra/runs/detail/{uuid.uuid4()}",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 404

    async def test_list_requires_auth(self, client, affaire):
        r = await client.get(f"/orchestra/runs/{affaire.id}")
        assert r.status_code == 403
