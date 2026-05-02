# AI LOG ENTRY — 2026-05-02

Branch: `work/chatgpt/external-runtime-options`

A: ChatGPT

## Objective

Classify optional external runtimes, workflow frameworks, context engines and graph/workspace tools without integrating or installing them.

## Context

The operating split remains:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

This intervention documents options only. It does not add runtime capability.

## Changes

- Added `docs/governance/EXTERNAL_RUNTIME_OPTIONS.md`.
- Updated `docs/governance/README.md` to index the new policy.
- Classified:
  - Hermes Agent as canonical external execution runtime.
  - LangChain / LangGraph as `allowed_as_library_in_hermes`, rejected for Pantheon core.
  - Langflow as `test_lab_only`, rejected for Pantheon core.
  - OpenClaw as `blocked_until_reviewed`, rejected for Pantheon core.
  - Graphify as `test_read_only` for repo/docs graph audit.
  - Layer Infinite / Layer as `to_verify`.
  - CTX as `to_verify`.
  - Binderly as `to_verify`.
  - NeverWrite as `watch`, rejected for Pantheon core.
- Added review checklist and approval policy for moving any external option to a safer status.

## Files Touched

- `docs/governance/EXTERNAL_RUNTIME_OPTIONS.md`
- `docs/governance/README.md`
- `ai_logs/2026-05-02-external-runtime-options.md`

## Critical files impacted

- `docs/governance/EXTERNAL_RUNTIME_OPTIONS.md`
- `docs/governance/README.md`

## Tests

- Not run. Documentation only.

## Guardrails

- No external runtime installed.
- No dependency added.
- No endpoint added.
- No OpenWebUI configuration changed.
- No Hermes configuration changed.
- No secrets added.
- No tool execution enabled.

## Open points

- Graphify may merit a future read-only sandbox test on a non-sensitive repo snapshot.
- CTX, Binderly and Layer require deeper review before classification upgrade.
- Langflow should remain a lab only unless a future policy explicitly changes that.
- OpenClaw remains blocked until full security/runtime review.

## Next action

- Review and merge PR.
- Future possible PR: add a `docs/governance/EXTERNAL_RUNTIME_REVIEW_TEMPLATE.md` to standardize C0/C1 reviews.
