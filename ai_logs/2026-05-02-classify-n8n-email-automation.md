# AI LOG ENTRY — 2026-05-02

Branch: `work/chatgpt/classify-n8n-email-automation`

A: ChatGPT

## Objective

Classify n8n as an external email/event automation orchestrator and add an operations note for safe future email-triggered workflows.

## Changes

- Updated `docs/governance/EXTERNAL_TOOLS_POLICY.md`.
- Added `operations/n8n_email_automation.md`.
- Added n8n to the external tools watchlist and approval mapping.
- Classified n8n as `test` / local sandbox first / external automation orchestrator.
- Defined allowed first use cases:
  - email received -> operator notification;
  - email with attachment -> controlled folder copy;
  - email -> candidate task note;
  - approved future handoff -> Hermes under Task Contract.
- Defined forbidden uses:
  - no automatic external replies;
  - no automatic memory promotion;
  - no automatic Knowledge ingestion;
  - no direct Hermes execution without Task Contract;
  - no direct Markdown mutation;
  - no secrets in repo;
  - no public exposure without review.

## Files Touched

- `docs/governance/EXTERNAL_TOOLS_POLICY.md`
- `operations/n8n_email_automation.md`
- `ai_logs/2026-05-02-classify-n8n-email-automation.md`

## Critical files impacted

- `docs/governance/EXTERNAL_TOOLS_POLICY.md`

## Tests

- Not run. Documentation only.

## Guardrails

- No code changed.
- No runtime behavior changed.
- No n8n installation.
- No connector configured.
- No secrets added.
- No workflow created.
- No email data added.
- No private project/client data added.

## Open points

- First test mailbox/label remains to define.
- Controlled NAS folder for attachments remains to define.
- Email-triggered Task Contract candidate format remains to define.
- n8n install procedure remains out of scope until approval.

## Next action

- Review and merge PR.
- Then create a first workflow specification for `email_received -> operator notification` before any n8n install.
