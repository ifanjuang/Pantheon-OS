# AI LOG ENTRY — 2026-05-10

Branch: `work/chatgpt/agents-doc-alignment`

A: ChatGPT

## Objective

Align `AGENTS.md` with the newly merged routing, role signal and role signal profile governance.

## Changes

- Renamed the document heading from Pantheon OS to Pantheon Next.
- Added references to `ROUTING_FOUNDATION.md`, `ROLE_SIGNALS.md` and `ROLE_SIGNAL_PROFILES.md`.
- Added an explicit runtime boundary section: Hermes Agent is not a Pantheon Role.
- Removed `HERMES` from the Pantheon Role responsibility table.
- Clarified IRIS as communication and signal mediation role.
- Added role-signal consultation rules and forbidden signal behavior.
- Updated AGORA, workflow adaptation, task contract, Evidence Pack, memory, skills and Hermes sections to use role signal terminology.
- Added `rich_elicitation` and `role_signal_formatter` to relevant candidate skill references.

## Files Touched

- `docs/governance/AGENTS.md`
- `ai_logs/2026-05-10-agents-doc-alignment.md`

## Critical files impacted

- `docs/governance/AGENTS.md`

## Tests

- Not run. Documentation-only intervention.

## Open points

- `WORKFLOW_ADAPTATION.md`, `RUN_GRAPH.md` and `EVIDENCE_PACK.md` should still reference `ROLE_SIGNALS.md` explicitly in later targeted PRs.
- HEPHAESTUS spelling is normalized in this file, but a repo-wide spelling audit remains useful.

## Next action

- Open a clean PR for review and merge if accepted.
