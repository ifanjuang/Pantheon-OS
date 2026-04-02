"""
Tests module webhooks — endpoints pour Paperclip.
L'agent ReAct est mocké (pas besoin d'Ollama).
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from core.settings import settings
from tests.conftest import auth_headers


WEBHOOK_HEADERS = {"Authorization": f"Bearer {settings.JWT_SECRET_KEY}"}


@pytest.fixture
def mock_run(mocker):
    """Mock de run_agent pour éviter d'appeler le vrai LLM."""
    run = MagicMock()
    run.id = __import__("uuid").uuid4()
    run.status = "completed"
    run.result = "Analyse de test."
    run.steps = []
    run.iterations = 1
    run.duration_ms = 100
    mocker.patch(
        "modules.webhooks.router.run_agent",
        new_callable=AsyncMock,
        return_value=run,
    )
    return run


class TestHealth:
    async def test_health_ok(self, client):
        r = await client.get("/webhooks/health", headers=WEBHOOK_HEADERS)
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    async def test_health_invalid_secret(self, client):
        r = await client.get(
            "/webhooks/health", headers={"Authorization": "Bearer mauvais-secret"}
        )
        assert r.status_code == 401

    async def test_health_no_auth(self, client):
        r = await client.get("/webhooks/health")
        assert r.status_code == 401


class TestHeartbeat:
    async def test_heartbeat_no_affaires(self, client, mock_run):
        r = await client.post("/webhooks/heartbeat", headers=WEBHOOK_HEADERS)
        assert r.status_code == 200
        assert r.json()["runs_triggered"] == 0

    async def test_heartbeat_triggers_argus(self, client, affaire, mock_run):
        r = await client.post("/webhooks/heartbeat", headers=WEBHOOK_HEADERS)
        assert r.status_code == 200
        data = r.json()
        assert data["runs_triggered"] == 1
        assert "TEST-001" in data["affaires"]

    async def test_heartbeat_skips_archived(self, client, db, affaire, mock_run):
        # Archiver l'affaire
        affaire.statut = "archive"
        await db.commit()

        r = await client.post("/webhooks/heartbeat", headers=WEBHOOK_HEADERS)
        assert r.status_code == 200
        assert r.json()["runs_triggered"] == 0

    async def test_heartbeat_requires_secret(self, client):
        r = await client.post("/webhooks/heartbeat")
        assert r.status_code == 401


class TestDocumentUploaded:
    async def test_triggers_themis(self, client, affaire, mock_run):
        import uuid
        r = await client.post(
            "/webhooks/document-uploaded",
            json={
                "document_id": str(uuid.uuid4()),
                "affaire_id": str(affaire.id),
                "nom": "CCTP_lot3.pdf",
            },
            headers=WEBHOOK_HEADERS,
        )
        assert r.status_code == 200
        data = r.json()
        assert "run_id" in data
        assert data["status"] == "completed"


class TestTriggerAgent:
    async def test_trigger_argus(self, client, affaire, mock_run):
        r = await client.post(
            "/webhooks/agent/argus",
            json={
                "affaire_id": str(affaire.id),
                "instruction": "Quels sont les risques actuels ?",
            },
            headers=WEBHOOK_HEADERS,
        )
        assert r.status_code == 200
        data = r.json()
        assert data["agent"] == "argus"
        assert data["status"] == "completed"

    async def test_trigger_invalid_agent(self, client, affaire):
        import uuid
        r = await client.post(
            "/webhooks/agent/zeus",
            json={
                "affaire_id": str(affaire.id),
                "instruction": "Test",
            },
            headers=WEBHOOK_HEADERS,
        )
        assert r.status_code == 400

    @pytest.mark.parametrize("agent", ["themis", "argus", "hermes", "mnemosyne", "athena"])
    async def test_all_agents_accessible(self, client, affaire, mock_run, agent):
        r = await client.post(
            f"/webhooks/agent/{agent}",
            json={"affaire_id": str(affaire.id), "instruction": "Test"},
            headers=WEBHOOK_HEADERS,
        )
        assert r.status_code == 200
        assert r.json()["agent"] == agent
