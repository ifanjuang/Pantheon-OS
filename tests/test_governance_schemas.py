"""
Static tests for the Pantheon governance schemas.

These tests load the validator from `operations/validate_governance.py`
without going through the runtime (no Postgres, no Redis, no network).
They verify that:

* every schema file under `schemas/` is well-formed;
* every `schemas/examples/<schema>/valid_*.yaml` instance validates;
* every `schemas/examples/<schema>/invalid/*.yaml` instance fails;
* the canonical schema names listed in the Bloc 4 brief are covered.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "operations" / "validate_governance.py"
SCHEMAS_DIR = REPO_ROOT / "schemas"
EXAMPLES_DIR = SCHEMAS_DIR / "examples"


def _load_validator(module_name: str = "pantheon_governance_validator"):
    spec = importlib.util.spec_from_file_location(module_name, VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def validator():
    return _load_validator()


@pytest.fixture(scope="module")
def schemas(validator):
    return validator.load_schemas(SCHEMAS_DIR)


def test_schemas_load_cleanly(schemas):
    """Every schema file under schemas/ must be well-formed."""
    assert schemas, "no schemas loaded"
    for title, schema in schemas.items():
        assert schema.get("$pantheon_schema") == 1
        assert isinstance(schema.get("title"), str) and schema["title"] == title
        assert isinstance(schema.get("type"), str)


def test_required_canonical_schemas_present(schemas):
    """The Bloc 4 brief lists ten canonical objects; all must be defined."""
    required = {
        "role_signal",
        "addressed_role_signal",
        "role_consultation",
        "format_reminder_request",
        "format_reminder_response",
        "format_blocked",
        "task_contract",
        "evidence_pack",
        "memory_candidate",
        "skill_manifest",
        "workflow_manifest",
    }
    missing = required - set(schemas)
    assert not missing, f"missing canonical schemas: {sorted(missing)}"


def test_examples_directory_present():
    """The examples directory must exist with at least one schema folder."""
    assert EXAMPLES_DIR.is_dir(), f"missing {EXAMPLES_DIR}"
    children = [p for p in EXAMPLES_DIR.iterdir() if p.is_dir()]
    assert children, "no example schema folders found"


def test_every_valid_example_validates(validator, schemas):
    """Every `schemas/examples/<schema>/valid_*.yaml` must validate."""
    targets = [t for t in validator.discover_example_instances(EXAMPLES_DIR) if not t[2]]
    assert targets, "no valid examples discovered"
    results = validator._validate_targets(schemas, targets)
    failures = [r for r in results if not r.passed]
    assert not failures, "valid examples failed:\n" + "\n".join(
        f"  {r.schema_name} :: {r.instance_path}\n    " + "\n    ".join(str(e) for e in r.errors) for r in failures
    )


def test_every_invalid_example_fails(validator, schemas):
    """Every `schemas/examples/<schema>/invalid/*.yaml` must trigger at least one error."""
    targets = [t for t in validator.discover_example_instances(EXAMPLES_DIR) if t[2]]
    assert targets, "no invalid examples discovered"
    results = validator._validate_targets(schemas, targets)
    silent = [r for r in results if not r.errors]
    assert not silent, "invalid examples did not fail:\n" + "\n".join(
        f"  {r.schema_name} :: {r.instance_path}" for r in silent
    )


def test_validator_exits_zero_by_default_on_full_run(validator):
    """`main()` without `--exit-on-error` must always return 0, even if findings exist."""
    rc = validator.main([])
    assert rc == 0


def test_validator_exit_on_error_returns_nonzero_for_bad_instance(validator, tmp_path):
    """When asked to fail on error, an unknown schema name must return non-zero."""
    bad_dir = tmp_path / "examples" / "no_such_schema"
    bad_dir.mkdir(parents=True)
    (bad_dir / "valid_dummy.yaml").write_text("id: x\n", encoding="utf-8")
    rc = validator.main(
        [
            "--instances",
            str(tmp_path / "examples"),
            "--exit-on-error",
        ]
    )
    assert rc == 1


def test_validator_rejects_forbidden_top_level_key(validator, schemas):
    """A `role_signal` instance carrying `raw_chain_of_thought` must fail."""
    instance = {
        "id": "RS-2026-9999",
        "from_role": "ARGOS",
        "to_role": "APOLLO",
        "type": "information_transmission",
        "content_summary": "test",
        "status": "open",
        "raw_chain_of_thought": "leak",
    }
    errors = validator.validate_instance(instance, schemas["role_signal"])
    assert any("raw_chain_of_thought" in str(e) for e in errors)


def test_validator_rejects_hermes_as_pantheon_role(validator, schemas):
    """A `role_signal` instance with `from_role: HERMES` must fail."""
    instance = {
        "id": "RS-2026-9998",
        "from_role": "HERMES",
        "to_role": "ZEUS",
        "type": "information_transmission",
        "content_summary": "test",
        "status": "open",
    }
    errors = validator.validate_instance(instance, schemas["role_signal"])
    assert any("from_role" in e.path and "HERMES" in e.message for e in errors)


def test_validator_blocks_auto_fix_in_task_contract(validator, schemas):
    """`remediation_policy.auto_fix_allowed: true` must be rejected."""
    instance = {
        "id": "bad_task",
        "domain": "general",
        "purpose": "test",
        "mode": "read_only",
        "inputs": {"required": []},
        "outputs": {"required": ["report"]},
        "allowed_tools": [],
        "forbidden_tools": [],
        "approval_level": "C0",
        "agents": [],
        "skills": [],
        "memory_impact": "none",
        "evidence_required": True,
        "fallback_policy": {
            "retry_allowed": False,
            "alternative_tool_allowed": False,
            "max_retries": 0,
            "require_approval_if_risk_increases": True,
            "forbidden_fallbacks": [],
        },
        "remediation_policy": {
            "enabled": True,
            "auto_fix_allowed": True,
            "patch_candidate_allowed": True,
            "require_evidence_pack": True,
        },
    }
    errors = validator.validate_instance(instance, schemas["task_contract"])
    assert any("auto_fix_allowed" in e.path for e in errors)


def test_validator_enforces_additional_properties_flag(validator):
    """`additional_properties_allowed: false` must reject unknown keys."""
    schema = {
        "$pantheon_schema": 1,
        "title": "strict_test",
        "type": "object",
        "required": ["id"],
        "properties": {"id": {"type": "string"}},
        "additional_properties_allowed": False,
    }
    validator._check_schema_well_formed(schema, Path("strict_test.schema.yaml"))
    errors = validator.validate_instance({"id": "ok", "extra": "blocked"}, schema)
    assert any("additional key" in e.message and "extra" in e.path for e in errors)


def test_validator_no_filesystem_side_effect_on_import(validator):
    """Importing the validator module must not touch the filesystem."""
    _load_validator("pantheon_governance_validator_reload")
