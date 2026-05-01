# ROADMAP — Pantheon OS

> Post-pivot roadmap.
> Pantheon OS is a Hermes-backed Domain Operating Layer: Pantheon defines and governs, Hermes Agent executes, OpenWebUI exposes the interface and Knowledge Bases.

---

# 1. Core doctrine

```text
Pantheon defines and governs.
Hermes executes.
OpenWebUI exposes.
Stirling processes PDFs.
External plugins remain under allowlist.
Validated memory remains Pantheon.
Fallbacks and patch candidates never bypass policy.
```

Pantheon OS must not become a full autonomous agent runtime.

Its value is to define:

- governance;
- agents;
- task contracts;
- approval levels;
- evidence requirements;
- domain packages;
- skills;
- workflows;
- memory policy;
- Knowledge taxonomy;
- external tool policy.

---

# 2. Source-of-truth documents

Reference Markdown files drive development:

```text
README.md
ARCHITECTURE.md
AGENTS.md
MODULES.md
MEMORY.md
ROADMAP.md
STATUS.md
APPROVALS.md
TASK_CONTRACTS.md
EVIDENCE_PACK.md
HERMES_INTEGRATION.md
KNOWLEDGE_TAXONOMY.md
ai_logs/README.md
```

Rules:

- documentation before code;
- no direct push to `main`;
- no autonomous Pantheon runtime revival;
- no real private project/client data in repository examples;
- `architecture_fr` is the only French architecture domain name;
- use `system memory`, not `agency memory`;
- use `domains/general`, not `skills/generic` or `workflows/generic`;
- use `domains/architecture_fr`, not `domains/architecture`.

---

# 3. Target repository anatomy

```text
Pantheon-OS/
  README.md
  STATUS.md
  ROADMAP.md
  ARCHITECTURE.md
  AGENTS.md
  MODULES.md
  MEMORY.md
  APPROVALS.md
  TASK_CONTRACTS.md
  EVIDENCE_PACK.md
  HERMES_INTEGRATION.md
  KNOWLEDGE_TAXONOMY.md
  EXTERNAL_TOOLS_POLICY.md
  ai_logs/README.md

  agents/

  domains/
    general/
      domain.md
      rules.md
      knowledge_policy.md
      output_formats.md
      skills/
      workflows/
      templates/
    architecture_fr/
      domain.md
      rules.md
      knowledge_policy.md
      output_formats.md
      skills/
      workflows/
      templates/
    software/
      domain.md
      rules.md
      knowledge_policy.md
      output_formats.md
      skills/
      workflows/
      templates/

  memory/
    session/
    candidates/
    project/
    system/

  knowledge/
    registry.yaml
    source_tiers.md
    freshness_policy.md
    openwebui_collections.md

  hermes/
    context/
    templates/

  operations/
  infra/
    compose/
  conventions/
```

Deprecated paths must not be recreated except as explicit legacy references:

```text
domains/architecture
skills/architecture
workflows/architecture
skills/generic
workflows/generic
memory/agency
```

---

# 4. P0 — Governance base

Status: mostly completed, with external-tool governance still to create.

Completed:

- `APPROVALS.md` — C0-C5 criticality and approval policy.
- `TASK_CONTRACTS.md` — executable task contract schema and first contracts.
- `EVIDENCE_PACK.md` — mandatory proof package schema.
- `HERMES_INTEGRATION.md` — Hermes/Pantheon/OpenWebUI boundary.
- `KNOWLEDGE_TAXONOMY.md` — Knowledge layers, reliability levels and source tiers.
- `operations/openwebui_hermes_pantheon.md` — three-system operating protocol.
- static `GET /runtime/context-pack` endpoint.
- local Hermes `pantheon-os` template under `hermes/templates/pantheon-os/`.
- candidate skill `domains/general/skills/adaptive_orchestration/`.
- candidate skill `domains/general/skills/project_context_resolution/`.

Still required in P0:

1. Create `EXTERNAL_TOOLS_POLICY.md`.
2. Complete `APPROVALS.md` with external tools, fallback and remediation rules.
3. Complete `EVIDENCE_PACK.md` with extended schema, fallbacks and remediation fields.
4. Complete `TASK_CONTRACTS.md` with PDF contracts, `fallback_policy` and `remediation_policy`.
5. Create `OPENWEBUI_EXTENSIONS_POLICY.md`.
6. Create `HERMES_PLUGIN_POLICY.md`.

---

# 5. P0 — External tools governance

