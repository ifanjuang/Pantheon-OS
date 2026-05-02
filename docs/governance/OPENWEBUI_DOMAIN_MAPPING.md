# OPENWEBUI DOMAIN MAPPING — Pantheon Next

> Mapping policy between Pantheon domains and OpenWebUI Knowledge Bases, Workspace Models and operator Skills.

---

## 1. Principle

Domains belong to Pantheon.

OpenWebUI may mirror, expose and organize domain assets, but it must not become the source of truth for domains.

```text
Pantheon defines domains.
OpenWebUI exposes domain-facing Knowledge, Models and operator Skills.
Hermes applies the domain through Task Contracts at execution time.
```

---

## 2. Authority boundary

| Layer | Authority |
|---|---|
| Pantheon Next | canonical domains, rules, workflows, skills contracts, memory policy, approvals |
| OpenWebUI | UI presets, Knowledge Bases, user-facing Models, operator Skills |
| Hermes | execution under Pantheon context, task contract and policy |

OpenWebUI configuration can help operators work faster.

It cannot override Pantheon governance.

---

## 3. Canonical Pantheon domains

Initial canonical domains:

```text
domains/general
domains/architecture_fr
domains/software
```

Rules:

- no `domains/architecture`;
- no `skills/generic`;
- no `workflows/generic`;
- no OpenWebUI-only domain authority;
- no Knowledge Base treated as canonical memory.

---

## 4. OpenWebUI mapping objects

OpenWebUI may expose four mapped object types:

```text
knowledge_base
workspace_model
operator_skill
action_or_router
```

### 4.1 Knowledge Bases

Knowledge Bases store or expose documents.

They are sources, not memory.

Example:

```text
architecture_fr_cctp_models
architecture_fr_dpgf_models
architecture_fr_contract_clauses
architecture_fr_sdis_erp
software_repo_docs
pantheon_governance
```

### 4.2 Workspace Models

Workspace Models are user-facing presets.

Example:

```text
ATHENA Planner
ARGOS Extractor
THEMIS Risk Check
APOLLO Validator
IRIS Communication
```

They may map to Pantheon abstract agents, but they do not define those agents.

### 4.3 Operator Skills

OpenWebUI Skills may provide practical prompts or methods for operators.

They are not Pantheon active skills unless reviewed through `SKILL_LIFECYCLE.md`.

### 4.4 Actions / Routers

OpenWebUI Actions may later display Evidence Packs, ask for approvals, or trigger Hermes handoff.

They must not mutate Pantheon source-of-truth files, memory or approvals without policy.

---

## 5. Mapping rules

A mapping entry must identify:

```text
Pantheon domain
OpenWebUI Knowledge Bases
OpenWebUI Workspace Models
OpenWebUI operator Skills
allowed use
forbidden use
privacy constraints
Evidence Pack requirements
owner / review status
```

A mapping is not valid if it lacks a Pantheon domain reference.

---

## 6. Domain: general

Purpose:

```text
cross-domain governance, source checks, approvals, evidence, memory candidates, skill lifecycle, external tool policy
```

OpenWebUI may expose:

```text
pantheon_governance
pantheon_approvals
pantheon_task_contracts
pantheon_evidence_pack
pantheon_memory_policy
```

Workspace Models:

```text
ATHENA Planner
THEMIS Risk Check
APOLLO Validator
ZEUS Arbitration
```

Operator Skills:

```text
source_check_playbook
approval_classification_playbook
evidence_pack_summary_playbook
```

Forbidden:

```text
promote memory
activate skills
modify governance Markdown
send external messages
install plugins
```

---

## 7. Domain: architecture_fr

Purpose:

```text
French architecture / maîtrise d'œuvre workflows, CCTP, DPGF, CCAP, notices, permits, chantier, ERP/SDIS, PLU, risks and professional outputs
```

OpenWebUI may expose:

```text
architecture_fr_cctp_models
architecture_fr_dpgf_models
architecture_fr_contract_clauses
architecture_fr_notices
architecture_fr_sdis_erp
architecture_fr_plu_reference
architecture_fr_site_reports
```

Workspace Models:

```text
ATHENA Architecture Planner
ARGOS Document Extractor
THEMIS Contract Risk Check
HEPHAESTUS Technical Review
APOLLO Architecture Validator
IRIS Client Communication
```

Operator Skills:

```text
cctp_review_prompt
dpgf_review_prompt
quote_vs_cctp_review_prompt
notice_architecturale_prompt
client_message_safety_prompt
```

Forbidden:

```text
using one project Knowledge Base for another project without trace
promoting client/project facts into system memory
sending external client messages without approval
issuing legal/contractual conclusions without Evidence Pack
mixing obsolete templates with active project documents silently
```

---

## 8. Domain: software

Purpose:

```text
repository audit, code/docs alignment, legacy classification, API review, context export, tests and controlled refactor planning
```

OpenWebUI may expose:

```text
software_repo_docs
pantheon_governance
code_audit_post_pivot
api_contract_docs
```

Workspace Models:

```text
ATHENA Software Planner
ARGOS Repo Inspector
HEPHAESTUS Code Reviewer
THEMIS Change Gate
APOLLO Merge Validator
```

Operator Skills:

```text
repo_md_audit_prompt
legacy_classification_prompt
api_contract_check_prompt
context_export_review_prompt
```

Forbidden:

```text
push to main
delete files without approval
install dependencies without policy
read secrets
create runtime endpoints that bypass governance
reactivate old autonomous runtime components
```

---

## 9. Knowledge Base status

Each OpenWebUI Knowledge Base should have a status:

```text
planned
active
deprecated
blocked
unknown
```

Each should also declare:

```text
source_tier
privacy_level
project_scope
freshness_policy
allowed_domains
forbidden_domains
```

If status is unknown, the Knowledge Base must be treated as untrusted until reviewed.

---

## 10. Workspace Model status

Each OpenWebUI Workspace Model should have a status:

```text
planned
active
deprecated
blocked
unknown
```

A Workspace Model is invalid if it claims a Pantheon agent role without mapping back to `AGENTS.md`.

---

## 11. Operator Skill status

OpenWebUI Skills are operator aids.

Statuses:

```text
planned
active
deprecated
blocked
unknown
```

An OpenWebUI Skill is not a Pantheon active skill unless it has passed:

```text
SKILL_LIFECYCLE.md
TASK_CONTRACTS.md
APPROVALS.md
EVIDENCE_PACK.md
```

---

## 12. Privacy

Private project data must remain project-scoped.

Rules:

- no cross-project mixing without explicit trace;
- no private data in examples;
- no client/project data promoted to system memory without review;
- no remote model/tool use unless policy allows it;
- no public sharing of OpenWebUI Knowledge content without approval.

---

## 13. Evidence requirements

When an output uses OpenWebUI-mapped assets and becomes consequential, Evidence Pack must record:

```text
pantheon_domain
openwebui_knowledge_bases_used
openwebui_workspace_model_used
openwebui_operator_skills_used
source_status
project_scope
privacy_level
unsupported_claims
fallbacks
approval_required
```

---

## 14. Future API surface

A future read-only endpoint may expose this mapping:

```text
GET /domain/openwebui-mapping
```

Forbidden until C3 approval flow exists:

```text
POST /domain/openwebui-mapping
PATCH /domain/openwebui-mapping
POST /openwebui/knowledge/sync
POST /openwebui/models/update
POST /openwebui/skills/install
```

---

## 15. Final rule

```text
Pantheon domains are canonical.
OpenWebUI assets are mapped surfaces.
Hermes applies the selected domain under contract.
```
