from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

STATUTS_LOT = {"planifie", "en_cours", "termine", "suspendu"}
STATUTS_TACHE = {"planifiee", "en_cours", "terminee", "bloquee", "annulee"}
STATUTS_JALON = {"a_venir", "atteint", "manque", "reporte"}
TYPES_JALON = {"administratif", "contractuel", "technique", "livraison"}
TYPES_LIEN = {"FS", "SS", "FF", "SF"}


# ── Lots ─────────────────────────────────────────────────────────────

class LotCreate(BaseModel):
    code: str
    nom: str
    entreprise: str | None = None
    date_debut: date | None = None
    date_fin: date | None = None
    statut: str = "planifie"
    montant_marche: float | None = None

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str) -> str:
        if v not in STATUTS_LOT:
            raise ValueError(f"Statut lot invalide. Valeurs : {sorted(STATUTS_LOT)}")
        return v

    @field_validator("montant_marche")
    @classmethod
    def montant_positif(cls, v: float | None) -> float | None:
        if v is not None and v < 0:
            raise ValueError("Le montant doit être positif")
        return v


class LotUpdate(BaseModel):
    code: str | None = None
    nom: str | None = None
    entreprise: str | None = None
    date_debut: date | None = None
    date_fin: date | None = None
    statut: str | None = None
    montant_marche: float | None = None

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUTS_LOT:
            raise ValueError(f"Statut lot invalide. Valeurs : {sorted(STATUTS_LOT)}")
        return v


class LotResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    code: str
    nom: str
    entreprise: str | None
    date_debut: date | None
    date_fin: date | None
    statut: str
    montant_marche: float | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Tâches ───────────────────────────────────────────────────────────

class TacheCreate(BaseModel):
    titre: str
    lot_id: UUID | None = None
    description: str | None = None
    responsable: str | None = None
    date_debut_prevue: date | None = None
    date_fin_prevue: date | None = None
    duree_jours: int | None = None
    statut: str = "planifiee"
    avancement: int = Field(default=0, ge=0, le=100)

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str) -> str:
        if v not in STATUTS_TACHE:
            raise ValueError(f"Statut tâche invalide. Valeurs : {sorted(STATUTS_TACHE)}")
        return v

    @field_validator("duree_jours")
    @classmethod
    def duree_positive(cls, v: int | None) -> int | None:
        if v is not None and v <= 0:
            raise ValueError("La durée doit être > 0")
        return v


class TacheUpdate(BaseModel):
    titre: str | None = None
    lot_id: UUID | None = None
    description: str | None = None
    responsable: str | None = None
    date_debut_prevue: date | None = None
    date_fin_prevue: date | None = None
    date_debut_reelle: date | None = None
    date_fin_reelle: date | None = None
    duree_jours: int | None = None
    avancement: int | None = Field(default=None, ge=0, le=100)
    statut: str | None = None

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUTS_TACHE:
            raise ValueError(f"Statut tâche invalide. Valeurs : {sorted(STATUTS_TACHE)}")
        return v


class TacheResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    lot_id: UUID | None
    titre: str
    description: str | None
    responsable: str | None
    date_debut_prevue: date | None
    date_fin_prevue: date | None
    date_debut_reelle: date | None
    date_fin_reelle: date | None
    duree_jours: int | None
    avancement: int
    statut: str
    critique: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Jalons ───────────────────────────────────────────────────────────

class JalonCreate(BaseModel):
    nom: str
    type: str = "technique"
    date_cible: date
    statut: str = "a_venir"
    tache_id: UUID | None = None

    @field_validator("type")
    @classmethod
    def type_valid(cls, v: str) -> str:
        if v not in TYPES_JALON:
            raise ValueError(f"Type jalon invalide. Valeurs : {sorted(TYPES_JALON)}")
        return v

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str) -> str:
        if v not in STATUTS_JALON:
            raise ValueError(f"Statut jalon invalide. Valeurs : {sorted(STATUTS_JALON)}")
        return v


class JalonUpdate(BaseModel):
    nom: str | None = None
    type: str | None = None
    date_cible: date | None = None
    date_reelle: date | None = None
    statut: str | None = None
    tache_id: UUID | None = None

    @field_validator("type")
    @classmethod
    def type_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in TYPES_JALON:
            raise ValueError(f"Type jalon invalide. Valeurs : {sorted(TYPES_JALON)}")
        return v

    @field_validator("statut")
    @classmethod
    def statut_valid(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUTS_JALON:
            raise ValueError(f"Statut jalon invalide. Valeurs : {sorted(STATUTS_JALON)}")
        return v


class JalonResponse(BaseModel):
    id: UUID
    affaire_id: UUID
    tache_id: UUID | None
    nom: str
    type: str
    date_cible: date
    date_reelle: date | None
    statut: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Liens de dépendance ──────────────────────────────────────────────

class LienCreate(BaseModel):
    predecesseur_id: UUID
    successeur_id: UUID
    type: str = "FS"
    delai_jours: int = 0

    @field_validator("type")
    @classmethod
    def type_valid(cls, v: str) -> str:
        if v not in TYPES_LIEN:
            raise ValueError(f"Type lien invalide. Valeurs : {sorted(TYPES_LIEN)}")
        return v

    @field_validator("successeur_id")
    @classmethod
    def no_self_loop(cls, v: UUID, info) -> UUID:
        if "predecesseur_id" in (info.data or {}) and v == info.data["predecesseur_id"]:
            raise ValueError("Une tâche ne peut pas dépendre d'elle-même")
        return v


class LienResponse(BaseModel):
    id: UUID
    predecesseur_id: UUID
    successeur_id: UUID
    type: str
    delai_jours: int

    model_config = {"from_attributes": True}


# ── Propagation ──────────────────────────────────────────────────────

class PropagateRequest(BaseModel):
    delta_jours: int = Field(..., description="Décalage en jours (positif = retard, négatif = avance)")


class PropagationResult(BaseModel):
    taches_impactees: int
    details: list[dict]


# ── Vues agrégées ────────────────────────────────────────────────────

class GanttResponse(BaseModel):
    affaire_id: UUID
    lots: list[LotResponse]
    taches: list[TacheResponse]
    jalons: list[JalonResponse]
    liens: list[LienResponse]


class CriticalPathTaskResult(BaseModel):
    id: UUID
    titre: str
    est: int    # Early Start (jours depuis t=0)
    eft: int    # Early Finish
    lst: int    # Late Start
    lft: int    # Late Finish
    float_jours: int   # Marge totale (0 = critique)
    critique: bool


class CriticalPathResult(BaseModel):
    affaire_id: UUID
    duree_projet_jours: int
    nb_taches_critiques: int
    cycle_detecte: bool
    taches: list[CriticalPathTaskResult]


class PlanningHealth(BaseModel):
    affaire_id: UUID
    # Tâches
    total_taches: int
    taches_planifiees: int
    taches_en_cours: int
    taches_terminees: int
    taches_bloquees: int
    taches_en_retard: int       # date_fin_prevue < aujourd'hui et non terminée/annulée
    avancement_moyen: float     # moyenne sur tâches non annulées
    # Jalons
    total_jalons: int
    jalons_atteints: int
    jalons_manques: int         # date_cible < aujourd'hui et statut != atteint
    jalons_a_venir: int
    # Lots
    total_lots: int
    lots_en_cours: int
    lots_termines: int
    # Score global 0-100
    score_sante: int
