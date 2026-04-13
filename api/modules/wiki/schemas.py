from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── Page ─────────────────────────────────────────────────────────────

class WikiPageCreateRequest(BaseModel):
    """Création manuelle d'une page wiki (sans passer par une décision)."""
    affaire_id: Optional[UUID] = None
    scope: str = Field("projet", pattern="^(projet|agence)$")
    titre: str = Field(..., min_length=3, max_length=512)
    contenu_md: str = Field(..., min_length=10)
    tags: list[str] = Field(default_factory=list)
    criticite: Optional[str] = Field(None, pattern="^C[1-5]$")
    score: Optional[int] = Field(None, ge=0, le=100)
    citations: list[dict] = Field(default_factory=list)


class WikiPageUpdateRequest(BaseModel):
    titre: Optional[str] = Field(None, min_length=3, max_length=512)
    contenu_md: Optional[str] = Field(None, min_length=10)
    tags: Optional[list[str]] = None
    criticite: Optional[str] = Field(None, pattern="^C[1-5]$")
    score: Optional[int] = Field(None, ge=0, le=100)
    scope: Optional[str] = Field(None, pattern="^(projet|agence)$")


class WikiPageResponse(BaseModel):
    id: UUID
    affaire_id: Optional[UUID]
    scope: str
    slug: str
    titre: str
    contenu_md: str
    tags: list[str]
    criticite: Optional[str]
    score: Optional[int]
    decision_id: Optional[UUID]
    source_run_id: Optional[UUID]
    citations: list[dict]
    validated_by: Optional[UUID]
    validated_at: Optional[datetime]
    reuse_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WikiPageSummary(BaseModel):
    """Version allégée pour les listes."""
    id: UUID
    scope: str
    slug: str
    titre: str
    tags: list[str]
    criticite: Optional[str]
    score: Optional[int]
    reuse_count: int
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Recherche & précédents ───────────────────────────────────────────

class WikiSearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    affaire_id: Optional[UUID] = None
    scope: Optional[str] = Field(None, pattern="^(projet|agence)$")
    top_k: int = Field(5, ge=1, le=20)


class WikiSearchHit(BaseModel):
    page: WikiPageSummary
    score: float
    extrait: str


class PrecedentCheckRequest(BaseModel):
    sujet: str = Field(..., min_length=3)
    affaire_id: Optional[UUID] = None
    top_k: int = Field(3, ge=1, le=10)
    increment_reuse: bool = True


class PrecedentResult(BaseModel):
    """
    Résultat d'une vérification de précédent pour le scoring.
    bonus_applicable : +5 si au moins un précédent agence validé est trouvé.
    """
    bonus_applicable: bool
    bonus_points: int
    precedents: list[WikiSearchHit]


# ── Promotion depuis une décision ────────────────────────────────────

class PromoteDecisionRequest(BaseModel):
    """
    Promeut une project_decision validée en page wiki.
    scope='agence' pour en faire un précédent réutilisable entre projets.
    """
    scope: str = Field("projet", pattern="^(projet|agence)$")
    tags: list[str] = Field(default_factory=list)
    contenu_md_override: Optional[str] = None
    # Si None : le service génère le markdown depuis les champs de la décision.
