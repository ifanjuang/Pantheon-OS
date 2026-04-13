"""
Schémas scoring — structure stricte des 5 axes et des calculs.

Les bornes viennent directement de l'architecture :
  Technique /25 : faisabilité /10, complexité /5, risque /10
  Contractuel /25 : conformité /10, responsabilité /10, traçabilité /5
  Planning /20 : impact délai /10, dépendances /5, urgence /5
  Cohérence /15 : alignement /10, lisibilité /5
  Robustesse /15 : hypothèses /10, incertitude /5
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, computed_field


# ── Sous-axes ────────────────────────────────────────────────────────

class TechniqueScore(BaseModel):
    faisabilite: int = Field(..., ge=0, le=10)
    complexite: int = Field(..., ge=0, le=5)
    risque: int = Field(..., ge=0, le=10)
    commentaire: str = ""

    @computed_field
    @property
    def total(self) -> int:
        return self.faisabilite + self.complexite + self.risque


class ContractuelScore(BaseModel):
    conformite: int = Field(..., ge=0, le=10)
    responsabilite: int = Field(..., ge=0, le=10)
    tracabilite: int = Field(..., ge=0, le=5)
    commentaire: str = ""

    @computed_field
    @property
    def total(self) -> int:
        return self.conformite + self.responsabilite + self.tracabilite


class PlanningScore(BaseModel):
    impact_delai: int = Field(..., ge=0, le=10)
    dependances: int = Field(..., ge=0, le=5)
    urgence: int = Field(..., ge=0, le=5)
    commentaire: str = ""

    @computed_field
    @property
    def total(self) -> int:
        return self.impact_delai + self.dependances + self.urgence


class CoherenceScore(BaseModel):
    alignement: int = Field(..., ge=0, le=10)
    lisibilite: int = Field(..., ge=0, le=5)
    commentaire: str = ""

    @computed_field
    @property
    def total(self) -> int:
        return self.alignement + self.lisibilite


class LogiqueScore(BaseModel):
    hypotheses: int = Field(..., ge=0, le=10)
    incertitude: int = Field(..., ge=0, le=5)
    commentaire: str = ""

    @computed_field
    @property
    def total(self) -> int:
        return self.hypotheses + self.incertitude


# ── Ensemble des 5 axes ─────────────────────────────────────────────

class AxesDetail(BaseModel):
    """
    Utilisé à la fois comme payload d'entrée (scoring manuel) et comme
    schéma de sortie du LLM via Instructor (scoring auto).
    """
    technique: TechniqueScore
    contractuel: ContractuelScore
    planning: PlanningScore
    coherence: CoherenceScore
    logique: LogiqueScore

    @computed_field
    @property
    def total(self) -> int:
        return (
            self.technique.total
            + self.contractuel.total
            + self.planning.total
            + self.coherence.total
            + self.logique.total
        )


# ── Bonus / malus ───────────────────────────────────────────────────

class BonusMalus(BaseModel):
    code: str
    label: str
    delta: int  # positif = bonus, négatif = malus
    reason: str = ""


# ── Requêtes ────────────────────────────────────────────────────────

class ScoreManualRequest(BaseModel):
    """Scoring manuel : l'utilisateur fournit directement les sous-scores."""
    sujet: str = Field(..., min_length=3, max_length=512)
    axes: AxesDetail
    affaire_id: Optional[UUID] = None
    decision_id: Optional[UUID] = None
    certitude: float = Field(1.0, ge=0.0, le=1.0)
    dette: Optional[str] = Field(None, pattern="^D[0-3]$")
    # Si None et decision_id fourni, le service lit la dette depuis project_decisions


class ScoreAutoRequest(BaseModel):
    """Scoring automatique via LLM (Instructor) à partir d'un contexte texte."""
    sujet: str = Field(..., min_length=3, max_length=512)
    contexte: str = Field(..., min_length=20)
    affaire_id: Optional[UUID] = None
    decision_id: Optional[UUID] = None
    certitude: float = Field(0.7, ge=0.0, le=1.0)
    dette: Optional[str] = Field(None, pattern="^D[0-3]$")


# ── Réponses ────────────────────────────────────────────────────────

class DecisionScoreResponse(BaseModel):
    id: UUID
    decision_id: Optional[UUID]
    affaire_id: Optional[UUID]
    sujet: str
    axes: dict
    total_raw: int
    bonus_malus: list[dict]
    total_final: int
    verdict: str
    certitude: float
    dette_snapshot: Optional[str]
    mode: str
    computed_by: Optional[UUID]
    computed_at: datetime

    model_config = {"from_attributes": True}


class ScoreSummary(BaseModel):
    """Version allégée pour listes et dashboard."""
    id: UUID
    decision_id: Optional[UUID]
    sujet: str
    total_final: int
    verdict: str
    mode: str
    computed_at: datetime

    model_config = {"from_attributes": True}


# ── Stats dashboard ─────────────────────────────────────────────────

class ScoringStats(BaseModel):
    """KPIs du dashboard — à afficher sur la vue scoring."""
    total_scores: int
    moyenne: float
    distribution: dict[str, int]  # {"robuste": 12, "acceptable": 7, ...}
    dettes_d3: int
    taux_robuste: float  # 0.0-1.0
