# AI LOG ENTRY — 2026-05-11

Branch: `work/chatgpt-local-role-signal-profiles`

A: ChatGPT

## Objective

Document the hybrid Role Signal Profile model: central protocol and invariants in governance documents, local per-agent usage profiles under `agents/{ROLE}/role_signal_profile.yaml`.

## Changes

- Updated `docs/governance/ROLE_SIGNAL_PROFILES.md` with detailed local profile doctrine, lifecycle, minimal schema, profile resolution order, allowed refinements and forbidden authority expansion.
- Updated `docs/governance/AGENTS.md` to define local agent files and Role Signal Profile rules.
- Added `agents/README.md` as the maintenance guide for local role profile files.
- Updated `docs/governance/EPISTEMIC_CONTROL_PROPAGATION.md` to mark Role Signal Profile adoption as started and mention local profiles.
- Updated `docs/governance/README.md` to index local agent profile policy.
- Updated `CHANGELOG.md` under `[Unreleased]`.

## Files Touched

- `docs/governance/ROLE_SIGNAL_PROFILES.md`
- `docs/governance/AGENTS.md`
- `agents/README.md`
- `docs/governance/EPISTEMIC_CONTROL_PROPAGATION.md`
- `docs/governance/README.md`
- `CHANGELOG.md`
- `ai_logs/2026-05-11-local-role-signal-profiles.md`

## Critical files impacted

- `docs/governance/ROLE_SIGNAL_PROFILES.md`
- `docs/governance/AGENTS.md`
- `docs/governance/EPISTEMIC_CONTROL_PROPAGATION.md`
- `docs/governance/README.md`
- `CHANGELOG.md`

## Tests

- Not run. Documentation-only change.

## Open points

- No actual per-agent `agents/{ROLE}/role_signal_profile.yaml` files were created yet.
- Direct propagation remains pending for `WORKFLOW_ADAPTATION.md`, `STATUS.md` and `ROADMAP.md`.
- No runtime, endpoint, Hermes binding, OpenWebUI action, skill activation, workflow activation or memory promotion was added.

## Next action

- Review and merge the documentation PR, then create first local profiles only after confirming final agent folder naming and casing convention.
