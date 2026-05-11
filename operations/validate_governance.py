"""
Pantheon Governance Schema Validator — read-only.

Static validator for the canonical governance objects defined under
`schemas/`. The validator never mutates input files, never executes
workflows, never activates skills, never promotes memory and never
calls the network. It only reads schema and instance YAML files and
reports pass/fail per instance.

See `schemas/README.md` for the schema format.
See `docs/governance/APPROVALS.md` for the C0 read-only authority level.

Usage:
    python operations/validate_governance.py [--schema-dir DIR]
                                              [--instance FILE ...]
                                              [--instances DIR]
                                              [--exit-on-error]

Default behaviour (no arguments): validate every example under
`schemas/examples/`, treating files under `<schema_name>/` as instances
of `<schema_name>` and files under `<schema_name>/invalid/` as
instances expected to fail. Exit code is 0 by default; pass
`--exit-on-error` to return 1 when any unexpected result is found.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml


# ── Schema format constants ────────────────────────────────────────────────

SUPPORTED_SCHEMA_VERSION = 1

ALLOWED_TYPES = {"object", "array", "string", "integer", "number", "boolean", "null", "any"}

ALLOWED_KEYWORDS = {
    "$pantheon_schema",
    "title",
    "description",
    "governance_refs",
    "type",
    "required",
    "properties",
    "additional_properties_allowed",
    "forbidden_keys",
    "items",
    "enum",
    "pattern",
    "min_items",
    "max_items",
    "min_length",
    "max_length",
    "nullable",
    "one_of",
}


# ── Result types ───────────────────────────────────────────────────────────


@dataclass
class ValidationError:
    path: str
    message: str

    def __str__(self) -> str:
        return f"  - {self.path or '<root>'}: {self.message}"


@dataclass
class ValidationResult:
    schema_name: str
    instance_path: Path
    expected_to_fail: bool
    errors: list[ValidationError] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        if self.expected_to_fail:
            return bool(self.errors)
        return not self.errors


# ── Schema loading ─────────────────────────────────────────────────────────


def _check_schema_well_formed(schema: Any, source: Path) -> None:
    """Reject malformed schema files at load time so instance validation can trust them."""
    if not isinstance(schema, dict):
        raise ValueError(f"{source}: top-level must be a mapping")
    version = schema.get("$pantheon_schema")
    if version != SUPPORTED_SCHEMA_VERSION:
        raise ValueError(f"{source}: unsupported $pantheon_schema={version!r}, expected {SUPPORTED_SCHEMA_VERSION}")
    _check_subschema_well_formed(schema, source, path="<root>")


def _check_subschema_well_formed(node: Any, source: Path, path: str) -> None:
    if not isinstance(node, dict):
        return
    unknown = set(node) - ALLOWED_KEYWORDS
    if unknown:
        raise ValueError(f"{source}:{path}: unknown schema keywords {sorted(unknown)}")
    declared_type = node.get("type")
    if declared_type is not None and declared_type not in ALLOWED_TYPES:
        raise ValueError(f"{source}:{path}: invalid type {declared_type!r}")
    properties = node.get("properties")
    if properties is not None:
        if not isinstance(properties, dict):
            raise ValueError(f"{source}:{path}: properties must be a mapping")
        for key, sub in properties.items():
            _check_subschema_well_formed(sub, source, f"{path}.properties.{key}")
    items = node.get("items")
    if items is not None:
        _check_subschema_well_formed(items, source, f"{path}.items")
    one_of = node.get("one_of")
    if one_of is not None:
        if not isinstance(one_of, list):
            raise ValueError(f"{source}:{path}: one_of must be a list")
        for index, sub in enumerate(one_of):
            _check_subschema_well_formed(sub, source, f"{path}.one_of[{index}]")


def load_schemas(schema_dir: Path) -> dict[str, dict]:
    schemas: dict[str, dict] = {}
    for path in sorted(schema_dir.glob("*.schema.yaml")):
        with path.open(encoding="utf-8") as fh:
            schema = yaml.safe_load(fh)
        _check_schema_well_formed(schema, path)
        title = schema.get("title")
        if not isinstance(title, str) or not title:
            raise ValueError(f"{path}: missing or invalid title")
        if title in schemas:
            raise ValueError(f"{path}: duplicate schema title {title!r}")
        schemas[title] = schema
    return schemas


# ── Instance validation ───────────────────────────────────────────────────


def validate_instance(instance: Any, schema: dict) -> list[ValidationError]:
    errors: list[ValidationError] = []
    _validate_node(instance, schema, "", errors)
    return errors


def _validate_node(value: Any, schema: dict, path: str, errors: list[ValidationError]) -> None:
    if value is None and schema.get("nullable"):
        return

    if "one_of" in schema:
        sub_errors_per_branch = []
        matches = 0
        for sub in schema["one_of"]:
            sub_errors: list[ValidationError] = []
            _validate_node(value, sub, path, sub_errors)
            if not sub_errors:
                matches += 1
            sub_errors_per_branch.append(sub_errors)
        if matches != 1:
            errors.append(
                ValidationError(
                    path,
                    f"one_of expected exactly one match, got {matches}",
                )
            )
        return

    if "enum" in schema:
        if value not in schema["enum"]:
            errors.append(
                ValidationError(
                    path,
                    f"value {value!r} not in enum {schema['enum']!r}",
                )
            )
        return

    declared_type = schema.get("type", "any")
    if declared_type == "any":
        pass
    elif declared_type == "object":
        _validate_object(value, schema, path, errors)
    elif declared_type == "array":
        _validate_array(value, schema, path, errors)
    elif declared_type == "string":
        _validate_string(value, schema, path, errors)
    elif declared_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(ValidationError(path, f"expected integer, got {type(value).__name__}"))
    elif declared_type == "number":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(ValidationError(path, f"expected number, got {type(value).__name__}"))
    elif declared_type == "boolean":
        if not isinstance(value, bool):
            errors.append(ValidationError(path, f"expected boolean, got {type(value).__name__}"))
    elif declared_type == "null":
        if value is not None:
            errors.append(ValidationError(path, f"expected null, got {type(value).__name__}"))


def _validate_object(value: Any, schema: dict, path: str, errors: list[ValidationError]) -> None:
    if not isinstance(value, dict):
        errors.append(ValidationError(path, f"expected object, got {type(value).__name__}"))
        return
    for key in schema.get("required", []):
        if key not in value:
            errors.append(ValidationError(path, f"missing required key {key!r}"))
    forbidden = set(schema.get("forbidden_keys", []))
    for key in forbidden & set(value):
        errors.append(ValidationError(_join(path, key), f"forbidden key {key!r} present"))
    properties = schema.get("properties", {})
    for key, sub_value in value.items():
        if key in properties:
            _validate_node(sub_value, properties[key], _join(path, key), errors)


def _validate_array(value: Any, schema: dict, path: str, errors: list[ValidationError]) -> None:
    if not isinstance(value, list):
        errors.append(ValidationError(path, f"expected array, got {type(value).__name__}"))
        return
    if "min_items" in schema and len(value) < schema["min_items"]:
        errors.append(ValidationError(path, f"array too short: {len(value)} < {schema['min_items']}"))
    if "max_items" in schema and len(value) > schema["max_items"]:
        errors.append(ValidationError(path, f"array too long: {len(value)} > {schema['max_items']}"))
    items_schema = schema.get("items")
    if items_schema is not None:
        for index, item in enumerate(value):
            _validate_node(item, items_schema, f"{path}[{index}]", errors)


def _validate_string(value: Any, schema: dict, path: str, errors: list[ValidationError]) -> None:
    if not isinstance(value, str):
        errors.append(ValidationError(path, f"expected string, got {type(value).__name__}"))
        return
    if "min_length" in schema and len(value) < schema["min_length"]:
        errors.append(ValidationError(path, f"string too short: {len(value)} < {schema['min_length']}"))
    if "max_length" in schema and len(value) > schema["max_length"]:
        errors.append(ValidationError(path, f"string too long: {len(value)} > {schema['max_length']}"))
    pattern = schema.get("pattern")
    if pattern is not None and not re.search(pattern, value):
        errors.append(ValidationError(path, f"string {value!r} does not match pattern {pattern!r}"))


def _join(parent: str, key: str) -> str:
    return f"{parent}.{key}" if parent else key


# ── Example discovery ─────────────────────────────────────────────────────


def discover_example_instances(examples_dir: Path) -> list[tuple[str, Path, bool]]:
    """Return triples (schema_name, instance_path, expected_to_fail) under examples/."""
    found: list[tuple[str, Path, bool]] = []
    if not examples_dir.is_dir():
        return found
    for schema_dir in sorted(examples_dir.iterdir()):
        if not schema_dir.is_dir():
            continue
        schema_name = schema_dir.name
        for path in sorted(schema_dir.glob("*.yaml")):
            if path.is_file():
                found.append((schema_name, path, False))
        invalid_dir = schema_dir / "invalid"
        if invalid_dir.is_dir():
            for path in sorted(invalid_dir.glob("*.yaml")):
                if path.is_file():
                    found.append((schema_name, path, True))
    return found


# ── CLI ───────────────────────────────────────────────────────────────────


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _default_schema_dir(repo: Path) -> Path:
    return repo / "schemas"


def _default_examples_dir(repo: Path) -> Path:
    return repo / "schemas" / "examples"


def _validate_targets(
    schemas: dict[str, dict],
    targets: Iterable[tuple[str, Path, bool]],
) -> list[ValidationResult]:
    results: list[ValidationResult] = []
    for schema_name, instance_path, expected_to_fail in targets:
        schema = schemas.get(schema_name)
        if schema is None:
            results.append(
                ValidationResult(
                    schema_name=schema_name,
                    instance_path=instance_path,
                    expected_to_fail=expected_to_fail,
                    errors=[ValidationError("", f"no schema named {schema_name!r} in schema dir")],
                )
            )
            continue
        with instance_path.open(encoding="utf-8") as fh:
            instance = yaml.safe_load(fh)
        errors = validate_instance(instance, schema)
        results.append(
            ValidationResult(
                schema_name=schema_name,
                instance_path=instance_path,
                expected_to_fail=expected_to_fail,
                errors=errors,
            )
        )
    return results


def _render_results(results: list[ValidationResult]) -> str:
    lines: list[str] = []
    passed = 0
    failed = 0
    for result in results:
        rel = result.instance_path
        marker = "OK" if result.passed else "FAIL"
        if result.passed:
            passed += 1
        else:
            failed += 1
        suffix = " (expected to fail)" if result.expected_to_fail else ""
        lines.append(f"[{marker}] {result.schema_name} :: {rel}{suffix}")
        if not result.passed and not result.expected_to_fail:
            for err in result.errors:
                lines.append(str(err))
        if not result.passed and result.expected_to_fail:
            lines.append("  - expected at least one validation error, got 0")
    lines.append("")
    lines.append(f"Summary: {passed} ok, {failed} unexpected outcome(s) over {len(results)} instances.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pantheon Governance Schema Validator (read-only)")
    parser.add_argument("--repo", type=Path, default=None, help="Repository root (defaults to autodetect)")
    parser.add_argument("--schema-dir", type=Path, default=None, help="Override schemas/ directory")
    parser.add_argument(
        "--instance",
        type=Path,
        action="append",
        default=[],
        help="Instance file with schema name resolved by parent directory",
    )
    parser.add_argument("--instances", type=Path, default=None, help="Override schemas/examples/ directory")
    parser.add_argument(
        "--exit-on-error", action="store_true", help="Return non-zero exit if any instance result is unexpected"
    )
    args = parser.parse_args(argv)

    repo = (args.repo or _default_repo_root()).resolve()
    schema_dir = (args.schema_dir or _default_schema_dir(repo)).resolve()
    examples_dir = (args.instances or _default_examples_dir(repo)).resolve()

    schemas = load_schemas(schema_dir)

    targets: list[tuple[str, Path, bool]] = []
    if args.instance:
        for path in args.instance:
            resolved = path.resolve()
            schema_name = _infer_schema_name(resolved)
            expected_to_fail = resolved.parent.name == "invalid"
            targets.append((schema_name, resolved, expected_to_fail))
    else:
        targets.extend(discover_example_instances(examples_dir))

    results = _validate_targets(schemas, targets)
    sys.stdout.write(_render_results(results))
    if not _render_results(results).endswith("\n"):
        sys.stdout.write("\n")

    if args.exit_on_error and any(not r.passed for r in results):
        return 1
    return 0


def _infer_schema_name(path: Path) -> str:
    parent = path.parent
    if parent.name == "invalid":
        parent = parent.parent
    return parent.name


if __name__ == "__main__":
    raise SystemExit(main())
