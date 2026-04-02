from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── CR ──────────────────────────────────────────────────────────────

class CRCreateRequest(BaseModel):
    """Saisie manuelle d'un CR (sans upload de fichier)."""
    affaire_id: UUID
    titre: str = Field(..., min_length=3)
    contenu_brut: str = Field(..., min_length=20)
    date_reunion: Optional[date] = None
    participants: list[str] = []


class CRResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    titre: str
    date_reunion: Optional[date]
    participants: list[str]
    synthese: Optional[str]
    analyse_status: str
    document_id: Optional[UUID]
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Actions ─────────────────────────────────────────────────────────

class ActionResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    cr_id: Optional[UUID]
    description: str
    responsable: Optional[str]
    echeance: Optional[date]
    priorite: str
    statut: str
    contexte: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ActionUpdateRequest(BaseModel):
    statut: Optional[str] = None          # ouvert | en_cours | clos | reporte
    responsable: Optional[str] = None
    echeance: Optional[date] = None
    priorite: Optional[str] = None


class ActionCreateRequest(BaseModel):
    """Création manuelle d'une action (hors CR)."""
    affaire_id: UUID
    description: str = Field(..., min_length=5)
    responsable: Optional[str] = None
    echeance: Optional[date] = None
    priorite: str = "normale"


# ── Agenda ──────────────────────────────────────────────────────────

class AgendaGenerateRequest(BaseModel):
    affaire_id: UUID
    date_prevue: Optional[date] = None
    instructions_supplementaires: Optional[str] = None
    # Ex : "Inclure un point sur le planning révisé"


class AgendaItem(BaseModel):
    ordre: int
    sujet: str
    type: str           # urgence | suivi | nouveau | decision
    porteur: str = ""
    duree_min: int = 10
    contexte: str = ""


class AgendaResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    titre: str
    date_prevue: Optional[date]
    items: list[dict]
    notes_preparatoires: Optional[str]
    actions_incluses: list
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Analyse CR (réponse interne) ─────────────────────────────────────

class CRAnalysisResult(BaseModel):
    titre_reunion: str = ""
    date_reunion: Optional[str] = None
    participants: list[str] = []
    actions: list[dict] = []
    synthese: str = ""
