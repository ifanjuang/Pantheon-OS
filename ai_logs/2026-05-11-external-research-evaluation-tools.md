# AI LOG ENTRY — 2026-05-11

Branch: `work/chatgpt/external-research-evaluation-tools`

A: ChatGPT

## Objective

Classify recent external research, discovery, markdown retrieval and browser-agent evaluation tools without integrating them into Pantheon core.

## Changes

- Updated `docs/governance/EXTERNAL_ECOSYSTEM_REVIEWS.md`.
- Added review states for `untrusted_discovery_only`, `evaluation_candidate` and `documentation_retrieval_candidate`.
- Classified `hermesguide.xyz/directory` as untrusted discovery only.
- Classified `PrinceGabriel-lgtm/freshcontext-mcp` as Hermes Lab only / blocked for core.
- Classified `lightfeed/resurf` as an evaluation candidate / Hermes Lab only / to verify.
- Classified `Dreeseaw/mdlens` as a documentation retrieval candidate / local developer tool candidate.
- Added candidate roadmap actions for markdown retrieval and browser-agent benchmark review.

## Files Touched

- `docs/governance/EXTERNAL_ECOSYSTEM_REVIEWS.md`
- `ai_logs/2026-05-11-external-research-evaluation-tools.md`

## Critical files impacted

- none

## Tests

- Not run. Documentation-only intervention.

## Open points

- Primary GitHub READMEs for `lightfeed/resurf` and `Dreeseaw/mdlens` should be reviewed directly before any installation or sandbox experiment.
- `hermesguide.xyz` should not be used for install commands, authentication, secrets or source-of-truth claims.
- `freshcontext-mcp` remains blocked for core and should only be tested with non-sensitive data under Task Contract.

## Next action

- Open a small PR and merge only if it remains documentation-only.