## 5.1 `EXTERNAL_TOOLS_POLICY.md`

Purpose:

```text
No external service, plugin, skill pack, framework or automation layer may be adopted without policy classification.
```

Initial tools to classify:

```text
Stirling-PDF
OpenWebUI extensions
Hermes plugins
Hermes community skills
GBrain
BrainAPI2
AgentScope
Hermes self-evolution
OCRmyPDF
Gotenberg
qpdf
```

Required fields:

```text
tool_name
repository
license
license_status
type
status
maturity
data_classification
local_only
network_exposure
auth_required
sandbox_required
file_access
network_access
memory_access
secrets_access
shell_access
side_effects
approval_level
allowed_usage
forbidden_usage
rollback_plan
review_frequency
last_reviewed
default_decision
```

Allowed statuses:

```text
allowed
test
blocked
rejected
watch
```

## 5.2 Fallback / retry / alternative execution

Rule:

```text
A fallback cannot bypass approval, allowlist, privacy, memory policy or tool policy.
```

Any failed, blocked or postponed action may propose an alternative only if:

- original intent is unchanged;
- fallback method is declared;
- risk level is equal or lower, or approval is requested;
- Evidence Pack records the failed attempt;
- unallowlisted tools are not used silently.

## 5.3 Remediation Candidate Lane

Rule:

```text
A detected issue may produce a patch candidate, but not an automatic fix.
```

A remediation lane may:

- analyze the issue;
- identify the affected component;
- propose a fix;
- prepare a patch candidate;
- generate an Evidence Pack.

It must not:

- apply the fix automatically;
- bypass approval;
- bypass allowlist;
- mutate memory, workflows, skills, policies or runtime configuration without approval.

---

# 6. P1 — Stirling-PDF as first external service

Purpose:

```text
Use Stirling-PDF as a governed external PDF service.
Pantheon does not recode PDF tools.
Hermes may call Stirling only inside policy and task contract.
```

Create:

```text
operations/stirling_pdf.md
operations/stirling_ocr.md
infra/compose/docker-compose.stirling.yml
hermes/context/stirling_pdf_context.md
```

Optional, if a separate policy is needed:

```text
STIRLING_PDF_POLICY.md
```

Rules:

- Stirling-PDF is an external governed service.
- Always work on a copy.
- Never overwrite the source PDF.
- Never commit real documents to the Pantheon repository.
- Do not expose Stirling publicly without auth and reverse-proxy policy.
- Redaction, sanitization and Knowledge export require approval.
- OpenWebUI receives only prepared documents.

## 6.1 PDF task contracts

Complete `TASK_CONTRACTS.md` with:

```text
pdf_info_check
pdf_metadata_check
pdf_text_layer_check
pdf_scanned_document_detect
pdf_ocr_prepare
pdf_sanitize_before_knowledge
pdf_split_project_documents
pdf_merge_export_bundle
pdf_compress_for_email
pdf_redaction_review
pdf_archive_prepare
```

Each PDF task contract must include:

```text
fallback_policy
remediation_policy
evidence_required
source_pdf_never_overwritten
```

## 6.2 PDF skills

Create under corrected paths:

```text
domains/general/skills/pdf_metadata_check/
domains/general/skills/pdf_text_layer_check/
domains/general/skills/pdf_ocr_prepare/
domains/general/skills/pdf_sanitize_check/
domains/general/skills/pdf_pipeline_design/
domains/architecture_fr/skills/pdf_project_document_prepare/
```

Priority:

1. `pdf_metadata_check`
2. `pdf_text_layer_check`
3. `pdf_ocr_prepare`
4. `pdf_sanitize_check`
5. `pdf_project_document_prepare`
6. `pdf_pipeline_design`

Each skill must contain:

```text
SKILL.md
manifest.yaml
examples.md
tests.md
UPDATES.md
```

Initial lifecycle:

```yaml
lifecycle:
  state: candidate
  level: 0
  xp:
    validated: 0
    pending: 0
```

## 6.3 PDF workflows

Create:

```text
domains/general/workflows/pdf_ocr_prepare.yaml
domains/general/workflows/pdf_sanitize_before_knowledge.yaml
domains/general/workflows/pdf_pipeline_review.yaml
domains/architecture_fr/workflows/cctp_pdf_ingestion_prepare.yaml
domains/architecture_fr/workflows/project_pdf_prepare.yaml
```

First priority workflow:

