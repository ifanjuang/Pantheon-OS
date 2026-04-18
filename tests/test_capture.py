"""
Tests module capture — upload audio, transcription, pipeline agent.
Services externes mockés (MinIO, Whisper, LLM).
"""

import io
import uuid

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from tests.conftest import auth_headers


@pytest.fixture
def mock_storage(mocker):
    mocker.patch(
        "modules.capture.router.StorageService.upload",
        new_callable=AsyncMock,
        return_value="capture/test-audio.mp3",
    )


@pytest.fixture
def mock_transcribe_ok(mocker):
    mocker.patch(
        "modules.capture.router.transcribe_audio",
        new_callable=AsyncMock,
        return_value="Le mur du bâtiment B présente des fissures.",
    )


@pytest.fixture
def mock_transcribe_none(mocker):
    """Simule l'absence d'endpoint Whisper."""
    mocker.patch(
        "modules.capture.router.transcribe_audio",
        new_callable=AsyncMock,
        return_value=None,
    )


def _audio_file(name="test.mp3", mime="audio/mpeg", size=1024):
    return ("file", (name, io.BytesIO(b"\x00" * size), mime))


class TestCaptureUpload:
    async def test_upload_requires_auth(self, client, affaire, mock_storage):
        r = await client.post(
            "/capture/upload",
            data={"affaire_id": str(affaire.id)},
            files=[_audio_file()],
        )
        assert r.status_code == 401

    async def test_upload_success_with_transcription(
        self, client, moe_token, affaire, mock_storage, mock_transcribe_ok, mocker
    ):
        # Mock le background task pour ne pas lancer l'agent
        mocker.patch(
            "modules.capture.service.process_capture",
            new_callable=AsyncMock,
        )
        r = await client.post(
            "/capture/upload",
            data={"affaire_id": str(affaire.id), "duration_seconds": "30"},
            files=[_audio_file()],
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 201
        data = r.json()
        assert data["status"] in ("transcribing", "pending")
        assert data["transcription"] is not None
        assert data["affaire_id"] == str(affaire.id)

    async def test_upload_without_whisper(self, client, moe_token, affaire, mock_storage, mock_transcribe_none):
        r = await client.post(
            "/capture/upload",
            data={"affaire_id": str(affaire.id)},
            files=[_audio_file()],
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 201
        data = r.json()
        assert data["status"] == "pending"
        assert data["transcription"] is None

    async def test_upload_rejects_bad_mime(self, client, moe_token, affaire, mock_storage):
        r = await client.post(
            "/capture/upload",
            data={"affaire_id": str(affaire.id)},
            files=[_audio_file(mime="application/pdf")],
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 415

    async def test_upload_rejects_oversized(self, client, moe_token, affaire, mock_storage):
        r = await client.post(
            "/capture/upload",
            data={"affaire_id": str(affaire.id)},
            files=[_audio_file(size=26 * 1024 * 1024)],
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 413

    async def test_upload_forbidden_for_lecteur(self, client, lecteur_token, affaire, mock_storage):
        r = await client.post(
            "/capture/upload",
            data={"affaire_id": str(affaire.id)},
            files=[_audio_file()],
            headers=auth_headers(lecteur_token),
        )
        assert r.status_code == 403


class TestCaptureList:
    async def test_list_empty(self, client, moe_token, affaire):
        r = await client.get(
            f"/capture/sessions/{affaire.id}",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 200
        assert r.json() == []

    async def test_list_requires_auth(self, client, affaire):
        r = await client.get(f"/capture/sessions/{affaire.id}")
        assert r.status_code == 401


class TestCaptureDetail:
    async def test_detail_not_found(self, client, moe_token):
        r = await client.get(
            f"/capture/sessions/detail/{uuid.uuid4()}",
            headers=auth_headers(moe_token),
        )
        assert r.status_code == 404

    async def test_detail_requires_auth(self, client):
        r = await client.get(f"/capture/sessions/detail/{uuid.uuid4()}")
        assert r.status_code == 401


class TestProcessCapture:
    async def test_process_capture_loads_transcription_from_db(self, db, affaire, moe_user):
        """process_capture sans transcription explicite charge depuis la DB."""
        from modules.capture.models import CaptureSession

        capture = CaptureSession(
            affaire_id=affaire.id,
            user_id=moe_user.id,
            audio_key="capture/test.mp3",
            transcription="Fissure sur le mur nord.",
            status="transcribing",
        )
        db.add(capture)
        await db.flush()

        with patch("modules.capture.service.run_agent", new_callable=AsyncMock) as mock_agent:
            mock_run = MagicMock()
            mock_run.id = uuid.uuid4()
            mock_run.result = "Observation : fissure mur nord."
            mock_run.status = "completed"
            mock_run.iterations = 2
            mock_agent.return_value = mock_run

            from modules.capture.service import process_capture

            await process_capture(
                db=db,
                capture_id=capture.id,
                affaire_id=affaire.id,
                user_id=moe_user.id,
                # pas de transcription fournie -> lit depuis DB
            )

            await db.refresh(capture)
            assert capture.status == "completed"
            assert capture.agent_run_id == mock_run.id
            mock_agent.assert_awaited_once()

    async def test_process_capture_fails_without_transcription(self, db, affaire, moe_user):
        """process_capture sans transcription en DB ni paramètre -> failed."""
        from modules.capture.models import CaptureSession

        capture = CaptureSession(
            affaire_id=affaire.id,
            user_id=moe_user.id,
            audio_key="capture/empty.mp3",
            transcription=None,
            status="pending",
        )
        db.add(capture)
        await db.flush()

        from modules.capture.service import process_capture

        await process_capture(
            db=db,
            capture_id=capture.id,
            affaire_id=affaire.id,
            user_id=moe_user.id,
        )

        await db.refresh(capture)
        assert capture.status == "failed"
        assert "transcription" in capture.error_message.lower()
