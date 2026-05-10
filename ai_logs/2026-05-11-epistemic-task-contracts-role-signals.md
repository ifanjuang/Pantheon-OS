# AI LOG ENTRY — 2026-05-11

Branch: `work/chatgpt-epistemic-task-signals`

A: ChatGPT

## Objective

Propagate claim-level epistemic control directly into Task Contracts and Role Signals without adding runtime behavior.

## Changes

- Updated `docs/governance/TASK_CONTRACTS.md` to add `epistemic_requirements` to the generic schema and first non-PDF task contracts.
- Added a Task Contract epistemic policy section covering Claim Register, unsupported claims, contradiction handling and final answer certainty.
- Updated `docs/governance/ROLE_SIGNALS.md` to add `epistemic_payload` to base role signals, addressed signals, consultations, handoffs, vetoes and stop gates.
- Added rules preventing IRIS, AGORA or handoffs from increasing claim certainty without new evidence.
- Updated `CHANGELOG.md` under `[Unreleased]`.

## Files Touched

- `docs/governance/TASK_CONTRACTS.md`
- `docs/governance/ROLE_SIGNALS.md`
- `CHANGELOG.md`
- `ai_logs/2026-05-11-epistemic-task-contracts-role-signals.md`

## Critical files impacted

- `docs/governance/TASK_CONTRACTS.md`
- `docs/governance/ROLE_SIGNALS.md`
- `CHANGELOG.md`

## Tests

- Not run. Documentation-only change.

## Open points

- Direct propagation remains pending for `ROLE_SIGNAL_PROFILES.md`, `WORKFLOW_ADAPTATION.md`, `STATUS.md` and `ROADMAP.md`.
- No runtime, endpoint, Hermes binding, OpenWebUI action, skill activation, workflow activation or memory promotion was added.

## Next action

- Review and merge the documentation PR, then continue with IRIS profile and workflow gate propagation.
