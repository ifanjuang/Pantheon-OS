# Legacy Runtime Audit — Pantheon Next

Date: 2026-05-11
Branch / ref: `work/claude/legacy-runtime-audit`
Mode: **C0 read-only** (no code change, no move, no refactor)
Operator: Claude (per Bloc 6 brief)

## 1. Scope and method

This audit answers the Bloc 6 brief of the Pantheon Next stabilization plan: identify components that *look* like the forbidden runtime concepts of `CODE_AUDIT_POST_PIVOT.md` §7, classify them with the brief vocabulary (`keep` / `document` / `move_to_legacy` / `refactor_later` / `delete_candidate` / `blocked_until_review`), and propose the **safe minimal action** for each.

The audit is strictly read-only. Nothing is deleted, moved, refactored or modified. The seven hard blockers from `CODE_AUDIT_POST_PIVOT.md` §7 are the categorisation axis:

```text
Execution Engine
Agent Runtime
Tool Runtime
LLM Provider Router
Scheduler
LangGraph central orchestrator
Memory auto-promotion
Plugin installer non gouverné
Runtime workflow loader ancien
Approval API ancienne
Installer UI ancienne
Tests liés à l'ancien runtime
```

Method:

1. Read `docs/governance/CODE_AUDIT_POST_PIVOT.md`, `docs/governance/PRE_REFACTOR_ARCHITECTURE_FINDINGS.md`, `docs/governance/STATUS.md`, `docs/governance/ARCHITECTURE.md`, `operations/doctor.md`.
2. Enumerate `platform/api/{apps,core,pantheon_domain,pantheon_context,pantheon_runtime}`, `scripts/install/ui/`, `legacy/`, `modules.yaml`, `plugins.yaml`, `docker-compose.yml`, `alembic/`, `tests/`.
3. Grep for `@router.post/put/patch/delete`, `langgraph`, `interrupt`, `StateGraph`, `Command`, `ARQ`, `enqueue_job`, `apscheduler`, `celery`.
4. Cross-reference each component with the existing classification table in `CODE_AUDIT_POST_PIVOT.md` §3.
5. Map the existing vocabulary (keep / reorient / archive / delete_later / to_verify / legacy) to the Bloc 6 vocabulary.

No code, no test, no migration was executed.

## 2. Vocabulary mapping

The brief introduces a slightly different vocabulary. The mapping used in this report:

| Brief term | Existing audit term | Meaning |
|---|---|---|
| `keep` | `keep` | Aligned with Pantheon Next; may stay active |
| `document` | `keep` / `reorient` | Stays today; needs explicit doctrine/contract framing |
| `move_to_legacy` | `legacy` | Belongs to former runtime; freeze, do not extend |
| `refactor_later` | `reorient` | Contains useful logic to reframe as governance, schema or Hermes-side |
| `delete_candidate` | `delete_later` | Obsolete on inspection; remove only after confirmation |
| `blocked_until_review` | `to_verify` | Requires explicit C3+ review before any change |

## 3. Findings summary

| Category (brief axis) | Components found | Highest risk |
|---|---:|---|
| Execution Engine | 2 | high |
| Agent Runtime | 4 | high |
| Tool Runtime | 2 | medium |
| LLM Provider Router | 1 | medium |
| Scheduler | 3 | high |
| LangGraph central orchestrator | 1 (10 files) | critical |
| Memory auto-promotion | 2 | high |
| Plugin installer non gouverné | 3 | medium |
| Runtime workflow loader ancien | 3 | medium |
| Approval API ancienne | 1 | medium |
| Installer UI ancienne | 1 | medium |
| Tests liés à l'ancien runtime | ≥ 12 files | low |

Net 0 deletions performed. Net 0 moves performed.

## 4. Classification table

Conventions: `path` is relative to repo root; `risk` is `low|medium|high|critical`; `status` is the brief vocabulary; `safe_minimal_action` always preserves the file on disk.

### 4.1 Execution Engine / Agent Runtime

