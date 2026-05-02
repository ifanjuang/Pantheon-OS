# Pantheon Next — Project Status

> Source of truth for the current project state after the Hermes-backed pivot.
> Governance Markdown files drive development under `docs/governance/`.

Last update: 2026-05-02

---

## 1. Structural decision

Status: ✅ Documented and still active.

Pantheon Next follows a Hermes-backed architecture.

```text
OpenWebUI = user cockpit + Knowledge surface + human validation
Hermes Agent = execution runtime + executable skills + tools
Pantheon Next = governed domain authority + source of truth + domain definitions
```

Canonical formula:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

This replaces the former direction where Pantheon would become a full autonomous agent runtime.

Pantheon must not silently recreate:

```text
Execution Engine
Agent Runtime
Tool Runtime
LLM Provider Router
custom scheduler
autonomous memory promotion
self-evolution auto-merge
uncontrolled plugin installation
```

---

## 2. Current global status

| Element | Status | Comment |
|---|---|---|
| Pantheon Next naming | ✅ Updated | README uses Pantheon Next as product name |
| Hermes-backed pivot | ✅ Done | Direction validated: Pantheon governance + Hermes runtime + OpenWebUI cockpit |
| `docs/governance/` | ✅ Canonical | Governance documents live under `docs/governance/` |
| `ai_logs/` | ✅ Canonical | AI intervention logs use one file per session |
| README | ✅ Updated | Product entry point rewritten for Pantheon Next |
| `docs/governance/README.md` | ✅ Updated | Index includes current governance docs |
| `ARCHITECTURE.md` | ✅ Updated | References the OpenWebUI / Hermes / Pantheon operating protocol |
| `MODULES.md` | ✅ Present | Must still be verified against actual domain folders before refactor |
| `AGENTS.md` | ✅ Present | Must stay non-runtime and approval/evidence-aware |
| `MEMORY.md` | ✅ Present | Canonical memory doctrine clarified; runtime incomplete |
| `APPROVALS.md` | ✅ Done | Defines C0-C5 criticality and approval levels |
| `TASK_CONTRACTS.md` | ✅ Done | Defines task contract schema and first contracts |
| `EVIDENCE_PACK.md` | ✅ Done | Defines evidence schema and mandatory use cases |
| `HERMES_INTEGRATION.md` | ✅ Done | Defines Hermes/Pantheon boundary and context export rules |
| `OPENWEBUI_INTEGRATION.md` | ✅ Added | Defines OpenWebUI cockpit, Knowledge and validation boundary |
| `OPENWEBUI_DOMAIN_MAPPING.md` | ✅ Added | Maps Pantheon domains to OpenWebUI Knowledge, Models and operator Skills |
| `MODEL_ROUTING_POLICY.md` | ✅ Added | Defines Ollama/OpenWebUI/Hermes model routing policy without a Pantheon router |
| `EXTERNAL_TOOLS_POLICY.md` | ✅ Done | Defines external tool classification and allowlist policy |
| `EXTERNAL_RUNTIME_OPTIONS.md` | ✅ Added | Classifies LangChain, Langflow, OpenClaw, Symphony, Graphify, CTX, Binderly, NeverWrite and related options |
| `EXTERNAL_AI_OPTION_REVIEWS.md` | ✅ Added | Classifies AnimoCerebro and Caliber/ai-setup |
| `KNOWLEDGE_TAXONOMY.md` | ✅ Done | Defines Knowledge layers, reliability levels and source tiers |
| `CODE_AUDIT_POST_PIVOT.md` | ✅ Added | Initial register for legacy/runtime component classification |
| `WORKFLOW_SCHEMA.md` | ✅ Added | Canonical workflow/task definition schema exists |
| `SKILL_LIFECYCLE.md` | ✅ Added | Skill lifecycle, XP/status and Hermes mapping policy exists |
| `MEMORY_EVENT_SCHEMA.md` | ✅ Added | Memory event/candidate schema exists |
| `VERSIONS.md` | ✅ Added | Runtime/model version tracking exists |
| `operations/openwebui_hermes_pantheon.md` | ✅ Done | Defines authority model, flows, Context Pack, Evidence Pack, Run Graph, anti-loop |
| `operations/openwebui_manual_setup.md` | ✅ Added | Manual OpenWebUI setup checklist exists |
| `operations/doctor.md` | ✅ Added | Read-only operations doctor checklist exists |
| Runtime Context Pack endpoint | ✅ First static implementation | `GET /runtime/context-pack` exists, read-only/static |
| API smoke tests | ✅ Added | `tests/test_api_smoke.py` added; local/CI execution still required |
| Hermes `pantheon-os` local skill | ✅ Template added | Template exists under `hermes/templates/pantheon-os/`; not installed locally |
| `domains/general` | ✅ Started | First invariant domain created |
| `domains/architecture_fr` | 🔄 Targeted | Main business domain; first workflows still to create/verify |
| `domains/software` | 🔄 Targeted | Audit/governance domain to verify in repo |
| `adaptive_orchestration` skill | ✅ Candidate | Created under `domains/general/skills/adaptive_orchestration/` |
| `project_context_resolution` skill | ✅ Candidate | Created under `domains/general/skills/project_context_resolution/` |
| OpenWebUI Knowledge Strategy | 🔄 Planned | Requires Knowledge Registry, Knowledge Selection and source metadata |
| Validated Pantheon memory | 🔄 Model clarified | Levels: session, candidates, project, system; runtime incomplete |
| Legacy FastAPI runtime | ⚠️ Legacy to audit | Existing autonomous runtime components must not be deleted without audit |
| Tests | ⚠️ Not executed here | Local/CI execution still required |

