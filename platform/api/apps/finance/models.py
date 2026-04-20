"""
Modèles finance — suivi financier des marchés de travaux.

Socle budgétaire :
  - affaire.budget_moa     : enveloppe totale MOA (déjà dans la table affaires)
  - affaire.honoraires     : honoraires MOE contractuels (idem)
  - planning_lots.montant_marche : montant de marché initial par lot (idem)

Ce module ajoute deux tables :

TABLE 1 : finance_avenants
  Modifications contractuelles au marché d'un lot.
  montant_ht peut être négatif (moins-value).
  Lié optionnellement à une décision projet (ProjectDecision).

TABLE 2 : finance_situations
  Demandes de paiement périodiques d'une entreprise pour un lot.
  Cycle : soumise → en_revision → validee → payee (ou contestee).
  Le champ avancement_valide est utilisé par Chronos pour croiser
  avec le planning réel (planning_taches.avancement).
"""

import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── Avenants ──────────────────────────────────────────────────────────


class Avenant(Base):
    __tablename__ = "finance_avenants"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    decision_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_decisions.id", ondelete="SET NULL"),
        nullable=True,
    )

    numero: Mapped[str] = mapped_column(String(64), nullable=False)
    # Ex : "AV-001", "AV-GEO-003"
    objet: Mapped[str] = mapped_column(String(512), nullable=False)
    montant_ht: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    # Positif = plus-value, négatif = moins-value
    impact_delai_jours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Impact en jours sur le planning (positif = allongement)

    statut: Mapped[str] = mapped_column(String(20), nullable=False, default="en_preparation")
    # en_preparation | soumis | accepte | refuse | annule
    date_soumission: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_acceptation: Mapped[date | None] = mapped_column(Date, nullable=True)

    storage_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    # Chemin MinIO — document contractuel PDF

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now, onupdate=_now)

    def __repr__(self) -> str:
        sign = "+" if self.montant_ht >= 0 else ""
        return f"<Avenant {self.numero} {sign}{self.montant_ht}€ {self.statut}>"


# ── Situations de travaux ─────────────────────────────────────────────


class SituationTravaux(Base):
    __tablename__ = "finance_situations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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

    entreprise: Mapped[str] = mapped_column(String(256), nullable=False)
    numero: Mapped[int] = mapped_column(Integer, nullable=False)
    # Numéro de situation (1, 2, 3…) par lot/entreprise

    periode_debut: Mapped[date] = mapped_column(Date, nullable=False)
    periode_fin: Mapped[date] = mapped_column(Date, nullable=False)

    montant_demande_ht: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    montant_valide_ht: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    # Montant retenu après vérification MOE

    avancement_declare: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # % d'avancement déclaré par l'entreprise (0-100)
    avancement_valide: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # % retenu par le MOE après visite chantier

    statut: Mapped[str] = mapped_column(String(20), nullable=False, default="soumise")
    # soumise | en_revision | validee | payee | contestee
    date_soumission: Mapped[date] = mapped_column(Date, nullable=False)
    date_validation: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_paiement: Mapped[date | None] = mapped_column(Date, nullable=True)

    storage_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    # Chemin MinIO — PDF de la situation

    remarques: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now, onupdate=_now)

    def __repr__(self) -> str:
        return f"<SituationTravaux n°{self.numero} {self.entreprise} {self.statut}>"
