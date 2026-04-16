from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, field_validator

PHASES_VALIDES = {"ESQ", "APS", "APD", "PRO", "ACT", "VISA", "DET", "AOR"}

ERP_TYPES = {
    "J", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "W", "X", "Y",
    "PA", "CTS", "SG", "OA", "GA", "EF", "REF",
}
ERP_CATEGORIES = {"1", "2", "3", "4", "5"}


class AffaireCreate(BaseModel):
    code: str
    nom: str
    description: str | None = None
    statut: str = "actif"

    # Contexte projet (migration 0009)
    typology: str | None = None
    region: str | None = None
    budget_moa: float | None = None
    honoraires: float | None = None
    date_debut: date | None = None
    date_fin_prevue: date | None = None
    phase_courante: str | None = None
    abf: bool = False
    zone_risque: dict[str, Any] | None = None

    # Classification ERP (migration 0020)
    erp_type: str | None = None
    erp_categorie: str | None = None

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str) -> str:
        if v not in {"actif", "archive", "clos"}:
            raise ValueError("Statut invalide. Valeurs acceptées : actif, archive, clos")
        return v

    @field_validator("code")
    @classmethod
    def code_clean(cls, v: str) -> str:
        return v.strip().upper()

    @field_validator("phase_courante")
    @classmethod
    def phase_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in PHASES_VALIDES:
            raise ValueError(f"Phase invalide. Valeurs : {sorted(PHASES_VALIDES)}")
        return v

    @field_validator("budget_moa", "honoraires")
    @classmethod
    def montant_positif(cls, v: float | None) -> float | None:
        if v is not None and v < 0:
            raise ValueError("Le montant doit être positif")
        return v

    @field_validator("erp_type")
    @classmethod
    def erp_type_valid(cls, v: str | None) -> str | None:
        if v is not None and v.upper() not in ERP_TYPES:
            raise ValueError(f"Type ERP invalide. Valeurs : {sorted(ERP_TYPES)}")
        return v.upper() if v is not None else None

    @field_validator("erp_categorie")
    @classmethod
    def erp_categorie_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in ERP_CATEGORIES:
            raise ValueError(f"Catégorie ERP invalide. Valeurs : {sorted(ERP_CATEGORIES)}")
        return v


class AffaireUpdate(BaseModel):
    nom: str | None = None
    description: str | None = None
    statut: str | None = None

    # Contexte projet (migration 0009)
    typology: str | None = None
    region: str | None = None
    budget_moa: float | None = None
    honoraires: float | None = None
    date_debut: date | None = None
    date_fin_prevue: date | None = None
    phase_courante: str | None = None
    abf: bool | None = None
    zone_risque: dict[str, Any] | None = None

    # Classification ERP (migration 0020)
    erp_type: str | None = None
    erp_categorie: str | None = None

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in {"actif", "archive", "clos"}:
            raise ValueError("Statut invalide. Valeurs acceptées : actif, archive, clos")
        return v

    @field_validator("phase_courante")
    @classmethod
    def phase_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in PHASES_VALIDES:
            raise ValueError(f"Phase invalide. Valeurs : {sorted(PHASES_VALIDES)}")
        return v

    @field_validator("budget_moa", "honoraires")
    @classmethod
    def montant_positif(cls, v: float | None) -> float | None:
        if v is not None and v < 0:
            raise ValueError("Le montant doit être positif")
        return v

    @field_validator("erp_type")
    @classmethod
    def erp_type_valid(cls, v: str | None) -> str | None:
        if v is not None and v.upper() not in ERP_TYPES:
            raise ValueError(f"Type ERP invalide. Valeurs : {sorted(ERP_TYPES)}")
        return v.upper() if v is not None else None

    @field_validator("erp_categorie")
    @classmethod
    def erp_categorie_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in ERP_CATEGORIES:
            raise ValueError(f"Catégorie ERP invalide. Valeurs : {sorted(ERP_CATEGORIES)}")
        return v


class AffaireResponse(BaseModel):
    id: UUID
    code: str
    nom: str
    description: str | None
    statut: str
    created_by: UUID | None
    created_at: datetime
    updated_at: datetime

    # Contexte projet (migration 0009)
    typology: str | None = None
    region: str | None = None
    budget_moa: float | None = None
    honoraires: float | None = None
    date_debut: date | None = None
    date_fin_prevue: date | None = None
    phase_courante: str | None = None
    abf: bool = False
    zone_risque: dict[str, Any] | None = None

    # Classification ERP (migration 0020)
    erp_type: str | None = None
    erp_categorie: str | None = None

    model_config = {"from_attributes": True}
