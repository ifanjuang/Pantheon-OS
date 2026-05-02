# AI LOG ENTRY — 2026-05-02

Branch: `work/chatgpt/knowledge-registry-example`

A: ChatGPT

## Objective

Create a first `knowledge/registry.example.yaml` to map OpenWebUI Knowledge Bases to Pantheon domains, source tiers, privacy levels, freshness policy and Evidence Pack requirements.

## Changes

- Added `knowledge/registry.example.yaml`.
- Defined registry-level rules:
  - Knowledge is source material, not memory.
  - Memory promotion remains candidate-only until Evidence Pack + C3 review.
  - Unknown sources are blocked until reviewed.
  - Cross-project use is forbidden without explicit trace.
- Defined source tiers T0-T5, reliability levels R0-R5, privacy levels and freshness policies.
- Added generic example collections for:
  - Pantheon governance;
  - approvals;
  - task contracts;
  - Evidence Pack policy;
  - architecture_fr CCTP / DPGF / contract clauses / notices / SDIS-ERP / PLU / site reports;
  - software repo docs;
  - code audit post pivot;
  - API contract docs.
- Added a project collection template using anonymized placeholder names only.

## Files Touched

- `knowledge/registry.example.yaml`
- `ai_logs/2026-05-02-knowledge-registry-example.md`

## Critical files impacted

- none

## Tests

- Not run. Documentation/config example only.

## Guardrails

- No code changed.
- No runtime behavior changed.
- No endpoint added.
- No OpenWebUI sync implemented.
- No private project/client data added.
- No memory promotion implemented.

## Open points

- The example registry has not been validated against a live OpenWebUI instance.
- No Knowledge Selection candidate skill has been created yet.
- `STATUS.md` and `ROADMAP.md` may be synchronized after merge to mark this example as added.

## Next action

- Review and merge PR.
- Then create a Knowledge Selection candidate skill or synchronize STATUS/ROADMAP.
