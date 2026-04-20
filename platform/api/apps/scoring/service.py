"""
ScoringService — calcul de score décisionnel sur 100 points.

Deux modes :
  score_manual()  : l'utilisateur fournit les sous-scores (AxesDetail)
  score_auto()    : LLM via Instructor remplit un AxesDetail à partir du contexte

Pipeline commun :
  1. Calcul total_raw = somme des 5 totaux d'axes (max 100)
  2. Application des bonus/malus (précédents wiki, dette, certitude)
  3. total_final = clamp(total_raw + sum(deltas), 0, 100)
  4. Verdict déduit :
       ≥ 80 : robuste
       ≥ 60 : acceptable
       ≥ 40 : fragile
       <  40 : dangereux

Bonus/malus :
  +5  code="precedent_valide"   si WikiService.check_precedents ok
  -10 code="dette_critique"     si dette == D3
  -5  code="certitude_faible"   si certitude < 0.5
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import get_logger
from core.services.llm_service import LlmService
from apps.scoring.models import DecisionScore
from apps.scoring.schemas import AxesDetail, BonusMalus
from apps.wiki.service import WikiService

log = get_logger("scoring.service")

# Seuils de verdict
VERDICT_THRESHOLDS = [
    (80, "robuste"),
    (60, "acceptable"),
    (40, "fragile"),
    (0, "dangereux"),
]

# Montants bonus/malus (alignés sur l'architecture utilisateur)
BONUS_PRECEDENT = 5
MALUS_DETTE_D3 = -10
MALUS_CERTITUDE = -5
CERTITUDE_SEUIL = 0.5


_AUTO_SCORING_PROMPT = """\
Tu es un scoring engine ARCEUS qui évalue la robustesse d'une décision projet
de maîtrise d'œuvre sur 100 points répartis en 5 axes.

## Sujet
{sujet}

## Contexte
{contexte}

## Barème
1. Technique (/25) — vue Héphaïstos
   - faisabilite (0-10) : est-ce réalisable techniquement ?
   - complexite (0-5)   : 0 = très complexe, 5 = simple
   - risque (0-10)      : 0 = risque défaut élevé, 10 = fiable

2. Contractuel (/25) — vue Thémis
   - conformite (0-10)     : respect des normes / DTU / code de l'urbanisme
   - responsabilite (0-10) : répartition claire des responsabilités MOE/entreprise
   - tracabilite (0-5)     : dossier traçable (pièces, échanges, décisions)

3. Planning (/20) — vue Chronos
   - impact_delai (0-10) : impact sur le planning général (0 = gros retard)
   - dependances (0-5)   : nombre et criticité des dépendances amont
   - urgence (0-5)       : 5 = non urgent, 0 = à faire immédiatement

4. Cohérence (/15) — vue Apollon
   - alignement (0-10) : cohérence avec les décisions du projet et le programme
   - lisibilite (0-5)  : clarté du raisonnement

5. Robustesse logique (/15) — vue Prométhée
   - hypotheses (0-10)  : hypothèses documentées et validées
   - incertitude (0-5)  : 5 = peu d'incertitudes résiduelles, 0 = beaucoup

