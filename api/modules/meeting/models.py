"""
Modèles meeting — Comptes rendus, actions et ordres du jour.

MeetingCR     → un compte rendu de réunion uploadé ou saisi
MeetingAction → une action extraite d'un CR (ou saisie manuellement)
MeetingAgenda → un ordre du jour généré pour une prochaine réunion
"""
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class MeetingCR(Base):
    """Compte rendu de réunion."""
    __tablename__ = "meeting_crs"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    affaire_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("affaires.id", ondelete="CASCADE"), nullable=False, index=True
    )
    uploaded_by: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    titre: Mapped[str] = mapped_column(String(256), nullable=False)
    date_reunion: Mapped[date | None] = mapped_column(Date, nullable=True)
    participants: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # ["Jean Dupont — MOE", "Marie Martin — Entreprise lot 2"]

    contenu_brut: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Texte du CR (extrait du PDF/DOCX ou saisi directement)

    synthese: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Résumé 2-3 phrases généré par Hermès

    analyse_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    # pending | running | completed | failed

    document_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True
    )
    # Lien vers le fichier uploadé dans le module documents (optionnel)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)


class MeetingAction(Base):
    """Action décidée en réunion, extraite d'un CR ou saisie manuellement."""
    __tablename__ = "meeting_actions"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    affaire_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("affaires.id", ondelete="CASCADE"), nullable=False, index=True
    )
    cr_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("meeting_crs.id", ondelete="SET NULL"), nullable=True, index=True
    )

    description: Mapped[str] = mapped_column(Text, nullable=False)
    responsable: Mapped[str | None] = mapped_column(String(128), nullable=True)
    echeance: Mapped[date | None] = mapped_column(Date, nullable=True)
    priorite: Mapped[str] = mapped_column(String(32), nullable=False, default="normale")
    # critique | haute | normale

    statut: Mapped[str] = mapped_column(String(32), nullable=False, default="ouvert")
    # ouvert | en_cours | clos | reporte

    contexte: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Phrase du CR source qui justifie l'action

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )


class MeetingAgenda(Base):
    """Ordre du jour généré par Athéna pour une prochaine réunion."""
    __tablename__ = "meeting_agendas"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    affaire_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("affaires.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    titre: Mapped[str] = mapped_column(String(256), nullable=False)
    date_prevue: Mapped[date | None] = mapped_column(Date, nullable=True)

    items: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # [{ordre, sujet, type, porteur, duree_min, contexte}]

    notes_preparatoires: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Analyse Athéna : points de vigilance avant la réunion

    actions_incluses: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # UUIDs des MeetingAction considérées pour cet agenda

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
