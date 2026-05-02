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
| FastAPI entrypoint | `platform/api/main.py` | API entrypoint | keep | Keep as lightweight Pantheon Next Domain Layer API entrypoint | May drift into runtime if execution endpoints are added | Do not add agent/tool execution endpoints | P0 |
| Domain Layer package | `platform/api/pantheon_domain/` | Domain API definitions | keep | Keep as read-only domain snapshot and approval classification surface | Low | Continue aligning terminology with Pantheon Next | P0 |
| Domain contracts | `platform/api/pantheon_domain/contracts.py` | Pydantic domain definitions | keep | Keep as definition contracts for agents, skills, workflows, memory, knowledge, legacy | Needs C0-C5 alignment | Add explicit C0-C5 mapping later | P1 |
| Domain repository | `platform/api/pantheon_domain/repository.py` | Static in-code registry | keep | Keep as bootstrap registry until file-backed registry exists | Legacy `agency_memory` / `generic` terminology fixed in PR #70 | Continue monitoring for stale terminology | P0 |
| Context export package | `platform/api/pantheon_context/` | Read-only context pack endpoint | keep | Use for new imports and keep endpoint `/runtime/context-pack` | Must remain context-only | Do not add execution endpoints | P0 |
| Runtime compatibility shim | `platform/api/pantheon_runtime/` | Former context-pack package name | reorient | Keep only as backward-compatible shim re-exporting `pantheon_context.router` | Package name suggests runtime | Do not add routes or logic; remove later only after import audit | P0 |
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
| Docker Compose | `docker-compose.yml` | Previous MVP stack | legacy | Keep as documented legacy MVP wiring until split OpenWebUI/Hermes/Pantheon compose exists | OpenWebUI still points to Pantheon `/v1` in legacy compose; shared DB remains legacy | Do not use as final target deployment model | P1 |
| `.env.example` | `.env.example` | Environment template | keep | Keep after domain correction | `DOMAIN=architecture_fr` fixed | Monitor future env templates | P0 |
| `CLAUDE.md` | `CLAUDE.md` | Claude guidance | keep after rewrite | Previously described autonomous runtime | Aligned with Pantheon Next doctrine | P0 |
| Installer UI | `scripts/install/ui/` | Installation interface | legacy | Archive or reorient after audit | Heavy UI before governance stabilized | Inspect before reuse | P2 |
| Legacy folder | `legacy/` | Archived components | archive | Keep non-imported | Accidental import | Add doctor check later | P2 |

---

## 4. Context export boundary note

New imports must use:

```text
pantheon_context.router
```

The legacy package:

```text
pantheon_runtime.router
```

is retained only as a compatibility shim.

Rules:

```text
No task execution.
No tool execution.
No workflow execution.
No memory promotion.
No scheduling.
No provider routing.
```

The public endpoint remains:

```text
/runtime/context-pack
```

---

## 5. Deployment boundary note

`docker-compose.yml` is explicitly legacy MVP wiring.

It currently preserves:

```text
OpenWebUI → Pantheon API /v1
shared PostgreSQL database
local Ollama
legacy FastAPI apps
```

Target deployment remains:

```text
OpenWebUI → Hermes Agent Gateway → Pantheon Context Pack / Domain API
```

Future split should create separate stacks or services for:

```text
Pantheon Domain API
Hermes Lab / Gateway
OpenWebUI bridge
OpenWebUI database
Pantheon database
```

---

## 6. Reclassification patterns

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

## 7. Hard blockers

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

## 8. Evidence required for audit decisions

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

## 9. Next action

Recommended next audit:

```text
repo_md_audit → code_audit_post_pivot → targeted code cleanup branch
```

Code cleanup should start only after the documentation changes in this register are merged.

---

## 10. CI / test breakage diagnostic (2026-05-02)

This section records the post-pivot state of the repository CI. It classifies
the breakage and proposes the safe next actions.

### 10.1 Lint job

Workflow: `.github/workflows/ci.yml` → job `Lint`.

```text
ruff check    platform/api/ tests/   → passes
ruff format --check platform/api/ tests/ → 4 files would be reformatted
```

Affected files:

