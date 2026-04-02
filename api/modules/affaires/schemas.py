from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class AffaireCreate(BaseModel):
    code: str
    nom: str
    description: str | None = None
    statut: str = "actif"

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str) -> str:
        allowed = {"actif", "archive", "clos"}
        if v not in allowed:
            raise ValueError(f"Statut invalide. Valeurs acceptées : {allowed}")
        return v

    @field_validator("code")
    @classmethod
    def code_clean(cls, v: str) -> str:
        return v.strip().upper()


class AffaireUpdate(BaseModel):
    nom: str | None = None
    description: str | None = None
    statut: str | None = None

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in {"actif", "archive", "clos"}:
            raise ValueError(f"Statut invalide. Valeurs acceptées : actif, archive, clos")
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

    model_config = {"from_attributes": True}