| file | current role | risk | status | safe_minimal_action | impact_if_removed | impact_if_kept |
|---|---|---|---|---|---|---|
| `platform/api/apps/agent/service.py` | ReAct loop, central agent execution (`run_agent`) | high | `move_to_legacy` | Already classified `legacy` in `CODE_AUDIT_POST_PIVOT.md`; keep the file unimported by new code, do not extend, mine for Evidence Pack trace fields only | Capture pipeline (`apps/capture/service.py`) imports `run_agent`; webhooks trigger it; removing now breaks the legacy MVP path with no Hermes replacement wired up | Continued risk of being mistaken for a Pantheon execution surface; mitigated by Doctor `forbidden_endpoints_absent` check (only blocks /agents/run, /runtime/execute, /memory/promote/auto — does not block /agent/run) |
| `platform/api/apps/agent/router.py` | Exposes `POST /agent/run` and history endpoints | high | `move_to_legacy` | Document explicitly as legacy MVP route; do not promote to canonical Pantheon API; consider adding to Doctor `forbidden_endpoints_absent` once Hermes-backed execution is wired | Same as above: capture, webhooks and tests rely on it | Pantheon API still appears to "execute" agents in the legacy compose wiring |
| `platform/api/worker.v2.py` | ARQ worker for orchestra/agent jobs (renamed `.v2.py` to disable) | medium | `move_to_legacy` | Keep `.v2.py` suffix so the file is not auto-loaded; document as historical execution backbone | Background processing of orchestra/agent runs disappears; legacy compose `worker` service would fail to start if ever activated | Dormant code surface; suggests Pantheon owns a queue runtime |
| `platform/api/core/base_engine.py` | Abstract base for v2 graph engine | medium | `move_to_legacy` | Document next to `worker.v2.py`; do not import in new code; flag for archival after Hermes-side runtime is firmly external | Removing forces a follow-up cleanup of all `*.v2.py` modules in one PR | Confuses Pantheon with a runtime engine framework |

### 4.2 Tool Runtime

| file | current role | risk | status | safe_minimal_action | impact_if_removed | impact_if_kept |
|---|---|---|---|---|---|---|
| `platform/api/apps/agent/tools.py` | Tool registry + web/RAG/document tools used by `run_agent` | medium | `refactor_later` | Per `CODE_AUDIT_POST_PIVOT.md` §3: extract trusted sources and fetch-before-cite rule into `architecture_fr/knowledge_policy.md` (governance), keep file in place for legacy execution | Breaks `apps.agent.service.run_agent` and all dependent capture/webhooks/orchestra flows | Pantheon appears to own a tool runtime; mitigated by classification |
| `platform/api/core/base_tool.py` | Base class for tool implementations | medium | `refactor_later` | Re-classify as Hermes-side capability interface in `EXTERNAL_TOOLS_POLICY.md`; keep file for legacy compatibility | Same as above | Same as above |

### 4.3 LLM Provider Router

| file | current role | risk | status | safe_minimal_action | impact_if_removed | impact_if_kept |
|---|---|---|---|---|---|---|
| `platform/api/core/services/llm_service.py` | OpenAI/Ollama client wrapper, Instructor-based extraction, fallback model logic | medium | `refactor_later` | Already classified `reorient`. Keep as a structured-extraction pattern, document that provider routing must live outside Pantheon governance (`MODEL_ROUTING_POLICY.md`). Do not extend as the canonical provider router | Breaks every app that performs LLM-backed extraction (guards, agent, orchestra, capture, meeting, scoring, communications) | Pantheon appears to be the provider router; mitigated by `MODEL_ROUTING_POLICY.md` clarification |

### 4.4 Scheduler