---

## 3. OpenWebUI / Hermes / Pantheon interaction layer

Status: 🔄 Planned, partially documented.

Current rule:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

Important deployment interpretation:

```text
OpenWebUI should point to Hermes Agent Gateway.
Pantheon API is a governance/context API, not an OpenAI-compatible model backend.
```

Documented components:

| Component | Status | Reference |
|---|---|---|
| OpenWebUI cockpit boundary | ✅ Documented | `OPENWEBUI_INTEGRATION.md` |
| OpenWebUI domain mapping | ✅ Documented | `OPENWEBUI_DOMAIN_MAPPING.md` |
| Manual OpenWebUI setup | ✅ Documented | `operations/openwebui_manual_setup.md` |
| Model routing policy | ✅ Documented | `MODEL_ROUTING_POLICY.md` + `config/model_routing.example.yaml` |
| Hermes integration boundary | ✅ Documented | `HERMES_INTEGRATION.md` |
| Hermes `pantheon-os` skill template | ✅ Added | `hermes/templates/pantheon-os/` |
| Pantheon Context Pack | ✅ First static implementation | `GET /runtime/context-pack` |
| Task Contract | ✅ Documented | `TASK_CONTRACTS.md` |
| Evidence Pack | ✅ Documented | `EVIDENCE_PACK.md` |
| Approval policy | ✅ Documented | `APPROVALS.md` |
| Operations Doctor | ✅ Documented | `operations/doctor.md` |

Planned or incomplete:

| Component | Status | Target |
|---|---|---|
| OpenWebUI Router Pipe | ⬜ Planned | Route user requests to Hermes Gateway with Pantheon context/contract constraints |
| OpenWebUI Actions | ⬜ Planned | View Evidence, approve, reject, request rerun or clarification |
| OpenWebUI Evidence display | ⬜ Planned | Display Evidence Pack summaries and approval requests |
| ConsultationRequest / ConsultationResult | ⬜ Planned | Govern Pantheon ↔ Hermes delegation |
| Run Graph | ⬜ Planned | Display agents, consultations, warnings, vetoes and approvals |
| Hermes Result Scorecard | ⬜ Planned | Source, execution, scope, governance and reuse confidence |
| Dynamic Knowledge Registry | ⬜ Planned | Align OpenWebUI Knowledge names, source tiers, privacy levels and freshness policy |

Not implemented yet:

```text
automatic Pantheon → Hermes task execution
OpenWebUI custom sidebar / Actions
persistent run graph storage
canonical skill promotion runtime
memory promotion runtime
automated PR workflow
Notion connector
dynamic Knowledge Registry
```

---

## 4. Documentation / code coherence

### 4.1 Documentation

Status: ✅ Stronger, but still requires audit against the tree.

Reliable now:

```text
README.md
CLAUDE.md
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
docs/governance/KNOWLEDGE_TAXONOMY.md
docs/governance/CODE_AUDIT_POST_PIVOT.md
docs/governance/WORKFLOW_SCHEMA.md
docs/governance/SKILL_LIFECYCLE.md
docs/governance/MEMORY_EVENT_SCHEMA.md
operations/openwebui_hermes_pantheon.md
operations/openwebui_manual_setup.md
operations/doctor.md
```

Still to align or verify:

```text
ROADMAP.md must stay synchronized after each governance addition.
AGENTS.md must remain explicit that agents are abstract roles, not autonomous workers.
MEMORY.md must keep C3 + Evidence Pack promotion as non-negotiable.
CODE_AUDIT_POST_PIVOT.md must be completed by real tree audit.
Domain folder contents must be verified against MODULES.md.
OpenWebUI/Hermes live wiring remains to verify outside the repo docs.
```

