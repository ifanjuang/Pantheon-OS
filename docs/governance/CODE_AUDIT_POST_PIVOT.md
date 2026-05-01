# CODE AUDIT POST PIVOT — Pantheon Next

> Audit register for code and operational assets created before or during the Hermes-backed pivot.

---

## 1. Purpose

Pantheon Next has pivoted away from an autonomous agentic runtime.

The current target is:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

This document prevents two opposite mistakes:

1. deleting useful legacy code too early;
2. silently reactivating the old autonomous runtime path.

Legacy code must be classified before reuse, deletion or extension.

Reference synthesis:

```text
docs/governance/PRE_REFACTOR_ARCHITECTURE_FINDINGS.md
```

---

## 2. Audit rule

Before changing legacy code, classify it.

Allowed decisions:

```text
keep
reorient
archive
delete_later
to_verify
legacy
```

Definitions:

| Status | Meaning |
|---|---|
| keep | Component is aligned with Pantheon Next and may remain active |
| reorient | Component contains useful logic but must be reframed as governance, context, schema, contract or Hermes-side capability |
| archive | Component is kept for history only and must not be imported by active runtime |
| delete_later | Component appears obsolete but must be removed only after confirmation |
| to_verify | Component requires inspection before decision |
| legacy | Component belongs to the previous autonomous architecture and must not be extended without review |

---

## 3. Current classification table

| Component | Path | Former role | Status | Proposed decision | Risk | Next action | Priority |
|---|---|---|---|---|---|---|---|
| FastAPI entrypoint | `platform/api/main.py` | API entrypoint | keep | Keep as lightweight Domain Layer API entrypoint | May drift into runtime if execution endpoints are added | Do not add agent/tool execution endpoints | P0 |
| Domain Layer package | `platform/api/pantheon_domain/` | Domain API definitions | keep | Keep as read-only domain snapshot and approval classification surface | Low | Align terminology with Pantheon Next | P0 |
| Domain contracts | `platform/api/pantheon_domain/contracts.py` | Pydantic domain definitions | keep | Keep as definition contracts for agents, skills, workflows, memory, knowledge, legacy | Needs C0-C5 alignment | Add explicit C0-C5 mapping later | P1 |
| Domain repository | `platform/api/pantheon_domain/repository.py` | Static in-code registry | keep | Keep as bootstrap registry until file-backed registry exists | Contains `agency_memory` / `generic` terminology | Rename conceptually to `system_memory` and `general` | P0 |
| Runtime context package | `platform/api/pantheon_runtime/` | Static context pack endpoint | reorient | Treat as context export only, not runtime authority | Name suggests Pantheon runtime | Avoid execution endpoints; consider later rename | P0 |
| Manifest contracts | `platform/api/core/contracts/manifest.py` | Runtime/module manifest | reorient | Use as schema source for skills, workflows, tools and operations doctor | Could revive registry runtime | Extract schema; do not reactivate auto-runtime | P1 |
| Task/workflow contracts | `platform/api/core/contracts/tasks.py` | Task and workflow model | reorient | Use as basis for `WORKFLOW_SCHEMA.md` and task contracts | Starts at C1, not C0 | Add C0 before active use | P1 |
| Workflow loader | `platform/api/core/registries/workflows.py` | Loads workflow/task YAML | reorient | Keep pattern for documentation validation, not execution | May become workflow engine | Use only as validator until policy exists | P1/P2 |
| Legacy dynamic registry | `platform/api/core/registry.py` | Runtime/module loader | legacy | Do not extend until audited; extract manifest quality ideas only | May revive old module runtime | Keep disabled from new architecture | P1 |
| Approvals app | `platform/api/apps/approvals/` | HITL approval API | reorient | Future Approval Queue after C0-C5 alignment | Could diverge from `APPROVALS.md` | Rename reasoning fields, bind Evidence Pack | P1 |
| OpenAI compatibility app | `platform/api/apps/openai_compat/` | OpenWebUI `/v1` backend | reorient | Preserve project-scoped RAG idea; move target to Hermes Gateway pattern | Makes Pantheon look like model backend | Do not treat as final OpenWebUI wiring | P1 |
| Documents app | `platform/api/apps/documents/` | Upload, storage, ingestion, search | reorient | Keep ingestion pattern under task contract | Auto THEMIS background analysis | Replace side effect with review task contract | P1 |
| Hybrid RAG service | `platform/api/core/services/rag_service.py` | RAG engine | reorient | Preserve as Knowledge capability pattern | Could be mistaken for memory engine | Document under Knowledge, not Memory | P2 |
| OCR service | `platform/api/core/services/ocr_service.py` | OCR fallback | reorient | External document-processing capability under policy | External endpoint / privacy | Require classification before use | P2 |
| LLM service | `platform/api/core/services/llm_service.py` | LLM provider wrapper | reorient | Keep structured extraction pattern | Provider router drift | Keep provider execution outside Pantheon authority | P2 |
| Circuit breaker | `platform/api/core/circuit_breaker.py` | LLM resilience | reorient | Use as future operations/resilience pattern | Redis dependency if enabled | Document in operations doctor later | P2 |
| Storage service | `platform/api/core/services/storage_service.py` | MinIO wrapper | reorient | Preserve object storage pattern for documents | MinIO not P0 | Keep P2, do not make mandatory now | P2 |
| Agent service | `platform/api/apps/agent/service.py` | ReAct loop runtime | legacy | Do not revive; extract trace fields for Evidence Pack/Run Graph | Core runtime drift | Keep classified as legacy | P1 |
| Agent memory | `platform/api/apps/agent/memory.py` | Automatic memory extraction/consolidation | legacy/reorient | Extract event/supersession schema only | Auto-promotion and agency memory | Block automatic promotion | P1 |
| Agent tools | `platform/api/apps/agent/tools.py` | Tool registry and web/RAG tools | reorient | Extract trusted sources and fetch-before-cite rule | Tool runtime drift | Move to `architecture_fr/knowledge_policy.md` | P1 |
| Hermes Console | `platform/api/apps/hermes_console/` | Runtime console and toggles | reorient | Future operations view; display first, mutations C3+ | Writes config without full approval path | Keep mutations inactive until approval wiring | P2/P3 |
| Alembic migrations | `platform/api/alembic/`, `alembic/` | Database migrations | to_verify | Keep only if supporting active Domain API or audited legacy data | Encodes old runtime assumptions | Audit migration chain before DB refactor | P1 |
| `modules.yaml` | `modules.yaml` | App/module enable registry | legacy | Do not extend as canonical registry | Reactivates old modules | Treat as legacy MVP stack control | P1 |
| Docker Compose | `docker-compose.yml` | Previous MVP stack | legacy | Keep until split OpenWebUI/Hermes/Pantheon compose exists | OpenWebUI points to Pantheon `/v1` | Document as legacy deployment | P1 |
| `.env.example` | `.env.example` | Environment template | keep | Keep after domain correction | Was `DOMAIN=architecture` | Set `DOMAIN=architecture_fr` | P0 |
| `CLAUDE.md` | `CLAUDE.md` | Claude guidance | keep after rewrite | Previously described autonomous runtime | Align with Pantheon Next doctrine | P0 |
| Installer UI | `scripts/install/ui/` | Installation interface | legacy | Archive or reorient after audit | Heavy UI before governance stabilized | Inspect before reuse | P2 |
| Legacy folder | `legacy/` | Archived components | archive | Keep non-imported | Accidental import | Add doctor check later | P2 |