```text
domains/architecture_fr/workflows/cctp_pdf_ingestion_prepare.yaml
```

Steps:

1. Identify PDF.
2. Classify document type: CCTP, quote, DPGF, notice, DOE, letter, administrative file.
3. Read metadata, page count, size, author and producer.
4. Detect usable text layer or scan.
5. Apply privacy check.
6. OCR if required.
7. Sanitize or redact if required.
8. Compress working copy if useful.
9. Generate Evidence Pack.
10. Ask approval before OpenWebUI Knowledge ingestion.

---

# 7. P1 — OpenWebUI extensions under allowlist

Create:

```text
OPENWEBUI_INTEGRATION.md
OPENWEBUI_EXTENSIONS_POLICY.md
hermes/context/openwebui_context.md
```

Rules:

```text
OpenWebUI = interface + document Knowledge.
OpenWebUI skills are not Pantheon skills.
OpenWebUI memory is not Pantheon memory.
OpenWebUI plugins are not Pantheon governance.
Pantheon remains the source of truth.
Hermes remains the operational runtime.
```

Install extensions one by one only after policy review.

Allowed first candidates:

```text
Markdown Normalizer
Export to Word
Export to Excel
Smart Mind Map
Smart Infographic
```

Test before regular use:

```text
Async Context Compression
Context Enhancement Filter
Folder Memory
OpenWebUI Skills Manager Tool
Web Gemini Multimodal Filter
```

Blocked by default:

```text
GitHub Copilot SDK Pipe
Batch Install Plugins from GitHub
```

Create skills:

```text
domains/general/skills/markdown_quality_check/
domains/general/skills/context_compression_check/
domains/general/skills/export_quality_check/
domains/general/skills/openwebui_plugin_review/
```

Priority:

1. `markdown_quality_check`
2. `openwebui_plugin_review`
3. `export_quality_check`
4. `context_compression_check`

---

# 8. P1 — Skill system inspired by GBrain

Create:

```text
SKILL_RESOLVER.md
```

Fields:

```text
Intent
Trigger phrases
Domain
Skill id
Priority
Required agents
Approval level
Fallback skill
```

Example route targets:

```text
domains/architecture_fr/skills/quote_vs_cctp_consistency
domains/general/skills/pdf_ocr_prepare
domains/general/skills/markdown_quality_check
domains/software/skills/repo_md_audit
```

Create global conventions:

```text
conventions/quality.md
conventions/pantheon-first.md
conventions/source-attribution.md
conventions/test-before-bulk.md
conventions/privacy.md
conventions/approval.md
```

Create:

```text
SKILL_LIFECYCLE.md
```

Skill lifecycle:

```text
error / repetition
→ skill draft
→ manifest
→ examples
→ tests
→ resolver entry
→ THEMIS/APOLLO review
→ candidate
→ active
→ evolution candidate only
```

Create skills:

```text
domains/general/skills/skill_creator/
domains/general/skills/skill_candidate_check/
domains/general/skills/skill_deduplication_check/
domains/general/skills/skillpack_check/
```

Create workflows:

```text
domains/general/workflows/skillify_review.yaml
domains/software/workflows/skillpack_check.yaml
```

---

# 9. P1/P2 — Structured memory

Create:

```text
MEMORY_EVENT_SCHEMA.md
```

Model:

```text
Actor → Action/Event → Target → Context
```

Fields:

```text
id
type
actor
action
target
context
date
source
source_excerpt
confidence
validation_status
related_project
related_domain
evidence_pack_id
relationships
conflicts
supersedes
```

Initial event types:

```text
client_request
company_quote
site_observation
contractual_warning
design_decision
approval_decision
document_received
document_sent
regulatory_constraint
payment_event
delay_event
nonconformity
scope_change
quote_revision
site_instruction
safety_notice
permit_event
commission_feedback
technical_reserve
contract_amendment
invoice_dispute
reception_reserve
insurance_risk
```

Create skills:

```text
domains/general/skills/memory_event_extraction/
domains/general/skills/memory_event_validation/
domains/general/skills/memory_deduplication_check/
domains/general/skills/provenance_trace_check/
domains/general/skills/relationship_conflict_check/
```

Create workflows:

```text
domains/general/workflows/memory_event_extraction.yaml
domains/general/workflows/memory_promotion_review.yaml
domains/general/workflows/memory_consolidation_review.yaml
domains/general/workflows/provenance_trace_review.yaml
```

Rule:

```text
No project or system memory is promoted automatically.
Every memory item follows candidate → validation → project/system.
```