| file | current role | risk | status | safe_minimal_action | impact_if_removed | impact_if_kept |
|---|---|---|---|---|---|---|
| `platform/api/core/queue.v2.py` | ARQ/Redis job queue (`.v2.py` → disabled) | high | `move_to_legacy` | Keep suffix; do not import in active code; document as legacy MVP scheduler | Reactivating legacy compose worker becomes impossible without a rewrite | Suggests Pantheon owns a scheduler runtime |
| `platform/api/core/checkpointer.v2.py` | LangGraph-style checkpointer (`.v2.py` → disabled) | high | `move_to_legacy` | Same as above; flag for explicit archival next to `core/base_engine.py` | Disables potential ARQ resume; no current consumer outside the disabled worker | Same as above |
| `platform/api/core/events.py` | Postgres LISTEN/NOTIFY event broadcaster | medium | `refactor_later` | Document as legacy event channel; classify under Hermes-side or operations responsibility | Removing breaks any code that imports `init_pool`/`close_pool`; conftest patches it as a no-op | Suggests Pantheon-side runtime eventing |

### 4.5 LangGraph central orchestrator

| file | current role | risk | status | safe_minimal_action | impact_if_removed | impact_if_kept |
|---|---|---|---|---|---|---|
| `platform/api/apps/orchestra/` (10 files; 3 159 lines) | Central LangGraph `StateGraph` with `interrupt`, `Command`, planner / executor / evaluator / synthesizer; exposes `POST /run`, `POST /run-hitl`, `POST /stream`, `POST /runs/{id}/approve` | **critical** | `blocked_until_review` | Not currently in `CODE_AUDIT_POST_PIVOT.md` §3 table. **Recommended new audit entry**: classify as `legacy` with a hard freeze ("Pantheon must not be a LangGraph central orchestrator", `CODE_AUDIT_POST_PIVOT.md` §7 + `PRE_REFACTOR_ARCHITECTURE_FINDINGS.md` §5). Do not extend, do not enable in `modules.yaml`. Consider adding `POST /orchestra/run` and `POST /orchestra/stream` to the Doctor `forbidden_endpoints_absent` list in a follow-up PR | Existing tests under `tests/test_orchestra.py` and webhook triggers (`apps/webhooks/router.py`) break; legacy compose stack loses its orchestration entrypoint | This is the most direct doctrine violation surface today: Pantheon ships a central LangGraph orchestrator with a HITL approve endpoint. Mitigated only by `modules.yaml` flag and lack of OpenWebUI wiring through Hermes Gateway |

### 4.6 Memory auto-promotion

| file | current role | risk | status | safe_minimal_action | impact_if_removed | impact_if_kept |
|---|---|---|---|---|---|---|
| `platform/api/apps/agent/memory.py` | `extract_and_store_memories`, LLM-driven extraction, auto-creates `scope=projet` / `scope=agence` rows after each agent run | high | `move_to_legacy` | Already classified `legacy/reorient`. Keep file in place; extract event/supersession schema only; never call from new code; map the data fields to `MEMORY_EVENT_SCHEMA.md` candidate path | `apps.agent.service.run_agent` calls `extract_and_store_memories` in its tail; removal breaks the legacy agent path | Auto-promotion of memory remains technically possible if anyone re-imports it |
| `platform/api/apps/memory/router.py` + `service.py` | CRUD over `AgentMemory` (scope=agence, scope=projet, scope=session) | high | `refactor_later` | Reclassify as candidate review API. The current `agence` scope reuses the forbidden `agency_memory` terminology — mark `MEMORY_EVENT_SCHEMA.md §2` as the canonical word (`system memory`) and plan a rename in a follow-up PR | Removes a working CRUD surface used by `apps/agent/memory.py`; legacy agent breaks | Forbidden `agency` terminology surfaces in tests and tables; Doctor cannot detect because path is `apps/memory/`, not `memory/agency/` |

### 4.7 Plugin installer non gouverné

