# ROADMAP — Pantheon Next

> Post-pivot roadmap.
> Pantheon Next is a Hermes-backed Domain Operating Layer: OpenWebUI exposes, Hermes Agent executes, Pantheon Next governs.

---

## 1. Core doctrine

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

Pantheon Next must not become a full autonomous agent runtime.

Its value is to define:

- governance;
- abstract agents;
- task contracts;
- approval levels;
- evidence requirements;
- domain packages;
- skills as governance contracts;
- workflows as structured definitions;
- memory policy;
- Knowledge taxonomy;
- Hermes context packs;
- OpenWebUI integration rules;
- external tool policy.

Hermes executes inside that frame.

OpenWebUI exposes the cockpit, Knowledge Bases and human validation surface.

---

## 2. Source-of-truth documents

Reference Markdown files drive development.

Canonical governance path:

```text
docs/governance/
```

Core files:

```text
README.md
ai_logs/README.md

docs/governance/STATUS.md
docs/governance/ROADMAP.md
docs/governance/ARCHITECTURE.md
docs/governance/MODULES.md
docs/governance/AGENTS.md
docs/governance/MEMORY.md
docs/governance/APPROVALS.md
docs/governance/TASK_CONTRACTS.md
docs/governance/EVIDENCE_PACK.md
docs/governance/HERMES_INTEGRATION.md
docs/governance/OPENWEBUI_INTEGRATION.md
docs/governance/EXTERNAL_TOOLS_POLICY.md
docs/governance/KNOWLEDGE_TAXONOMY.md
docs/governance/CODE_AUDIT_POST_PIVOT.md
```

Rules:

- documentation before code;
- no direct push to `main`;
- no autonomous Pantheon runtime revival;
- no real private project/client data in repository examples;
- `architecture_fr` is the only French architecture domain name;
- use `system memory`, not `agency memory`;
- use `domains/general`, not `skills/generic` or `workflows/generic`;
- use `domains/architecture_fr`, not `domains/architecture`;
- unknown external tools are `blocked until reviewed`.

---

## 3. Target repository anatomy

```text
Pantheon-Next/
  README.md

  ai_logs/
    README.md
    YYYY-MM-DD-slug.md

  docs/
    governance/
      README.md
      STATUS.md
      ROADMAP.md
      ARCHITECTURE.md
      MODULES.md
      AGENTS.md
      MEMORY.md
      APPROVALS.md
      TASK_CONTRACTS.md
      EVIDENCE_PACK.md
      HERMES_INTEGRATION.md
      OPENWEBUI_INTEGRATION.md
      EXTERNAL_TOOLS_POLICY.md
      KNOWLEDGE_TAXONOMY.md
      CODE_AUDIT_POST_PIVOT.md

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
  platform/
    api/
      pantheon_domain/
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

## 4. P0 — Governance base

Status: mostly completed.

Completed or started:

- `README.md` — Pantheon Next product entry point.
- `docs/governance/README.md` — governance document index.
- `STATUS.md` — current state after Pantheon Next naming and pivot.
- `ARCHITECTURE.md` — Hermes-backed technical anatomy.
- `APPROVALS.md` — C0-C5 criticality and approval policy.
- `TASK_CONTRACTS.md` — task contract schema and first contracts.
- `EVIDENCE_PACK.md` — mandatory proof package schema.
- `HERMES_INTEGRATION.md` — Hermes/Pantheon/OpenWebUI boundary.
- `OPENWEBUI_INTEGRATION.md` — OpenWebUI cockpit, Knowledge and validation boundary.
- `EXTERNAL_TOOLS_POLICY.md` — external tool classification and allowlist policy.
- `KNOWLEDGE_TAXONOMY.md` — Knowledge layers, reliability levels and source tiers.
- `CODE_AUDIT_POST_PIVOT.md` — initial legacy/runtime component classification register.
- `operations/openwebui_hermes_pantheon.md` — three-system operating protocol.
- static `GET /runtime/context-pack` endpoint.
- local Hermes `pantheon-os` template under `hermes/templates/pantheon-os/`.
- candidate skill `domains/general/skills/adaptive_orchestration/`.
- candidate skill `domains/general/skills/project_context_resolution/`.

Still required in P0/P1:

1. Update `ARCHITECTURE.md` wording from Pantheon OS to Pantheon Next where useful.
2. Complete `AGENTS.md` with explicit non-runtime agent doctrine and veto mapping.
3. Complete `MEMORY.md` with Evidence Pack and C3 promotion references if missing.
4. Complete `CODE_AUDIT_POST_PIVOT.md` after real code audit.
5. Verify `platform/api/pantheon_runtime/` does not drift into autonomous execution.
6. Verify `OpenWebUI → Hermes Gateway → Pantheon Context Pack` wiring.

---

## 5. P1 — Hermes and OpenWebUI integration

Purpose:

```text
Make Hermes consume Pantheon context and make OpenWebUI expose the result without becoming the authority.
```

Tasks:

1. Create Hermes context exports:

```text
hermes/context/pantheon_context.md
hermes/context/agents_context.md
hermes/context/rules_context.md
hermes/context/memory_context.md
hermes/context/tools_policy.md
hermes/context/openwebui_context.md
hermes/context/architecture_fr_context.md
hermes/context/software_context.md
```

2. Define `hermes_context_consultation` in `TASK_CONTRACTS.md`.
3. Verify or document `PANTHEON_CONTEXT_URL` consumption.
4. Create OpenWebUI Router Pipe specification.
5. Create OpenWebUI Actions specification.
6. Add approval request and Evidence Pack summary display requirements.
7. Add SearXNG to `EXTERNAL_TOOLS_POLICY.md` if used.
8. Add Hermes Dashboard as local-only/test under `EXTERNAL_TOOLS_POLICY.md` if used.

Rules:

- OpenWebUI points to Hermes Gateway, not Pantheon API.
- Pantheon API is not an OpenAI-compatible backend.
- Hermes outputs remain candidates until validated.
- OpenWebUI Knowledge is not Pantheon Memory.

---

## 6. P1 — Domain packages and first useful capabilities

Create missing rule files where absent:

```text
domains/general/rules.md
domains/general/knowledge_policy.md
domains/general/output_formats.md

