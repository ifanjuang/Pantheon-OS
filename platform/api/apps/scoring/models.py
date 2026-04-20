"""
Modèles scoring — DecisionScore.

Évalue la robustesse d'une décision projet sur 100 points répartis en
5 axes alignés sur le panthéon ARCEUS :

  - Technique (/25)        → Héphaïstos    (faisabilité + complexité + risque)
  - Contractuel (/25)      → Thémis        (conformité + responsabilité + traçabilité)
  - Planning (/20)         → Chronos       (impact délai + dépendances + urgence)
  - Cohérence (/15)        → Apollon       (alignement + lisibilité)
  - Robustesse logique (/15) → Prométhée   (hypothèses + incertitude)

Une ligne = un calcul (historique complet). Pour récupérer le score
actif d'une décision, prendre le plus récent.

Bonus/malus appliqués automatiquement par ScoringService :
  +5  si précédent validé trouvé dans le wiki (scope=agence)
  -10 si dette = D3
  -5  si certitude < 0.5
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


VERDICTS = ("robuste", "acceptable", "fragile", "dangereux")
MODES = ("manuel", "auto_llm", "hybride")


class DecisionScore(Base):
    __tablename__ = "decision_scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    decision_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("project_decisions.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    affaire_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("affaires.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # Sujet libre pour scorer une hypothèse hors décision formalisée
    sujet: Mapped[str] = mapped_column(String(512), nullable=False)

    # Détail des axes (structure validée par schemas.AxesDetail)
    # {
    #   "technique":   {"faisabilite": 8, "complexite": 4, "risque": 7,
    #                   "total": 19, "commentaire": "..."},
    #   "contractuel": {...},
    #   "planning":    {...},
    #   "coherence":   {...},
    #   "logique":     {...}
    # }
    axes: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    total_raw: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Somme des axes avant bonus/malus (0-100)

    bonus_malus: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # [{"code": "precedent_valide", "label": "Déjà validé en agence", "delta": 5,
    #   "reason": "Précédent page-slug"}]

    total_final: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Clamp(total_raw + sum(deltas), 0, 100)

    verdict: Mapped[str] = mapped_column(String(16), nullable=False, default="fragile")
    # robuste | acceptable | fragile | dangereux

    certitude: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    # 0-1 : confiance subjective dans le scoring (source du malus -5 si < 0.5)

    dette_snapshot: Mapped[str | None] = mapped_column(String(2), nullable=True)
    # Snapshot de la dette (D0-D3) au moment du scoring, source du malus -10

    mode: Mapped[str] = mapped_column(String(16), nullable=False, default="manuel")
    # manuel | auto_llm | hybride

    computed_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=_now)

    def __repr__(self) -> str:
        return f"<DecisionScore {self.total_final}/100 ({self.verdict})>"
