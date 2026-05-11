"""
Read-only tests for `operations/doctor.py`.

These tests import the Doctor module directly (no shell, no network) and
verify that:

* The Doctor exposes the expected check identifiers.
* Running the checks against the real repository succeeds.
* The Doctor never mutates source files (it only writes under
  `reports/doctor/` when explicitly asked, and can be run with `--no-write`).
* The Doctor rejects custom report output paths outside `reports/doctor/`.
* The rendered report contains the canonical Markdown sections required
  by `operations/doctor.md` section 27 (Doctor report template).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCTOR_PATH = REPO_ROOT / "operations" / "doctor.py"


def _load_doctor(module_name: str = "pantheon_doctor"):
    spec = importlib.util.spec_from_file_location(module_name, DOCTOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # Required because the module uses @dataclass, which resolves type names
    # via sys.modules during class creation.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def doctor():
    return _load_doctor()


def test_doctor_exposes_expected_checks(doctor):
    expected = {
        "check_root_entries",
        "check_ai_logs_readme",
        "check_governance_docs",
        "check_role_signal_docs",
        "check_doctrine_strings",
        "check_hermes_not_pantheon_agent",
        "check_governance_index_coverage",
        "check_governance_dead_links",
        "check_forbidden_endpoints",
        "check_legacy_runtime_surfaces",
        "check_forbidden_paths",
        "check_legacy_path_classification",
        "check_critical_todos",
    }
    actual = {fn.__name__ for fn in doctor.CHECKS}
    assert expected.issubset(actual), f"missing checks: {expected - actual}"


def test_doctor_runs_against_repo(doctor):
    report = doctor.run_checks(REPO_ROOT, date="2026-01-01")
    assert report.date == "2026-01-01"
    assert report.repo == REPO_ROOT
    assert report.findings, "doctor produced no findings"

    statuses = {f.status for f in report.findings}
    allowed = {
        doctor.PASS,
        doctor.WARN,
        doctor.FAIL,
        doctor.NOT_APPLICABLE,
        doctor.TO_VERIFY,
        doctor.BLOCKED_BY_POLICY,
    }
    assert statuses.issubset(allowed), f"unexpected statuses: {statuses - allowed}"


def test_doctor_required_canonical_checks_pass(doctor):
    """Canonical doctrine and boundary checks must pass on the current tree."""
    report = doctor.run_checks(REPO_ROOT, date="2026-01-01")
    by_check = {f.check: f for f in report.findings}
    must_pass = (
        "root_entry_points",
        "ai_logs_readme_present",
        "governance_docs_present",
        "role_signal_docs_present",
        "doctrine_lines_present",
        "hermes_not_in_agents_table",
        "forbidden_endpoints_absent",
        "forbidden_paths_absent",
    )
    for name in must_pass:
        assert name in by_check, f"missing required check: {name}"
        assert by_check[name].status == doctor.PASS, (
            f"check {name} expected PASS, got {by_check[name].status} — {by_check[name].evidence}"
        )


def test_doctor_renders_required_sections(doctor):
    report = doctor.run_checks(REPO_ROOT, date="2026-01-01")
    rendered = doctor.render_report(report)
    for section in (
        "# Pantheon Doctor Report — 2026-01-01",
        "Mode: C0 read-only",
        "## Summary",
        "## Findings",
        "## Required approvals before fix",
        "## Evidence Pack references",
    ):
        assert section in rendered, f"section missing: {section}"


def test_doctor_no_write_when_disabled(doctor):
    """`main(--no-write)` must not create the default report file."""
    default_report = doctor._default_report_path(REPO_ROOT, "1999-12-31")
    assert not default_report.exists()
    rc = doctor.main(["--no-write", "--date", "1999-12-31"])
    assert rc == 0
    assert not default_report.exists()


def test_doctor_writes_under_reports_doctor_when_allowed(doctor):
    """When asked to write, Doctor may write only under reports/doctor/."""
    output = REPO_ROOT / "reports" / "doctor" / "1999-12-31-test-doctor-report.md"
    if output.exists():
        output.unlink()
    try:
        rc = doctor.main(["--output", str(output), "--date", "1999-12-31"])
        assert rc == 0
        assert output.is_file()
        content = output.read_text(encoding="utf-8")
        assert content.startswith("# Pantheon Doctor Report — 1999-12-31")
        assert "## Findings" in content
    finally:
        if output.exists():
            output.unlink()


def test_doctor_blocks_output_outside_reports_doctor(doctor, tmp_path, capsys):
    """A custom --output outside reports/doctor/ must be blocked and must not create a file."""
    output = tmp_path / "doctor-out.md"
    rc = doctor.main(["--output", str(output), "--date", "2026-01-02"])
    captured = capsys.readouterr()
    assert rc == 0
    assert not output.exists()
    assert "Doctor output blocked" in captured.err
    assert "reports/doctor" in captured.err


def test_doctor_module_has_no_side_effect_on_import(doctor):
    """Importing the doctor module must not touch the filesystem."""
    _load_doctor("pantheon_doctor_reload")
    # Sanity: importing the module did not silently create a default report
    assert not doctor._default_report_path(REPO_ROOT, "0000-00-00").exists()


# ── Legacy runtime surface detection (Bloc 7) ──────────────────────────────


def _legacy_finding(doctor, repo: Path):
    report = doctor.run_checks(repo, date="2026-05-11")
    by_check = {f.check: f for f in report.findings}
    return by_check["legacy_runtime_surfaces_absent"]


def test_legacy_runtime_surfaces_detected_on_real_tree(doctor):
    """The current tree carries the legacy /agent/run and /orchestra/* surfaces.

    Per `CODE_AUDIT_POST_PIVOT.md` §3 (entries for `apps/agent/router.py` and
    `apps/orchestra/`), the surfaces are present by design during the
    transition to Hermes Gateway. Doctor must WARN on them.
    """
    finding = _legacy_finding(doctor, REPO_ROOT)
    assert finding.status == doctor.WARN, f"expected WARN, got {finding.status} — {finding.evidence}"
    for expected_path in (
        "/agent/run",
        "/orchestra/run",
        "/orchestra/run-hitl",
        "/orchestra/stream",
        "/orchestra/runs/{run_id}/approve",
    ):
        assert expected_path in finding.evidence, f"missing {expected_path} in evidence"


def test_legacy_runtime_surfaces_pass_on_clean_tree(doctor, tmp_path):
    """A repo that does not define those routes must surface PASS."""
    apps = tmp_path / "platform" / "api" / "apps"
    (apps / "agent").mkdir(parents=True)
    (apps / "orchestra").mkdir(parents=True)
    (apps / "agent" / "router.py").write_text(
        "from fastapi import APIRouter\nrouter = APIRouter()\n",
        encoding="utf-8",
    )
    (apps / "orchestra" / "router.py").write_text(
        "from fastapi import APIRouter\nrouter = APIRouter()\n",
        encoding="utf-8",
    )

    report = doctor.Report(repo=tmp_path, date="2026-05-11")
    doctor.check_legacy_runtime_surfaces(tmp_path, report)
    findings = {f.check: f for f in report.findings}
    finding = findings["legacy_runtime_surfaces_absent"]
    assert finding.status == doctor.PASS, finding.evidence


def test_legacy_runtime_surfaces_not_applicable_without_apps(doctor, tmp_path):
    """If `platform/api/apps/` is missing entirely, surface NOT_APPLICABLE."""
    report = doctor.Report(repo=tmp_path, date="2026-05-11")
    doctor.check_legacy_runtime_surfaces(tmp_path, report)
    findings = {f.check: f for f in report.findings}
    finding = findings["legacy_runtime_surfaces_absent"]
    assert finding.status == doctor.NOT_APPLICABLE


def test_legacy_runtime_surfaces_match_full_set(doctor, tmp_path):
    """A synthetic repo defining all five legacy routes must report all five."""
    apps = tmp_path / "platform" / "api" / "apps"
    (apps / "agent").mkdir(parents=True)
    (apps / "orchestra").mkdir(parents=True)
    (apps / "agent" / "router.py").write_text(
        'from fastapi import APIRouter\nrouter = APIRouter()\n@router.post("/run")\ndef run() -> dict: return {}\n',
        encoding="utf-8",
    )
    (apps / "orchestra" / "router.py").write_text(
        "from fastapi import APIRouter\nrouter = APIRouter()\n"
        '@router.post("/run")\ndef run() -> dict: return {}\n'
        '@router.post("/run-hitl")\ndef hitl() -> dict: return {}\n'
        '@router.post("/stream")\ndef stream() -> dict: return {}\n'
        '@router.post("/runs/{run_id}/approve")\ndef approve(run_id: str) -> dict: return {}\n',
        encoding="utf-8",
    )

    report = doctor.Report(repo=tmp_path, date="2026-05-11")
    doctor.check_legacy_runtime_surfaces(tmp_path, report)
    findings = {f.check: f for f in report.findings}
    finding = findings["legacy_runtime_surfaces_absent"]
    assert finding.status == doctor.WARN
    for path in (
        "/agent/run",
        "/orchestra/run",
        "/orchestra/run-hitl",
        "/orchestra/stream",
        "/orchestra/runs/{run_id}/approve",
    ):
        assert path in finding.evidence


def test_legacy_runtime_surfaces_ignores_governance_get_endpoints(doctor):
    """Read-only governance GET endpoints (Bloc 5) must not trip the check."""
    finding = _legacy_finding(doctor, REPO_ROOT)
    # The Domain API GET endpoints from Bloc 5 live under /domain/role-signals,
    # /domain/role-signal-profiles, /domain/routing-foundation,
    # /domain/governance-index. None of them should appear in the evidence
    # of a check whose scope is legacy POST runtime surfaces.
    for governance_path in (
        "/domain/role-signals",
        "/domain/role-signal-profiles",
        "/domain/routing-foundation",
        "/domain/governance-index",
    ):
        assert governance_path not in finding.evidence


def test_legacy_runtime_surfaces_check_remains_read_only(doctor, tmp_path):
    """Running the check must not write anywhere on disk."""
    apps = tmp_path / "platform" / "api" / "apps" / "agent"
    apps.mkdir(parents=True)
    router = apps / "router.py"
    router.write_text(
        'from fastapi import APIRouter\nrouter = APIRouter()\n@router.post("/run")\ndef r() -> dict: return {}\n',
        encoding="utf-8",
    )
    before_mtime = router.stat().st_mtime_ns
    before_content = router.read_bytes()

    report = doctor.Report(repo=tmp_path, date="2026-05-11")
    doctor.check_legacy_runtime_surfaces(tmp_path, report)

    assert router.stat().st_mtime_ns == before_mtime
    assert router.read_bytes() == before_content


def test_doctor_main_still_exits_zero_with_warn(doctor):
    """Even when legacy surfaces are present (WARN), main() must still exit 0."""
    rc = doctor.main(["--no-write", "--date", "2026-05-11"])
    assert rc == 0
