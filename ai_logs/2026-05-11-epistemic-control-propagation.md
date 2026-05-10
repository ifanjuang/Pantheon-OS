# AI LOG ENTRY — 2026-05-11

Branch: `work/chatgpt-epistemic-control-propagation`

A: ChatGPT

## Objective

Propagate the new claim-level epistemic control doctrine into existing governance references without adding runtime behavior.

## Changes

- Updated `docs/governance/EVIDENCE_PACK.md` to include Claim Register, epistemic summary and certainty discipline inside Evidence Packs.
- Updated `docs/governance/SKILL_LIFECYCLE.md` to reference skill `epistemic_contract` blocks in manifests.
- Added `docs/governance/EPISTEMIC_CONTROL_PROPAGATION.md` as an adoption map for applying `EPISTEMIC_CONTROL.md` across governance documents.
- Updated `docs/governance/README.md` inventory.
- Updated `CHANGELOG.md` under `[Unreleased]`.

## Files Touched

- `docs/governance/EVIDENCE_PACK.md`
- `docs/governance/SKILL_LIFECYCLE.md`
- `docs/governance/EPISTEMIC_CONTROL_PROPAGATION.md`
- `docs/governance/README.md`
- `CHANGELOG.md`
- `ai_logs/2026-05-11-epistemic-control-propagation.md`

## Critical files impacted

- `docs/governance/EVIDENCE_PACK.md`
- `docs/governance/SKILL_LIFECYCLE.md`
- `docs/governance/README.md`
- `CHANGELOG.md`
- New governance document: `docs/governance/EPISTEMIC_CONTROL_PROPAGATION.md`

## Tests

- Not run. Documentation-only change.

## Open points

- Direct edits to `TASK_CONTRACTS.md`, `ROLE_SIGNALS.md`, `ROLE_SIGNAL_PROFILES.md`, `WORKFLOW_ADAPTATION.md`, `STATUS.md` and `ROADMAP.md` remain pending.
- `EPISTEMIC_CONTROL_PROPAGATION.md` records the adoption map and explicitly marks those items as pending where not directly edited.
- No runtime, endpoint, Hermes binding, OpenWebUI action, skill activation, workflow activation or memory promotion was added.

## Next action

- Review and merge the documentation propagation PR, then continue with direct references in Task Contracts and Role Signals.