| file | current role | risk | status | safe_minimal_action | impact_if_removed | impact_if_kept |
|---|---|---|---|---|---|---|
| `scripts/install/ui/installer_api.py`, `installer_runner.py`, `installer_state.py` | FastAPI installer UI for stacks, plugins, env. Listens on local port, enables/disables Docker profiles | medium | `move_to_legacy` | Already classified `legacy`. Document as archived MVP installer; do not extend; do not auto-start | Removes the only single-step install path for the legacy stack | A FastAPI surface labelled "installer" with mutation capability persists in the tree, even if unbound |
| `plugins.yaml` | Plugin registry (Ollama, Hermes Agent, Portainer, etc.) with `enabled: true/false` flags | medium | `refactor_later` | Already partly covered by `OPENWEBUI_PLUGIN_POLICY.md` and `EXTERNAL_TOOLS_POLICY.md`. Reframe as a Hermes-side / OpenWebUI plugin index. Do not let the installer mutate it without C3 approval | Compose `--profile` activation loses its source of truth | Pantheon appears to own a plugin lifecycle; mitigated by classification |
| `modules.yaml` | App/module enable registry consumed by `core/registry.py` | high | `move_to_legacy` | Already classified `legacy`. Document as MVP toggle file; do not extend; flag for replacement by file-backed Domain repository | Disabling drops every legacy MVP app at boot; Pantheon API would lose 24 routers | Confuses with canonical Pantheon module definition (`MODULES.md` is the authority) |

### 4.8 Runtime workflow loader ancien

| file | current role | risk | status | safe_minimal_action | impact_if_removed | impact_if_kept |
|---|---|---|---|---|---|---|
| `platform/api/core/registries/workflows.py` | Reads `workflow.yaml` + `tasks.yaml`, validates dependencies | medium | `refactor_later` | Already classified `reorient`. Keep pattern as documentation validator (governance schema); do not promote to runtime workflow loader | Removes static workflow validation used by tests | Could be mistaken for a workflow engine entry point |
| `platform/api/core/registries/loader.py` | Generic manifest loader | medium | `refactor_later` | Document as static manifest reader; align with `schemas/` validators added by Bloc 4 | Same as above | Same as above |
| `platform/api/core/registry.py` | Legacy dynamic module registry | high | `move_to_legacy` | Already classified `legacy`. Keep file unmodified; do not extend; flag for replacement by Domain repository | `modules.yaml` consumers break; legacy MVP app loading disappears | Suggests Pantheon owns a dynamic registry runtime |

### 4.9 Approval API ancienne

| file | current role | risk | status | safe_minimal_action | impact_if_removed | impact_if_kept |
|---|---|---|---|---|---|---|
| `platform/api/apps/approvals/router.py` + `service.py` + `models.py` + `schemas.py` | Approval queue: create, list, decide, expire, escalate | medium | `refactor_later` | Already classified `reorient`. Re-align reasoning fields with `APPROVALS.md` C0-C5 and Evidence Pack ; keep file in place ; do not extend the legacy "decide" route without C3 review | Breaks the existing approval queue tests (`tests/test_approval_contracts.py`) and the orchestra HITL `approve` route | Approval contract may drift from `APPROVALS.md` and Evidence Pack discipline |

### 4.10 Installer UI ancienne

See §4.7 — `scripts/install/ui/` is already classified `move_to_legacy`.

### 4.11 Tests liés à l'ancien runtime