---

# 10. P1/P2 — Self-evolution, candidate-only

Create:

```text
SELF_EVOLUTION.md
EVALUATION.md
```

Rules:

- no auto-merge;
- no direct mutation;
- no active modification without PR or patch candidate;
- no code evolution now;
- no real non-anonymized sessions;
- candidate-only evolution;
- tests required;
- Evidence Pack required;
- semantic preservation required;
- rollback required.

Self-evolution must never directly mutate source-of-truth Markdown.

Create skills:

```text
domains/general/skills/skill_evolution_candidate_check/
domains/general/skills/semantic_preservation_check/
domains/general/skills/evaluation_dataset_check/
domains/general/skills/before_after_benchmark_check/
domains/general/skills/prompt_bloat_check/
domains/general/skills/evolution_pr_review/
```

Create workflows:

```text
domains/general/workflows/skill_evolution_review.yaml
domains/general/workflows/evaluation_dataset_review.yaml
```

Explicitly postpone:

```text
tool description optimization
system prompt optimization
code evolution
continuous self-evolution
```

---

# 11. P2 — Workflow schema inspired by AgentScope

Create:

```text
WORKFLOW_SCHEMA.md
```

Fields:

```text
id
domain
status
task_contract_id
participants
steps
inputs
outputs
allowed_tools
forbidden_tools
approval_points
memory_impact
evidence_required
source_documents
expected_artifacts
interrupt_if
resume_after_approval
rollback_policy
failure_modes
quality_gates
```

Later additions to `TASK_CONTRACTS.md`:

```text
toolkit.allowed
toolkit.forbidden
approval_interrupt
resume_policy
```

Rule:

```text
AgentScope is schema inspiration only.
Do not integrate AgentScope as Pantheon runtime.
```

---

# 12. P2 — Hermes ecosystem radar and allowlists

Create:

```text
HERMES_ECOSYSTEM_SOURCES.md
HERMES_SKILL_ALLOWLIST.md
HERMES_PLUGIN_ALLOWLIST.md
HERMES_BLOCKLIST.md
```

Fields:

```text
repository
category
maturity
license
license_status
risk
decision
status
review_date
allowed_features
blocked_features
notes
```

Test later:

```text
wondelai/skills
lintlang
SkillClaw
rtk-hermes
mnemo-hermes
agent-analytics-hermes-plugin
portainer-stack-hermes
```

Block by default:

```text
payments / crypto
browser profiles
autonomous marketplaces
life-os
social plugins
remote MCP not audited
swarms multi-agents
autonomous incident remediation
job application automation
```

---

# 13. P2 — Hermes plugins, sandbox only

Create:

```text
HERMES_PLUGIN_POLICY.md
HERMES_PLUGIN_ALLOWLIST.md
```

Rules:

- license must be verified before use;
- no code copied while license is unclear;
- conceptual inspiration is allowed;
- production installation is blocked by default;
- sandbox required for every test.

Test only in sandbox:

```text
status / telemetry / validate / email guard / reflect
```

Block:

```text
autonomy
learner
memory adaptive
memory consolidate
identity
sandbox
mqtt
bridge
remote MCP not audited
```

Translate useful ideas into Pantheon skills:

```text
domains/general/skills/hallucination_check/
domains/general/skills/prompt_injection_check/
domains/general/skills/reflection_check/
domains/general/skills/delegation_result_score/
domains/general/skills/hermes_plugin_review/
```

---

# 14. P2 — Remediation Candidate Lane

Create:

```text
domains/general/skills/remediation_candidate/
domains/general/workflows/remediation_candidate_review.yaml
```

Role:

- analyze a failure;
- identify affected component;
- propose a correction;
- prepare patch candidate;
- generate Evidence Pack;
- request approval before application.

Rule:

```text
A remediation lane cannot bypass a blocked action.
```

---

# 15. P2 — Legacy audit

Create:

```text
CODE_AUDIT_POST_PIVOT.md
```

Mandatory table columns:

```text
Component
Path
Former role
Status
Proposed decision
Risk
Next action
Priority
```

Allowed statuses:

```text
keep
reorient
archive
delete_later
to_verify
legacy
```

Components to audit:

```text
modules.yaml
docker-compose.yml
platform/api/apps/*
platform/api/core/registry.py
platform/api/core/registries/*
platform/api/apps/approvals/
platform/api/alembic/
scripts/install/ui/
platform/data/db/init.sql
core/
modules/
```

