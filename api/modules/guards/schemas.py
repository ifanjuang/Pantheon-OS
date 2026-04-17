"""
Schémas guards — quatre gardes-fous explicites.

  CriticalityImpacts / CriticalityVerdict
    Entrée + sortie du `criticality_guard`. Calcule C1-C5 depuis
    l'impact financier, le délai, la sévérité déclarée et l'intent
    Hermès (pas d'appel LLM, règles pures).

  ReversibilityDecision
    Sortie du `reversibility_guard` (LLM). Distingue les décisions
    réversibles (Arès peut agir C3) des irréversibles (HITL obligatoire
    même si C3/C4).

  VetoDecision
    Sortie du `structured_veto` (LLM, remplace la détection keyword).
    Renvoyée par Thémis / Héphaïstos / Apollon. Contient :
      - veto : booléen tranché
      - severity : bloquant (stop) | reserve (garder en trace) | information
      - motif : justification courte
      - condition_levee : ce qu'il faut pour débloquer
"""
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator


# ── criticality_guard ────────────────────────────────────────────────

class CriticalityImpacts(BaseModel):
    """Entrée du criticality_guard."""
    impact_cout: Optional[float] = Field(
        None, description="Impact financier estimé en € TTC"
    )
    impact_delai: Optional[int] = Field(
        None, description="Impact planning estimé en jours"
    )
    severity: Optional[str] = Field(
        None,
        description=(
            "Sévérité déclarée — ex: risque_majeur / securite / litige / "
            "peril / contentieux / decision_engageante / engagement / "
            "contrat / decision_locale / information"
        ),
    )
    intent: Optional[str] = Field(
        None, description="Intent Hermès (alerte, question, production, …)"
    )
    reversible: Optional[bool] = Field(
        None, description="Si False → remonte au moins à C4"
    )


class CriticalityVerdict(BaseModel):
    """Sortie du criticality_guard / criticality_guard_hybrid."""
    criticite: str = Field(..., pattern=r"^C[1-5]$")
    triggers: list[str] = Field(
        default_factory=list,
        description="Raisons qui ont poussé à ce niveau (audit)",
    )
    ai_reasoning: str = Field(
        "",
        description="Raisonnement de la couche AI (vide si couche règles suffit)",
    )
    source: Literal["rules", "hybrid"] = Field(
        "rules",
        description="'rules' = décision purement déterministe | 'hybrid' = AI a confirmé ou upgradé",
    )

    @model_validator(mode="after")
    def _ai_reasoning_requires_hybrid(self) -> "CriticalityVerdict":
        if self.ai_reasoning and self.source == "rules":
            self.source = "hybrid"
        return self


# ── reversibility_guard ─────────────────────────────────────────────

class ReversibilityDecision(BaseModel):
    """Sortie du reversibility_guard (LLM)."""
    reversible: bool = Field(
        ..., description="True si la décision peut être défaite sans coût majeur"
    )
    reasoning: str = Field(
        ..., description="Justification courte (1-2 phrases)"
    )
    rollback_cost: Literal["null", "faible", "modere", "eleve", "bloquant"] = Field(
        "null", description="Coût estimé du rollback si décision prise"
    )
    requires_hitl: bool = Field(
        False,
        description="True si la décision exige une validation humaine quelle que soit la criticité",
    )


# ── structured_veto ──────────────────────────────────────────────────

class VetoDecision(BaseModel):
    """Sortie du structured_veto (LLM) — remplace la détection keyword."""
    veto: bool = Field(..., description="True si l'agent oppose un veto")
    agent: str = Field(..., description="Nom d'agent émetteur (themis, hephaistos, …)")
    severity: Literal["bloquant", "reserve", "information"] = Field(
        "information",
        description=(
            "bloquant  → interrompt l'orchestration (HITL)\n"
            "reserve   → trace la réserve mais continue\n"
            "information → simple signal, pas de veto"
        ),
    )
    motif: str = Field("", description="Justification courte du veto (1-2 phrases)")
    condition_levee: str = Field(
        "",
        description="Ce qu'il faut produire / valider pour lever le veto",
    )


# ── loop_guard ───────────────────────────────────────────────────────

class LoopGuardVerdict(BaseModel):
    """Sortie du loop_guard (règle pure, sans LLM)."""
    should_continue: bool = Field(
        ..., description="False si la boucle d'enrichissement doit s'arrêter"
    )
    reason: str = Field(
        "",
        description="Motif (max_complements atteint, rien à enrichir, …)",
    )
    iteration: int = Field(
        0, description="Numéro d'itération courante (0 = première passe)"
    )


# ── Requêtes router (debug / preview) ───────────────────────────────

class VetoPreviewRequest(BaseModel):
    """Requête POST /guards/veto/preview."""
    agent: str = Field(..., min_length=2, max_length=64)
    agent_output: str = Field(..., min_length=3, max_length=8000)
    criticite: str = Field("C3", pattern=r"^C[1-5]$")


class ReversibilityPreviewRequest(BaseModel):
    """Requête POST /guards/reversibility/preview."""
    decision: str = Field(..., min_length=3, max_length=4000)
    criticite: str = Field("C3", pattern=r"^C[1-5]$")
    impact_cout: Optional[float] = None
    impact_delai: Optional[int] = None