| file | current role | risk | status | safe_minimal_action | impact_if_removed | impact_if_kept |
|---|---|---|---|---|---|---|
| `tests/test_agent.py` (alias `tests/test_agent_*.py` if any) | Tests for the legacy `run_agent` ReAct loop | low | `move_to_legacy` | Keep tests in place; they protect the legacy MVP path. Add a `pytestmark = pytest.mark.legacy_runtime` marker in a future PR for selective runs | CI loses regression coverage on the legacy agent runtime | Tests anchor the legacy runtime as if it were canonical |
| `tests/test_orchestra.py` | Tests the LangGraph orchestra runtime | low | `blocked_until_review` | Keep file untouched; reclassify orchestra itself first (§4.5), then decide whether to mark tests legacy or to remove them | Same as above | Same as above |
| `tests/test_webhooks.py` | Triggers `run_agent`/orchestra via webhooks | low | `move_to_legacy` | Same legacy marker plan as above | Webhooks regression coverage lost | Anchors legacy webhooks as canonical |
| `tests/test_memory.py` + `test_guards.py::TestMemoryPromotion` | Test memory extraction/promotion side of `apps.agent.memory` | low | `move_to_legacy` | Keep; mark legacy in a follow-up | Memory regression coverage lost | Anchors auto-promotion as if validated |
| `tests/test_capture.py`, `tests/test_meeting.py`, `tests/test_documents.py`, `tests/test_affaires.py`, `tests/test_auth.py` | MVP business CRUD via legacy apps | low | `document` | Keep as-is; document as MVP business coverage in CI | Coverage drops below 30% threshold | Tests do not strictly anchor runtime — they anchor business endpoints |
| `tests/test_document_analysis_workflow.py` | Calls auto THEMIS pipeline triggered after upload | low | `refactor_later` | Keep file; align with `PRE_REFACTOR_ARCHITECTURE_FINDINGS.md` §3 "auto THEMIS after upload" → ingestion review task contract | Coverage hole | Reinforces auto side-effect that the doctrine wants replaced |
| `tests/test_manifest_loader.py`, `tests/test_workflow_definition_loader.py` | Validate static loaders | low | `keep` | Keep as static loader regression | None | None |
| `tests/test_task_contracts.py` | Validate Task Contract shapes | low | `keep` | Keep as governance contract regression | None | None |
| `tests/test_api_smoke.py`, `tests/test_doctor_readonly.py`, `tests/test_governance_api.py`, `tests/test_governance_schemas.py` | Pantheon Next governance / API smoke | low | `keep` | Already aligned with Pantheon Next | None | None |
| `tests/test_circuit_breaker.py`, `tests/test_rag_advanced.py` | Resilience / RAG patterns | low | `refactor_later` | Keep; reclassify under Knowledge + operations resilience patterns | None | Reinforces legacy services as canonical |

## 5. Newly identified components not yet in `CODE_AUDIT_POST_PIVOT.md` §3

These rows should be added to `CODE_AUDIT_POST_PIVOT.md` §3 in a follow-up `docs:` PR (out of scope of this read-only audit).

| Component | Path | Former role | Proposed status (brief) | Risk | Priority |
|---|---|---|---|---|---|
| Orchestra LangGraph runtime | `platform/api/apps/orchestra/` | LangGraph `StateGraph` with HITL interrupts and `POST /run`, `POST /run-hitl`, `POST /stream`, `POST /runs/{id}/approve` | `blocked_until_review` | critical | P1 |
| Guards service (hybrid criticality + veto patterns) | `platform/api/apps/guards/` | Rule + LLM criticality classification and structured veto patterns | `refactor_later` (extract into `APPROVALS.md`/`EVIDENCE_PACK.md` patterns; do not run as auto-classification on incoming requests) | medium | P2 |
| Decisions / Planning / Chantier / Communications / Finance / Flowmanager / Scoring / Wiki | `platform/api/apps/{decisions,planning,chantier,communications,finance,flowmanager,scoring,wiki}/` | MVP business CRUD with POST/PUT/PATCH/DELETE routes | `document` (label as legacy MVP business surface; not Pantheon Next core) | medium | P2 |
| Capture / Meeting / Preprocessing | `platform/api/apps/{capture,meeting,preprocessing}/` | Upload + LLM extraction; calls into `run_agent` after upload | `refactor_later` (replace auto side-effect with ingestion-review Task Contract per `PRE_REFACTOR_ARCHITECTURE_FINDINGS.md` §3) | medium | P2 |
| Admin app | `platform/api/apps/admin/` | Admin operations | `blocked_until_review` | medium | P2 |
| Webhooks app | `platform/api/apps/webhooks/` | Webhook entrypoints + Telegram bot integration | `move_to_legacy` (trigger surface for the legacy runtime) | medium | P2 |
| Telegram bot | `platform/api/apps/webhooks/telegram.py` | Telegram integration imports `apps.agent.service.run_agent` | `move_to_legacy` | high | P2 |
| `worker.v2.py` / `core/queue.v2.py` / `core/checkpointer.v2.py` / `core/base_engine.py` | `platform/api/{worker.v2.py, core/queue.v2.py, core/checkpointer.v2.py, core/base_engine.py}` | V2 ARQ + LangGraph checkpointer scaffolding, disabled via `.v2.py` rename | `move_to_legacy` | medium | P2 |
| `evaluation` app | `platform/api/apps/evaluation/` | OpenClaw evaluation CLI + dataset scaffolding | `document` (used by CI; aligned with `EVALUATION.md`) | low | P2 |

