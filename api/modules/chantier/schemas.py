from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

SOURCES = {"photo", "voix", "note", "mail"}
STATUTS_OBS = {"a_analyser", "en_cours", "analyse", "ignore"}
GRAVITES = {"mineure", "majeure", "critique", "arret_chantier"}
STATUTS_NC = {"ouverte", "en_cours", "resolue", "contestee"}


# ── Observations terrain ──────────────────────────────────────────────

class ObservationCreate(BaseModel):
    source: str
    date_constat: date
    contenu_brut: str | None = None
    storage_key: str | None = None
    localisation: str | None = None
    entreprise: str | None = None
    lot_id: UUID | None = None
    statut: str = "a_analyser"

    @field_validator("source")
    @classmethod
    def source_valid(cls, v: str) -> str:
        if v not in SOURCES:
            raise ValueError(f"Source invalide. Valeurs : {sorted(SOURCES)}")
        return v

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str) -> str:
        if v not in STATUTS_OBS:
            raise ValueError(f"Statut invalide. Valeurs : {sorted(STATUTS_OBS)}")
        return v


class ObservationUpdate(BaseModel):
    source: str | None = None
    date_constat: date | None = None
    contenu_brut: str | None = None
    storage_key: str | None = None
    localisation: str | None = None
    entreprise: str | None = None
    lot_id: UUID | None = None
    statut: str | None = None
    analyse_argos: str | None = None

    @field_validator("source")
    @classmethod
    def source_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in SOURCES:
            raise ValueError(f"Source invalide. Valeurs : {sorted(SOURCES)}")
        return v

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUTS_OBS:
            raise ValueError(f"Statut invalide. Valeurs : {sorted(STATUTS_OBS)}")
        return v


class ObservationResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    lot_id: UUID | None
    source: str
    date_constat: date
    contenu_brut: str | None
    storage_key: str | None
    localisation: str | None
    entreprise: str | None
    auteur: UUID | None
    analyse_argos: str | None
    statut: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Non-conformités ───────────────────────────────────────────────────

class NonConformiteCreate(BaseModel):
    description: str
    gravite: str = "mineure"
    date_detection: date
    observation_id: UUID | None = None
    lot_id: UUID | None = None
    entreprise: str | None = None
    date_echeance: date | None = None
    responsable: str | None = None
    action_requise: str | None = None
    decision_id: UUID | None = None

    @field_validator("gravite")
    @classmethod
    def gravite_valid(cls, v: str) -> str:
        if v not in GRAVITES:
            raise ValueError(f"Gravité invalide. Valeurs : {sorted(GRAVITES)}")
        return v


class NonConformiteUpdate(BaseModel):
    description: str | None = None
    gravite: str | None = None
    date_echeance: date | None = None
    date_resolution: date | None = None
    statut: str | None = None
    responsable: str | None = None
    action_requise: str | None = None
    analyse_hephaistos: str | None = None
    decision_id: UUID | None = None
    arret_chantier: bool | None = None

    @field_validator("gravite")
    @classmethod
    def gravite_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in GRAVITES:
            raise ValueError(f"Gravité invalide. Valeurs : {sorted(GRAVITES)}")
        return v

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUTS_NC:
            raise ValueError(f"Statut NC invalide. Valeurs : {sorted(STATUTS_NC)}")
        return v


class NonConformiteResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    observation_id: UUID | None
    lot_id: UUID | None
    decision_id: UUID | None
    entreprise: str | None
    description: str
    gravite: str
    date_detection: date
    date_echeance: date | None
    date_resolution: date | None
    statut: str
    responsable: str | None
    action_requise: str | None
    analyse_hephaistos: str | None
    arret_chantier: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Réponses pipeline ─────────────────────────────────────────────────

class AnalyzeJobResponse(BaseModel):
    job_queued: bool
    id: UUID
    message: str


# ── Dashboard ─────────────────────────────────────────────────────────

class ChantierDashboard(BaseModel):
    affaire_id: UUID
    # Observations
    total_observations: int
    observations_a_analyser: int
    observations_analysees: int
    # Non-conformités
    total_nc: int
    nc_ouvertes: int
    nc_en_cours: int
    nc_resolues: int
    nc_critiques: int           # gravite=critique ou arret_chantier
    nc_en_retard: int           # date_echeance < today et non résolue
    # Alertes
    alerte_arret_chantier: bool # au moins une NC arret_chantier ouverte
