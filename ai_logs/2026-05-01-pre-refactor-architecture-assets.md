# AI LOG ENTRY — 2026-05-01

Branch: `work/chatgpt/pre-refactor-architecture-assets`

A: ChatGPT

## Objective

Record useful existing repository assets before refactor and align governance docs with the Pantheon Next architecture.

## Changes

- Added `PRE_REFACTOR_ARCHITECTURE_FINDINGS.md` to classify useful code assets to preserve or reclassify.
- Added `WORKFLOW_SCHEMA.md` for governed workflow/task definitions.
- Added `SKILL_LIFECYCLE.md` for skill states, XP, Hermes mapping and candidate-first lifecycle.
- Added `MEMORY_EVENT_SCHEMA.md` for memory events, candidates and supersession.
- Added `domains/architecture_fr/knowledge_policy.md` with trusted source tiers and fetch-before-cite rule.
- Updated `.env.example` to use `DOMAIN=architecture_fr`.
- Rewrote `CLAUDE.md` to align Claude Code guidance with Pantheon Next and remove autonomous-runtime assumptions.
- Updated `docs/governance/README.md` to index the new governance documents.
- Updated `docs/governance/CODE_AUDIT_POST_PIVOT.md` with current keep/reorient/legacy classifications.
- Updated `docs/governance/MEMORY.md` to reference `MEMORY_EVENT_SCHEMA.md` and supersession fields.

## Files Touched

- `docs/governance/PRE_REFACTOR_ARCHITECTURE_FINDINGS.md`
- `docs/governance/WORKFLOW_SCHEMA.md`
- `docs/governance/SKILL_LIFECYCLE.md`
- `docs/governance/MEMORY_EVENT_SCHEMA.md`
- `domains/architecture_fr/knowledge_policy.md`
- `.env.example`
- `CLAUDE.md`
- `docs/governance/README.md`
- `docs/governance/CODE_AUDIT_POST_PIVOT.md`
- `docs/governance/MEMORY.md`
- `ai_logs/2026-05-01-pre-refactor-architecture-assets.md`

## Critical files impacted

- `CLAUDE.md`
- `docs/governance/README.md`
- `docs/governance/CODE_AUDIT_POST_PIVOT.md`
- `docs/governance/MEMORY.md`
- `.env.example`

## Tests

- Not run. Documentation and configuration-convention changes only.

## Open points

- `platform/api/pantheon_domain/repository.py` still contains legacy terminology such as `agency_memory` and `generic`; code cleanup should happen after this documentation PR is reviewed.
- `platform/api/pantheon_runtime/` remains named as runtime even though it is now documented as context export only.
- `docker-compose.yml` still reflects the legacy MVP wiring where OpenWebUI points to Pantheon `/v1`; final target should be OpenWebUI → Hermes Gateway.
- `ROADMAP.md`, `ARCHITECTURE.md` and `MODULES.md` may receive a second pass after this PR if more explicit references to the new files are desired.

## Next action

- Review and merge this documentation PR.
- Then open a targeted cleanup PR for terminology and low-risk code/document consistency fixes: `agency_memory` → `system_memory`, `generic` → `general`, and context-export naming guardrails.