domains/architecture_fr/rules.md
domains/architecture_fr/knowledge_policy.md
domains/architecture_fr/output_formats.md

domains/software/rules.md
domains/software/knowledge_policy.md
domains/software/output_formats.md
```

First architecture_fr target:

```text
quote_vs_cctp_analysis / quote_vs_cctp_review
```

Recommended first skills:

```text
domains/architecture_fr/skills/quote_vs_cctp_consistency/
domains/architecture_fr/skills/dpgf_quantity_sanity_check/
domains/architecture_fr/skills/client_message_safety/
domains/software/skills/repo_md_audit/
domains/software/skills/code_audit_post_pivot/
domains/general/skills/markdown_quality_check/
domains/general/skills/openwebui_plugin_review/
```

---

## 7. P1 — External services under policy

External services are capabilities, not authorities.

Initial services to classify or keep classified:

```text
Stirling-PDF
SearXNG
OpenWebUI extensions
Hermes plugins
Hermes community skills
OCRmyPDF
Gotenberg
qpdf
Hermes Dashboard
GHCR
Docker socket
remote MCP servers
```

Rules:

- no batch install from GitHub;
- no Docker socket by default;
- no secrets access by default;
- no public dashboard without auth/VPN and approval;
- no PDF source overwrite;
- no Knowledge ingestion without Evidence Pack where consequential.

Stirling-PDF remains P1/P2, not a reason to change Pantheon into a PDF runtime.

---

## 8. P1/P2 — Skill system and resolver

Create:

```text
SKILL_RESOLVER.md
SKILL_LIFECYCLE.md
```

Resolver fields:

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

Skill lifecycle:

```text
need / error / repetition
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

Rule:

```text
Pantheon skill = domain contract + governance.
Hermes skill = executable capability.
```

---

## 9. P1/P2 — Structured memory

Create:

```text
MEMORY_EVENT_SCHEMA.md
```

Model:

```text
Actor → Action/Event → Target → Context
```

Rule:

```text
No project or system memory is promoted automatically.
Every memory item follows candidate → Evidence Pack → validation → project/system.
```

Initial event types may include:

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

---

## 10. P2 — Workflow schema and evaluation

Create:

```text
WORKFLOW_SCHEMA.md
EVALUATION.md
```

Workflow fields:

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

Evaluation starts simple:

- Evidence quality;
- citation quality;
- unsupported claim count;
- limitation clarity;
- approval correctness.

Do not create a heavy evaluation runtime in P2.

---

## 11. P2 — Code audit post pivot

Use:

```text
docs/governance/CODE_AUDIT_POST_PIVOT.md
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
platform/api/pantheon_runtime/
legacy/
```

Allowed decisions:

```text
keep
reorient
archive
delete_later
to_verify
legacy
```

Rule:

```text
Do not delete before diagnosis.
Do not reactivate the autonomous runtime path by accident.
```

---

## 12. P2 — Operations documentation

Create or complete:

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

## 13. P3 — Lightweight operations view

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

## 14. Do not implement now

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

## 15. Target result

Pantheon Next becomes a governed professional domain layer.

Its value is not to execute everything.

Its value is to define:

- rules;
- roles;
- workflows;
- skills as governance contracts;
- sources;
- memory;
- approvals;
- evidence;
- domain boundaries;
- external tool governance.

Hermes executes inside that frame.

OpenWebUI exposes it.

Pantheon Next canonizes it.
