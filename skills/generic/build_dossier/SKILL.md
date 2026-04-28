# Build Dossier

## Purpose

Assemble structured deliverable packages from validated content: regulatory files, consultation files, closure files, contractual reports. Verify completeness, cross-references, and recipient-specific requirements before delivery.

## Inputs

- `summary` (text) — synthesized analysis from upstream
- `facts` (list) — validated facts to include
- `citations` (list) — source references for each fact
- `dossier_type` (string) — type of file (regulatory / consultation / closure / report)
- `recipient` (string) — final recipient (authority / client / partner)

## Outputs

- `dossier` (structured object) — assembled file with sections, pieces, and metadata

## Required agents

- `@Daedalus` — file architecture and assembly
- `@Kairos` — final synthesis injected into the dossier

## Activation conditions

- A formal deliverable is requested (not a chat answer)
- Criticality ≥ C3 and the output crosses an organizational boundary
- Triggered explicitly via workflow `dossier_build` or by Zeus on engaging decisions

## Rules

- Mark every required piece with status: ✅ present / ⚠️ to verify / ❌ missing / 📋 to request
- Never ship a dossier with `[TO BE FILLED]` without explicitly flagging it to the user
- Always specify the final recipient — requirements vary by authority/client
- Verify cross-references (figures, dates, names) for internal consistency

## Risks

- Submission rejection due to a missing piece silently passed through
- Recipient mismatch (regulatory format used for client, or vice-versa)
- Stale content if upstream facts were updated after dossier was built