```text
platform/api/apps/approvals/router.py
platform/api/core/contracts/manifest.py
platform/api/pantheon_domain/repository.py
tests/test_manifest_loader.py
```

Cause: cosmetic line-length / wrap drift. No behavior change.

Classification:

| Field | Value |
|---|---|
| Status | `keep` |
| Approval level | C3 (file mutation, candidate patch on a branch) |
| Risk | none beyond cosmetic |
| Proposed action | apply `ruff format platform/api/ tests/` |

### 10.2 Tests job

Workflow: `.github/workflows/ci.yml` → job `Tests`.

```text
pytest tests/ -q --cov-fail-under=30 -x
```

Cause: stale `modules.*` import paths in test mocks after the recent
top-level `modules/ → workflows/` reorganization. The pytest fixture
context (`PYTHONPATH=platform/api`) means the active code namespace is
now `apps.*`, not `modules.*`.

Confirmed pattern in 7 test files:

| Test file | Stale patch target | Current location | Notes |
|---|---|---|---|
| `tests/test_guards.py` | `modules.guards.service.LlmService.extract` | `apps.guards.service` (imports `LlmService` from `core.services.llm_service`) | rename `modules` → `apps` |
| `tests/test_guards.py` | `modules.agent.memory.LlmService` | `apps.agent.memory` | rename `modules` → `apps` |
| `tests/test_memory.py` | `modules.agent.memory.LlmService` | `apps.agent.memory` | rename `modules` → `apps` |
| `tests/test_webhooks.py` | `modules.webhooks.router.run_agent` | `apps.webhooks.router` (imports `run_agent` from `apps.agent.service`) | rename `modules` → `apps` |
| `tests/test_orchestra.py` | `modules.orchestra.router.run_orchestra` / `get_queue` | `apps.orchestra.router` | rename `modules` → `apps` |
| `tests/test_meeting.py` | `modules.meeting.service._llm` | `apps.meeting.service` | rename `modules` → `apps` |
| `tests/test_capture.py` | `modules.capture.router.StorageService.upload` / `transcribe_audio` | `apps.capture.router` | rename `modules` → `apps` |
| `tests/test_capture.py` | `modules.capture.service.process_capture` | `apps.capture.service` | rename `modules` → `apps` |
| `tests/test_capture.py` | `modules.capture.service.run_agent` | `apps.capture.service` imports `run_agent` **inside** `process_capture` (line 92), so the module-level attribute does not exist | architectural — patch should target `apps.agent.service.run_agent` instead |

Note on `tests/conftest.py`: the reference to `modules.yaml` (line 129) is
the YAML config file at repository root, not a Python module. It is
unaffected by the reorganization.

Classification:

| Field | Value |
|---|---|
| Status | `to_verify` |
| Approval level | C3 (test patches mutate test files only) |
| Risk | mostly mechanical, but `tests/test_capture.py::run_agent` patch needs an architectural decision (rebind to `apps.agent.service.run_agent`) |
| Proposed action | open a follow-up branch `work/<agent>/ci-tests-modules-rename`, apply per-file rename, verify each `patch()` target exists at module level after rename, run pytest collection then full suite under CI services |

### 10.3 Coverage gate

The `--cov-fail-under=30` threshold may compound the test breakage. Once
the import-path issues are fixed, coverage may still fall below 30% if a
significant fraction of tests still fails at runtime (services, fixtures,
data). The coverage gate is **not** itself a bug; it is a quality gate
that will need attention after the import fix.

### 10.4 Security audit job

`Security audit` (pip-audit) is **passing**. No action needed.

### 10.5 OpenClaw regression job

`OpenClaw regression` is **skipped** on non-`main`/`develop` branches by
design (`if: github.ref == 'refs/heads/main' || ...`). No action needed.

### 10.6 Summary

| Job | Status on `main` HEAD | Cause | Decision |
|---|---|---|---|
| Lint | failure | `ruff format` drift in 4 files | apply `ruff format` (this PR) |
| Tests | failure | stale `modules.*` import paths in 7 test files post-reorg | follow-up PR after per-symbol mapping |
| Security audit | success | — | none |
| OpenClaw regression | skipped | branch filter | none |
