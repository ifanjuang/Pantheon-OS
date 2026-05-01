"""
MonitoringService — agrégation des KPIs ARCEUS.

Collecte des KPIs depuis 3 tables sources :
  - orchestra_runs   : durées, criticité, status, HITL, vetos, précheck
  - agent_runs       : durée moyenne, taux d'erreur, itérations
  - decision_scores  : verdicts, scores, axes

Les requêtes utilisent des window functions PostgreSQL pour les
percentiles et évitent les N+1 queries. Tous les agrégats sont filtrés
par la fenêtre temporelle (24h / 7d / 30d / 90d).
"""

from datetime import datetime, timezone
from typing import Literal

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from apps.monitoring.schemas import (
    AgentKPIs,
    GuardsKPIs,
    MonitoringSnapshot,
    OrchestraKPIs,
    ScoringKPIs,
)

log = get_logger("monitoring.service")


_WINDOW_SECONDS: dict[str, int] = {
    "24h": 86_400,
    "7d": 7 * 86_400,
    "30d": 30 * 86_400,
    "90d": 90 * 86_400,
}

Window = Literal["24h", "7d", "30d", "90d"]


class MonitoringService:
    @classmethod
    async def snapshot(
        cls,
        db: AsyncSession,
        *,
        window: Window = "7d",
    ) -> MonitoringSnapshot:
        """Calcule un snapshot complet des KPIs sur la fenêtre demandée."""
        if window not in _WINDOW_SECONDS:
            window = "7d"
        seconds = _WINDOW_SECONDS[window]

        orchestra, guards = await cls._orchestra_and_guards(db, seconds)
        agents = await cls._agent_kpis(db, seconds)
        scoring = await cls._scoring_kpis(db, seconds)

        return MonitoringSnapshot(
            window=window,
            window_seconds=seconds,
            computed_at=datetime.now(timezone.utc).isoformat(),
            orchestra=orchestra,
            agents=agents,
            scoring=scoring,
            guards=guards,
        )

    # ── orchestra + guards (même source table) ──────────────────────

    @classmethod
    async def _orchestra_and_guards(cls, db: AsyncSession, seconds: int) -> tuple[OrchestraKPIs, GuardsKPIs]:
        sql = """
            WITH win AS (
                SELECT *
                FROM orchestra_runs
                WHERE created_at > NOW() - (:secs || ' seconds')::interval
            )
            SELECT
                COUNT(*)                                                AS runs_total,
                COUNT(*) FILTER (WHERE status = 'completed')            AS runs_completed,
                COUNT(*) FILTER (WHERE status = 'failed')               AS runs_failed,
                COUNT(*) FILTER (WHERE status = 'awaiting_approval')    AS runs_awaiting,
                COALESCE(PERCENTILE_DISC(0.5)  WITHIN GROUP (ORDER BY duration_ms), 0) AS p50,
                COALESCE(PERCENTILE_DISC(0.95) WITHIN GROUP (ORDER BY duration_ms), 0) AS p95,
                COALESCE(AVG(duration_ms), 0)                           AS mean,
                COUNT(*) FILTER (WHERE criticite = 'C1')                AS c1,
                COUNT(*) FILTER (WHERE criticite = 'C2')                AS c2,
                COUNT(*) FILTER (WHERE criticite = 'C3')                AS c3,
                COUNT(*) FILTER (WHERE criticite = 'C4')                AS c4,
                COUNT(*) FILTER (WHERE criticite = 'C5')                AS c5,
                COUNT(*) FILTER (WHERE hitl_enabled = TRUE)             AS hitl_total,
                -- Guards
                COUNT(*) FILTER (WHERE veto_agent IS NOT NULL)          AS veto_total,
                COUNT(*) FILTER (WHERE veto_severity = 'bloquant')      AS veto_bloquant,
                COUNT(*) FILTER (WHERE veto_severity = 'reserve')       AS veto_reserve,
                COUNT(*) FILTER (WHERE precheck_verdict = 'approved')      AS pc_approved,
                COUNT(*) FILTER (WHERE precheck_verdict = 'trim')          AS pc_trim,
                COUNT(*) FILTER (WHERE precheck_verdict = 'upgrade')       AS pc_upgrade,
                COUNT(*) FILTER (WHERE precheck_verdict = 'clarification') AS pc_clari,
                COUNT(*) FILTER (WHERE precheck_verdict = 'blocked')       AS pc_blocked
            FROM win
        """
        row = (await db.execute(text(sql), {"secs": seconds})).first()

        total = int(row.runs_total or 0)
        hitl_total = int(row.hitl_total or 0)
        completed = int(row.runs_completed or 0)

        # Taux d'enrichissement : estimation via sous-tâches "needs_complement"
        # (approximation — pas persisté explicitement aujourd'hui)
        complement_sql = """
            SELECT COUNT(*) AS n
            FROM orchestra_runs
            WHERE created_at > NOW() - (:secs || ' seconds')::interval
              AND jsonb_array_length(agent_run_ids) > jsonb_array_length(assignments)
        """
        complement_row = (await db.execute(text(complement_sql), {"secs": seconds})).first()
        complement_n = int(complement_row.n or 0)

        orchestra = OrchestraKPIs(
            runs_total=total,
            runs_completed=completed,
            runs_failed=int(row.runs_failed or 0),
            runs_awaiting_approval=int(row.runs_awaiting or 0),
            duration_p50_ms=int(row.p50 or 0),
            duration_p95_ms=int(row.p95 or 0),
            duration_mean_ms=int(row.mean or 0),
            by_criticite={
                "C1": int(row.c1 or 0),
                "C2": int(row.c2 or 0),
                "C3": int(row.c3 or 0),
                "C4": int(row.c4 or 0),
                "C5": int(row.c5 or 0),
            },
            complement_rate=round(complement_n / total, 3) if total else 0.0,
            hitl_triggered=hitl_total,
            hitl_rate=round(hitl_total / total, 3) if total else 0.0,
        )

        pc_shortcircuit = int(row.pc_clari or 0) + int(row.pc_blocked or 0)
        guards = GuardsKPIs(
            veto_total=int(row.veto_total or 0),
            veto_bloquant=int(row.veto_bloquant or 0),
            veto_reserve=int(row.veto_reserve or 0),
            precheck_verdicts={
                "approved": int(row.pc_approved or 0),
                "trim": int(row.pc_trim or 0),
                "upgrade": int(row.pc_upgrade or 0),
                "clarification": int(row.pc_clari or 0),
                "blocked": int(row.pc_blocked or 0),
            },
            precheck_shortcircuit_rate=(round(pc_shortcircuit / total, 3) if total else 0.0),
        )
        return orchestra, guards

    # ── agent_runs ──────────────────────────────────────────────────

    @classmethod
    async def _agent_kpis(cls, db: AsyncSession, seconds: int) -> AgentKPIs:
        sql = """
            WITH win AS (
                SELECT *
                FROM agent_runs
                WHERE created_at > NOW() - (:secs || ' seconds')::interval
            )
            SELECT
                COUNT(*)                                                AS runs_total,
                COUNT(*) FILTER (WHERE status = 'completed')            AS runs_ok,
                COUNT(*) FILTER (WHERE status = 'failed' OR error_message IS NOT NULL) AS runs_err,
                COALESCE(AVG(iterations)::float, 0)                     AS iter_mean,
                COALESCE(AVG(duration_ms)::float, 0)                    AS dur_mean
            FROM win
        """
        row = (await db.execute(text(sql), {"secs": seconds})).first()
        total = int(row.runs_total or 0)
        err = int(row.runs_err or 0)

        top_sql = """
            SELECT
                agent_name,
                COUNT(*) AS runs,
                COUNT(*) FILTER (WHERE status = 'failed' OR error_message IS NOT NULL) AS errs
            FROM agent_runs
            WHERE created_at > NOW() - (:secs || ' seconds')::interval
              AND agent_name IS NOT NULL
            GROUP BY agent_name
            ORDER BY runs DESC
            LIMIT 10
        """
        top_rows = (await db.execute(text(top_sql), {"secs": seconds})).all()
        top_agents: list[dict] = []
        for r in top_rows:
            n = int(r.runs or 0)
            e = int(r.errs or 0)
            top_agents.append(
                {
                    "agent": r.agent_name,
                    "runs": n,
                    "error_rate": round(e / n, 3) if n else 0.0,
                }
            )

        return AgentKPIs(
            runs_total=total,
            runs_ok=int(row.runs_ok or 0),
            runs_error=err,
            error_rate=round(err / total, 3) if total else 0.0,
            iterations_mean=round(float(row.iter_mean or 0), 2),
            duration_mean_ms=int(row.dur_mean or 0),
            top_agents=top_agents,
        )

    # ── decision_scores ─────────────────────────────────────────────

    @classmethod
    async def _scoring_kpis(cls, db: AsyncSession, seconds: int) -> ScoringKPIs:
        sql = """
            WITH win AS (
                SELECT *
                FROM decision_scores
                WHERE computed_at > NOW() - (:secs || ' seconds')::interval
            )
            SELECT
                COUNT(*)                                                AS scored_total,
                COUNT(*) FILTER (WHERE verdict = 'robuste')             AS v_rob,
                COUNT(*) FILTER (WHERE verdict = 'acceptable')          AS v_acc,
                COUNT(*) FILTER (WHERE verdict = 'fragile')             AS v_fra,
                COUNT(*) FILTER (WHERE verdict = 'dangereux')           AS v_dan,
                COALESCE(AVG(total_final)::float, 0)                    AS score_mean,
                COALESCE(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY total_final), 0) AS score_p50
            FROM win
        """
        row = (await db.execute(text(sql), {"secs": seconds})).first()

        # Agrégat par axe (structure axes = {axe_name: {note, commentaire, ...}})
        axes_sql = """
            SELECT axes FROM decision_scores
            WHERE computed_at > NOW() - (:secs || ' seconds')::interval
              AND axes IS NOT NULL
              AND axes <> '{}'::jsonb
        """
        axes_rows = (await db.execute(text(axes_sql), {"secs": seconds})).all()
        axes_sum: dict[str, float] = {}
        axes_count: dict[str, int] = {}
        for r in axes_rows:
            axes_obj = r.axes or {}
            if not isinstance(axes_obj, dict):
                continue
            for axe, data in axes_obj.items():
                note = None
                if isinstance(data, dict):
                    note = data.get("note") or data.get("score")
                elif isinstance(data, (int, float)):
                    note = data
                if note is None:
                    continue
                try:
                    note_f = float(note)
                except (TypeError, ValueError):
                    continue
                axes_sum[axe] = axes_sum.get(axe, 0.0) + note_f
                axes_count[axe] = axes_count.get(axe, 0) + 1
        axes_mean = {axe: round(axes_sum[axe] / axes_count[axe], 2) for axe in axes_sum if axes_count[axe]}

        return ScoringKPIs(
            scored_total=int(row.scored_total or 0),
            verdicts={
                "robuste": int(row.v_rob or 0),
                "acceptable": int(row.v_acc or 0),
                "fragile": int(row.v_fra or 0),
                "dangereux": int(row.v_dan or 0),
            },
            score_mean=round(float(row.score_mean or 0), 2),
            score_p50=int(row.score_p50 or 0),
            axes_mean=axes_mean,
        )
