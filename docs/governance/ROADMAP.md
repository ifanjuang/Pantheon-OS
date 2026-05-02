# ROADMAP — Pantheon Next

> Post-pivot roadmap.
> Pantheon Next is a Hermes-backed Domain Operating Layer: OpenWebUI exposes, Hermes Agent executes, Pantheon Next governs.

Last update: 2026-05-02

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
- model routing policy;
- Hermes context packs;
- OpenWebUI integration rules;
- external tool/runtime policy;
- operations checks.

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
CLAUDE.md
ai_logs/README.md

docs/governance/README.md
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
docs/governance/OPENWEBUI_DOMAIN_MAPPING.md
docs/governance/MODEL_ROUTING_POLICY.md
docs/governance/EXTERNAL_TOOLS_POLICY.md
docs/governance/EXTERNAL_RUNTIME_OPTIONS.md
docs/governance/EXTERNAL_AI_OPTION_REVIEWS.md
docs/governance/EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md
docs/governance/KNOWLEDGE_TAXONOMY.md
docs/governance/CODE_AUDIT_POST_PIVOT.md
docs/governance/WORKFLOW_SCHEMA.md
docs/governance/SKILL_LIFECYCLE.md
docs/governance/MEMORY_EVENT_SCHEMA.md
docs/governance/VERSIONS.md
```

Operational and asset docs:

```text
operations/openwebui_hermes_pantheon.md
operations/openwebui_manual_setup.md
operations/doctor.md
docs/assets/README.md
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
- unknown external tools are `blocked until reviewed`;
- Doctor observes and reports only.

---

## 3. Target repository anatomy