Pour chaque axe, fournis un commentaire d'une phrase justifiant la note.
Sois conservateur : en cas de doute, note plus bas.
"""


class ScoringService:
    # ── Pipeline interne ────────────────────────────────────────────

    @staticmethod
    def _verdict(total: int) -> str:
        for threshold, label in VERDICT_THRESHOLDS:
            if total >= threshold:
                return label
        return "dangereux"

    @staticmethod
    def _clamp(value: int, lo: int = 0, hi: int = 100) -> int:
        return max(lo, min(hi, value))

    @classmethod
    async def _build_bonus_malus(
        cls,
        db: AsyncSession,
        *,
        sujet: str,
        affaire_id: Optional[UUID],
        dette: Optional[str],
        certitude: float,
    ) -> list[BonusMalus]:
        adjustments: list[BonusMalus] = []

        # Précédents wiki → +5
        try:
            precedent = await WikiService.check_precedents(
                db,
                sujet=sujet,
                affaire_id=affaire_id,
                top_k=3,
                increment_reuse=True,
            )
            if precedent["bonus_applicable"]:
                first = precedent["precedents"][0] if precedent["precedents"] else {}
                slug = first.get("slug", "inconnu")
                adjustments.append(
                    BonusMalus(
                        code="precedent_valide",
                        label="Déjà validé dans projets passés",
                        delta=BONUS_PRECEDENT,
                        reason=f"Précédent agence : {slug}",
                    )
                )
        except Exception as exc:
            log.warning("scoring.precedents_failed", error=str(exc))

        # Dette D3 → -10
        if dette == "D3":
            adjustments.append(
                BonusMalus(
                    code="dette_critique",
                    label="Dette D3 (critique en retard)",
                    delta=MALUS_DETTE_D3,
                    reason="La décision porte une dette critique",
                )
            )

        # Certitude faible → -5
        if certitude < CERTITUDE_SEUIL:
            adjustments.append(
                BonusMalus(
                    code="certitude_faible",
                    label="Faible certitude",
                    delta=MALUS_CERTITUDE,
                    reason=f"Certitude auto-déclarée : {certitude:.2f}",
                )
            )

        return adjustments

    @classmethod
    async def _read_decision_dette(cls, db: AsyncSession, decision_id: UUID) -> Optional[str]:
        """Lit la dette courante d'une project_decision (raw SQL)."""
        row = (
            await db.execute(
                text("SELECT dette FROM project_decisions WHERE id = :id"),
                {"id": str(decision_id)},
            )
        ).first()
        return row[0] if row else None

    @classmethod
    async def _persist(
        cls,
        db: AsyncSession,
        *,
        sujet: str,
        axes: AxesDetail,
        adjustments: list[BonusMalus],
        certitude: float,
        dette: Optional[str],
        mode: str,
        affaire_id: Optional[UUID],
        decision_id: Optional[UUID],
        computed_by: Optional[UUID],
    ) -> DecisionScore:
        total_raw = cls._clamp(axes.total)
        total_final = cls._clamp(total_raw + sum(a.delta for a in adjustments))
        verdict = cls._verdict(total_final)

        score = DecisionScore(
            decision_id=decision_id,
            affaire_id=affaire_id,
            sujet=sujet[:512],
            axes=axes.model_dump(),
            total_raw=total_raw,
            bonus_malus=[a.model_dump() for a in adjustments],
            total_final=total_final,
            verdict=verdict,
            certitude=certitude,
            dette_snapshot=dette,
            mode=mode,
            computed_by=computed_by,
        )
        db.add(score)
        await db.commit()
        await db.refresh(score)

        log.info(
            "scoring.persisted",
            score_id=str(score.id),
            total_raw=total_raw,
            total_final=total_final,
            verdict=verdict,
            adjustments=len(adjustments),
            mode=mode,
        )
        return score

    # ── API publique ────────────────────────────────────────────────

    @classmethod
    async def score_manual(
        cls,
        db: AsyncSession,
        *,
        sujet: str,
        axes: AxesDetail,
        affaire_id: Optional[UUID] = None,
        decision_id: Optional[UUID] = None,
        certitude: float = 1.0,
        dette: Optional[str] = None,
        computed_by: Optional[UUID] = None,
    ) -> DecisionScore:
        """Scoring manuel — l'utilisateur fournit les sous-scores."""
        if dette is None and decision_id is not None:
            dette = await cls._read_decision_dette(db, decision_id)

        adjustments = await cls._build_bonus_malus(
            db,
            sujet=sujet,
            affaire_id=affaire_id,
            dette=dette,
            certitude=certitude,
        )
        return await cls._persist(
            db,
            sujet=sujet,
            axes=axes,
            adjustments=adjustments,
            certitude=certitude,
            dette=dette,
            mode="manuel",
            affaire_id=affaire_id,
            decision_id=decision_id,
            computed_by=computed_by,
        )

    @classmethod
    async def score_auto(
        cls,
        db: AsyncSession,
        *,
        sujet: str,
        contexte: str,
        affaire_id: Optional[UUID] = None,
        decision_id: Optional[UUID] = None,
        certitude: float = 0.7,
        dette: Optional[str] = None,
        computed_by: Optional[UUID] = None,
    ) -> DecisionScore:
        """
        Scoring automatique — le LLM remplit un AxesDetail via Instructor.
        Temperature basse pour stabilité.
        """
        if dette is None and decision_id is not None:
            dette = await cls._read_decision_dette(db, decision_id)

        prompt = _AUTO_SCORING_PROMPT.format(sujet=sujet, contexte=contexte[:4000])
        axes = await LlmService.extract(
            messages=[{"role": "user", "content": prompt}],
            response_model=AxesDetail,
            temperature=0.1,
            max_retries=3,
        )

        adjustments = await cls._build_bonus_malus(
            db,
            sujet=sujet,
            affaire_id=affaire_id,
            dette=dette,
            certitude=certitude,
        )
        return await cls._persist(
            db,
            sujet=sujet,
            axes=axes,
            adjustments=adjustments,
            certitude=certitude,
            dette=dette,
            mode="auto_llm",
            affaire_id=affaire_id,
            decision_id=decision_id,
            computed_by=computed_by,
        )

    # ── Stats dashboard ─────────────────────────────────────────────

    @classmethod
    async def stats_for_affaire(cls, db: AsyncSession, affaire_id: Optional[UUID] = None) -> dict:
        """
        KPIs agrégés : moyenne, distribution des verdicts, dettes D3.
        Si affaire_id=None → stats globales agence.
        """
        where = ""
        params: dict = {}
        if affaire_id:
            where = "WHERE affaire_id = :affaire_id"
            params["affaire_id"] = str(affaire_id)

        # Une ligne par decision_id (garder le score le plus récent)
        # Si pas de decision_id, on prend directement le score (sujet libre).
        sql = f"""
            WITH latest AS (
                SELECT DISTINCT ON (COALESCE(decision_id::text, id::text))
                    id, decision_id, affaire_id, total_final, verdict,
                    dette_snapshot, computed_at
                FROM decision_scores
                {where}
                ORDER BY COALESCE(decision_id::text, id::text), computed_at DESC
            )
            SELECT
                COUNT(*) AS total,
                COALESCE(AVG(total_final), 0) AS moyenne,
                COUNT(*) FILTER (WHERE verdict = 'robuste')    AS robuste,
                COUNT(*) FILTER (WHERE verdict = 'acceptable') AS acceptable,
                COUNT(*) FILTER (WHERE verdict = 'fragile')    AS fragile,
                COUNT(*) FILTER (WHERE verdict = 'dangereux')  AS dangereux,
                COUNT(*) FILTER (WHERE dette_snapshot = 'D3')  AS dettes_d3
            FROM latest
        """
        row = (await db.execute(text(sql), params)).first()
        total = int(row.total or 0)
        robuste = int(row.robuste or 0)
        return {
            "total_scores": total,
            "moyenne": round(float(row.moyenne or 0), 2),
            "distribution": {
                "robuste": robuste,
                "acceptable": int(row.acceptable or 0),
                "fragile": int(row.fragile or 0),
                "dangereux": int(row.dangereux or 0),
            },
            "dettes_d3": int(row.dettes_d3 or 0),
            "taux_robuste": round(robuste / total, 2) if total else 0.0,
        }
