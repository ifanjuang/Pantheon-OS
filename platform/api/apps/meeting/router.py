"""
Router meeting

── Comptes rendus ────────────────────────────────────────────────────
POST /meeting/cr/upload              → upload fichier CR (PDF/DOCX/TXT) + analyse Hermès
POST /meeting/cr/                    → créer CR depuis texte brut + analyse
GET  /meeting/cr/{affaire_id}        → liste des CRs d'une affaire
GET  /meeting/cr/detail/{cr_id}      → CR + actions extraites
DELETE /meeting/cr/{cr_id}           → supprimer CR + actions liées

── Actions ───────────────────────────────────────────────────────────
GET  /meeting/actions/{affaire_id}   → toutes les actions ouvertes (triées priorité/échéance)
POST /meeting/actions/               → créer action manuelle
PATCH /meeting/actions/{action_id}   → mettre à jour statut/responsable/échéance

── Ordre du jour ─────────────────────────────────────────────────────
POST /meeting/agenda/generate        → Athéna génère un ordre du jour
GET  /meeting/agenda/{affaire_id}    → liste des agendas
GET  /meeting/agenda/detail/{id}     → détail agenda
GET  /meeting/agenda/export/{id}     → texte formaté (copier-coller)
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import get_current_user, require_role
from core.logging import get_logger
from database import get_db
from modules.meeting.models import MeetingAction, MeetingAgenda, MeetingCR
from modules.meeting.schemas import (
    ActionCreateRequest,
    ActionResponse,
    ActionUpdateRequest,
    AgendaGenerateRequest,
    AgendaResponse,
    CRCreateRequest,
    CRResponse,
)
from modules.meeting.service import agenda_to_text, analyse_cr, generate_agenda

log = get_logger("meeting.router")

ALLOWED_MIME = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
}


def get_router(config: dict) -> APIRouter:
    router = APIRouter()

    # ── Comptes rendus ────────────────────────────────────────────────────

    @router.post("/cr/upload", response_model=CRResponse, status_code=201)
    async def upload_cr(
        background_tasks: BackgroundTasks,
        file: Annotated[UploadFile, File()],
        affaire_id: Annotated[uuid.UUID, Form()],
        titre: Annotated[str, Form()] = "",
        date_reunion: Annotated[str, Form()] = "",
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        """
        Upload un fichier CR (PDF, DOCX, TXT) et lance l'analyse Hermès en arrière-plan.
        Retourne immédiatement avec analyse_status=pending.
        """
        if file.content_type not in ALLOWED_MIME:
            raise HTTPException(status_code=415, detail=f"Type non supporté : {file.content_type}")

        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Fichier trop volumineux (max 10 Mo)")

        # Extraire le texte selon le format
        contenu_brut = await _extract_text(content, file.content_type, file.filename or "")

        # Titre par défaut
        nom_fichier = file.filename or "CR"
        titre_final = titre.strip() or f"CR — {nom_fichier.rsplit('.', 1)[0]}"

        # Parser la date si fournie
        date_obj = None
        if date_reunion:
            from datetime import date

            try:
                date_obj = date.fromisoformat(date_reunion)
            except ValueError:
                pass

        cr = MeetingCR(
            affaire_id=affaire_id,
            uploaded_by=current_user.id,
            titre=titre_final[:256],
            date_reunion=date_obj,
            contenu_brut=contenu_brut,
            analyse_status="pending",
        )
        db.add(cr)
        await db.commit()
        await db.refresh(cr)

        # Analyse en arrière-plan
        async def _run_analyse():
            from database import AsyncSessionLocal

            async with AsyncSessionLocal() as bg_db:
                cr_fresh = await bg_db.get(MeetingCR, cr.id)
                if cr_fresh:
                    await analyse_cr(bg_db, cr_fresh)

        background_tasks.add_task(_run_analyse)

        log.info("meeting.cr_uploaded", cr_id=str(cr.id), affaire_id=str(affaire_id))
        return cr

    @router.post("/cr/", response_model=CRResponse, status_code=201)
    async def create_cr(
        background_tasks: BackgroundTasks,
        payload: CRCreateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        """Créer un CR depuis texte brut et lancer l'analyse."""
        cr = MeetingCR(
            affaire_id=payload.affaire_id,
            uploaded_by=current_user.id,
            titre=payload.titre[:256],
            date_reunion=payload.date_reunion,
            participants=payload.participants,
            contenu_brut=payload.contenu_brut,
            analyse_status="pending",
        )
        db.add(cr)
        await db.commit()
        await db.refresh(cr)

        async def _run():
            from database import AsyncSessionLocal

            async with AsyncSessionLocal() as bg_db:
                cr_fresh = await bg_db.get(MeetingCR, cr.id)
                if cr_fresh:
                    await analyse_cr(bg_db, cr_fresh)

        background_tasks.add_task(_run)
        return cr

    @router.get("/cr/{affaire_id}", response_model=list[CRResponse])
    async def list_crs(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        result = await db.execute(
            select(MeetingCR)
            .where(MeetingCR.affaire_id == affaire_id)
            .order_by(MeetingCR.date_reunion.desc().nulls_last(), MeetingCR.created_at.desc())
        )
        return result.scalars().all()

    @router.get("/cr/detail/{cr_id}")
    async def get_cr(
        cr_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """Retourne le CR avec ses actions extraites."""
        cr = await db.get(MeetingCR, cr_id)
        if not cr:
            raise HTTPException(status_code=404, detail="CR introuvable")

        result = await db.execute(
            select(MeetingAction)
            .where(MeetingAction.cr_id == cr_id)
            .order_by(MeetingAction.priorite.desc(), MeetingAction.echeance.asc().nulls_last())
        )
        actions = result.scalars().all()

        return {
            "cr": CRResponse.model_validate(cr),
            "actions": [ActionResponse.model_validate(a) for a in actions],
        }

    @router.delete("/cr/{cr_id}", status_code=204)
    async def delete_cr(
        cr_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _admin=Depends(require_role("admin", "moe")),
    ):
        cr = await db.get(MeetingCR, cr_id)
        if not cr:
            raise HTTPException(status_code=404, detail="CR introuvable")
        await db.delete(cr)
        await db.commit()

    # ── Actions ───────────────────────────────────────────────────────────

    @router.get("/actions/{affaire_id}", response_model=list[ActionResponse])
    async def list_actions(
        affaire_id: uuid.UUID,
        statut: str = "ouvert,en_cours",
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """
        Liste les actions d'une affaire.
        Paramètre statut : valeurs séparées par virgule (défaut: ouvert,en_cours).
        Passer statut=all pour tout voir.
        """
        from datetime import date as date_cls

        query = select(MeetingAction).where(MeetingAction.affaire_id == affaire_id)

        if statut != "all":
            statuts = [s.strip() for s in statut.split(",")]
            query = query.where(MeetingAction.statut.in_(statuts))

        query = query.order_by(
            MeetingAction.priorite.desc(),
            MeetingAction.echeance.asc().nulls_last(),
        )
        result = await db.execute(query)
        return result.scalars().all()

    @router.post("/actions/", response_model=ActionResponse, status_code=201)
    async def create_action(
        payload: ActionCreateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        action = MeetingAction(**payload.model_dump())
        db.add(action)
        await db.commit()
        await db.refresh(action)
        return action

    @router.patch("/actions/{action_id}", response_model=ActionResponse)
    async def update_action(
        action_id: uuid.UUID,
        payload: ActionUpdateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        action = await db.get(MeetingAction, action_id)
        if not action:
            raise HTTPException(status_code=404, detail="Action introuvable")

        for field, value in payload.model_dump(exclude_none=True).items():
            setattr(action, field, value)

        await db.commit()
        await db.refresh(action)
        return action

    # ── Ordre du jour ──────────────────────────────────────────────────────

    @router.post("/agenda/generate", response_model=AgendaResponse, status_code=201)
    async def generate(
        payload: AgendaGenerateRequest,
        db: AsyncSession = Depends(get_db),
        current_user=Depends(require_role("admin", "moe", "collaborateur")),
    ):
        """
        Athéna génère un ordre du jour basé sur les actions ouvertes et le contexte projet.
        """
        agenda = await generate_agenda(
            db=db,
            affaire_id=payload.affaire_id,
            user_id=current_user.id,
            date_prevue=payload.date_prevue,
            instructions_supplementaires=payload.instructions_supplementaires,
        )
        return agenda

    @router.get("/agenda/{affaire_id}", response_model=list[AgendaResponse])
    async def list_agendas(
        affaire_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        result = await db.execute(
            select(MeetingAgenda)
            .where(MeetingAgenda.affaire_id == affaire_id)
            .order_by(MeetingAgenda.created_at.desc())
        )
        return result.scalars().all()

    @router.get("/agenda/detail/{agenda_id}", response_model=AgendaResponse)
    async def get_agenda(
        agenda_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        agenda = await db.get(MeetingAgenda, agenda_id)
        if not agenda:
            raise HTTPException(status_code=404, detail="Agenda introuvable")
        return agenda

    @router.get("/agenda/export/{agenda_id}", response_class=PlainTextResponse)
    async def export_agenda(
        agenda_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        _user=Depends(get_current_user),
    ):
        """Retourne l'ordre du jour en texte brut (copier-coller, email)."""
        agenda = await db.get(MeetingAgenda, agenda_id)
        if not agenda:
            raise HTTPException(status_code=404, detail="Agenda introuvable")
        return agenda_to_text(agenda)

    return router


# ── Extraction texte selon format ─────────────────────────────────────────────


async def _extract_text(content: bytes, mime: str, filename: str) -> str:
    """Extrait le texte brut d'un fichier selon son type MIME."""
    if mime == "text/plain" or mime == "text/markdown":
        return content.decode("utf-8", errors="replace")

    if mime == "application/pdf":
        try:
            import io
            import pypdf

            reader = pypdf.PdfReader(io.BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError:
            # pypdf optionnel — fallback texte brut
            return content.decode("utf-8", errors="replace")

    if "wordprocessingml" in mime:
        try:
            import io
            import docx

            doc = docx.Document(io.BytesIO(content))
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            return content.decode("utf-8", errors="replace")

    return content.decode("utf-8", errors="replace")
