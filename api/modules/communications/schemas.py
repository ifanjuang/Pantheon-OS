from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, field_validator

SENS = {"entrant", "sortant"}
TYPES_DOC = {"courrier", "email", "lr", "mise_en_demeure", "bc", "devis", "pv", "cr", "autre"}
STATUTS = {"recu", "en_attente_reponse", "traite", "sans_suite", "archive"}


# ── Courrier ──────────────────────────────────────────────────────────


class CourrierCreate(BaseModel):
    sens: str
    objet: str
    emetteur: str
    destinataire: str
    type_doc: str = "courrier"
    reference: str | None = None
    resume: str | None = None
    storage_key: str | None = None
    date_emission: date | None = None
    date_reception: date | None = None
    delai_reponse: date | None = None
    statut: str = "recu"
    # Liens métier
    lot_id: UUID | None = None
    decision_id: UUID | None = None
    observation_id: UUID | None = None
    reponse_id: UUID | None = None

    @field_validator("sens")
    @classmethod
    def sens_valid(cls, v: str) -> str:
        if v not in SENS:
            raise ValueError(f"Sens invalide. Valeurs : {sorted(SENS)}")
        return v

    @field_validator("type_doc")
    @classmethod
    def type_valid(cls, v: str) -> str:
        if v not in TYPES_DOC:
            raise ValueError(f"Type invalide. Valeurs : {sorted(TYPES_DOC)}")
        return v

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str) -> str:
        if v not in STATUTS:
            raise ValueError(f"Statut invalide. Valeurs : {sorted(STATUTS)}")
        return v


class CourrierUpdate(BaseModel):
    sens: str | None = None
    objet: str | None = None
    emetteur: str | None = None
    destinataire: str | None = None
    type_doc: str | None = None
    reference: str | None = None
    resume: str | None = None
    storage_key: str | None = None
    date_emission: date | None = None
    date_reception: date | None = None
    delai_reponse: date | None = None
    date_reponse_effective: date | None = None
    statut: str | None = None
    lot_id: UUID | None = None
    decision_id: UUID | None = None
    observation_id: UUID | None = None
    reponse_id: UUID | None = None
    draft_iris: str | None = None

    @field_validator("sens")
    @classmethod
    def sens_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in SENS:
            raise ValueError(f"Sens invalide. Valeurs : {sorted(SENS)}")
        return v

    @field_validator("type_doc")
    @classmethod
    def type_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in TYPES_DOC:
            raise ValueError(f"Type invalide. Valeurs : {sorted(TYPES_DOC)}")
        return v

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUTS:
            raise ValueError(f"Statut invalide. Valeurs : {sorted(STATUTS)}")
        return v


class CourrierResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    sens: str
    type_doc: str
    reference: str | None
    emetteur: str
    destinataire: str
    objet: str
    resume: str | None
    storage_key: str | None
    date_emission: date | None
    date_reception: date | None
    delai_reponse: date | None
    date_reponse_effective: date | None
    statut: str
    lot_id: UUID | None
    decision_id: UUID | None
    observation_id: UUID | None
    reponse_id: UUID | None
    auteur_id: UUID | None
    draft_iris: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Pipeline Iris ─────────────────────────────────────────────────────


class DraftJobResponse(BaseModel):
    job_queued: bool
    id: UUID
    message: str


# ── Dashboard ─────────────────────────────────────────────────────────


class CommunicationsDashboard(BaseModel):
    affaire_id: UUID
    total: int
    entrants: int
    sortants: int
    en_attente_reponse: int  # statut = en_attente_reponse
    en_retard: int  # delai_reponse < today et non traité/archivé
    mises_en_demeure: int  # type_doc = mise_en_demeure
    sans_suite: int
