# AI LOG ENTRY — 2026-05-11

Branch: `work/chatgpt-claim-register-epistemic-contracts`

A: ChatGPT

## Objective

Add doctrine for claim-level evidence, uncertainty propagation and epistemic contracts across Pantheon Roles, Hermes skills, Task Contracts and Evidence Packs.

## Changes

- Added `docs/governance/EPISTEMIC_CONTROL.md`.
- Defined Claim Register doctrine for material assertions.
- Defined `epistemic_payload` for Role Signals.
- Defined `epistemic_contract` for skill manifests.
- Defined `epistemic_requirements` for Task Contracts.
- Defined Source Gate, Uncertainty Gate, Risk Gate and Final Claim Gate.
- Updated `docs/governance/README.md` inventory.
- Updated `CHANGELOG.md` under `[Unreleased]`.

## Files Touched

- `docs/governance/EPISTEMIC_CONTROL.md`
- `docs/governance/README.md`
- `CHANGELOG.md`
- `ai_logs/2026-05-11-epistemic-control-claim-register.md`

## Critical files impacted

- `docs/governance/README.md`
- `CHANGELOG.md`
- New governance document: `docs/governance/EPISTEMIC_CONTROL.md`

## Tests

- Not run. Documentation-only change.

## Open points

- `EVIDENCE_PACK.md`, `TASK_CONTRACTS.md`, `ROLE_SIGNALS.md`, `ROLE_SIGNAL_PROFILES.md`, `SKILL_LIFECYCLE.md` and `WORKFLOW_ADAPTATION.md` should later be updated to reference `EPISTEMIC_CONTROL.md` directly.
- `STATUS.md` and `ROADMAP.md` should be synchronized in a follow-up if this doctrine is accepted.
- No runtime, endpoint, skill activation, memory promotion or Hermes binding was added.

## Next action

- Review the doctrine, then decide whether to propagate short references into the existing governance schemas or keep `EPISTEMIC_CONTROL.md` as the single doctrine source first.
