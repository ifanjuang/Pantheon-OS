"""
CaptureService — transcription audio et structuration via agent.

Transcription :
  - Si WHISPER_ENDPOINT est configuré, POST vers l'endpoint Whisper externe.
  - Sinon, le fichier est stocké et la session reste en « awaiting_transcription ».

Structuration :
  - La transcription est envoyée à l'agent Hermès (routage) qui la structure
    via le pipeline agent standard (run_agent).
"""

import uuid

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.settings import settings

log = get_logger("capture.service")

# Récupérer WHISPER_ENDPOINT depuis settings (optionnel)
WHISPER_ENDPOINT: str | None = getattr(settings, "WHISPER_ENDPOINT", None)


async def transcribe_audio(audio_bytes: bytes, filename: str) -> str | None:
    """Transcrit un fichier audio en texte.

    Returns:
        Le texte transcrit, ou None si aucun endpoint Whisper n'est disponible.
    """
    if not WHISPER_ENDPOINT:
        log.info("capture.transcribe.no_endpoint", filename=filename)
        return None

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                WHISPER_ENDPOINT,
                files={"file": (filename, audio_bytes, "audio/mpeg")},
            )
            resp.raise_for_status()
            data = resp.json()
            # Support standard Whisper API response format
            text = data.get("text", "")
            log.info(
                "capture.transcribe.ok",
                filename=filename,
                chars=len(text),
            )
            return text
    except Exception as exc:
        log.error("capture.transcribe.failed", filename=filename, error=str(exc))
        raise


async def process_capture(
    db: AsyncSession,
    capture_id: uuid.UUID,
    affaire_id: uuid.UUID,
    user_id: uuid.UUID | None,
    transcription: str | None = None,
) -> None:
    """Traite une capture vocale via l'agent et met a jour la CaptureSession.

    1. Charge la transcription depuis la DB si non fournie (cas worker ARQ).
    2. Passe la transcription a l'agent Hermes (routage + structuration).
    3. Stocke le resultat structure et le lien vers l'AgentRun.
    """
    from apps.capture.models import CaptureSession

    capture = await db.get(CaptureSession, capture_id)
    if not capture:
        log.error("capture.process.not_found", capture_id=str(capture_id))
        return

    # Si pas de transcription fournie, utiliser celle stockée en DB
    if transcription is None:
        transcription = capture.transcription
    if not transcription:
        log.error("capture.process.no_transcription", capture_id=str(capture_id))
        capture.status = "failed"
        capture.error_message = "Aucune transcription disponible"
        await db.commit()
        return

    capture.status = "processing"
    await db.commit()

    try:
        from apps.agent.service import run_agent

        instruction = (
            "Tu reçois la transcription d'une note vocale enregistrée sur chantier. "
            "Analyse le contenu et extrais les informations clés : "
            "observations, problèmes identifiés, décisions prises, actions à mener, "
            "intervenants mentionnés et points de vigilance.\n\n"
            f"--- Transcription ---\n{transcription}"
        )

        agent_run = await run_agent(
            db=db,
            instruction=instruction,
            affaire_id=affaire_id,
            user_id=user_id,
            agent_name="hermes",
        )

        capture.agent_run_id = agent_run.id
        capture.structured_output = {
            "agent_result": agent_run.result,
            "agent_status": agent_run.status,
            "iterations": agent_run.iterations,
        }
        capture.status = "completed"

        log.info(
            "capture.process.ok",
            capture_id=str(capture_id),
            agent_run_id=str(agent_run.id),
        )

    except Exception as exc:
        log.error(
            "capture.process.failed",
            capture_id=str(capture_id),
            error=str(exc),
        )
        capture.status = "failed"
        capture.error_message = str(exc)

    await db.commit()