```text
Pantheon-Next/
  README.md
  CLAUDE.md

  ai_logs/
    README.md
    YYYY-MM-DD-slug.md

  docs/
    assets/
      README.md
      pantheon-next-overview.png
      pantheon-governed-flow.png
      pantheon-hermes-contract.png
      pantheon-agent-roles.png
      pantheon-knowledge-vs-memory.png
      pantheon-repository-map.png
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
      OPENWEBUI_DOMAIN_MAPPING.md
      MODEL_ROUTING_POLICY.md
      EXTERNAL_TOOLS_POLICY.md
      EXTERNAL_RUNTIME_OPTIONS.md
      EXTERNAL_AI_OPTION_REVIEWS.md
      EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md
      KNOWLEDGE_TAXONOMY.md
      CODE_AUDIT_POST_PIVOT.md
      WORKFLOW_SCHEMA.md
      SKILL_LIFECYCLE.md
      MEMORY_EVENT_SCHEMA.md
      VERSIONS.md

  agents/

  domains/
    general/
      domain.md
      rules.md
      knowledge_policy.md
      output_formats.md
      skills/
        adaptive_orchestration/
        project_context_resolution/
        knowledge_selection/
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
    registry.example.yaml
    registry.yaml
    source_tiers.md
    freshness_policy.md
    openwebui_collections.md

  config/
    model_routing.example.yaml
    openwebui_domain_mapping.example.yaml

  hermes/
    context/
    templates/

  operations/
    openwebui_hermes_pantheon.md
    openwebui_manual_setup.md
    doctor.md
    install.md
    update.md
    backup.md
    hermes_lab.md
    openwebui_knowledge.md
    domain_api.md

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

Status: completed as documentation baseline.

Completed:

```text
README.md
docs/assets/README.md
docs/governance/README.md
STATUS.md
ROADMAP.md
ARCHITECTURE.md
APPROVALS.md
TASK_CONTRACTS.md
EVIDENCE_PACK.md
HERMES_INTEGRATION.md
OPENWEBUI_INTEGRATION.md
OPENWEBUI_DOMAIN_MAPPING.md
MODEL_ROUTING_POLICY.md
EXTERNAL_TOOLS_POLICY.md
EXTERNAL_RUNTIME_OPTIONS.md
EXTERNAL_AI_OPTION_REVIEWS.md
EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md
KNOWLEDGE_TAXONOMY.md
CODE_AUDIT_POST_PIVOT.md
WORKFLOW_SCHEMA.md
SKILL_LIFECYCLE.md
MEMORY_EVENT_SCHEMA.md
operations/openwebui_hermes_pantheon.md
operations/openwebui_manual_setup.md
operations/doctor.md
knowledge/registry.example.yaml
```

Also completed or started:

```text
static GET /runtime/context-pack endpoint
API smoke tests under tests/test_api_smoke.py
local Hermes pantheon-os template under hermes/templates/pantheon-os/
candidate skill domains/general/skills/adaptive_orchestration/
candidate skill domains/general/skills/project_context_resolution/
candidate skill domains/general/skills/knowledge_selection/
README Lucid diagram sources registered under docs/assets/README.md
```

P0 guardrail:

```text
No new runtime abstraction without documented gain and approval.
```

---

## 5. P1 — Immediate next work

Purpose:

```text
Turn the documentation baseline into a verifiable, minimal operating setup without creating a Pantheon runtime.
```

Priority order:

1. Review and merge Claude's Hermes context export PR when available.

Expected files:

```text
hermes/context/README.md
hermes/context/pantheon_context.md
hermes/context/agents_context.md
hermes/context/rules_context.md
hermes/context/memory_context.md
hermes/context/tools_policy.md
hermes/context/openwebui_context.md
hermes/context/architecture_fr_context.md
hermes/context/software_context.md
```

2. Run the read-only Doctor checklist against the repository tree.
3. Execute API smoke tests locally or in CI:

```text
pytest tests/test_api_smoke.py
```

4. Validate `knowledge/registry.example.yaml` against live OpenWebUI Knowledge Base names, then decide whether to create `knowledge/registry.yaml`.
5. Define Hermes retrieval preflight mapping for `knowledge_selection`.
6. Verify or document `PANTHEON_CONTEXT_URL` consumption by Hermes.
7. Complete domain package rule files if missing:

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

8. Create first `architecture_fr` capability:

```text
domains/architecture_fr/skills/quote_vs_cctp_consistency/
domains/architecture_fr/workflows/quote_vs_cctp_review.yaml
```

9. Complete `CODE_AUDIT_POST_PIVOT.md` after real tree audit.
10. Define OpenWebUI Router Pipe specification.
11. Define OpenWebUI Actions specification.
12. Export clean colored README diagrams from Lucid, commit them under `docs/assets/`, then embed them in `README.md`.

---

## 6. P1 — Hermes and OpenWebUI integration

Purpose:

```text
Make Hermes consume Pantheon context and make OpenWebUI expose the result without becoming the authority.
```

Rules:

```text
OpenWebUI points to Hermes Gateway, not Pantheon API.
Pantheon API is not an OpenAI-compatible backend.
Hermes outputs remain candidates until validated.
OpenWebUI Knowledge is not Pantheon Memory.
OpenWebUI Workspace Models are presets, not Pantheon agents.
OpenWebUI Skills are operator aids, not active Pantheon skills.
```

Tasks:

1. Review Hermes context exports after Claude's PR lands.
2. Create OpenWebUI Router Pipe specification.
3. Create OpenWebUI Actions specification.
4. Add approval request and Evidence Pack summary display requirements.
5. Add SearXNG to `EXTERNAL_TOOLS_POLICY.md` if used.
6. Add Hermes Dashboard as local-only/test under `EXTERNAL_TOOLS_POLICY.md` if used.
7. Add manual OpenWebUI setup verification after live configuration.
8. Align live Knowledge names with `knowledge/registry.example.yaml` before creating a real registry.

---

## 7. P1 — Domain packages and first useful capabilities

Existing general-domain candidates:

```text
adaptive_orchestration
project_context_resolution
knowledge_selection
```

First architecture_fr target:

```text
quote_vs_cctp_analysis / quote_vs_cctp_review
```

Recommended next skills:

```text
domains/architecture_fr/skills/quote_vs_cctp_consistency/
domains/architecture_fr/skills/dpgf_quantity_sanity_check/
domains/architecture_fr/skills/client_message_safety/
domains/software/skills/repo_md_audit/
domains/software/skills/code_audit_post_pivot/
domains/general/skills/markdown_quality_check/
domains/general/skills/openwebui_plugin_review/
```

Rule:

```text
A Pantheon skill is a governance contract.
A Hermes skill is executable capability.
```

---

## 8. P1 — Knowledge Registry and Knowledge Selection

Status:

```text
knowledge/registry.example.yaml exists.
domains/general/skills/knowledge_selection/ exists as candidate.
knowledge/registry.yaml is not created yet.
```

The example registry defines:

```text
source tiers T0-T5
reliability levels R0-R5
privacy levels
freshness policies
OpenWebUI Knowledge Base mappings
allowed use / forbidden use
evidence requirements
memory candidate constraints
anonymized project collection template
```

The `knowledge_selection` candidate defines:

```text
domain filter
privacy filter
project-scope filter
source-tier filter
reliability filter
freshness filter
forbidden-source filter
Evidence Pack requirement filter
AKS-inspired provenance fields
Six-Hats-inspired source selection lenses
```

Minimum fields for any future live registry entry:

```text
id
domain
source_tier
privacy_level
project_scope
freshness_policy
openwebui_knowledge_base
allowed_use
forbidden_use
evidence_required
memory_candidate_allowed
```

Initial mapped Knowledge Bases:

```text
pantheon_governance
pantheon_approvals
pantheon_task_contracts
pantheon_evidence_pack
architecture_fr_cctp_models
architecture_fr_dpgf_models
architecture_fr_contract_clauses
architecture_fr_notices
architecture_fr_sdis_erp
architecture_fr_plu_reference
architecture_fr_site_reports
software_repo_docs
code_audit_post_pivot
api_contract_docs
```

Rules:

```text
Knowledge is not Memory.
OpenWebUI Knowledge is source material.
Memory requires candidate → Evidence Pack → validation.
Live registry must not be created until OpenWebUI names and source scopes are verified.
Knowledge Selection does not retrieve documents; it constrains retrieval.
```

---

## 9. P1/P2 — External services under policy

External services are capabilities, not authorities.

Initial services and options already classified or to keep classified:

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
Cycles / runcycles
Omnigraph
RAGFlow
Thoth
kontext-brain-ts
Kanwas
AKS Reference Server
AgentRQ
opencode-loop
six-hats-skill
OpenConcho
Honcho
LangChain / LangGraph
Langflow
OpenClaw
OpenAI Symphony
Graphify
Layer Infinite / Layer
CTX
Binderly
NeverWrite
AnimoCerebro
Caliber / ai-setup
```

