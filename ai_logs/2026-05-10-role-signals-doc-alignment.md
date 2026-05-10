# AI LOG ENTRY — 2026-05-10

Branch: `work/claude/role-signals-doc-alignment`

A: Claude

## Objective

Align the consuming and tracing governance documents (`WORKFLOW_ADAPTATION.md`, `RUN_GRAPH.md`, `EVIDENCE_PACK.md`, `TASK_CONTRACT_REVISIONS.md`) with the recently merged `ROLE_SIGNALS.md`, `ROLE_SIGNAL_PROFILES.md` and `ROUTING_FOUNDATION.md` so that the role-signal vocabulary becomes coherent across the governance stack.

## Changes

- `docs/governance/WORKFLOW_ADAPTATION.md`
  - Added `ROLE_SIGNALS.md`, `ROLE_SIGNAL_PROFILES.md` and `ROUTING_FOUNDATION.md` to the non-negotiable boundaries list.
  - Extended the canonical vocabulary table with `role_signal`, `addressed_role_signal`, `role_consultation`, `handoff_signal`, `format_reminder_request`, `format_reminder_response`, `format_blocked` and added cross-references to the relevant governance docs.
  - Section 5 now states that workflow design consultations must be expressed as structured Role Signals; introduces format-reminder and format-blocked rules in the consultation flow.
  - Section 11 lists the additional Role Signals (`veto_signal`, `stop_gate_signal`, `risk_warning`, `source_gap_signal`, `skill_gap_signal`) that may also imply a workflow revision; explicit reference to `task_contract_revision`.
  - Section 17 (Evidence requirements) explicitly references role signal artifacts and points to `EVIDENCE_PACK.md` for canonical fields.
- `docs/governance/RUN_GRAPH.md`
  - Added section 10b (Role Signal visibility) clarifying that Role Signals appear only as public summaries, with explicit allowed/forbidden surface forms and display constraints (no raw chain-of-thought, no secrets, no source dumps, no private file paths, no internal Hermes tool transcripts).
  - Added a reference flow pointer (ROLE_SIGNALS, ROLE_SIGNAL_PROFILES, EVIDENCE_PACK, TASK_CONTRACT_REVISIONS).
- `docs/governance/EVIDENCE_PACK.md`
  - Added section 6b (Role signal traceability) with required-when-relevant fields for `role_signals`, `addressed_role_signals`, `role_consultations`, `format_reminder_request`, `format_reminder_response`, `format_blocked`, `handoff_signals`, `veto_signal`, `stop_gate_signal`, `workflow_revision_signal`.
  - Added the `role_signal_traceability` shape and explicit rules forbidding raw chain-of-thought and softened risk levels in evidence.
- `docs/governance/TASK_CONTRACT_REVISIONS.md`
  - Added `ROLE_SIGNALS.md`, `ROLE_SIGNAL_PROFILES.md` and `ROUTING_FOUNDATION.md` to the addendum cross-reference list.
  - Added section 4b (Role Signal triggers for revision) listing which signals can trigger pause, escalation, reroute, reset-to-baseline or stop_and_report, and reaffirming THEMIS veto and APOLLO stop gate authority.
  - Section 9 (Evidence requirements) now references the new `role_signal_traceability` fields from `EVIDENCE_PACK.md`.
- `docs/governance/STATUS.md`
  - Added rows for `ROUTING_FOUNDATION.md`, `ROLE_SIGNALS.md`, `ROLE_SIGNAL_PROFILES.md` to the documentation status table.
  - Listed the same files in the reliable documentation block (section 4.1).
- `docs/governance/ROADMAP.md`
  - Added `ROUTING_FOUNDATION.md`, `ROLE_SIGNALS.md`, `ROLE_SIGNAL_PROFILES.md`, `RUN_GRAPH.md` to the core files list and to the target repository anatomy.

## Files Touched

- docs/governance/WORKFLOW_ADAPTATION.md
- docs/governance/RUN_GRAPH.md
- docs/governance/EVIDENCE_PACK.md
- docs/governance/TASK_CONTRACT_REVISIONS.md
- docs/governance/STATUS.md
- docs/governance/ROADMAP.md
- ai_logs/2026-05-10-role-signals-doc-alignment.md

## Critical files impacted

- docs/governance/STATUS.md
- docs/governance/ROADMAP.md
- docs/governance/EVIDENCE_PACK.md

## Tests

- not run (Markdown-only changes)

## Open points

- `RUN_GRAPH.md` was not previously listed in `ROADMAP.md` core files; added in this PR for consistency. This is documentation alignment, not new doctrine.
- HEPHAISTOS / HEPHAESTUS spelling reconciliation is still open across governance docs (per `STATUS.md`); both spellings are kept in this alignment PR to avoid mixing scopes.
- No runtime, scheduler, message bus, agent loop, endpoint or skill activation introduced.

## Next action

- Run the smallest-safe-path Doctor / lint pass once Bloc 2 (CI/lint/tests repair) is opened.
- Consider Bloc 4 (governance schema validators) so that `role_signal`, `addressed_role_signal`, `format_reminder_request`, `format_blocked` and the new Evidence Pack `role_signal_traceability` block can be statically validated.