### 4.2 Code

Status: 🔄 First aligned layer exists, still partial.

Current API entrypoint:

```text
platform/api/main.py
```

Existing Domain Layer package:

```text
platform/api/pantheon_domain/
```

Runtime context package:

```text
platform/api/pantheon_runtime/
```

Interpretation:

```text
`pantheon_runtime` currently exposes static context-pack functionality.
It must not be extended into an autonomous Pantheon runtime without documented approval.
```

Known endpoints:

```text
/health
/runtime/context-pack
/domain/health
/domain/snapshot
/domain/agents
/domain/skills
/domain/workflows
/domain/memory
/domain/knowledge
/domain/legacy
/domain/approval/classify
```

Smoke tests added:

```text
tests/test_api_smoke.py
```

Tests still need to be executed locally or in CI.

---

## 5. Memory model

Status: ✅ Doctrine clarified, runtime incomplete.

```text
session    = temporary context
candidates = persisted but not validated
project    = validated project context
system     = validated reusable rules, methods and patterns
```

Cycle:

```text
SESSION → CANDIDATES → Evidence Pack → validation → PROJECT or SYSTEM
```

Rules:

```text
No automatic promotion.
Use system memory, not agency memory.
Memory promotion is at least C3 and requires Evidence Pack review.
OpenWebUI Knowledge is not Pantheon memory.
Hermes local memory is not Pantheon memory.
```

---

## 6. Knowledge / document strategy

Status: 🔄 Planned, with mapping now documented.

Current target:

```text
NAS folders
→ OpenWebUI Knowledge Bases
→ retrieval
→ Pantheon Knowledge Registry
→ Knowledge Selection
→ Evidence Pack
→ Memory candidates only after validation
```

Reference:

```text
KNOWLEDGE_TAXONOMY.md
OPENWEBUI_INTEGRATION.md
OPENWEBUI_DOMAIN_MAPPING.md
operations/openwebui_manual_setup.md
```

Current gap:

```text
knowledge/registry.yaml is not created yet.
Knowledge Selection candidate skill is not created yet.
```

---

## 7. Candidate skills and workflows

Existing candidate skills:

```text
domains/general/skills/adaptive_orchestration/
domains/general/skills/project_context_resolution/
```

Status: ✅ Candidate.

First business-domain target:

```text
quote_vs_cctp_analysis / quote_vs_cctp_review
```

Status: ⬜ Not created yet.

Target domain:

```text
domains/architecture_fr/
```

---

## 8. External options and tool governance

Status: ✅ Strongly documented; no integration performed.

Current external classification docs:

```text
EXTERNAL_TOOLS_POLICY.md
EXTERNAL_RUNTIME_OPTIONS.md
EXTERNAL_AI_OPTION_REVIEWS.md
```

Classified options include:

```text
Stirling-PDF
SearXNG
OpenWebUI extensions
Hermes plugins
Cycles / runcycles
Omnigraph
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
Unknown external tools are blocked until classified.
External runtimes may assist Pantheon but must not become Pantheon.
OpenClaw and AnimoCerebro are not Pantheon core.
LangChain/LangGraph are only allowed as Hermes-side library options later.
Langflow is lab-only.
Caliber is test_read_only and inspiration for Doctor/config parity.
Symphony is watch/rejected_for_core and inspiration for lifecycle/workspace/proof-of-work only.
Graphify is test_read_only for possible repo/docs graph audit.
```

---

## 9. Legacy components

Status: ⚠️ Present, not deleted.

Reference:

```text
CODE_AUDIT_POST_PIVOT.md
operations/doctor.md
```

Legacy elements still need audit:

```text
old dynamic module registry
modules.yaml
previous workflow loader
initial approval API
Alembic approval migration
Installer UI
old tests tied to autonomous runtime assumptions
naming and purpose of platform/api/pantheon_runtime/
```

Rule:

```text
Do not delete before diagnosis.
Do not reactivate the autonomous runtime path by accident.
```

---

## 10. Immediate action list

### P0 — completed governance base

