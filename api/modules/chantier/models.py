"""
Modèles chantier — observations terrain + non-conformités.

TABLE 1 : chantier_observations
  Entrée terrain brute (photo, voix, note, mail).
  `analyse_argos` est rempli par le job ARQ `analyze_chantier_obs_job`
  qui appelle l'agent Argos.

TABLE 2 : chantier_nonconformites
  Non-conformité / action corrective dérivée d'une observation.
  `analyse_hephaistos` est rempli par le job ARQ `qualify_nc_job`
  qui appelle l'agent Héphaïstos.

Pipeline :
  [Terrain] → ObservationChantier (brute) → [Argos] analyse_argos
           → NonConformite (si NC détectée) → [Héphaïstos] analyse_hephaistos
           → action corrective assignée → résolution
"""
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── Observations terrain ──────────────────────────────────────────────

class ObservationChantier(Base):
    __tablename__ = "chantier_observations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    affaire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("affaires.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lot_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("planning_lots.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    source: Mapped[str] = mapped_column(String(16), nullable=False)
    # photo | voix | note | mail

    contenu_brut: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Transcription vocale, corps du mail, ou texte libre

    storage_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    # Chemin MinIO — fichier binaire (photo, audio)

    localisation: Mapped[str | None] = mapped_column(String(512), nullable=True)
    # Ex : "R+2 cage escalier Nord", "Façade Est niveau toiture"

    entreprise: Mapped[str | None] = mapped_column(String(256), nullable=True)
    # Entreprise concernée par l'observation

    auteur: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    date_constat: Mapped[date] = mapped_column(Date, nullable=False)

    analyse_argos: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Constat objectif produit par l'agent Argos (rempli par ARQ)

    statut: Mapped[str] = mapped_column(String(20), nullable=False, default="a_analyser")
    # a_analyser | en_cours | analyse | ignore

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    def __repr__(self) -> str:
        return f"<ObservationChantier {self.source} {self.date_constat} {self.statut}>"


# ── Non-conformités ───────────────────────────────────────────────────

class NonConformite(Base):
    __tablename__ = "chantier_nonconformites"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    affaire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("affaires.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    observation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chantier_observations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    lot_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("planning_lots.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    decision_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_decisions.id", ondelete="SET NULL"),
        nullable=True,
    )

    entreprise: Mapped[str | None] = mapped_column(String(256), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    gravite: Mapped[str] = mapped_column(String(20), nullable=False, default="mineure")
    # mineure | majeure | critique | arret_chantier

    date_detection: Mapped[date] = mapped_column(Date, nullable=False)
    date_echeance: Mapped[date | None] = mapped_column(Date, nullable=True)
    # Deadline de correction
    date_resolution: Mapped[date | None] = mapped_column(Date, nullable=True)

    statut: Mapped[str] = mapped_column(String(20), nullable=False, default="ouverte")
    # ouverte | en_cours | resolue | contestee

    responsable: Mapped[str | None] = mapped_column(String(128), nullable=True)
    action_requise: Mapped[str | None] = mapped_column(Text, nullable=True)

    analyse_hephaistos: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Diagnostic technique produit par Héphaïstos (rempli par ARQ)

    arret_chantier: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    # True si Héphaïstos ou gravite="arret_chantier" → alerte critique

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    def __repr__(self) -> str:
        return f"<NonConformite {self.gravite} {self.statut} {self.description[:40]!r}>"
