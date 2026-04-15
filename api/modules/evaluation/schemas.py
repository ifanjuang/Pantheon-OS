"""
Schémas evaluation — OpenClaw harness.

Datasets YAML :
  chaque fichier .yaml dans `datasets/` décrit un jeu de cas de test.
  Un cas contient une instruction + critères de validation :
    - expected_criticite       : C1-C5 attendue (si connue)
    - expected_intent          : intent Hermès attendu (information, question, ...)
    - expected_precheck        : verdict du gate attendu (approved, trim, …)
    - expected_agents          : agents minimums attendus dans l'assignment
    - forbidden_agents         : agents qui ne doivent PAS être appelés
    - expected_veto            : True si le cas doit déclencher un veto
    - must_contain             : tokens obligatoires dans final_answer
    - must_not_contain         : tokens interdits dans final_answer
    - max_duration_ms          : budget temps (soft limit pour le rapport)

Score d'éval (distinct du scoring décisionnel !) :
  - relevance    : final_answer répond effectivement à la question
  - security     : pas de recommandation dangereuse ou hallucination
  - completeness : tous les attendus sont satisfaits
"""
from typing import Literal, Optional

from pydantic import BaseModel, Field


# ── Définition d'un cas ──────────────────────────────────────────────

class EvalCase(BaseModel):
    """Cas d'éval individuel au sein d'un dataset."""
    id: str = Field(..., min_length=1, max_length=64)
    instruction: str = Field(..., min_length=3, max_length=4000)
    criticite: str = Field("C2", pattern=r"^C[1-5]$")
    tags: list[str] = Field(default_factory=list)
    description: str = ""

    # Attendus qualitatifs
    expected_criticite: Optional[str] = Field(None, pattern=r"^C[1-5]$")
    expected_intent: Optional[str] = None
    expected_precheck: Optional[
        Literal["approved", "trim", "upgrade", "clarification", "blocked"]
    ] = None
    expected_agents: list[str] = Field(default_factory=list)
    forbidden_agents: list[str] = Field(default_factory=list)
    expected_veto: bool = False
    must_contain: list[str] = Field(default_factory=list)
    must_not_contain: list[str] = Field(default_factory=list)
    max_duration_ms: Optional[int] = None


class EvalDataset(BaseModel):
    """Un dataset = ensemble de cas (fichier YAML)."""
    id: str = Field(..., min_length=1, max_length=64)
    title: str = ""
    description: str = ""
    cases: list[EvalCase] = Field(default_factory=list)


# ── Résultat d'un run d'éval ─────────────────────────────────────────

class CaseCheck(BaseModel):
    """Résultat par cas (checks individuels)."""
    name: str
    passed: bool
    detail: str = ""


class CaseResult(BaseModel):
    case_id: str
    passed: bool
    relevance: float = Field(0.0, ge=0.0, le=1.0)
    security: float = Field(0.0, ge=0.0, le=1.0)
    completeness: float = Field(0.0, ge=0.0, le=1.0)
    score: float = Field(0.0, ge=0.0, le=1.0)
    duration_ms: int = 0

    checks: list[CaseCheck] = Field(default_factory=list)

    # Trace utile (tronquée)
    run_id: Optional[str] = None
    final_answer_excerpt: str = ""
    error: Optional[str] = None


class EvalReport(BaseModel):
    """Rapport agrégé pour un dataset."""
    dataset_id: str
    started_at: str  # ISO 8601
    finished_at: str
    total: int = 0
    passed: int = 0
    failed: int = 0
    pass_rate: float = 0.0
    mean_score: float = 0.0
    mean_duration_ms: int = 0
    cases: list[CaseResult] = Field(default_factory=list)
    summary: dict[str, float] = Field(
        default_factory=dict,
        description="{relevance, security, completeness} moyens",
    )


# ── Requêtes API ─────────────────────────────────────────────────────

class RunEvalRequest(BaseModel):
    dataset_id: str = Field(..., min_length=1, max_length=64)
    affaire_id: Optional[str] = Field(
        None, description="UUID d'affaire pour contextualiser (sinon : sans contexte)"
    )
    max_cases: Optional[int] = Field(
        None, ge=1, le=100, description="Limite le nombre de cas (debug)"
    )
    dry_run: bool = Field(
        False,
        description="Si True, valide les attendus sans exécuter le graphe (stub)",
    )
