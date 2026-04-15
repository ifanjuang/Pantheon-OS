"""
Service evaluation — exécute un dataset OpenClaw contre le graphe Zeus
et produit un rapport agrégé (EvalReport).

Principes :
  - Pure I/O sur DB : les cas exécutent `run_orchestra()`, le scoring
    reste dans `scoring.py` (fonctions pures).
  - Chargement lazy des datasets YAML depuis `./datasets/*.yaml`.
  - `dry_run=True` n'exécute pas le graphe : rapport vide (useful pour
    vérifier qu'un dataset est bien parsé en CI).
  - Pas de side-effect mémoire (affaire_id par défaut = UUID zéro pour
    ne pas polluer Hestia/Mnémosyne avec des cas de test).
"""
from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from uuid import UUID

import structlog
import yaml
from sqlalchemy.ext.asyncio import AsyncSession

from modules.evaluation.schemas import (
    CaseResult,
    EvalCase,
    EvalDataset,
    EvalReport,
)
from modules.evaluation.scoring import score_case


log = structlog.get_logger(__name__)

# UUID sentinelle pour éviter de créer de faux rattachements affaire.
_EVAL_AFFAIRE_UUID = UUID("00000000-0000-0000-0000-000000000000")

# Répertoire des datasets YAML (colocalisé avec le code du module).
_DATASETS_DIR = Path(__file__).parent / "datasets"


# ── Chargement datasets ──────────────────────────────────────────────

def _datasets_dir() -> Path:
    return _DATASETS_DIR


def list_datasets() -> list[str]:
    """Retourne les id des datasets disponibles (noms de fichiers .yaml)."""
    if not _DATASETS_DIR.exists():
        return []
    return sorted(p.stem for p in _DATASETS_DIR.glob("*.yaml"))


def load_dataset(dataset_id: str) -> EvalDataset:
    """Charge un dataset YAML et le valide via Pydantic."""
    path = _DATASETS_DIR / f"{dataset_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Dataset introuvable : {dataset_id}")

    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    # id du fichier prime sur la valeur interne (garantit cohérence)
    raw["id"] = dataset_id
    return EvalDataset.model_validate(raw)


# ── Exécution d'un cas ───────────────────────────────────────────────

def _trace_from_run(run, preprocessed_input: dict) -> dict[str, Any]:
    """Construit la trace utilisée par scoring.score_case().
    On lit les champs pertinents depuis l'OrchestraRun final + le
    preprocessed_input (pour intent si le run a été trim/blocked avant).
    """
    called = list((run.agent_results or {}).keys())
    for a in run.assignments or []:
        if isinstance(a, dict) and a.get("agent") and a["agent"] not in called:
            called.append(a["agent"])

    return {
        "run_id": str(run.id),
        "agents_called": called,
        "assignments": run.assignments or [],
        "preprocessed_input": preprocessed_input or run.preprocessed_input or {},
        "criticite": run.criticite,
        "veto_agent": run.veto_agent,
        "veto_severity": run.veto_severity,
        "veto_motif": run.veto_motif,
        "final_answer": run.final_answer or "",
        "precheck_verdict": run.precheck_verdict,
        "duration_ms": run.duration_ms or 0,
        "error": run.error_message,
    }


async def _run_case(
    db: AsyncSession,
    case: EvalCase,
    affaire_id: UUID,
    user_id: Optional[UUID],
) -> CaseResult:
    """Exécute un cas via run_orchestra puis score le résultat."""
    # Import local pour éviter cycle (orchestra importe aussi des schémas eval
    # éventuellement à l'avenir).
    from modules.orchestra.service import run_orchestra

    t_start = time.monotonic()
    try:
        run = await run_orchestra(
            db=db,
            instruction=case.instruction,
            affaire_id=affaire_id,
            user_id=user_id,
            agents=None,
            criticite=case.criticite,
        )
    except Exception as exc:
        # Exécution impossible : score 0 sur tous les axes mais trace conservée.
        log.error("evaluation.case_failed", case_id=case.id, error=str(exc))
        return CaseResult(
            case_id=case.id,
            passed=False,
            relevance=0.0,
            security=0.0,
            completeness=0.0,
            score=0.0,
            duration_ms=int((time.monotonic() - t_start) * 1000),
            checks=[],
            run_id=None,
            final_answer_excerpt="",
            error=str(exc),
        )

    trace = _trace_from_run(run, run.preprocessed_input or {})
    return score_case(case, trace)


# ── API publique ─────────────────────────────────────────────────────

async def run_eval(
    db: AsyncSession,
    dataset_id: str,
    affaire_id: Optional[UUID] = None,
    user_id: Optional[UUID] = None,
    max_cases: Optional[int] = None,
    dry_run: bool = False,
) -> EvalReport:
    """Exécute un dataset complet et retourne l'EvalReport agrégé."""
    started_at = datetime.now(timezone.utc).isoformat()
    t_start = time.monotonic()

    dataset = load_dataset(dataset_id)
    cases = dataset.cases[:max_cases] if max_cases else dataset.cases
    effective_affaire = affaire_id or _EVAL_AFFAIRE_UUID

    log.info(
        "evaluation.start",
        dataset_id=dataset_id,
        total=len(cases),
        dry_run=dry_run,
    )

    results: list[CaseResult] = []

    if dry_run:
        # Mode CI-friendly : on valide juste que chaque case est bien parsable.
        results = [
            CaseResult(
                case_id=c.id,
                passed=True,
                relevance=0.0,
                security=0.0,
                completeness=0.0,
                score=0.0,
                duration_ms=0,
                final_answer_excerpt="[dry_run]",
            )
            for c in cases
        ]
    else:
        for case in cases:
            result = await _run_case(db, case, effective_affaire, user_id)
            results.append(result)
            log.info(
                "evaluation.case_done",
                case_id=case.id,
                passed=result.passed,
                score=result.score,
                duration_ms=result.duration_ms,
            )

    # Agrégation
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    mean_score = round(sum(r.score for r in results) / total, 3) if total else 0.0
    mean_duration = int(sum(r.duration_ms for r in results) / total) if total else 0

    summary = {
        "relevance": round(sum(r.relevance for r in results) / total, 3) if total else 0.0,
        "security": round(sum(r.security for r in results) / total, 3) if total else 0.0,
        "completeness": round(sum(r.completeness for r in results) / total, 3) if total else 0.0,
    }

    finished_at = datetime.now(timezone.utc).isoformat()

    report = EvalReport(
        dataset_id=dataset_id,
        started_at=started_at,
        finished_at=finished_at,
        total=total,
        passed=passed,
        failed=failed,
        pass_rate=round(passed / total, 3) if total else 0.0,
        mean_score=mean_score,
        mean_duration_ms=mean_duration,
        cases=results,
        summary=summary,
    )

    log.info(
        "evaluation.done",
        dataset_id=dataset_id,
        pass_rate=report.pass_rate,
        mean_score=mean_score,
        elapsed_ms=int((time.monotonic() - t_start) * 1000),
    )
    return report
