"""
Tests module orchestra — orchestration multi-agents Zeus via LangGraph.
run_orchestra est mocké pour éviter d'appeler le vrai LLM.
"""
import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from tests.conftest import auth_headers


@pytest.fixture
def mock_orchestra_run(mocker):
    """Mock de run_orchestra pour éviter d'appeler LangGraph + LLM."""
    run = MagicMock()
    run.id = uuid.uuid4()
    run.status = "completed"
    run.instruction = "Quels sont les risques sur ce projet ?"
    run.initial_agents = ["themis", "argus"]
    run.zeus_reasoning = "Thémis pour la conformité, Argus pour les risques."
    run.assignments = [
        {"agent": "themis", "instruction": "Analyse la conformité.", "priority": 1},
        {"agent": "argus", "instruction": "Analyse les risques.", "priority": 1},
    ]
    run.agent_results = {
        "themis": "Aucune non-conformité détectée.",
        "argus": "Risque de retard sur lot 3.",
    }
    run.agent_run_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
    run.synthesis_agent = "mnemosyne"
    run.final_answer = "Synthèse : projet globalement conforme, vigilance sur le lot 3."
    run.duration_ms = 1200
    mocker.patch(
        "modules.orchestra.router.run_orchestra",
        new_callable=AsyncMock,
        return_value=run,
    )
    return run


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

    async def test_run_success(self, client, moe_token, affaire, mock_orchestra_run):
        r = await client.post(
            "/orchestra/run",
            json={
                "instruction": "Quels sont les risques sur ce projet ?",
                "affaire_id": str(affaire.id),
            },
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "completed"
        assert "final_answer" in data
        assert "zeus_reasoning" in data
        assert len(data["assignments"]) == 2

    async def test_run_with_specific_agents(self, client, moe_token, affaire, mock_orchestra_run):
        r = await client.post(
            "/orchestra/run",
            json={
                "instruction": "Analyse de conformité.",
                "affaire_id": str(affaire.id),
                "agents": ["themis", "mnemosyne"],
            },
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        assert r.json()["status"] == "completed"

    async def test_run_forbidden_for_lecteur(self, client, lecteur_token, affaire):
        r = await client.post(
            "/orchestra/run",
            json={
                "instruction": "Test",
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
