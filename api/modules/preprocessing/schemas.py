"""
Schémas preprocessing — normalisation d'entrée et verdict Precheck.

Deux structures principales :

  PreprocessedInput : sortie d'Hermès (preprocessor)
    - cleaned_question / reformulated_question : texte normalisé
    - intent / phase_projet / domaine : qualification Hermès
    - project_detected : indice d'affaire
    - missing_information / confidence : qualité de l'interprétation
    - suggested_criticite : C1-C5 estimée

  PrecheckDecision : verdict du gate avant dispatch
    - verdict : approved | trim | upgrade | clarification | blocked
    - suggested_subtask_ids / suggested_criticite : ajustements
    - clarification_message : question à renvoyer à l'utilisateur
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field


# ── Preprocessor output ─────────────────────────────────────────────


class PreprocessedInput(BaseModel):
    """Entrée brute normalisée par Hermès."""

    cleaned_question: str = Field(..., description="Message nettoyé (salutations, fautes, ponctuation parasite)")
    reformulated_question: str = Field(..., description="Demande reformulée en mode opérationnel (1-2 phrases)")
    intent: Literal[
        "information",
        "question",
        "decision_locale",
        "decision_engageante",
        "alerte",
        "production",
    ] = Field("question", description="Type de demande Hermès")
    phase_projet: Optional[str] = Field(
        None,
        description="ESQ/APS/APD/PRO/ACT/VISA/DET/AOR/Hors-phase — null si inconnu",
    )
    domaine: Optional[str] = Field(
        None,
        description="Technique/Contractuel/Planning/Relationnel/Administratif/Financier",
    )
    project_detected: Optional[str] = Field(None, description="Indice d'affaire détecté (nom, numéro, adresse)")
    missing_information: list[str] = Field(
        default_factory=list,
        description="Infos critiques manquantes pour trancher",
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confiance globale de l'interprétation")
    suggested_criticite: Optional[str] = Field(
        None,
        pattern=r"^C[1-5]$",
        description="Criticité suggérée par Hermès",
    )


# ── Precheck verdict ─────────────────────────────────────────────────


class PrecheckDecision(BaseModel):
    """Verdict du gate Precheck après zeus_distribute."""

    verdict: Literal["approved", "trim", "upgrade", "clarification", "blocked"] = Field(
        ..., description="Décision du gate"
    )
    reasoning: str = Field(..., description="Justification courte (1-2 phrases)")
    suggested_subtask_ids: list[str] = Field(
        default_factory=list,
        description="IDs des subtasks à conserver (verdict=trim)",
    )
    suggested_criticite: Optional[str] = Field(
        None,
        pattern=r"^C[1-5]$",
        description="Nouvelle criticité (verdict=upgrade)",
    )
    clarification_message: str = Field(
        "",
        description="Message à retourner à l'utilisateur (clarification|blocked)",
    )


# ── Requêtes router (debug / preview) ───────────────────────────────


class PreprocessRequest(BaseModel):
    message: str = Field(..., min_length=3, max_length=4000)
    affaire_hint: Optional[str] = None
    phase_hint: Optional[str] = None
    domaine_hint: Optional[str] = None


class PrecheckRequest(BaseModel):
    instruction: str = Field(..., min_length=3, max_length=4000)
    criticite: str = Field("C2", pattern=r"^C[1-5]$")
    subtasks: list[dict] = Field(default_factory=list)
    preprocessed: Optional[dict] = None