Recommendations:

- mark `modules.yaml` as legacy until reoriented;
- create `docker-compose.domain.yml` for the Domain Layer API;
- keep `docker-compose.yml` as legacy until audited.

---

# 16. P2 — Operations documentation

Create:

```text
operations/install.md
operations/update.md
operations/backup.md
operations/doctor.md
operations/hermes_lab.md
operations/openwebui_knowledge.md
operations/domain_api.md
```

`operations/hermes_lab.md` must state:

- isolated installation;
- no Docker socket;
- no secrets;
- no write access to Pantheon volumes by default;
- controlled read access to context exports;
- doctor tests;
- skill tests;
- authorized tool tests.

---

# 17. P2 — Templates

Create:

```text
domains/general/templates/evidence_pack.md
domains/general/templates/approval_report.md
domains/general/templates/memory_candidate.md
domains/general/templates/skill_review.md
domains/general/templates/postmortem_report.md

domains/architecture_fr/templates/quote_review_report.md
domains/architecture_fr/templates/client_message_review.md
domains/architecture_fr/templates/notice_architecturale_report.md
domains/architecture_fr/templates/dpgf_review_report.md

domains/software/templates/repo_audit_report.md
domains/software/templates/legacy_component_decision.md
domains/software/templates/context_export_review.md
```

---

# 18. P3 — Lightweight operations view

Do not create a heavy React dashboard now.

Expose simple API state first:

```text
/domain/snapshot
/domain/skills
/domain/workflows
/domain/quality-gates
/domain/approval/policy
/domain/legacy
/domain/context-pack
```

Later only:

- skill candidates;
- workflow candidates;
- approval queue;
- legacy audit status;
- Hermes context export status;
- Knowledge collection status.

---

# 19. Do not implement now

Do not implement now:

```text
custom task queue
Pantheon autonomous runtime
agent CRUD
heavy React dashboard
direct reading of ~/.hermes/state.db
browser automation
WhatsApp / Telegram gateway
automatic cron
autonomous employees
Obsidian as source of truth
custom scheduler
terminal backend
model routing system
global plugin installation
batch install from GitHub
remote MCP not audited
self-evolution code
Docker socket
secrets access
```

---

# 20. Strict order

1. `EXTERNAL_TOOLS_POLICY.md`
2. Complete `APPROVALS.md` with external tools, fallback and remediation.
3. Complete `EVIDENCE_PACK.md` with extended schema, fallback and remediation.
4. Complete `TASK_CONTRACTS.md` with PDF contracts, fallback policy and remediation policy.
5. `OPENWEBUI_EXTENSIONS_POLICY.md`
6. `HERMES_PLUGIN_POLICY.md`
7. `operations/stirling_pdf.md`
8. `operations/stirling_ocr.md`
9. `infra/compose/docker-compose.stirling.yml`
10. `hermes/context/stirling_pdf_context.md`
11. `domains/general/skills/pdf_metadata_check/`
12. `domains/general/skills/pdf_text_layer_check/`
13. `domains/general/skills/pdf_ocr_prepare/`
14. `domains/general/skills/pdf_sanitize_check/`
15. `domains/architecture_fr/workflows/cctp_pdf_ingestion_prepare.yaml`
16. `OPENWEBUI_INTEGRATION.md`
17. `hermes/context/openwebui_context.md`
18. `domains/general/skills/markdown_quality_check/`
19. `SKILL_RESOLVER.md`
20. `conventions/*`
21. `SKILL_LIFECYCLE.md`
22. `MEMORY_EVENT_SCHEMA.md`
23. `SELF_EVOLUTION.md`
24. `EVALUATION.md`
25. `WORKFLOW_SCHEMA.md`
26. `HERMES_ECOSYSTEM_SOURCES.md`
27. `HERMES_SKILL_ALLOWLIST.md`
28. `HERMES_PLUGIN_ALLOWLIST.md`
29. `HERMES_BLOCKLIST.md`
30. `domains/general/skills/remediation_candidate/`
31. `CODE_AUDIT_POST_PIVOT.md`

---

# 21. Target result

Pantheon OS becomes a governed professional domain layer.

Its value is not to execute everything.

Its value is to define:

- rules;
- roles;
- workflows;
- skills;
- sources;
- memory;
- approvals;
- evidence;
- domain boundaries;
- external tool governance.

Hermes executes inside that frame. OpenWebUI exposes it. Pantheon canonizes it.
