"""
Schémas monitoring — KPIs ARCEUS.

Regroupe 4 familles de KPIs :

  OrchestraKPIs    : runs orchestra (durée, coût, enrichissement, HITL, veto)
  AgentKPIs        : runs agent (durée, erreurs, itérations, sources)
  ScoringKPIs      : distribution des verdicts (robuste/acceptable/fragile/dangereux)
  GuardsKPIs       : taux veto / HITL / enrichissement / précheck verdicts

MonitoringSnapshot agrège les 4 sur une fenêtre temporelle donnée
(7 jours par défaut).
"""

from typing import Literal

from pydantic import BaseModel, Field


# ── Paramètres de fenêtre ────────────────────────────────────────────

Window = Literal["24h", "7d", "30d", "90d"]


# ── KPIs orchestra ───────────────────────────────────────────────────


class OrchestraKPIs(BaseModel):
    runs_total: int = 0
    runs_completed: int = 0
    runs_failed: int = 0
    runs_awaiting_approval: int = 0

    # Durées (ms)
    duration_p50_ms: int = 0
    duration_p95_ms: int = 0
    duration_mean_ms: int = 0

    # Distribution criticité
    by_criticite: dict[str, int] = Field(default_factory=dict)

    # Taux d'enrichissement (complément zeus_judge)
    complement_rate: float = 0.0

    # HITL
    hitl_triggered: int = 0
    hitl_rate: float = 0.0


# ── KPIs agent ───────────────────────────────────────────────────────


class AgentKPIs(BaseModel):
    runs_total: int = 0
    runs_ok: int = 0
    runs_error: int = 0
    error_rate: float = 0.0
    iterations_mean: float = 0.0
    duration_mean_ms: int = 0
    top_agents: list[dict] = Field(
        default_factory=list,
        description="Liste [{agent, runs, error_rate}] — 10 plus sollicités",
    )


# ── KPIs scoring ─────────────────────────────────────────────────────


class ScoringKPIs(BaseModel):
    scored_total: int = 0
    verdicts: dict[str, int] = Field(
        default_factory=dict,
        description="{robuste, acceptable, fragile, dangereux}",
    )
    score_mean: float = 0.0
    score_p50: int = 0
    # Distribution par axe (si disponible)
    axes_mean: dict[str, float] = Field(default_factory=dict)


# ── KPIs guards (M2) ─────────────────────────────────────────────────


class GuardsKPIs(BaseModel):
    veto_total: int = 0
    veto_bloquant: int = 0
    veto_reserve: int = 0
    precheck_verdicts: dict[str, int] = Field(
        default_factory=dict,
        description="{approved, trim, upgrade, clarification, blocked}",
    )
    precheck_shortcircuit_rate: float = 0.0
    # % de runs où le précheck a coupé avant dispatch_subtasks


# ── Snapshot agrégé ──────────────────────────────────────────────────


class MonitoringSnapshot(BaseModel):
    window: Window = "7d"
    window_seconds: int = 0
    computed_at: str = ""  # ISO 8601

    orchestra: OrchestraKPIs = Field(default_factory=OrchestraKPIs)
    agents: AgentKPIs = Field(default_factory=AgentKPIs)
    scoring: ScoringKPIs = Field(default_factory=ScoringKPIs)
    guards: GuardsKPIs = Field(default_factory=GuardsKPIs)
