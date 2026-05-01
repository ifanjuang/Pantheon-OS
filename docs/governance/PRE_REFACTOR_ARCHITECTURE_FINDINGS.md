# PRE-REFACTOR ARCHITECTURE FINDINGS — Pantheon Next

> Read-only audit synthesis before any structural refactor.
> Purpose: identify useful existing code assets that should influence the target architecture without reviving the former autonomous runtime.

---

## 1. Decision frame

Pantheon Next remains a governed domain layer.

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

This document does not authorize implementation. It records useful existing assets to preserve, reclassify or reject before refactor.

---

## 2. Assets to preserve or reclassify

| Asset | Current path | Architectural value | Decision | Priority |
|---|---|---|---|---|
| Domain Layer API | `platform/api/main.py`, `platform/api/pantheon_domain/` | Lightweight exposure of agents, skills, workflows, memory, knowledge, legacy and approval classification | keep | P0 |
| Context Pack endpoint | `platform/api/pantheon_runtime/router.py` | Runtime-facing orientation pack for Hermes/OpenWebUI | reorient as context export | P0 |
| Domain contracts | `platform/api/pantheon_domain/contracts.py` | Pydantic definitions for domain snapshot, agents, skills, workflows, memory, knowledge and legacy | keep | P0/P1 |
| Bootstrap repository | `platform/api/pantheon_domain/repository.py` | Temporary read-only registry while legacy audit is incomplete | keep but correct terminology | P0/P1 |
| Manifest contracts | `platform/api/core/contracts/manifest.py` | Component manifest with type, risk profile, side effects, tools and approval fields | reorient as schema source | P1 |
| Task/workflow contracts | `platform/api/core/contracts/tasks.py` | TaskDefinition, WorkflowDefinition, workflow patterns and dependency validation | reorient as schema source | P1 |
| Workflow loader | `platform/api/core/registries/workflows.py` | Reads `workflow.yaml` + `tasks.yaml` and validates dependencies | reorient as documentation validator | P1/P2 |
| Approval app | `platform/api/apps/approvals/` | Approval queue with create, list, decide, expire and escalate | reorient as future Approval Queue | P1 |
| Hybrid RAG | `platform/api/core/services/rag_service.py` | pgvector + PostgreSQL FTS + RRF, adaptive chunking, contextual retrieval, rerank | preserve as Knowledge capability pattern | P2 |
| OCR fallback | `platform/api/core/services/ocr_service.py` | Vision/OCR fallback for scanned PDFs and images | external capability under policy | P2 |
| LLM structured extraction | `platform/api/core/services/llm_service.py` | OpenAI/Ollama wrapper and Instructor/Pydantic extraction | preserve as schema-validation pattern | P1/P2 |
| Circuit breaker | `platform/api/core/circuit_breaker.py` | fail-fast provider resilience, Redis optional state | preserve for operations/resilience | P2 |
| Document ingestion | `platform/api/apps/documents/` | upload, MIME/size validation, storage, ingestion and deletion | reorient under task contract | P1/P2 |
| Storage wrapper | `platform/api/core/services/storage_service.py` | MinIO/S3 wrapper with retries and object keys | future document storage pattern | P2 |
| Agent run telemetry | `platform/api/apps/agent/service.py` | steps, sources, iterations, duration, errors | reuse for Evidence Pack and Run Graph fields | P1/P2 |
| Agent memory model | `platform/api/apps/agent/memory.py` | categories, deduplication, valid_until, superseded_by | reclassify as memory candidate schema only | P1/P2 |
| Trusted source list | `platform/api/apps/agent/tools.py` | professional source whitelist and fetch-before-cite rule | preserve in `architecture_fr/knowledge_policy.md` | P1 |
| Hermes Console | `platform/api/apps/hermes_console/` | agents/skills/workflows/logs/settings/dashboard operations view | reorient; mutations require approval | P2/P3 |
| Hermes skill policy | `hermes/skill_policy.md` | lifecycle, XP, quarantine, mapping to Hermes skills | move into `SKILL_LIFECYCLE.md` | P1 |
| External skill repos classification | `hermes/external_skill_repos.md` | external repository decision model and retained patterns | align with `EXTERNAL_TOOLS_POLICY.md` | P1 |
| Adaptive orchestration candidate | `domains/general/skills/adaptive_orchestration/` | preflight, adaptation, signals, reports and candidate updates | retain as candidate; avoid runtime drift | P1 |
| Project context resolution candidate | `domains/general/skills/project_context_resolution/` | project detection, aliases, Knowledge Registry, Notion read-only policy | retain as candidate; make project workflows use it | P1 |

