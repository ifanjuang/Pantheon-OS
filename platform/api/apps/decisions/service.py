"""
DecisionsService — vues dashboard + KPIs.

Les CRUD simples sont gérés directement dans le router. Ce service porte
la logique agrégée :

  - view_critiques()    : filtre C4/C5
  - view_dettes()       : D2/D3 ouvertes
  - view_non_validees() : C4/C5 sans validation
  - view_par_lot()      : regroupement métier
  - view_timeline()     : vision par phase

  - kpis()      : nombre critiques, dette moyenne, délai résolution, % revues
  - enrich_with_scores() : join dynamique avec decision_scores pour obtenir
                           le dernier score de chaque décision
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger

log = get_logger("decisions.service")

DETTE_NUMERIQUE = {"D0": 0, "D1": 1, "D2": 2, "D3": 3}


class DecisionsService:
    # ── Helpers filtre affaire ──────────────────────────────────────

    @staticmethod
    def _affaire_clause(affaire_id: Optional[UUID]) -> tuple[str, dict]:
        if affaire_id is None:
            return ("1 = 1", {})
        return ("affaire_id = :affaire_id", {"affaire_id": str(affaire_id)})

    # ── Vues dashboard ──────────────────────────────────────────────

    @classmethod
    async def view_critiques(cls, db: AsyncSession, affaire_id: Optional[UUID] = None) -> list[dict]:
        """VUE 1 — Décisions critiques (C4/C5)."""
        clause, params = cls._affaire_clause(affaire_id)
        rows = (
            (
                await db.execute(
                    text(
                        f"""
                    SELECT d.*,
                           (
                               SELECT total_final
                               FROM decision_scores s
                               WHERE s.decision_id = d.id
                               ORDER BY s.computed_at DESC
                               LIMIT 1
                           ) AS score
                    FROM project_decisions d
                    WHERE {clause}
                      AND criticite IN ('C4', 'C5')
                    ORDER BY
                        CASE criticite WHEN 'C5' THEN 0 ELSE 1 END,
                        date_decision DESC NULLS LAST,
                        created_at DESC
                    """
                    ),
                    params,
                )
            )
            .mappings()
            .all()
        )
        return [dict(r) for r in rows]

    @classmethod
    async def view_dettes(cls, db: AsyncSession, affaire_id: Optional[UUID] = None) -> list[dict]:
        """VUE 2 — Dettes ouvertes (D2/D3)."""
        clause, params = cls._affaire_clause(affaire_id)
        rows = (
            (
                await db.execute(
                    text(
                        f"""
                    SELECT d.*,
                           (
                               SELECT total_final
                               FROM decision_scores s
                               WHERE s.decision_id = d.id
                               ORDER BY s.computed_at DESC
                               LIMIT 1
                           ) AS score
                    FROM project_decisions d
                    WHERE {clause}
                      AND dette IN ('D2', 'D3')
                      AND statut != 'caduc'
                    ORDER BY
                        CASE dette WHEN 'D3' THEN 0 ELSE 1 END,
                        created_at DESC
                    """
                    ),
                    params,
                )
            )
            .mappings()
            .all()
        )
        return [dict(r) for r in rows]

    @classmethod
    async def view_non_validees(cls, db: AsyncSession, affaire_id: Optional[UUID] = None) -> list[dict]:
        """VUE 3 — Décisions critiques C4/C5 sans validation."""
        clause, params = cls._affaire_clause(affaire_id)
        rows = (
            (
                await db.execute(
                    text(
                        f"""
                    SELECT d.*,
                           (
                               SELECT total_final
                               FROM decision_scores s
                               WHERE s.decision_id = d.id
                               ORDER BY s.computed_at DESC
                               LIMIT 1
                           ) AS score
                    FROM project_decisions d
                    WHERE {clause}
                      AND criticite IN ('C4', 'C5')
                      AND statut NOT IN ('validé', 'caduc')
                    ORDER BY created_at DESC
                    """
                    ),
                    params,
                )
            )
            .mappings()
            .all()
        )
        return [dict(r) for r in rows]

    @classmethod
    async def view_par_lot(cls, db: AsyncSession, affaire_id: Optional[UUID] = None) -> list[dict]:
        """VUE 4 — Regroupement par lot métier avec score moyen."""
        clause, params = cls._affaire_clause(affaire_id)
        rows = (
            (
                await db.execute(
                    text(
                        f"""
                    SELECT
                        COALESCE(d.lot, 'non_affecte') AS lot,
                        COUNT(*) AS total,
                        COUNT(*) FILTER (WHERE d.criticite IN ('C4', 'C5')) AS critiques,
                        AVG(latest.total_final) AS score_moyen
                    FROM project_decisions d
                    LEFT JOIN LATERAL (
                        SELECT total_final
                        FROM decision_scores s
                        WHERE s.decision_id = d.id
                        ORDER BY s.computed_at DESC
                        LIMIT 1
                    ) latest ON TRUE
                    WHERE {clause}
                    GROUP BY COALESCE(d.lot, 'non_affecte')
                    ORDER BY critiques DESC, total DESC
                    """
                    ),
                    params,
                )
            )
            .mappings()
            .all()
        )
        return [
            {
                "lot": r["lot"],
                "total": int(r["total"]),
                "critiques": int(r["critiques"] or 0),
                "score_moyen": float(r["score_moyen"]) if r["score_moyen"] is not None else None,
            }
            for r in rows
        ]

    @classmethod
    async def view_timeline(cls, db: AsyncSession, affaire_id: Optional[UUID] = None) -> list[dict]:
        """VUE 5 — Timeline par phase."""
        clause, params = cls._affaire_clause(affaire_id)
        rows = (
            (
                await db.execute(
                    text(
                        f"""
                    SELECT
                        COALESCE(phase, 'non_affectee') AS phase,
                        COUNT(*) AS total,
                        COUNT(*) FILTER (WHERE criticite IN ('C4', 'C5')) AS critiques,
                        COUNT(*) FILTER (WHERE dette IN ('D2', 'D3')) AS dettes_d2_d3
                    FROM project_decisions
                    WHERE {clause}
                    GROUP BY COALESCE(phase, 'non_affectee')
                    ORDER BY
                        CASE COALESCE(phase, 'zzz')
                            WHEN 'APS' THEN 1
                            WHEN 'APD' THEN 2
                            WHEN 'PRO' THEN 3
                            WHEN 'DCE' THEN 4
                            WHEN 'ACT' THEN 5
                            WHEN 'EXE' THEN 6
                            WHEN 'DOE' THEN 7
                            ELSE 9
                        END
                    """
                    ),
                    params,
                )
            )
            .mappings()
            .all()
        )
        return [
            {
                "phase": r["phase"],
                "total": int(r["total"]),
                "critiques": int(r["critiques"] or 0),
                "dettes_d2_d3": int(r["dettes_d2_d3"] or 0),
            }
            for r in rows
        ]

    # ── KPIs ────────────────────────────────────────────────────────

    @classmethod
    async def kpis(cls, db: AsyncSession, affaire_id: Optional[UUID] = None) -> dict:
        """
        KPIs principaux du dashboard :
          - nombre de décisions critiques (C4/C5)
          - dette moyenne (0-3)
          - délai de résolution moyen : EXTRACT(days) FROM (updated_at - created_at)
            pour les décisions passées à 'validé' ou 'caduc'
          - taux de décisions revues (phase_revision non nulle ou statut 'a_revoir')
          - totaux tâches ouvertes et observations à traiter
        """
        clause, params = cls._affaire_clause(affaire_id)

        sql = f"""
            WITH d AS (
                SELECT * FROM project_decisions WHERE {clause}
            )
            SELECT
                COUNT(*) FILTER (WHERE criticite IN ('C4', 'C5')) AS critiques,
                COUNT(*) AS total,
                AVG(CASE dette
                        WHEN 'D0' THEN 0
                        WHEN 'D1' THEN 1
                        WHEN 'D2' THEN 2
                        WHEN 'D3' THEN 3
                        ELSE 0
                    END) AS dette_moyenne,
                AVG(
                    CASE
                        WHEN statut IN ('validé', 'caduc') AND updated_at IS NOT NULL
                        THEN EXTRACT(EPOCH FROM (updated_at - created_at)) / 86400.0
                    END
                ) AS delai_resolution,
                COUNT(*) FILTER (
                    WHERE phase_revision IS NOT NULL OR statut = 'a_revoir'
                ) AS revues
            FROM d
        """
        row = (await db.execute(text(sql), params)).first()

        total = int(row.total or 0)
        revues = int(row.revues or 0)

        # Sous-totaux tâches et observations (mêmes filtres)
        tasks_clause, tasks_params = cls._affaire_clause(affaire_id)
        tasks_row = (
            await db.execute(
                text(
                    f"""
                    SELECT COUNT(*) AS n
                    FROM project_tasks
                    WHERE {tasks_clause} AND statut IN ('ouvert', 'en_cours', 'bloque')
                    """
                ),
                tasks_params,
            )
        ).first()

        obs_row = (
            await db.execute(
                text(
                    f"""
                    SELECT COUNT(*) AS n
                    FROM project_observations
                    WHERE {tasks_clause} AND traitement IN ('a_traiter', 'en_cours')
                    """
                ),
                tasks_params,
            )
        ).first()

        return {
            "decisions_critiques": int(row.critiques or 0),
            "dette_moyenne": round(float(row.dette_moyenne or 0), 2),
            "delai_resolution_moyen": round(float(row.delai_resolution or 0), 1),
            "taux_revues": round(revues / total, 2) if total else 0.0,
            "total_decisions": total,
            "total_taches_ouvertes": int(tasks_row.n or 0),
            "total_observations_a_traiter": int(obs_row.n or 0),
        }