---

## 4. Reclassification patterns

| Old runtime concept | Correct reclassification |
|---|---|
| Agent loop Pantheon | Task Contracts + abstract agents + Hermes execution |
| DecisionPlan | Task Contract |
| ExecutionResult | Evidence Pack |
| Tool registry | External Tools Policy |
| Workflow engine | Workflow definitions executed by Hermes |
| Scheduler | External scheduler or Hermes-side capability under approval |
| Provider router | Runtime/provider concern handled outside Pantheon governance |
| Patch auto-apply | Patch candidate + Evidence Pack + approval |
| Memory consolidation job | Memory candidate + C3 promotion review |
| Plugin manager | Policy + sandbox + allowlist/blocklist |
| Dashboard runtime | Domain snapshot + OpenWebUI display |
| Runtime traces | Evidence Pack + Run Graph fields |
| RAG | Knowledge retrieval capability, not memory |

---

## 5. Hard blockers

The following must not be reactivated inside Pantheon Next:

```text
Execution Engine
Agent Runtime
Tool Runtime
LLM Provider Router
Scheduler
LangGraph central orchestrator
memory auto-promotion
agency memory
self-evolution auto-merge
plugin batch install
Docker socket access
secret access by default
public admin dashboard without auth/VPN
```

---

## 6. Evidence required for audit decisions

Every audit decision must identify:

- files read;
- imports checked;
- active routes checked;
- configuration files checked;
- commands run, if any;
- risk level;
- proposed decision;
- rollback or archive path.

Consequential decisions require an Evidence Pack.

Reference:

```text
docs/governance/EVIDENCE_PACK.md
```

---

## 7. Next action

Recommended next audit:

```text
repo_md_audit → code_audit_post_pivot → targeted code cleanup branch
```

Code cleanup should start only after the documentation changes in this register are merged.
