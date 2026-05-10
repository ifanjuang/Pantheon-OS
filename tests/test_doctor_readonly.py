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
