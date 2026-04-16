"""
Modèles planning — lots, tâches, jalons, liens de dépendance.

Les liens forment un DAG (Directed Acyclic Graph) sur les tâches.
PlanningService.compute_critical_path() applique l'algorithme CPM
(forward/backward pass) sur ce DAG pour identifier le chemin critique
et calculer les marges (float).

PlanningService.propagate_delays() propage un décalage en cascade
en remontant le graphe FS (Finish-to-Start) depuis une tâche modifiée.
"""
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── Lots ──────────────────────────────────────────────────────────────

class Lot(Base):
    __tablename__ = "planning_lots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    affaire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("affaires.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(String(32), nullable=False)
    # GEO, TCE, ELE, PLOM, CVC, FACADE, VRD, SERRURERIE, ...
    nom: Mapped[str] = mapped_column(String(256), nullable=False)
    entreprise: Mapped[str | None] = mapped_column(String(256), nullable=True)
    date_debut: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_fin: Mapped[date | None] = mapped_column(Date, nullable=True)
    statut: Mapped[str] = mapped_column(String(20), nullable=False, default="planifie")
    # planifie | en_cours | termine | suspendu
    montant_marche: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    # Montant contractuel du lot (€ HT)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    def __repr__(self) -> str:
        return f"<Lot {self.code} — {self.nom}>"


# ── Tâches ────────────────────────────────────────────────────────────

class Tache(Base):
    __tablename__ = "planning_taches"

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

    titre: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsable: Mapped[str | None] = mapped_column(String(128), nullable=True)

    date_debut_prevue: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_fin_prevue: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_debut_reelle: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_fin_reelle: Mapped[date | None] = mapped_column(Date, nullable=True)
    duree_jours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Durée nominale en jours — utilisée par CPM si dates non renseignées

    avancement: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # 0-100 %
    statut: Mapped[str] = mapped_column(String(20), nullable=False, default="planifiee")
    # planifiee | en_cours | terminee | bloquee | annulee
    critique: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # True si sur le chemin critique — mis à jour par compute_critical_path()

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    def __repr__(self) -> str:
        return f"<Tache {self.titre[:40]!r}{'*' if self.critique else ''}>"


# ── Jalons ────────────────────────────────────────────────────────────

class Jalon(Base):
    __tablename__ = "planning_jalons"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    affaire_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("affaires.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    tache_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("planning_taches.id", ondelete="SET NULL"),
        nullable=True,
    )

    nom: Mapped[str] = mapped_column(String(256), nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False, default="technique")
    # administratif | contractuel | technique | livraison
    date_cible: Mapped[date] = mapped_column(Date, nullable=False)
    date_reelle: Mapped[date | None] = mapped_column(Date, nullable=True)
    statut: Mapped[str] = mapped_column(String(20), nullable=False, default="a_venir")
    # a_venir | atteint | manque | reporte

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    def __repr__(self) -> str:
        return f"<Jalon {self.nom[:40]!r} {self.date_cible}>"


# ── Liens de dépendance ───────────────────────────────────────────────

class LienDependance(Base):
    __tablename__ = "planning_liens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    predecesseur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("planning_taches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    successeur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("planning_taches.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    type: Mapped[str] = mapped_column(String(4), nullable=False, default="FS")
    # FS (Finish→Start) | SS (Start→Start) | FF (Finish→Finish) | SF (Start→Finish)
    delai_jours: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Lag (>0) ou Lead (<0) en jours

    def __repr__(self) -> str:
        return f"<Lien {self.predecesseur_id} -{self.type}({self.delai_jours:+d})→ {self.successeur_id}>"
