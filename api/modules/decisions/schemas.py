"""
Schémas Pydantic du module decisions.

Trois entités CRUD :
  - Decision    (CRUD + filtres dashboard)
  - Task        (CRUD léger, toujours lié à une décision ou une affaire)
  - Observation (CRUD léger + analyse Argos)

Plus les schémas KPI pour alimenter le dashboard.
"""
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── Décisions ────────────────────────────────────────────────────────

class DecisionCreateRequest(BaseModel):
    affaire_id: Optional[UUID] = None
    objet: str = Field(..., min_length=3, max_length=2000)
    sujet: Optional[str] = Field(None, max_length=256)
    contexte: Optional[str] = None
    constat: Optional[str] = None
    analyse: Optional[str] = None
    impacts: Optional[str] = None
    options: Optional[list[dict]] = None
    criticite: str = Field("C2", pattern="^C[1-5]$")
    dette: str = Field("D0", pattern="^D[0-3]$")
    statut: str = Field("ouvert", pattern="^(ouvert|validé|suspendu|caduc|a_revoir)$")
    agent_source: Optional[str] = None
    phase: Optional[str] = Field(None, pattern="^(APS|APD|PRO|DCE|ACT|EXE|DOE)$")
    lot: Optional[str] = Field(None, max_length=64)
    agents_impliques: list[str] = Field(default_factory=list)
    impact_cout: Optional[float] = None
    impact_delai: Optional[int] = None
    responsable: Optional[str] = Field(None, max_length=128)
    date_decision: Optional[date] = None


class DecisionUpdateRequest(BaseModel):
    objet: Optional[str] = Field(None, min_length=3, max_length=2000)
    sujet: Optional[str] = Field(None, max_length=256)
    contexte: Optional[str] = None
    constat: Optional[str] = None
    analyse: Optional[str] = None
    impacts: Optional[str] = None
    options: Optional[list[dict]] = None
    criticite: Optional[str] = Field(None, pattern="^C[1-5]$")
    dette: Optional[str] = Field(None, pattern="^D[0-3]$")
    statut: Optional[str] = Field(
        None, pattern="^(ouvert|validé|suspendu|caduc|a_revoir)$"
    )
    phase: Optional[str] = Field(None, pattern="^(APS|APD|PRO|DCE|ACT|EXE|DOE)$")
    lot: Optional[str] = None
    agents_impliques: Optional[list[str]] = None
    impact_cout: Optional[float] = None
    impact_delai: Optional[int] = None
    responsable: Optional[str] = None
    date_decision: Optional[date] = None
    phase_revision: Optional[str] = Field(
        None, pattern="^(APS|APD|PRO|DCE|ACT|EXE|DOE)$"
    )


class DecisionResponse(BaseModel):
    id: UUID
    affaire_id: Optional[UUID]
    run_id: Optional[UUID]
    objet: str
    sujet: Optional[str]
    contexte: Optional[str]
    constat: Optional[str]
    analyse: Optional[str]
    impacts: Optional[str]
    options: Optional[list]
    criticite: str
    dette: str
    statut: str
    agent_source: Optional[str]
    phase: Optional[str]
    lot: Optional[str]
    agents_impliques: list
    impact_cout: Optional[float]
    impact_delai: Optional[int]
    responsable: Optional[str]
    date_decision: Optional[date]
    phase_revision: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class DecisionRow(BaseModel):
    """Version pour la TABLE 1 du dashboard — colonnes exactes de l'archi."""
    id: UUID
    phase: Optional[str]
    sujet: Optional[str]
    lot: Optional[str]
    criticite: str
    dette: str
    statut: str
    agents_impliques: list
    impact_cout: Optional[float]
    impact_delai: Optional[int]
    responsable: Optional[str]
    date_decision: Optional[date]
    phase_revision: Optional[str]
    # Enrichissement dynamique (join avec decision_scores)
    score: Optional[int] = None

    model_config = {"from_attributes": True}


# ── Tâches ───────────────────────────────────────────────────────────

class TaskCreateRequest(BaseModel):
    affaire_id: Optional[UUID] = None
    decision_id: Optional[UUID] = None
    titre: str = Field(..., min_length=3, max_length=256)
    description: Optional[str] = None
    urgence: int = Field(3, ge=1, le=5)
    statut: str = Field("ouvert", pattern="^(ouvert|en_cours|clos|bloque)$")
    responsable: Optional[str] = Field(None, max_length=128)
    echeance: Optional[date] = None


class TaskUpdateRequest(BaseModel):
    titre: Optional[str] = Field(None, min_length=3, max_length=256)
    description: Optional[str] = None
    urgence: Optional[int] = Field(None, ge=1, le=5)
    statut: Optional[str] = Field(None, pattern="^(ouvert|en_cours|clos|bloque)$")
    responsable: Optional[str] = None
    echeance: Optional[date] = None


class TaskResponse(BaseModel):
    id: UUID
    affaire_id: Optional[UUID]
    decision_id: Optional[UUID]
    titre: str
    description: Optional[str]
    urgence: int
    statut: str
    responsable: Optional[str]
    echeance: Optional[date]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Observations ────────────────────────────────────────────────────

class ObservationCreateRequest(BaseModel):
    affaire_id: Optional[UUID] = None
    decision_id: Optional[UUID] = None
    source: str = Field(..., pattern="^(voix|photo|mail|note)$")
    contenu_brut: Optional[str] = None
    storage_key: Optional[str] = None


class ObservationUpdateRequest(BaseModel):
    analyse_argos: Optional[str] = None
    traitement: Optional[str] = Field(
        None, pattern="^(a_traiter|en_cours|traite|ignore)$"
    )
    decision_id: Optional[UUID] = None


class ObservationResponse(BaseModel):
    id: UUID
    affaire_id: Optional[UUID]
    decision_id: Optional[UUID]
    source: str
    contenu_brut: Optional[str]
    storage_key: Optional[str]
    analyse_argos: Optional[str]
    traitement: str
    auteur: Optional[UUID]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Dashboard KPIs ──────────────────────────────────────────────────

class DecisionKPIs(BaseModel):
    """KPIs du dashboard — alignés sur l'archi utilisateur."""
    decisions_critiques: int       # C4 + C5
    dette_moyenne: float           # 0-3 (D0=0, D3=3)
    delai_resolution_moyen: float  # jours
    taux_revues: float             # 0.0-1.0 (décisions ayant changé de statut)
    total_decisions: int
    total_taches_ouvertes: int
    total_observations_a_traiter: int


class TimelineBucket(BaseModel):
    phase: str
    total: int
    critiques: int
    dettes_d2_d3: int


class LotBucket(BaseModel):
    lot: str
    total: int
    critiques: int
    score_moyen: Optional[float]