1. ✅ Governance docs under `docs/governance/`.
2. ✅ AI logs convention under `ai_logs/`.
3. ✅ Static `GET /runtime/context-pack` endpoint created.
4. ✅ Hermes `pantheon-os` local skill template created.
5. ✅ `APPROVALS.md` added.
6. ✅ `TASK_CONTRACTS.md` added.
7. ✅ `EVIDENCE_PACK.md` added.
8. ✅ `HERMES_INTEGRATION.md` added.
9. ✅ `KNOWLEDGE_TAXONOMY.md` added.
10. ✅ `EXTERNAL_TOOLS_POLICY.md` added.
11. ✅ `OPENWEBUI_INTEGRATION.md` added.
12. ✅ `OPENWEBUI_DOMAIN_MAPPING.md` added.
13. ✅ `MODEL_ROUTING_POLICY.md` added.
14. ✅ `EXTERNAL_RUNTIME_OPTIONS.md` added.
15. ✅ `EXTERNAL_AI_OPTION_REVIEWS.md` added.
16. ✅ `CODE_AUDIT_POST_PIVOT.md` initial register added.
17. ✅ README rewritten around Pantheon Next.
18. ✅ API smoke tests added.
19. ✅ `operations/openwebui_manual_setup.md` added.
20. ✅ `operations/doctor.md` added.

### P1 — next documentation/contracts

1. Run the Doctor checklist manually against the current tree.
2. Create `knowledge/registry.example.yaml` or `knowledge/registry.yaml`.
3. Create Knowledge Selection candidate skill.
4. Create Hermes context exports under `hermes/context/`.
5. Create/verify domain package rule files: `rules.md`, `knowledge_policy.md`, `output_formats.md`.
6. Create first `architecture_fr` skill/workflow: `quote_vs_cctp_review`.
7. Complete `CODE_AUDIT_POST_PIVOT.md` from a real tree audit.
8. Run `pytest tests/test_api_smoke.py` locally or in CI.
9. Define OpenWebUI Router Pipe specification.
10. Define OpenWebUI Actions specification.

### P2 — later implementation

1. Implement real ConsultationRequest / ConsultationResult.
2. Implement Run Graph storage.
3. Add run event stream.
4. Add Hermes result scorecard.
5. Add controlled PR workflow.
6. Evaluate whether `pantheon_runtime` should be renamed or documented as context export only.
7. Consider a read-only `operations/doctor.py` only after C3 approval.

---

## 11. Risks

| Risk | Status | Guardrail |
|---|---|---|
| Hermes becomes implicit authority | Active risk | Hermes outputs remain candidates |
| OpenWebUI becomes business engine | Active risk | OpenWebUI remains cockpit only |
| Pantheon duplicates Hermes runtime | Active risk | Pantheon governs, Hermes executes |
| Skill duplication | Active risk | Pantheon skill lifecycle + Hermes skill mapping |
| Memory pollution | Active risk | Candidate memory + validation only |
| Cross-project RAG contamination | Active risk | Knowledge Selection + source tiers |
| Legacy runtime confusion | Active risk | Legacy audit before reuse or deletion |
| Over-abstraction | Active risk | Documented gain required before new modules |
| Approval bypass | Active risk | C0-C5 policy in `APPROVALS.md` |
| Unsupported conclusions | Active risk | Evidence Pack required for consequential outputs |
| OpenWebUI misrouting | Active risk | OpenWebUI must point to Hermes Gateway, not Pantheon API |
| Public Hermes Dashboard exposure | Active risk | Local-only unless auth/VPN and explicit approval |
| Model fallback misuse | Active risk | `MODEL_ROUTING_POLICY.md` forbids silent C4/C5 fallback |
| External runtime drift | Active risk | `EXTERNAL_RUNTIME_OPTIONS.md` + `EXTERNAL_AI_OPTION_REVIEWS.md` |
| Doctor used as auto-fixer | Active risk | `operations/doctor.md` is read-only and report-only |

---

## 12. Final summary

Reliable now:

```text
Pantheon Next product direction
Hermes-backed direction
OpenWebUI / Hermes / Pantheon operating protocol
approval criticality policy
initial task contracts
Evidence Pack doctrine
Hermes integration doctrine
OpenWebUI integration doctrine
OpenWebUI domain mapping
model routing policy
external tools/runtime/AI option policies
Knowledge taxonomy
adaptive_orchestration candidate skill
project_context_resolution candidate skill
skill lifecycle / XP doctrine
static /runtime/context-pack endpoint
API smoke tests
initial code audit post-pivot register
manual OpenWebUI setup checklist
read-only Doctor checklist
```

Partial:

```text
Domain Layer API
Knowledge strategy
Hermes pantheon-os skill installation
OpenWebUI router/actions
legacy runtime classification
architecture_fr workflows
software domain verification
```

Not implemented yet:

```text
real Pantheon ↔ Hermes task execution
OpenWebUI router/actions
run graph runtime
consultation persistence
memory promotion runtime
skill promotion runtime
Notion connector
Knowledge Registry
completed post-pivot code audit
Doctor automation
```

Next logical step:

```text
Run the read-only Doctor checklist, then create the Knowledge Registry example.
```
