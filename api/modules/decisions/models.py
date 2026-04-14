"""
Modèles decisions — dashboard mémoire projet.

TABLE 1 : project_decisions (déjà créée en 0008, enrichie en 0015)
TABLE 2 : project_tasks     (tâches liées à une décision)
TABLE 3 : project_observations (entrées terrain, analysées par Argos)

La table project_decisions existe depuis la migration 0008 mais n'avait
pas d'ORM model dédié. On la matérialise ici pour pouvoir en faire le
CRUD propre et la relier aux tâches et observations.

Champs ajoutés en 0015 pour aligner sur l'archi dashboard :
  - phase            (APS, APD, PRO, DCE, EXE, DOE, ...)
  - sujet            (titre court indexable)
  - lot              (gros œuvre, étanchéité, électricité, ...)
  - agents_impliques (JSONB — liste des agents du panthéon ayant contribué)
  - impact_cout      (euros — négatif = surcoût)
  - impact_delai     (jours — positif = retard)
  - responsable      (personne MOE ou entreprise)
  - date_decision    (date effective de la décision)
  - phase_revision   (phase pendant laquelle la décision a été revue)
"""
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── Table 1 : Décisions ──────────────────────────────────────────────

class ProjectDecision(Base):
    __tablename__ = "project_decisions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    affaire_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("affaires.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    run_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orchestra_runs.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Colonnes d'origine (0008)
    objet: Mapped[str] = mapped_column(Text, nullable=False)
    contexte: Mapped[str | None] = mapped_column(Text, nullable=True)
    constat: Mapped[str | None] = mapped_column(Text, nullable=True)
    analyse: Mapped[str | None] = mapped_column(Text, nullable=True)
    impacts: Mapped[str | None] = mapped_column(Text, nullable=True)
    options: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    criticite: Mapped[str] = mapped_column(String(2), nullable=False, default="C2")
    # C1-C5
    dette: Mapped[str] = mapped_column(String(2), nullable=False, default="D0")
    # D0 = résolu | D1 = suspendu | D2 = bloquant | D3 = critique en retard
    statut: Mapped[str] = mapped_column(String(20), nullable=False, default="ouvert")
    # ouvert | validé | suspendu | caduc | a_revoir
    agent_source: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Enrichissements (0015)
    sujet: Mapped[str | None] = mapped_column(String(256), nullable=True, index=True)
    phase: Mapped[str | None] = mapped_column(String(16), nullable=True)
    # APS | APD | PRO | DCE | ACT | EXE | DOE
    lot: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    agents_impliques: Mapped[list] = mapped_column(
        JSONB, nullable=False, default=list
    )
    impact_cout: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    impact_delai: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # jours (positif = retard)
    responsable: Mapped[str | None] = mapped_column(String(128), nullable=True)
    date_decision: Mapped[date | None] = mapped_column(Date, nullable=True)
    phase_revision: Mapped[str | None] = mapped_column(String(16), nullable=True)

    # Enrichissements (0019) — guards module
    condition_levee: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Si un veto a été opposé, ce qu'il faut produire/valider pour le lever
    reversible: Mapped[bool | None] = mapped_column(nullable=True)
    # Réversibilité de la décision (reversibility_guard)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=_now, onupdate=_now
    )

    def __repr__(self) -> str:
        return f"<ProjectDecision {self.criticite}/{self.dette} {self.objet[:40]!r}>"


# ── Table 2 : Tâches ─────────────────────────────────────────────────

class ProjectTask(Base):
    __tablename__ = "project_tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    affaire_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("affaires.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    decision_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_decisions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    titre: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    urgence: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    # 1-5 (1 = faible, 5 = immédiat)
    statut: Mapped[str] = mapped_column(String(20), nullable=False, default="ouvert")
    # ouvert | en_cours | clos | bloque
    responsable: Mapped[str | None] = mapped_column(String(128), nullable=True)
    echeance: Mapped[date | None] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    def __repr__(self) -> str:
        return f"<ProjectTask U{self.urgence} {self.titre[:40]!r}>"


# ── Table 3 : Observations ───────────────────────────────────────────

class ProjectObservation(Base):
    __tablename__ = "project_observations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    affaire_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("affaires.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    decision_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_decisions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    source: Mapped[str] = mapped_column(String(16), nullable=False)
    # voix | photo | mail | note
    contenu_brut: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Transcription ou texte brut

    storage_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    # MinIO — pour les sources binaires (photo, audio)

    analyse_argos: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Constat objectif produit par l'agent Argos

    traitement: Mapped[str] = mapped_column(String(20), nullable=False, default="a_traiter")
    # a_traiter | en_cours | traite | ignore

    auteur: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )

    def __repr__(self) -> str:
        return f"<ProjectObservation {self.source} {self.traitement}>"
