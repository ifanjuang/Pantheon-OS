# AI LOG ENTRY — 2026-04-29

Branch: `work/chatgpt/hermes-docs-architecture-fr`

Assistant: ChatGPT

## Objective

Create the external tools governance base and complete the approval, evidence and task-contract documents with external tools, fallback/retry and remediation candidate rules.

## Changes

- Created `EXTERNAL_TOOLS_POLICY.md`.
- Extended `APPROVALS.md` with:
  - external tool action mapping;
  - PDF action mapping;
  - OpenWebUI/Hermes plugin install mapping;
  - fallback / retry / alternative execution policy;
  - remediation candidate lane policy.
- Extended `EVIDENCE_PACK.md` with:
  - minimum evidence pack;
  - extended evidence pack;
  - fallback evidence;
  - remediation evidence;
  - PDF processing evidence requirements.
- Extended `TASK_CONTRACTS.md` with:
  - `fallback_policy`;
  - `remediation_policy`;
  - updated non-PDF task contracts;
  - PDF task contracts for info, metadata, text layer, OCR, sanitize, split, merge, compress, redaction and archive preparation.

## Critical files touched

- `EXTERNAL_TOOLS_POLICY.md`
- `APPROVALS.md`
- `EVIDENCE_PACK.md`
- `TASK_CONTRACTS.md`

## Tests run

No tests were run. Documentation-only intervention.

## Points to verify

- `AI_LOG.md` still needs to be consolidated with this entry in the main log file.
- No runtime code was modified.
- No external tool was installed.
- No Stirling-PDF container was created.
- No OpenWebUI extension was installed.
- No Hermes plugin was installed.
- Licenses in `EXTERNAL_TOOLS_POLICY.md` remain marked `to_verify` or `not_checked` where applicable.
- PDF task contracts are documentary contracts only; no execution backend exists yet.

## Recommended next action

1. Consolidate this entry into `AI_LOG.md`.
2. Update `STATUS.md` to mark `EXTERNAL_TOOLS_POLICY.md` as created.
3. Create `operations/stirling_pdf.md`.
4. Create `operations/stirling_ocr.md`.
5. Create `infra/compose/docker-compose.stirling.yml` only after the policy review is accepted.
