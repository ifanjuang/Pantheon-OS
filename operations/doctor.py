"""
Pantheon Doctor — read-only governance coherence checker.

Companion to `operations/doctor.md`. Observes the repository and writes a
Markdown report under `reports/doctor/`. Doctor never mutates source files,
runs no network calls, installs no dependency, accesses no secret and
performs no automatic fix.

See `docs/governance/APPROVALS.md` for the C0 read-only authority level.
See `operations/doctor.md` section 1 (Purpose) and section 28 (Future
automation boundary) for the doctrine that bounds this script.

Usage:
    python operations/doctor.py [--repo PATH] [--output PATH] [--print] [--no-write]

Exit code is always 0. Findings live in the report.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable


# ── Status vocabulary (mirrors operations/doctor.md section 4) ──────────────

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
NOT_APPLICABLE = "NOT_APPLICABLE"
TO_VERIFY = "TO_VERIFY"
BLOCKED_BY_POLICY = "BLOCKED_BY_POLICY"

RISK_LOW = "low"
RISK_MEDIUM = "medium"
RISK_HIGH = "high"
RISK_CRITICAL = "critical"


@dataclass
class Finding:
    check: str
    status: str
    evidence: str = ""
    risk: str = RISK_LOW
    next_action: str = ""
    category: str = "misc"


@dataclass
class Report:
    repo: Path
    date: str
    findings: list[Finding] = field(default_factory=list)

    def add(self, **kwargs: str) -> None:
        self.findings.append(Finding(**kwargs))

    def by_category(self) -> dict[str, list[Finding]]:
        grouped: dict[str, list[Finding]] = {}
        for f in self.findings:
            grouped.setdefault(f.category, []).append(f)
        return grouped


# ── Helpers (all read-only) ─────────────────────────────────────────────────


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _iter_files(root: Path, glob: str) -> Iterable[Path]:
    for p in sorted(root.glob(glob)):
        if p.is_file():
            yield p


# ── Required governance documents (mirrors operations/doctor.md §6) ─────────

REQUIRED_GOVERNANCE_DOCS = [
    "README.md",
    "STATUS.md",
    "ROADMAP.md",
    "ARCHITECTURE.md",
    "MODULES.md",
    "AGENTS.md",
    "MEMORY.md",
    "APPROVALS.md",
    "TASK_CONTRACTS.md",
    "TASK_CONTRACT_REVISIONS.md",
    "EVIDENCE_PACK.md",
    "HERMES_INTEGRATION.md",
    "OPENWEBUI_INTEGRATION.md",
    "OPENWEBUI_DOMAIN_MAPPING.md",
    "MODEL_ROUTING_POLICY.md",
    "EXTERNAL_TOOLS_POLICY.md",
    "EXTERNAL_RUNTIME_OPTIONS.md",
    "EXTERNAL_AI_OPTION_REVIEWS.md",
    "EXECUTION_DISCIPLINE.md",
    "EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md",
    "KNOWLEDGE_TAXONOMY.md",
    "CODE_AUDIT_POST_PIVOT.md",
    "WORKFLOW_SCHEMA.md",
    "WORKFLOW_ADAPTATION.md",
    "SKILL_LIFECYCLE.md",
    "MEMORY_EVENT_SCHEMA.md",
    "VERSIONS.md",
]

ROLE_SIGNAL_DOCS = [
    "ROLE_SIGNALS.md",
    "ROLE_SIGNAL_PROFILES.md",
    "ROUTING_FOUNDATION.md",
]

DOCTRINE_LINES = (
    "OpenWebUI expose.",
    "Hermes Agent exécute.",
    "Pantheon Next gouverne.",
)

DOCTRINE_TARGETS = (
    Path("README.md"),
    Path("CLAUDE.md"),
    Path("docs/governance/STATUS.md"),
)

# ARCHITECTURE.md paraphrases the doctrine in prose; verify only that the
# three layer names co-occur, without requiring the exact French triplet.
ARCHITECTURE_DOCTRINE_TOKENS = ("OpenWebUI", "Hermes Agent", "Pantheon")

# Forbidden Pantheon HTTP endpoints — must never be defined in platform/api/
FORBIDDEN_ENDPOINTS = (
    ("POST", "/agents/run"),
    ("POST", "/runtime/execute"),
    ("POST", "/memory/promote/auto"),
)

# Forbidden / suspicious paths (operations/doctor.md §8)
FORBIDDEN_PATHS = (
    "domains/architecture",  # canonical replacement: domains/architecture_fr
    "workflows/generic",  # canonical replacement: domains/general/workflows
    "memory/agency",  # canonical replacement: memory/system
)

# Path that exists today but is legacy and should be classified.
LEGACY_PATHS_TO_CLASSIFY = ("skills/generic",)


# ── Individual checks ───────────────────────────────────────────────────────


def check_root_entries(repo: Path, report: Report) -> None:
    required = ("README.md", "CLAUDE.md", "CHANGELOG.md", "VERSION")
    missing = [name for name in required if not (repo / name).is_file()]
    if not missing:
        report.add(
            check="root_entry_points",
            status=PASS,
            evidence="README.md, CLAUDE.md, CHANGELOG.md, VERSION present",
            category="root",
        )
    else:
        report.add(
            check="root_entry_points",
            status=FAIL if "README.md" in missing else WARN,
            evidence=f"missing: {', '.join(missing)}",
            risk=RISK_HIGH if "README.md" in missing else RISK_LOW,
            next_action="restore missing root entry points",
            category="root",
        )


def check_ai_logs_readme(repo: Path, report: Report) -> None:
    path = repo / "ai_logs" / "README.md"
    if path.is_file():
        report.add(
            check="ai_logs_readme_present",
            status=PASS,
            evidence="ai_logs/README.md found",
            category="ai_logs",
        )
    else:
        report.add(
            check="ai_logs_readme_present",
            status=FAIL,
            evidence="ai_logs/README.md missing",
            risk=RISK_HIGH,
            next_action="restore ai_logs/README.md",
            category="ai_logs",
        )


def check_governance_docs(repo: Path, report: Report) -> None:
    gov = repo / "docs" / "governance"
    missing = [name for name in REQUIRED_GOVERNANCE_DOCS if not (gov / name).is_file()]
    if not missing:
        report.add(
            check="governance_docs_present",
            status=PASS,
            evidence=f"{len(REQUIRED_GOVERNANCE_DOCS)} required governance docs present under docs/governance/",
            category="governance",
        )
    else:
        report.add(
            check="governance_docs_present",
            status=FAIL,
            evidence=f"missing: {', '.join(missing)}",
            risk=RISK_HIGH,
            next_action="restore missing governance documents",
            category="governance",
        )


def check_role_signal_docs(repo: Path, report: Report) -> None:
    gov = repo / "docs" / "governance"
    missing = [name for name in ROLE_SIGNAL_DOCS if not (gov / name).is_file()]
    if not missing:
        report.add(
            check="role_signal_docs_present",
            status=PASS,
            evidence=", ".join(ROLE_SIGNAL_DOCS) + " present",
            category="governance",
        )
    else:
        report.add(
            check="role_signal_docs_present",
            status=FAIL,
            evidence=f"missing: {', '.join(missing)}",
            risk=RISK_HIGH,
            next_action="restore role-signal governance documents",
            category="governance",
        )


def check_doctrine_strings(repo: Path, report: Report) -> None:
    misses: list[str] = []
    for rel in DOCTRINE_TARGETS:
        text = _read_text(repo / rel)
        if text is None:
            misses.append(f"{rel} unreadable")
            continue
        for line in DOCTRINE_LINES:
            if line not in text:
                misses.append(f"{rel} lacks '{line}'")
    if not misses:
        report.add(
            check="doctrine_lines_present",
            status=PASS,
            evidence="canonical OpenWebUI/Hermes/Pantheon Next triplet found in README, CLAUDE, STATUS",
            category="doctrine",
        )
    else:
        report.add(
            check="doctrine_lines_present",
            status=FAIL,
            evidence="; ".join(misses[:5]),
            risk=RISK_HIGH,
            next_action="restore canonical doctrine lines in the listed files",
            category="doctrine",
        )

    arch_text = _read_text(repo / "docs" / "governance" / "ARCHITECTURE.md")
    if arch_text is None:
        report.add(
            check="architecture_doctrine_layers",
            status=FAIL,
            evidence="docs/governance/ARCHITECTURE.md unreadable",
            risk=RISK_HIGH,
            category="doctrine",
        )
        return
    missing_tokens = [tok for tok in ARCHITECTURE_DOCTRINE_TOKENS if tok not in arch_text]
    if not missing_tokens:
        report.add(
            check="architecture_doctrine_layers",
            status=PASS,
            evidence="ARCHITECTURE.md mentions OpenWebUI, Hermes Agent and Pantheon",
            category="doctrine",
        )
    else:
        report.add(
            check="architecture_doctrine_layers",
            status=WARN,
            evidence=f"missing tokens: {', '.join(missing_tokens)}",
            risk=RISK_MEDIUM,
            next_action="ensure ARCHITECTURE.md references the three operating layers explicitly",
            category="doctrine",
        )


_AGENT_ROW_RE = re.compile(r"^\|\s*(HERMES|Hermes Agent|Hermes)\s*\|", re.MULTILINE)


def check_hermes_not_pantheon_agent(repo: Path, report: Report) -> None:
    """AGENTS.md must not list HERMES as a Pantheon role.

    Hermes Agent is the runtime executor, not a Pantheon Role. The agents
    table in `docs/governance/AGENTS.md` must therefore not contain a row
    keyed on `HERMES` / `Hermes` / `Hermes Agent`.
    """
    path = repo / "docs" / "governance" / "AGENTS.md"
    text = _read_text(path)
    if text is None:
        report.add(
            check="hermes_not_in_agents_table",
            status=FAIL,
            evidence="AGENTS.md unreadable",
            risk=RISK_HIGH,
            next_action="restore AGENTS.md",
            category="doctrine",
        )
        return
    matches = _AGENT_ROW_RE.findall(text)
    if not matches:
        report.add(
            check="hermes_not_in_agents_table",
            status=PASS,
            evidence="no `| HERMES |` row found in AGENTS.md",
            category="doctrine",
        )
    else:
        report.add(
            check="hermes_not_in_agents_table",
            status=FAIL,
            evidence=f"{len(matches)} Hermes row(s) detected in AGENTS.md",
            risk=RISK_CRITICAL,
            next_action="remove Hermes rows from the Pantheon agents table",
            category="doctrine",
        )


def check_governance_index_coverage(repo: Path, report: Report) -> None:
    """Every *.md under docs/governance/ should be referenced by README.md."""
    gov = repo / "docs" / "governance"
    readme = _read_text(gov / "README.md")
    if readme is None:
        report.add(
            check="governance_index_coverage",
            status=FAIL,
            evidence="docs/governance/README.md unreadable",
            risk=RISK_HIGH,
            category="governance",
        )
        return
    unreferenced: list[str] = []
    for path in _iter_files(gov, "*.md"):
        if path.name == "README.md":
            continue
        if path.name not in readme:
            unreferenced.append(path.name)
    if not unreferenced:
        report.add(
            check="governance_index_coverage",
            status=PASS,
            evidence="docs/governance/README.md references every other governance doc by file name",
            category="governance",
        )
    else:
        report.add(
            check="governance_index_coverage",
            status=WARN,
            evidence=f"unreferenced in README.md: {', '.join(unreferenced)}",
            risk=RISK_LOW,
            next_action="add missing entries to docs/governance/README.md",
            category="governance",
        )


_POST_DECORATOR_RE = re.compile(
    r"""@(?:router|app)\.post\(\s*['"]([^'"]+)['"]""",
)


def check_forbidden_endpoints(repo: Path, report: Report) -> None:
    """No FastAPI POST handler may expose the forbidden Pantheon endpoints."""
    api = repo / "platform" / "api"
    if not api.is_dir():
        report.add(
            check="forbidden_endpoints_absent",
            status=NOT_APPLICABLE,
            evidence="platform/api/ not present",
            category="runtime_boundary",
        )
        return
    forbidden_paths = {p for _, p in FORBIDDEN_ENDPOINTS}
    hits: list[str] = []
    for py in api.rglob("*.py"):
        text = _read_text(py)
        if not text:
            continue
        for match in _POST_DECORATOR_RE.finditer(text):
            route = match.group(1)
            if route in forbidden_paths or any(route.endswith(p) for p in forbidden_paths):
                hits.append(f"{py.relative_to(repo)}: POST {route}")
    if not hits:
        report.add(
            check="forbidden_endpoints_absent",
            status=PASS,
            evidence="no POST /agents/run, /runtime/execute or /memory/promote/auto handler in platform/api/",
            category="runtime_boundary",
        )
    else:
        report.add(
            check="forbidden_endpoints_absent",
            status=FAIL,
            evidence="; ".join(hits),
            risk=RISK_CRITICAL,
            next_action="remove or relocate forbidden POST handlers",
            category="runtime_boundary",
        )


def check_forbidden_paths(repo: Path, report: Report) -> None:
    found: list[str] = []
    for rel in FORBIDDEN_PATHS:
        path = repo / rel
        if path.exists():
            found.append(rel)
    if not found:
        report.add(
            check="forbidden_paths_absent",
            status=PASS,
            evidence="no domains/architecture, workflows/generic or memory/agency present",
            category="canonical_paths",
        )
    else:
        report.add(
            check="forbidden_paths_absent",
            status=FAIL,
            evidence=f"forbidden paths present: {', '.join(found)}",
            risk=RISK_HIGH,
            next_action="rename to canonical replacement or relocate to legacy/",
            category="canonical_paths",
        )


def check_legacy_path_classification(repo: Path, report: Report) -> None:
    """Legacy paths that may exist must be referenced in CODE_AUDIT_POST_PIVOT.md."""
    audit_text = _read_text(repo / "docs" / "governance" / "CODE_AUDIT_POST_PIVOT.md") or ""
    unclassified: list[str] = []
    classified: list[str] = []
    for rel in LEGACY_PATHS_TO_CLASSIFY:
        if not (repo / rel).exists():
            continue
        if rel in audit_text:
            classified.append(rel)
        else:
            unclassified.append(rel)
    if not unclassified:
        if classified:
            evidence = f"legacy paths classified in CODE_AUDIT_POST_PIVOT.md: {', '.join(classified)}"
        else:
            evidence = "no legacy paths needing classification today"
        report.add(
            check="legacy_paths_classified",
            status=PASS,
            evidence=evidence,
            category="canonical_paths",
        )
    else:
        report.add(
            check="legacy_paths_classified",
            status=WARN,
            evidence=f"present but unclassified: {', '.join(unclassified)}",
            risk=RISK_MEDIUM,
            next_action="add a classification row in CODE_AUDIT_POST_PIVOT.md",
            category="canonical_paths",
        )


_CRITICAL_TODO_RE = re.compile(r"\b(TODO!|FIXME!|XXX!)\b")


def check_critical_todos(repo: Path, report: Report) -> None:
    """Count obvious critical TODO/FIXME markers in tracked governance, ops and api files."""
    scan_roots = ("docs", "operations", "platform/api", "ai_logs")
    hits: list[str] = []
    for root in scan_roots:
        base = repo / root
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in (".md", ".py", ".yaml", ".yml"):
                continue
            text = _read_text(path)
            if not text or not _CRITICAL_TODO_RE.search(text):
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                if _CRITICAL_TODO_RE.search(line):
                    hits.append(f"{path.relative_to(repo)}:{lineno}")
                    if len(hits) >= 20:
                        break
            if len(hits) >= 20:
                break
        if len(hits) >= 20:
            break
    if not hits:
        report.add(
            check="critical_todos_absent",
            status=PASS,
            evidence="no TODO!/FIXME!/XXX! markers in docs, operations, platform/api or ai_logs",
            category="hygiene",
        )
    else:
        report.add(
            check="critical_todos_absent",
            status=WARN,
            evidence=f"{len(hits)} hit(s): " + "; ".join(hits[:5]),
            risk=RISK_LOW,
            next_action="resolve or downgrade critical markers",
            category="hygiene",
        )


def check_governance_dead_links(repo: Path, report: Report) -> None:
    """Detect references to `docs/governance/<NAME>.md` that do not resolve."""
    gov = repo / "docs" / "governance"
    if not gov.is_dir():
        report.add(
            check="governance_dead_links",
            status=NOT_APPLICABLE,
            evidence="docs/governance/ not present",
            category="governance",
        )
        return
    pattern = re.compile(r"docs/governance/([A-Za-z0-9_]+\.md)")
    seen: set[str] = set()
    dead: set[str] = set()
    scan_roots = ("docs", "README.md", "CLAUDE.md", "operations", "ai_logs")
    for root in scan_roots:
        base = repo / root
        targets: Iterable[Path]
        if base.is_file():
            targets = [base]
        elif base.is_dir():
            targets = (p for p in base.rglob("*.md") if p.is_file())
        else:
            continue
        for path in targets:
            text = _read_text(path)
            if not text:
                continue
            for match in pattern.finditer(text):
                name = match.group(1)
                if name in seen:
                    continue
                seen.add(name)
                if not (gov / name).is_file():
                    dead.add(name)
    if not dead:
        report.add(
            check="governance_dead_links",
            status=PASS,
            evidence=f"{len(seen)} unique docs/governance/*.md references all resolve",
            category="governance",
        )
    else:
        report.add(
            check="governance_dead_links",
            status=WARN,
            evidence=f"unresolved: {', '.join(sorted(dead))}",
            risk=RISK_MEDIUM,
            next_action="add the missing docs or fix the dead references",
            category="governance",
        )


# ── Orchestrator ────────────────────────────────────────────────────────────

CHECKS: tuple[Callable[[Path, Report], None], ...] = (
    check_root_entries,
    check_ai_logs_readme,
    check_governance_docs,
    check_role_signal_docs,
    check_doctrine_strings,
    check_hermes_not_pantheon_agent,
    check_governance_index_coverage,
    check_governance_dead_links,
    check_forbidden_endpoints,
    check_forbidden_paths,
    check_legacy_path_classification,
    check_critical_todos,
)


def run_checks(repo: Path, date: str | None = None) -> Report:
    """Run every read-only check and return a structured Report."""
    report = Report(repo=repo, date=date or _dt.date.today().isoformat())
    for fn in CHECKS:
        fn(repo, report)
    return report


# ── Report rendering ────────────────────────────────────────────────────────


_CATEGORY_LABEL = {
    "root": "Root entry points",
    "ai_logs": "AI logs",
    "governance": "Governance documents",
    "doctrine": "Doctrine coherence",
    "runtime_boundary": "Runtime boundary",
    "canonical_paths": "Canonical paths",
    "hygiene": "Hygiene",
    "misc": "Other",
}


def render_report(report: Report) -> str:
    lines: list[str] = []
    lines.append(f"# Pantheon Doctor Report — {report.date}")
    lines.append("")
    lines.append(f"Repository: `{report.repo}`")
    lines.append("Mode: C0 read-only")
    lines.append("Operator: `operations/doctor.py`")
    lines.append("")
    lines.append("> Companion to `operations/doctor.md`. Doctor observes and reports.")
    lines.append("> Doctor does not repair, does not mutate sources, does not call the network.")
    lines.append("")

    grouped = report.by_category()
    summary_rows = []
    for cat in ("root", "ai_logs", "governance", "doctrine", "runtime_boundary", "canonical_paths", "hygiene"):
        findings = grouped.get(cat, [])
        if not findings:
            continue
        worst = _worst_status(f.status for f in findings)
        summary_rows.append((cat, worst, len(findings)))

    lines.append("## Summary")
    lines.append("")
    lines.append("| Category | Status | Checks |")
    lines.append("|---|---|---:|")
    for cat, status, count in summary_rows:
        lines.append(f"| {_CATEGORY_LABEL.get(cat, cat)} | {status} | {count} |")
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    lines.append("| Check | Status | Evidence | Risk | Next action |")
    lines.append("|---|---|---|---|---|")
    for finding in report.findings:
        evidence = finding.evidence.replace("|", "\\|")
        next_action = (finding.next_action or "—").replace("|", "\\|")
        lines.append(f"| `{finding.check}` | {finding.status} | {evidence} | {finding.risk} | {next_action} |")
    lines.append("")

    lines.append("## Required approvals before fix")
    lines.append("")
    lines.append("| Finding | Approval |")
    lines.append("|---|---|")
    for finding in report.findings:
        if finding.status in (FAIL, WARN):
            approval = "C3" if finding.status == FAIL else "C1"
            lines.append(f"| `{finding.check}` | {approval} |")
    lines.append("")

    lines.append("## Evidence Pack references")
    lines.append("")
    lines.append(
        "- files read: governance Markdown under `docs/governance/`, `README.md`, `CLAUDE.md`, `ai_logs/README.md`, `platform/api/**/*.py`"
    )
    lines.append("- commands run: none (no shell, no network, no mutation)")
    lines.append("- assumptions: doctor checks reflect `operations/doctor.md` C0 scope")
    lines.append("- limitations: live API endpoints, OpenWebUI runtime, Hermes runtime and Docker stack are not probed")
    lines.append("")
    return "\n".join(lines)


_STATUS_RANK = {
    BLOCKED_BY_POLICY: 0,
    FAIL: 1,
    WARN: 2,
    TO_VERIFY: 3,
    NOT_APPLICABLE: 4,
    PASS: 5,
}


def _worst_status(statuses: Iterable[str]) -> str:
    return min(statuses, key=lambda s: _STATUS_RANK.get(s, 99), default=PASS)


# ── CLI ─────────────────────────────────────────────────────────────────────


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _default_report_path(repo: Path, date: str) -> Path:
    return repo / "reports" / "doctor" / f"{date}-doctor-report.md"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pantheon Doctor — read-only governance checker")
    parser.add_argument("--repo", type=Path, default=None, help="Repository root (defaults to autodetect)")
    parser.add_argument(
        "--output", type=Path, default=None, help="Report path (defaults to reports/doctor/{date}-doctor-report.md)"
    )
    parser.add_argument("--print", dest="print_to_stdout", action="store_true", help="Print the report to stdout")
    parser.add_argument("--no-write", action="store_true", help="Do not write the report file")
    parser.add_argument("--date", default=None, help="Override the report date (YYYY-MM-DD)")
    args = parser.parse_args(argv)

    repo = (args.repo or _default_repo_root()).resolve()
    report = run_checks(repo, date=args.date)
    rendered = render_report(report)

    if args.print_to_stdout or args.no_write:
        sys.stdout.write(rendered)
        if not rendered.endswith("\n"):
            sys.stdout.write("\n")

    if not args.no_write:
        output = (args.output or _default_report_path(repo, report.date)).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
