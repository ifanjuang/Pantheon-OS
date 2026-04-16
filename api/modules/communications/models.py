"""
Modèles communications — registre probatoire.

TABLE : communications_courriers
  Chaque ligne représente un courrier entrant ou sortant rattaché à une
  affaire. La colonne `reponse_id` permet de chaîner un courrier sortant
  à son courrier entrant d'origine (self-référence nullable).

  `draft_iris` est rempli par le job ARQ `draft_courrier_job` qui
  appelle l'agent Iris pour rédiger un projet de réponse.

Cas d'usage :
  - Lettre recommandée MOA → log entrant + délai réponse
  - Mise en demeure → log entrant, gravité, lien décision
  - Réponse à entreprise → log sortant, lien au courrier entrant
  - Bon de commande → log sortant, lien lot/entreprise
  - CR de réunion → log sortant (ou lien meeting)
"""
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Courrier(Base):
    __tablename__ = "communications_courriers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    affaire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("affaires.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Classement ────────────────────────────────────────────────────
    sens: Mapped[str] = mapped_column(String(16), nullable=False)
    # entrant | sortant
    type_doc: Mapped[str] = mapped_column(String(32), nullable=False, default="courrier")
    # courrier | email | lr | mise_en_demeure | bc | devis | pv | cr | autre
    reference: Mapped[str | None] = mapped_column(String(128), nullable=True)
    # Ex : "C-2025-042", "LR/MOA/2025-06-01"

    # ── Parties ───────────────────────────────────────────────────────
    emetteur: Mapped[str] = mapped_column(String(256), nullable=False)
    destinataire: Mapped[str] = mapped_column(String(256), nullable=False)

    # ── Contenu ───────────────────────────────────────────────────────
    objet: Mapped[str] = mapped_column(String(512), nullable=False)
    resume: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Résumé du contenu ou extrait pertinent
    storage_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    # Chemin MinIO — scan PDF ou pièce jointe

    # ── Dates ─────────────────────────────────────────────────────────
    date_emission: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_reception: Mapped[date | None] = mapped_column(Date, nullable=True)
    delai_reponse: Mapped[date | None] = mapped_column(Date, nullable=True)
    # Date limite pour répondre (entrant → en_attente_reponse)
    date_reponse_effective: Mapped[date | None] = mapped_column(Date, nullable=True)

    # ── Statut ────────────────────────────────────────────────────────
    statut: Mapped[str] = mapped_column(String(32), nullable=False, default="recu")
    # recu | en_attente_reponse | traite | sans_suite | archive

    # ── Liens métier (tous optionnels) ────────────────────────────────
    lot_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("planning_lots.id", ondelete="SET NULL"),
        nullable=True,
    )
    decision_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_decisions.id", ondelete="SET NULL"),
        nullable=True,
    )
    observation_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chantier_observations.id", ondelete="SET NULL"),
        nullable=True,
    )
    reponse_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("communications_courriers.id", ondelete="SET NULL"),
        nullable=True,
    )
    # Courrier sortant qui répond à ce courrier entrant

    # ── Auteur et pipeline Iris ────────────────────────────────────────
    auteur_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    draft_iris: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Brouillon de réponse rédigé par Iris (rempli par ARQ)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    def __repr__(self) -> str:
        return f"<Courrier {self.sens} {self.type_doc} {self.objet[:40]!r}>"
