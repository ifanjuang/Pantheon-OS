# AI LOG ENTRY — 2026-05-10

Branch: `work/chatgpt/role-signals-consultation`

A: ChatGPT

## Objective

Make inter-role consultation an explicit governed capability by adding structured role signals, IRIS signal mediation, recipient profiles and format reminder rules.

## Changes

- Added `docs/governance/ROLE_SIGNALS.md`.
- Added `docs/governance/ROLE_SIGNAL_PROFILES.md`.
- Indexed `ROLE_SIGNALS.md` in `docs/governance/README.md`.
- Defined role signals, addressed role signals, role consultations, information transmission, risk/veto signals, stop gate signals, workflow revision signals, handoff signals and AGORA relationship.
- Clarified that roles may consult other roles through bounded structured signals, not free-form hidden debate.
- Defined IRIS as a signal mediator/formatter, not a runtime message bus.
- Added recipient profiles per Pantheon role, so IRIS can format messages according to the addressed role.
- Added `format_reminder_request`, `format_reminder_response` and `format_blocked` rules.
- Added `domains/general/skills/role_signal_formatter/` as a candidate skill.

## Files Touched

- `docs/governance/ROLE_SIGNALS.md`
- `docs/governance/ROLE_SIGNAL_PROFILES.md`
- `docs/governance/README.md`
- `domains/general/skills/role_signal_formatter/SKILL.md`
- `domains/general/skills/role_signal_formatter/manifest.yaml`
- `domains/general/skills/role_signal_formatter/examples.md`
- `domains/general/skills/role_signal_formatter/tests.md`
- `domains/general/skills/role_signal_formatter/UPDATES.md`
- `ai_logs/2026-05-10-role-signals-consultation.md`

## Critical files impacted

- `docs/governance/README.md`

## Tests

- Not run. Documentation-only intervention.

## Open points

- `AGENTS.md` should later reference `ROLE_SIGNALS.md` and `ROLE_SIGNAL_PROFILES.md` directly.
- `AGENTS.md` should later clarify IRIS as signal mediator and remove any ambiguity around Hermes as a Pantheon Role.
- `WORKFLOW_ADAPTATION.md` may later reuse the `role_signal` schema instead of embedding similar structures.
- `RUN_GRAPH.md` may later reference `role_signal` as event input.
- `EVIDENCE_PACK.md` may later include role signal trace fields explicitly.
- `ROLE_SIGNAL_PROFILES.md` was not indexed in `docs/governance/README.md` because the connector blocked the large README replacement; this should be retried in a small targeted patch or a later PR.
- No runtime message bus was implemented.
- No Hermes skill was activated.

## Next action

- Review and merge PR #127 if accepted, then open a targeted PR to align `AGENTS.md`, `WORKFLOW_ADAPTATION.md`, `RUN_GRAPH.md` and `EVIDENCE_PACK.md`.
