# 2026-05-06 — Hermes execution model

## Summary

Consolidated the governance doctrine for Hermes-backed execution.

Confirmed the architectural separation:

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

Added a dedicated execution model document clarifying:

- runtime boundaries;
- declarative cognitive agents;
- subagent execution model;
- approval interrupts;
- Evidence Pack responsibilities;
- LangGraph scope limitations;
- prohibited runtime patterns.

## Files

- docs/governance/HERMES_EXECUTION_MODEL.md
- docs/governance/README.md

## Decisions

- Pantheon remains governance-only.
- Hermes remains the only execution runtime.
- OpenWebUI remains a cockpit and validation layer.
- LangGraph is allowed only inside Hermes.
- Automatic canonical memory promotion is prohibited.

## Risks

- Legacy runtime code still requires audit.
- OpenWebUI plugins remain a potential governance drift vector.
- Future workflow orchestration must remain Hermes-scoped.

## Status

Documentation-only intervention.
No runtime mutation.
No infrastructure mutation.
