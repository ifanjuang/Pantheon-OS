"""
CLI OpenClaw — exécute un dataset d'éval depuis le terminal.

Usages :
    python -m modules.evaluation.cli list
    python -m modules.evaluation.cli run openclaw-devis
    python -m modules.evaluation.cli run openclaw-devis --max-cases 2
    python -m modules.evaluation.cli run openclaw-devis --dry-run
    python -m modules.evaluation.cli run openclaw-devis --json > report.json

Écriture dans `stdout` : récapitulatif lisible.
Option `--json` : sérialise le rapport complet (pour CI / archivage).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import Optional

from modules.evaluation.schemas import EvalReport
from modules.evaluation.service import list_datasets, load_dataset, run_eval


def _print_report(report: EvalReport) -> None:
    """Format lisible terminal."""
    print(f"=== OpenClaw — {report.dataset_id} ===")
    print(f"Started  : {report.started_at}")
    print(f"Finished : {report.finished_at}")
    print(f"Total    : {report.total} | Passed : {report.passed} | Failed : {report.failed}")
    print(f"Pass rate: {report.pass_rate:.1%}")
    print(f"Mean score: {report.mean_score:.3f}  (mean duration: {report.mean_duration_ms} ms)")
    print(
        f"Axes moyens: relevance={report.summary.get('relevance', 0):.2f} "
        f"security={report.summary.get('security', 0):.2f} "
        f"completeness={report.summary.get('completeness', 0):.2f}"
    )
    print()
    print(f"{'case_id':<40} {'pass':<6} {'score':<7} {'rel':<5} {'sec':<5} {'comp':<5} {'ms':<6}")
    print("-" * 80)
    for c in report.cases:
        flag = "OK" if c.passed else "KO"
        print(
            f"{c.case_id:<40} {flag:<6} {c.score:<7.3f} "
            f"{c.relevance:<5.2f} {c.security:<5.2f} {c.completeness:<5.2f} "
            f"{c.duration_ms:<6}"
        )
        if c.error:
            print(f"    ⚠ error: {c.error}")


async def _cmd_run(
    dataset_id: str,
    max_cases: Optional[int],
    dry_run: bool,
    as_json: bool,
) -> int:
    # Import local : évite de charger l'engine DB si on fait juste `list`.
    from database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        report = await run_eval(
            db=db,
            dataset_id=dataset_id,
            max_cases=max_cases,
            dry_run=dry_run,
        )

    if as_json:
        print(json.dumps(report.model_dump(), indent=2, ensure_ascii=False))
    else:
        _print_report(report)

    # Code retour non-zéro si au moins un cas échoue (utile CI).
    return 0 if report.failed == 0 else 1


def _cmd_list() -> int:
    names = list_datasets()
    if not names:
        print("Aucun dataset trouvé.")
        return 0
    print("Datasets disponibles :")
    for name in names:
        try:
            ds = load_dataset(name)
            print(f"  {name:<30} — {ds.title or '(sans titre)'} ({len(ds.cases)} cas)")
        except Exception as exc:
            print(f"  {name:<30} — ⚠ parse error: {exc}")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="openclaw", description="ARCEUS — OpenClaw evaluation harness")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="Liste les datasets disponibles")

    p_run = sub.add_parser("run", help="Exécute un dataset")
    p_run.add_argument("dataset_id", help="ex: openclaw-devis")
    p_run.add_argument("--max-cases", type=int, default=None, help="Limite le nombre de cas")
    p_run.add_argument("--dry-run", action="store_true", help="Parse seulement, sans exécution")
    p_run.add_argument("--json", action="store_true", help="Sortie JSON brute")

    args = parser.parse_args(argv)

    if args.command == "list":
        return _cmd_list()

    if args.command == "run":
        return asyncio.run(
            _cmd_run(
                dataset_id=args.dataset_id,
                max_cases=args.max_cases,
                dry_run=args.dry_run,
                as_json=args.json,
            )
        )

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
