"""
Modèles affaires — Affaire (dossier/projet MOE)
"""
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


STATUTS = ("actif", "archive", "clos")


class Affaire(Base):
    __tablename__ = "affaires"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    nom: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    statut: Mapped[str] = mapped_column(String(32), nullable=False, default="actif")

    # Contexte projet — injecté automatiquement dans les prompts agents
    typology: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Logement collectif / Maison individuelle / ERP / Industrie / Équipement public / Réhabilitation / Autre
    region: Mapped[str | None] = mapped_column(String(100), nullable=True)
    budget_moa: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    # Budget MOA total (€ HT)
    honoraires: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    # Honoraires MOE contractuels (€ HT)
    date_debut: Mapped[date | None] = mapped_column(Date, nullable=True)
    date_fin_prevue: Mapped[date | None] = mapped_column(Date, nullable=True)
    phase_courante: Mapped[str | None] = mapped_column(String(20), nullable=True)
    # ESQ | APS | APD | PRO | ACT | VISA | DET | AOR
    abf: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Secteur Architecte des Bâtiments de France
    zone_risque: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    # {inondation: bool, sismique: str, archeo: bool, bruit: str, retrait_gonflement: str}

    # Classification ERP — migration 0020
    erp_type: Mapped[str | None] = mapped_column(String(10), nullable=True)
    # J L M N O P R S T U V W X Y PA CTS SG OA GA EF REF — NULL si non-ERP
    erp_categorie: Mapped[str | None] = mapped_column(String(2), nullable=True)
    # 1 (>1500) | 2 (701-1500) | 3 (301-700) | 4 (≤300) | 5 (seuil réduit) — NULL si non-ERP

    created_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=_now, onupdate=_now
    )

    permissions: Mapped[list["AffairePermission"]] = relationship(  # type: ignore[name-defined]
        back_populates="affaire", cascade="all, delete-orphan"
    )
    documents: Mapped[list["Document"]] = relationship(  # type: ignore[name-defined]
        back_populates="affaire", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Affaire {self.code} — {self.nom}>"
