"""
ClawMark Runner — adaptateur ARCEUS pour le benchmark ClawMark.

ClawMark est un benchmark pour agents « coworker » multimodaux.
Ce runner adapte les tâches ClawMark aux agents ARCEUS et produit un rapport de scoring.

Usage :
    cd api && python -m benchmarks.clawmark_runner run --dataset ../benchmarks/datasets/clawmark/sample.json
    cd api && python -m benchmarks.clawmark_runner run --task cm-001
    cd api && python -m benchmarks.clawmark_runner list
    cd api && python -m benchmarks.clawmark_runner run --dataset ... --json > report.json

Format de tâche ClawMark :
    {
        "task_id": "cm-001",
        "title": "...",
        "type": "search" | "document_analysis" | "planning" | "multi_step" | "compliance",
        "agent": "apollon" | "athena" | "hephaistos" | "themis" | "chronos",
        "instruction": "...",
        "affaire_code": "TEST-001",   // optionnel — affaire à utiliser
        "expected": {
            "contains": ["mot_clé"],        // doit contenir ces mots
            "not_contains": ["erreur"],     // ne doit PAS contenir ces mots
            "min_length": 100,             // longueur minimale réponse
            "judge_prompt": "..."          // prompt LLM pour juger la qualité
        },
        "timeout_s": 60
    }
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

DATASETS_DIR = Path(__file__).parent / "datasets" / "clawmark"

# ── Schémas ──────────────────────────────────────────────────────────────────

@dataclass
class ClawMarkTask:
    task_id: str
    title: str
    type: str
    agent: str
    instruction: str
    affaire_code: str = ""
    expected: dict = field(default_factory=dict)
    timeout_s: int = 60


@dataclass
class TaskResult:
    task_id: str
    agent: str
    passed: bool
    score: float          # 0.0 – 1.0
    result_excerpt: str
    error: str
    duration_ms: int
    checks: dict = field(default_factory=dict)


@dataclass
class ClawMarkReport:
    dataset: str
    started_at: str
    finished_at: str
    total: int
    passed: int
    failed: int
    pass_rate: float
    mean_score: float
    mean_duration_ms: int
    results: list[TaskResult]


# ── Loader ───────────────────────────────────────────────────────────────────

def load_dataset(path: Path) -> list[ClawMarkTask]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    tasks = raw if isinstance(raw, list) else raw.get("tasks", [raw])
    return [
        ClawMarkTask(
            task_id=t["task_id"],
            title=t.get("title", t["task_id"]),
            type=t.get("type", "generic"),
            agent=t.get("agent", "athena"),
            instruction=t["instruction"],
            affaire_code=t.get("affaire_code", ""),
            expected=t.get("expected", {}),
            timeout_s=t.get("timeout_s", 60),
        )
        for t in tasks
    ]


def list_datasets() -> list[str]:
    if not DATASETS_DIR.exists():
        return []
    return [p.stem for p in sorted(DATASETS_DIR.glob("*.json"))]


# ── Scorer ───────────────────────────────────────────────────────────────────

def _score_task(result_text: str, expected: dict) -> tuple[float, dict, bool]:
    """
    Score un résultat contre les critères expected.
    Retourne (score_0_to_1, checks_dict, passed).
    """
    checks: dict[str, bool] = {}
    points = 0
    total = 0

    text_lower = result_text.lower()

    # Vérification contains
    for kw in expected.get("contains", []):
        key = f"contains:{kw}"
        ok = kw.lower() in text_lower
        checks[key] = ok
        points += 1 if ok else 0
        total += 1

    # Vérification not_contains
    for kw in expected.get("not_contains", []):
        key = f"not_contains:{kw}"
        ok = kw.lower() not in text_lower
        checks[key] = ok
        points += 1 if ok else 0
        total += 1

    # Longueur minimale
    min_len = expected.get("min_length", 0)
    if min_len:
        ok = len(result_text.strip()) >= min_len
        checks["min_length"] = ok
        points += 1 if ok else 0
        total += 1

    score = points / total if total > 0 else 1.0
    passed = score >= expected.get("min_score", 0.5)
    return score, checks, passed


# ── Runner ───────────────────────────────────────────────────────────────────

async def run_task(
    task: ClawMarkTask,
    db,
    affaire_id,
) -> TaskResult:
    from modules.agent.service import run_agent

    t0 = time.monotonic()
    error = ""
    result_text = ""

    try:
        run = await asyncio.wait_for(
            run_agent(
                db=db,
                instruction=task.instruction,
                affaire_id=affaire_id,
                user_id=None,
                agent_name=task.agent,
                max_iterations=6,
            ),
            timeout=task.timeout_s,
        )
        result_text = run.result or ""
        if run.status == "failed":
            error = run.error_message or "run failed"
    except asyncio.TimeoutError:
        error = f"timeout after {task.timeout_s}s"
    except Exception as exc:
        error = str(exc)[:200]

    duration_ms = int((time.monotonic() - t0) * 1000)

    if error and not result_text:
        return TaskResult(
            task_id=task.task_id,
            agent=task.agent,
            passed=False,
            score=0.0,
            result_excerpt="",
            error=error,
            duration_ms=duration_ms,
        )

    score, checks, passed = _score_task(result_text, task.expected)
    return TaskResult(
        task_id=task.task_id,
        agent=task.agent,
        passed=passed,
        score=score,
        result_excerpt=result_text[:200],
        error=error,
        duration_ms=duration_ms,
        checks=checks,
    )


async def run_benchmark(
    dataset_path: Path,
    task_id: Optional[str] = None,
    max_tasks: Optional[int] = None,
    dry_run: bool = False,
) -> ClawMarkReport:
    from database import AsyncSessionLocal
    from modules.affaires.service import create_affaire
    from modules.auth.service import create_user

    tasks = load_dataset(dataset_path)
    if task_id:
        tasks = [t for t in tasks if t.task_id == task_id]
    if max_tasks:
        tasks = tasks[:max_tasks]

    if not tasks:
        raise ValueError("Aucune tâche trouvée.")

    started = datetime.now(timezone.utc).isoformat()

    if dry_run:
        print(f"DRY RUN — {len(tasks)} tâche(s) dans {dataset_path.name}")
        for t in tasks:
            print(f"  [{t.task_id}] {t.title} — agent:{t.agent} timeout:{t.timeout_s}s")
        return ClawMarkReport(
            dataset=dataset_path.stem,
            started_at=started,
            finished_at=started,
            total=len(tasks),
            passed=0,
            failed=0,
            pass_rate=0.0,
            mean_score=0.0,
            mean_duration_ms=0,
            results=[],
        )

    results: list[TaskResult] = []

    async with AsyncSessionLocal() as db:
        # Affaire de benchmark dédiée
        try:
            bench_user = await create_user(
                db, "bench@clawmark.local", "clawmark-bench", "ClawMark", "moe"
            )
        except Exception:
            from modules.auth.models import User
            from sqlalchemy import select
            row = (await db.execute(select(User).where(User.email == "bench@clawmark.local"))).scalars().first()
            bench_user = row

        try:
            affaire = await create_affaire(
                db,
                code="CLW-BENCH",
                nom="ClawMark Benchmark",
                description="Affaire dédiée aux runs de benchmark ClawMark",
                statut="actif",
                created_by=bench_user.id,
            )
            await db.commit()
        except Exception:
            from modules.affaires.models import Affaire
            from sqlalchemy import select
            row = (await db.execute(select(Affaire).where(Affaire.code == "CLW-BENCH"))).scalars().first()
            affaire = row

        for i, task in enumerate(tasks, 1):
            print(f"[{i}/{len(tasks)}] {task.task_id} ({task.agent})...", end=" ", flush=True)
            result = await run_task(task, db, affaire.id)
            results.append(result)
            status = "PASS" if result.passed else "FAIL"
            print(f"{status}  score={result.score:.2f}  {result.duration_ms}ms")
            if result.error:
                print(f"         ⚠ {result.error}")

    finished = datetime.now(timezone.utc).isoformat()
    passed = sum(1 for r in results if r.passed)
    mean_score = sum(r.score for r in results) / len(results) if results else 0.0
    mean_dur = int(sum(r.duration_ms for r in results) / len(results)) if results else 0

    return ClawMarkReport(
        dataset=dataset_path.stem,
        started_at=started,
        finished_at=finished,
        total=len(results),
        passed=passed,
        failed=len(results) - passed,
        pass_rate=passed / len(results) if results else 0.0,
        mean_score=mean_score,
        mean_duration_ms=mean_dur,
        results=results,
    )


# ── CLI ──────────────────────────────────────────────────────────────────────

def _print_report(report: ClawMarkReport) -> None:
    print(f"\n=== ClawMark — {report.dataset} ===")
    print(f"Démarré  : {report.started_at}")
    print(f"Terminé  : {report.finished_at}")
    print(f"Total    : {report.total}  Passé : {report.passed}  Échoué : {report.failed}")
    print(f"Taux     : {report.pass_rate:.1%}  Score moyen : {report.mean_score:.3f}")
    print(f"Durée    : {report.mean_duration_ms} ms / tâche en moyenne")
    print()
    print(f"{'task_id':<35} {'agent':<14} {'pass':<6} {'score':<7} {'ms':<7}")
    print("-" * 75)
    for r in report.results:
        flag = "OK" if r.passed else "KO"
        print(f"{r.task_id:<35} {r.agent:<14} {flag:<6} {r.score:<7.3f} {r.duration_ms:<7}")
        if r.error:
            print(f"    ⚠ {r.error}")
        for check, ok in r.checks.items():
            icon = "✓" if ok else "✗"
            print(f"    {icon} {check}")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="clawmark", description="ARCEUS — ClawMark benchmark runner"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="Liste les datasets disponibles")

    p_run = sub.add_parser("run", help="Exécute un dataset ClawMark")
    p_run.add_argument("--dataset", default=None, help="Chemin vers un fichier JSON de tâches")
    p_run.add_argument("--task", default=None, help="ID d'une tâche spécifique")
    p_run.add_argument("--max-tasks", type=int, default=None)
    p_run.add_argument("--dry-run", action="store_true")
    p_run.add_argument("--json", action="store_true", help="Sortie JSON brute")

    args = parser.parse_args(argv)

    if args.command == "list":
        datasets = list_datasets()
        if not datasets:
            print("Aucun dataset trouvé dans", DATASETS_DIR)
            return 0
        for name in datasets:
            path = DATASETS_DIR / f"{name}.json"
            try:
                tasks = load_dataset(path)
                print(f"  {name:<30} — {len(tasks)} tâches")
            except Exception as exc:
                print(f"  {name:<30} — ⚠ erreur: {exc}")
        return 0

    if args.command == "run":
        if args.dataset:
            dataset_path = Path(args.dataset)
        else:
            # Utilise le premier dataset disponible
            names = list_datasets()
            if not names:
                print("Aucun dataset disponible. Créez un fichier dans", DATASETS_DIR)
                return 1
            dataset_path = DATASETS_DIR / f"{names[0]}.json"

        report = asyncio.run(
            run_benchmark(
                dataset_path=dataset_path,
                task_id=args.task,
                max_tasks=args.max_tasks,
                dry_run=args.dry_run,
            )
        )

        if args.json:
            import dataclasses
            print(json.dumps(dataclasses.asdict(report), indent=2, ensure_ascii=False))
        else:
            _print_report(report)

        return 0 if report.failed == 0 else 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
