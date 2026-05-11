# Pantheon Governance Schemas

> Static, declarative schemas for Pantheon Next governance objects.
>
> The validator is `operations/validate_governance.py`. It is read-only and
> produces no automatic fix.

---

## 1. Purpose

Each canonical governance object — `role_signal`, `addressed_role_signal`,
`role_consultation`, `format_reminder_request`, `format_reminder_response`,
`format_blocked`, `task_contract`, `single_role_task_contract`,
`task_contract_revision`, `evidence_pack`, `memory_candidate`,
`skill_manifest`, `workflow_manifest` — is defined by a separate
`<name>.schema.yaml` file in this directory.

The schemas mirror the canonical Markdown definitions in
`docs/governance/`. They do not introduce new doctrine. When a Markdown
governance file disagrees with a schema, the Markdown wins (per
`CLAUDE.md`); the schema must be updated, not the doctrine.

---

## 2. Doctrine boundary

The schemas and the validator are governance utilities, not runtime.

They must not:

```text
execute a task
activate a skill
promote memory
canonize a workflow
mutate any source file
call the network
read or print secrets
```

They may only:

```text
read schema files
read instance files
emit pass/fail records
emit human-readable error messages
```

This complements the C0 read-only scope of `operations/doctor.py` and
`operations/doctor.md`.

---

## 3. Schema format

A schema file uses the following YAML structure. It is a deliberately small
subset of JSON Schema, expressed in YAML for governance readability.

```yaml
$pantheon_schema: 1
title: <object_name>
description: |
  Short doctrinal note pointing to the source-of-truth Markdown.
governance_refs:
  - docs/governance/<DOC>.md
type: object
required:
  - field_a
  - field_b
properties:
  field_a:
    type: string
  field_b:
    enum: [VALUE_1, VALUE_2]
  optional_field:
    type: string
forbidden_keys:
  - raw_chain_of_thought
  - secret
  - api_key
```

Supported keywords:

| Keyword | Meaning |
|---|---|
| `$pantheon_schema` | Schema format version, currently `1` |
| `title` | Canonical object name |
| `description` | Free text, doctrinal pointer |
| `governance_refs` | Source-of-truth Markdown files |
| `type` | `object`, `array`, `string`, `integer`, `number`, `boolean`, `null`, `any` |
| `required` | Required keys for an object |
| `properties` | Per-key sub-schemas for an object |
| `additional_properties_allowed` | Whether unknown keys are tolerated (default `true`) |
| `forbidden_keys` | Keys that must not appear at this level |
| `items` | Sub-schema for array items |
| `enum` | Allowed scalar values |
| `pattern` | Regex pattern for strings |
| `min_items` / `max_items` | Length bounds for arrays |
| `min_length` / `max_length` | Length bounds for strings |
| `nullable` | When `true`, `null` is also accepted |
| `one_of` | List of sub-schemas; instance must match exactly one |

The validator rejects unknown keywords loudly, so adding a new keyword
requires updating the validator deliberately.

---

## 4. Examples

`examples/<schema_name>/valid_*.yaml` — instances that must validate.

`examples/<schema_name>/invalid_*.yaml` — instances that must fail
validation. Each invalid example carries a top-level comment stating which
rule it violates, so reviewers can see the intent without running the
validator.

The test suite `tests/test_governance_schemas.py` enforces:

* every schema file is well-formed;
* every valid example validates;
* every invalid example fails with at least one error.

---

## 5. What this is not

These schemas do not implement runtime validation, request rejection,
contract enforcement, automatic memory promotion or skill activation. They
exist only to detect drift between the canonical Markdown doctrine and the
YAML artifacts that the doctrine describes.