---

## 3. Corrections required before refactor

| Element | Problem | Required correction | Priority |
|---|---|---|---|
| `pantheon_runtime` package name | suggests Pantheon owns runtime | document as context export only; do not add execution endpoints | P0 |
| `agency_memory` in code/docs | obsolete term | use `system_memory` | P0 |
| `generic` skill domain | obsolete naming | use `general` | P0 |
| `.env.example` domain | `DOMAIN=architecture` | use `DOMAIN=architecture_fr` | P0 |
| OpenWebUI compose target | points to Pantheon `/v1` API | target should be Hermes Gateway, not Pantheon API | P1 |
| shared OpenWebUI/Pantheon DB in compose | authority and data boundary ambiguity | split or explicitly document as legacy MVP stack | P1 |
| auto THEMIS after upload | uncontracted analysis side effect | replace by ingestion review task contract | P1 |
| auto memory extraction/promotion | violates candidate-first memory | convert to memory candidates only | P1 |
| `CLAUDE.md` | still describes autonomous runtime architecture | rewrite as Pantheon Next guidance | P0 |
| `modules.yaml` | old runtime registry | keep as legacy until audited | P1 |

---

## 4. Patterns to extract into governance

### 4.1 Manifest quality model

Useful fields:

```text
id
type
version
dependencies
inputs
outputs
risk_profile
side_effect_profile
approval_required_if
tools
behavior
```

Target files:

```text
SKILL_LIFECYCLE.md
WORKFLOW_SCHEMA.md
EXTERNAL_TOOLS_POLICY.md
operations/doctor.md
```

### 4.2 Task and workflow schema

Useful patterns:

```text
solo
parallel
cascade
arena
```

Secondary patterns:

```text
crew
flow
conditional
```

Required correction:

```text
TaskCriticity must support C0-C5, not only C1-C5.
```

### 4.3 Evidence trace model

Useful fields from existing agent runs:

```text
steps
sources
tool_calls
tool_outputs
iterations
duration_ms
errors
status
```

These fields should inform Evidence Pack and Run Graph design, not preserve the old ReAct runtime.

### 4.4 Memory supersession model

Useful fields:

```text
category
scope
source_run_id
valid_until
superseded_by
```

Required rule:

```text
No automatic memory promotion.
No LLM consolidation without Evidence Pack and C3 review.
```

### 4.5 Knowledge retrieval model

Useful Knowledge engine features:

```text
adaptive chunking by document type
SentenceWindow for CCTP/DTU
semantic search via pgvector
full-text search via PostgreSQL
RRF fusion
source_type filtering
fetch-before-cite discipline
```

Target classification:

```text
Knowledge/RAG capability, not Pantheon memory.
```

---

## 5. Components not to revive

The following must not be reactivated as Pantheon core:

```text
AgentService ReAct loop
openai_compat as OpenWebUI target backend
modules.yaml as canonical module registry
auto THEMIS analysis after document upload
auto memory extraction and agency promotion
Hermes Console toggles without approval
provider router inside Pantheon
scheduler inside Pantheon
LangGraph central orchestrator inside Pantheon
ARQ/Redis worker path as required core
```

---

## 6. Documentation updates triggered by this audit

| File | Required update |
|---|---|
| `ARCHITECTURE.md` | reference this document as pre-refactor asset map |
| `CODE_AUDIT_POST_PIVOT.md` | classify assets keep/reorient/legacy |
| `ROADMAP.md` | add schema docs to P1/P2 |
| `MODULES.md` | reflect workflow schema, skill lifecycle and trusted sources |
| `MEMORY.md` | reference memory event schema and supersession fields |
| `CLAUDE.md` | align with Pantheon Next doctrine |
| `.env.example` | set `DOMAIN=architecture_fr` |

---

## 7. Final rule

```text
Extract contracts, schemas, patterns, evidence and guardrails.
Do not extract the old runtime as Pantheon core.
```
