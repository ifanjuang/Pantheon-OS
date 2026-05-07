# AI LOG ENTRY — 2026-05-07

Branch: `work/chatgpt/prompts-system-registry`

AI: ChatGPT

## Objective

Add a governed system prompt registry and verify it against recent post-pivot governance commits.

## Changes

- Added a prompt registry under `prompts/`.
- Added `prompts/system/manifest.yaml` for governed prompt routing metadata.
- Added prompt files for general, governance, Hermes, OpenWebUI, architecture_fr, software repo audit, client communication, Evidence Pack trace and memory governance use cases.
- Added `prompts/system/prompt_router.md` for safe prompt selection.
- Rebased the branch onto current `main` after detecting that the initial branch point was behind recent governance commits.
- Aligned prompt wording with `docs/governance/HERMES_EXECUTION_MODEL.md`: Hermes may supervise runtime execution internally, but Pantheon must not become the runtime.

## Files Touched

- prompts/README.md
- prompts/system/manifest.yaml
- prompts/system/general.md
- prompts/system/pantheon_next_governance.md
- prompts/system/hermes_operator.md
- prompts/system/openwebui_cockpit.md
- prompts/system/architecture_fr.md
- prompts/system/software_repo_audit.md
- prompts/system/client_communication.md
- prompts/system/evidence_pack.md
- prompts/system/memory_governance.md
- prompts/system/prompt_router.md
- ai_logs/2026-05-07-prompts-system-registry.md

## Critical files impacted

none

## Tests

- Documentation only.
- No runtime execution.
- Compared branch against current `main` before finalizing the prompt registry.

## Open points

- Runtime binding is not implemented.
- Hermes prompt loading must be verified separately using `SOUL.md` and project context files.
- OpenWebUI workspace profile alignment remains pending.
- Evidence Pack prompt is currently intentionally compact because tool-side content filtering blocked more detailed wording.

## Next action

Add a dedicated Hermes context export that references `prompts/system/manifest.yaml` and the relevant prompt files.
