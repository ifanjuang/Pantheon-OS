# AI LOG ENTRY — 2026-05-02

Branch: `work/chatgpt/legacy-wiring-context-export`

A: ChatGPT

## Objective

Mark the remaining legacy MVP deployment wiring and context-export boundary before the next Pantheon Next refactor.

## Changes

- Updated `docker-compose.yml` comments to mark the file as legacy MVP wiring.
- Clarified that OpenWebUI currently points to Pantheon `/v1` only in the legacy compose.
- Clarified that the target wiring is OpenWebUI → Hermes Agent Gateway → Pantheon Context Pack / Domain API.
- Clarified that the shared PostgreSQL database in the compose is legacy and should be split later.
- Updated `platform/api/main.py` labels from Pantheon OS to Pantheon Next.
- Clarified in `platform/api/main.py` that the API is a governance/context API, not the final OpenAI-compatible backend.
- Updated `platform/api/pantheon_runtime/router.py` to mark it as read-only context export, not runtime execution.
- Changed the router tag from `pantheon-runtime` to `context-export`.
- Updated `docs/governance/CODE_AUDIT_POST_PIVOT.md` with current terminology and deployment-boundary status.

## Files Touched

- `docker-compose.yml`
- `platform/api/main.py`
- `platform/api/pantheon_runtime/router.py`
- `docs/governance/CODE_AUDIT_POST_PIVOT.md`
- `ai_logs/2026-05-02-legacy-wiring-context-export.md`

## Critical files impacted

- `docker-compose.yml`
- `platform/api/main.py`
- `platform/api/pantheon_runtime/router.py`
- `docs/governance/CODE_AUDIT_POST_PIVOT.md`

## Tests

- Not run. Documentation/comments/OpenAPI-label cleanup only.

## Open points

- `docker-compose.yml` remains functionally legacy and still points OpenWebUI to `api:8000/v1`; this is intentionally documented, not refactored.
- `platform/api/pantheon_runtime/` package name remains unchanged for compatibility, but it is documented as context export only.
- Future deployment refactor should introduce separate OpenWebUI, Hermes Gateway and Pantheon Domain API stacks/databases.

## Next action

- Review and merge the PR if the context-export and legacy-wiring wording is accepted.
- Then proceed to a targeted refactor plan for deployment split and context export package naming.
