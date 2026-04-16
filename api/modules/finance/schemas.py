from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

STATUTS_AVENANT = {"en_preparation", "soumis", "accepte", "refuse", "annule"}
STATUTS_SITUATION = {"soumise", "en_revision", "validee", "payee", "contestee"}


# ── Avenants ─────────────────────────────────────────────────────────

class AvenantCreate(BaseModel):
    numero: str
    objet: str
    montant_ht: float
    lot_id: UUID | None = None
    decision_id: UUID | None = None
    impact_delai_jours: int | None = None
    statut: str = "en_preparation"
    date_soumission: date | None = None
    date_acceptation: date | None = None
    storage_key: str | None = None

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str) -> str:
        if v not in STATUTS_AVENANT:
            raise ValueError(f"Statut invalide. Valeurs : {sorted(STATUTS_AVENANT)}")
        return v


class AvenantUpdate(BaseModel):
    numero: str | None = None
    objet: str | None = None
    montant_ht: float | None = None
    lot_id: UUID | None = None
    decision_id: UUID | None = None
    impact_delai_jours: int | None = None
    statut: str | None = None
    date_soumission: date | None = None
    date_acceptation: date | None = None
    storage_key: str | None = None

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUTS_AVENANT:
            raise ValueError(f"Statut invalide. Valeurs : {sorted(STATUTS_AVENANT)}")
        return v


class AvenantResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    lot_id: UUID | None
    decision_id: UUID | None
    numero: str
    objet: str
    montant_ht: float
    impact_delai_jours: int | None
    statut: str
    date_soumission: date | None
    date_acceptation: date | None
    storage_key: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Situations de travaux ─────────────────────────────────────────────

class SituationCreate(BaseModel):
    entreprise: str
    numero: int = Field(ge=1)
    periode_debut: date
    periode_fin: date
    montant_demande_ht: float = Field(ge=0)
    date_soumission: date
    lot_id: UUID | None = None
    avancement_declare: int = Field(default=0, ge=0, le=100)
    statut: str = "soumise"
    storage_key: str | None = None
    remarques: str | None = None

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str) -> str:
        if v not in STATUTS_SITUATION:
            raise ValueError(f"Statut invalide. Valeurs : {sorted(STATUTS_SITUATION)}")
        return v


class SituationUpdate(BaseModel):
    entreprise: str | None = None
    periode_debut: date | None = None
    periode_fin: date | None = None
    montant_demande_ht: float | None = None
    montant_valide_ht: float | None = None
    avancement_declare: int | None = Field(default=None, ge=0, le=100)
    avancement_valide: int | None = Field(default=None, ge=0, le=100)
    statut: str | None = None
    date_validation: date | None = None
    date_paiement: date | None = None
    storage_key: str | None = None
    remarques: str | None = None

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUTS_SITUATION:
            raise ValueError(f"Statut invalide. Valeurs : {sorted(STATUTS_SITUATION)}")
        return v


class SituationResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    lot_id: UUID | None
    entreprise: str
    numero: int
    periode_debut: date
    periode_fin: date
    montant_demande_ht: float
    montant_valide_ht: float | None
    avancement_declare: int
    avancement_valide: int | None
    statut: str
    date_soumission: date
    date_validation: date | None
    date_paiement: date | None
    storage_key: str | None
    remarques: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Dashboard financier ───────────────────────────────────────────────

class FinanceDashboard(BaseModel):
    affaire_id: UUID

    # Enveloppe MOA
    budget_moa: float | None           # affaire.budget_moa
    honoraires_moe: float | None       # affaire.honoraires

    # Marchés de travaux (somme planning_lots.montant_marche)
    montant_marches_initial: float     # base contractuelle brute

    # Avenants
    avenants_acceptes_ht: float        # somme avenants acceptés
    avenants_en_attente_ht: float      # soumis + en_preparation
    nb_avenants_en_attente: int

    # Montant contractuel total = initial + acceptés
    montant_contractuel_ht: float

    # Situations
    montant_reclame_ht: float          # somme demandes soumises+en_revision+validees+payees
    montant_valide_ht: float           # somme validées + payées
    montant_paye_ht: float             # somme payées uniquement
    nb_situations_en_attente: int      # soumises + en_revision

    # Ratios et dérives
    taux_engagement: float | None      # contractuel / budget_moa * 100
    taux_realisation: float | None     # valide / contractuel * 100
    derive_ht: float | None            # contractuel - budget_moa (positif = dépassement)