## 6. Doctrine alignment notes

The brief lists three forbidden POST endpoints already monitored by the Doctor (`forbidden_endpoints_absent`):

```text
POST /agents/run
POST /runtime/execute
POST /memory/promote/auto
```

This audit observes that the actual legacy endpoints follow a different naming and therefore slip past the Doctor:

| Endpoint observed | Forbidden category | Doctor coverage today |
|---|---|---|
| `POST /agent/run` (no `s`) | Agent Runtime | not covered |
| `POST /orchestra/run`, `POST /orchestra/run-hitl`, `POST /orchestra/stream`, `POST /orchestra/runs/{id}/approve` | LangGraph central orchestrator | not covered |
| `POST /memory/...` (CRUD) | Memory auto-promotion | not directly covered |
| `POST /approvals/...` | Approval API ancienne | not covered |
| `POST /webhooks/...` | Trigger surface | not covered |

**Recommendation (follow-up PR, not this one)**: extend the Doctor `FORBIDDEN_ENDPOINTS` constant with the orchestra and agent-run patterns once classification §4.1 / §4.5 is reflected in `CODE_AUDIT_POST_PIVOT.md`. Out of scope for this read-only audit.

## 7. Hard blocker map

Each line below maps a `CODE_AUDIT_POST_PIVOT.md` §7 hard blocker to the components confirmed by this audit.

| Hard blocker | Confirmed components |
|---|---|
| Execution Engine | `apps/agent/service.py`, `apps/orchestra/service.py`, `worker.v2.py`, `core/base_engine.py` |
| Agent Runtime | `apps/agent/{service,router,memory,tools}.py` |
| Tool Runtime | `apps/agent/tools.py`, `core/base_tool.py` |
| LLM Provider Router | `core/services/llm_service.py` (partial — also a structured-extraction pattern) |
| Scheduler | `core/queue.v2.py`, `core/checkpointer.v2.py`, `core/events.py` (notify-based) |
| LangGraph central orchestrator | `apps/orchestra/` (10 files, 3 159 lines) |
| Memory auto-promotion | `apps/agent/memory.py`, `apps/memory/{router,service}.py` (the `scope=agence` row creation) |
| Plugin batch install | `scripts/install/ui/` + `plugins.yaml` |
| Docker socket access | Not observed in active code (good) |
| Secret access by default | Not observed (good) — secrets remain in `.env.example` placeholders |
| Public admin dashboard without auth/VPN | `apps/admin/` + `apps/hermes_console/` exist but auth-gated by `core/auth.py` |

## 8. Constraint compliance

| Constraint | Result |
|---|---|
| Ne rien supprimer | OK — no file removed |
| Ne rien déplacer | OK — no file moved |
| Ne rien refactorer | OK — no file modified |
| Ne pas modifier le runtime | OK — no source mutated |
| Lecture seule | OK — only `read_text`, `find`, `grep` used |
| Aucun appel réseau | OK |
| Aucun Docker | OK |
| Aucun secret | OK |
| Aucun outil destructif | OK |

## 9. Recommended next actions (out of scope for this PR)

The following follow-up PRs are recommended but **not** included here.

