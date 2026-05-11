# AI LOG ENTRY — 2026-05-11

Branch: `work/chatgpt/legacy-runtime-audit-findings`

A: ChatGPT

## Objective

Register the findings from `reports/code_audit/2026-05-11-legacy-runtime-audit.md` into the official post-pivot code audit register without modifying runtime code.

## Changes

- Updated `docs/governance/CODE_AUDIT_POST_PIVOT.md`.
- Added `reports/code_audit/2026-05-11-legacy-runtime-audit.md` as an explicit reference synthesis.
- Registered the critical `platform/api/apps/orchestra/` LangGraph central orchestrator surface.
- Registered legacy `POST /agent/run` through `platform/api/apps/agent/router.py`.
- Registered `platform/api/apps/memory/` as a memory-review refactor target because of legacy `scope=agence` terminology.
- Registered `platform/api/apps/webhooks/` and `platform/api/apps/webhooks/telegram.py` as legacy external trigger surfaces.
- Registered `platform/api/worker.v2.py`, `platform/api/core/queue.v2.py`, `platform/api/core/checkpointer.v2.py` and `platform/api/core/base_engine.py` as frozen V2 worker/runtime scaffolding.
- Added the known legacy endpoints to the hard-blocker visibility list.
- Added a follow-up instruction to extend Doctor forbidden endpoint checks in a later C3 PR.

## Files Touched

- `docs/governance/CODE_AUDIT_POST_PIVOT.md`
- `ai_logs/2026-05-11-legacy-runtime-audit-findings.md`

## Critical files impacted

- `docs/governance/CODE_AUDIT_POST_PIVOT.md`

## Tests

- Not run. Documentation-only intervention.

## Open points

- Doctor still does not block `/agent/run` or `/orchestra/*`; this must be handled in a separate PR because it changes validation behavior.
- No runtime file was modified.
- No module was disabled.
- No route was removed.
- `scope=agence` remains in legacy code and should be renamed only through a later controlled refactor.

## Next action

- Open a small PR and merge if documentation-only.
- Then open a separate Doctor PR to extend forbidden endpoint checks.