Rules:

```text
no batch install from GitHub
no Docker socket by default
no secrets access by default
no public dashboard without auth/VPN and approval
no PDF source overwrite
no Knowledge ingestion without Evidence Pack where consequential
external runtimes may assist Pantheon but must not become Pantheon
external memory runtimes may be studied but must not become Pantheon Memory
```

Possible near-term external test:

```text
Graphify read-only sandbox on non-sensitive repo snapshot
```

Only after:

```text
external runtime review template
C2/C3 approval
Evidence Pack
no automatic memory promotion
```

---

## 10. P2 — Workflow schema and evaluation

Existing:

```text
WORKFLOW_SCHEMA.md
```

Still to create or complete:

```text
EVALUATION.md
```

Evaluation starts simple:

```text
Evidence quality
citation quality
unsupported claim count
limitation clarity
approval correctness
model fallback trace
source tier correctness
Knowledge Selection correctness
```

Do not create a heavy evaluation runtime in P2.

---

## 11. P2 — Code audit post pivot

Use:

```text
docs/governance/CODE_AUDIT_POST_PIVOT.md
operations/doctor.md
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

Rules:

```text
Do not delete before diagnosis.
Do not reactivate the autonomous runtime path by accident.
```

---

## 12. P2 — Operations documentation

Existing:

```text
operations/openwebui_hermes_pantheon.md
operations/openwebui_manual_setup.md
operations/doctor.md
```

Create or complete:

```text
operations/install.md
operations/update.md
operations/backup.md
operations/hermes_lab.md
operations/openwebui_knowledge.md
operations/domain_api.md
```

`operations/hermes_lab.md` must state:

```text
isolated installation
no Docker socket
no secrets
no write access to Pantheon volumes by default
controlled read access to context exports
doctor tests
skill tests
authorized tool tests
```

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

```text
skill candidates
workflow candidates
approval queue
legacy audit status
Hermes context export status
Knowledge collection status
Doctor report status
Memory candidate review status
```

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
model routing system inside Pantheon
global plugin installation
batch install from GitHub
remote MCP not audited
self-evolution code
Docker socket
secrets access
Doctor auto-fix
Knowledge auto-sync without approval
Honcho/OpenConcho memory backend
memory consolidation without Evidence Pack and approval
```

---

## 15. Target result

Pantheon Next becomes a governed professional domain layer.

Its value is not to execute everything.

Its value is to define:

```text
rules
roles
workflows
skills as governance contracts
sources
memory
approvals
evidence
domain boundaries
model policy
external tool governance
operations checks
```

Hermes executes inside that frame.

OpenWebUI exposes it.

Pantheon Next canonizes it.