| Action | Type | Approval |
|---|---|---|
| Add the orchestra row + the 8 newly identified rows to `CODE_AUDIT_POST_PIVOT.md` §3 | `docs:` | C3 |
| Extend Doctor `FORBIDDEN_ENDPOINTS` with `/agent/run` and `/orchestra/*` once §3 update lands | `feat:` (small) | C3 |
| Rename `apps/memory/router.py` `scope=agence` enum value to `system` to align with `MEMORY_EVENT_SCHEMA.md §2` | `refactor:` | C3 |
| Add `@pytest.mark.legacy_runtime` markers to legacy-runtime tests for selective CI runs | `chore:` | C3 |
| Plan a Hermes-Gateway wiring PR that removes OpenWebUI → Pantheon `/v1` legacy route | `feat:` | C4 (deployment change) |

## 10. Evidence Pack

Read-only audit, minimum Evidence Pack per `EVIDENCE_PACK.md` §3.

```yaml
evidence_pack:
  id: EP-2026-LEGACY-RUNTIME-AUDIT-001
  task_id: legacy_runtime_audit_bloc6
  date: '2026-05-11'
  operator: claude_code
  files_read:
    - docs/governance/CODE_AUDIT_POST_PIVOT.md
    - docs/governance/PRE_REFACTOR_ARCHITECTURE_FINDINGS.md
    - docs/governance/STATUS.md
    - docs/governance/ARCHITECTURE.md
    - operations/doctor.md
    - platform/api/main.py
    - platform/api/apps/agent/{service,router,memory,tools}.py
    - platform/api/apps/orchestra/{service,_planner,_executor,_evaluator,_synthesizer,router}.py
    - platform/api/apps/memory/router.py
    - platform/api/apps/approvals/router.py
    - platform/api/apps/webhooks/router.py
    - platform/api/apps/webhooks/telegram.py
    - platform/api/core/{base_engine,registry,queue.v2,checkpointer.v2,events,base_tool}.py
    - platform/api/core/registries/{loader,workflows}.py
    - platform/api/core/services/{llm_service,rag_service,storage_service,ocr_service}.py
    - platform/api/worker.v2.py
    - scripts/install/ui/installer_*.py
    - modules.yaml
    - plugins.yaml
  sources_used: []
  commands_run:
    - find platform/api -type d
    - grep -rln "@router.(post|put|patch|delete)" platform/api/apps
    - grep -l "langgraph" platform/api -r
    - wc -l platform/api/apps/orchestra/*.py
  tools_used: []
  knowledge_bases_consulted: []
  documents_used:
    - docs/governance/CODE_AUDIT_POST_PIVOT.md
    - docs/governance/PRE_REFACTOR_ARCHITECTURE_FINDINGS.md
  assumptions:
    - "Brief vocabulary maps to existing audit terms per §2 of this report."
    - "`.v2.py` suffix is the project convention to disable a module at import time."
    - "Doctor `forbidden_endpoints_absent` covers only the three endpoints listed in operations/doctor.py."
  unsupported_claims:
    - "Live confirmation that orchestra's POST routes are not reachable from OpenWebUI today (compose stack not started during audit)."
  limitations:
    - "Audit is static: no service was started, no endpoint was hit."
    - "Risk levels are qualitative; not derived from a quantitative impact-analysis tool."
    - "Test classification §4.11 is non-exhaustive (10 entries selected from ~20 files in tests/)."
  outputs:
    - reports/code_audit/2026-05-11-legacy-runtime-audit.md
    - ai_logs/2026-05-11-legacy-runtime-audit.md
  approval_required:
    level: C0
    reason: "Read-only audit; report-only output."
  next_safe_action: "Open a docs: PR to add the §5 newly identified rows to CODE_AUDIT_POST_PIVOT.md §3, then a small feat: PR extending Doctor FORBIDDEN_ENDPOINTS. Both follow-ups are explicitly out of scope of this audit."
```

## 11. Final rule

```text
This audit observes and reports.
No file is deleted, moved, refactored or modified.
The Pantheon Next pivot remains the source of truth.
Legacy code is recorded, not reactivated.
```
