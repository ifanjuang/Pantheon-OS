# Pantheon Next — Project Status

> Source of truth for the current project state after the Hermes-backed pivot.
> Governance Markdown files drive development under `docs/governance/`.

Last update: 2026-05-04

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
LangGraph central orchestrator
workflow runtime hidden inside Pantheon
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
| README diagram asset registry | ✅ Added | `docs/assets/README.md` tracks Lucid sources and target export paths; PNG exports still missing on `main` |
| `docs/governance/README.md` | ✅ Updated | Index includes current governance docs |
| `ARCHITECTURE.md` | ✅ Updated | References the OpenWebUI / Hermes / Pantheon operating protocol |
| `MODULES.md` | ✅ Present | Still needs verification against actual domain folders after each domain package merge |
| `AGENTS.md` | ✅ Present | Must stay non-runtime and approval/evidence-aware; HEPHAISTOS/HEPHAESTUS spelling reconciliation remains open |
| `MEMORY.md` | ✅ Present | Canonical memory doctrine clarified; runtime incomplete |
| `APPROVALS.md` | ✅ Done | Defines C0-C5 criticality and approval levels |
| `TASK_CONTRACTS.md` | ✅ Done | Defines task contract schema and first contracts |
| `TASK_CONTRACT_REVISIONS.md` | ✅ Added | Addendum for single-role task contracts, revision signals, contract revisions, resume policy and reset-to-baseline |
| `EVIDENCE_PACK.md` | ✅ Done | Defines evidence schema and mandatory use cases |
| `HERMES_INTEGRATION.md` | ✅ Done | Defines Hermes/Pantheon boundary and context export rules |
| `OPENWEBUI_INTEGRATION.md` | ✅ Added | Defines OpenWebUI cockpit, Knowledge and validation boundary |
| `OPENWEBUI_DOMAIN_MAPPING.md` | ✅ Added | Maps Pantheon domains to OpenWebUI Knowledge, Models and operator Skills |
| `MODEL_ROUTING_POLICY.md` | ✅ Added | Defines Ollama/OpenWebUI/Hermes model routing policy without a Pantheon router |
| `EXTERNAL_TOOLS_POLICY.md` | ✅ Done | Defines external tool classification and allowlist policy, including n8n as external automation orchestrator |
| `EXTERNAL_RUNTIME_OPTIONS.md` | ✅ Added | Classifies optional runtimes, workflow labs, context engines and graph/workspace tools |
| `EXTERNAL_AI_OPTION_REVIEWS.md` | ✅ Updated | Classifies AnimoCerebro, Caliber, Andrej Karpathy Skills, Promptfoo, Instructor, Outlines, Guidance, DSPy, Brainlid LangChain, Recursive-Language-Models and Warp |
| `EXECUTION_DISCIPLINE.md` | ✅ Added | Defines smallest-safe-path discipline, single-role before workflow, surgical changes and evidence before assertion |
| `EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md` | ✅ Added | Classifies OpenConcho/Honcho as watch/test-only memory options, rejected for core |
| `KNOWLEDGE_TAXONOMY.md` | ✅ Done | Defines Knowledge layers, reliability levels and source tiers |
| `knowledge/registry.example.yaml` | ✅ Added | Example registry maps OpenWebUI Knowledge Bases to domains, tiers, privacy, freshness and evidence rules |
| `CODE_AUDIT_POST_PIVOT.md` | ✅ Added | Initial register for legacy/runtime component classification |
| `WORKFLOW_SCHEMA.md` | ✅ Added | Canonical workflow/task definition schema exists, including `solo` / `single_role_task` path |
| `WORKFLOW_ADAPTATION.md` | ✅ Added | Defines adaptive workflows as governed dependency graphs with role consultation, ZEUS arbitration, reset and candidate rules |
| `SKILL_LIFECYCLE.md` | ✅ Added | Skill lifecycle, XP/status and Hermes mapping policy exists |
| `MEMORY_EVENT_SCHEMA.md` | ✅ Added | Memory event/candidate schema exists |
| `VERSIONS.md` | ✅ Added | Runtime/model version tracking exists |
| `operations/openwebui_hermes_pantheon.md` | ✅ Done | Defines authority model, flows, Context Pack, Evidence Pack, Run Graph, anti-loop |
| `operations/openwebui_manual_setup.md` | ✅ Added | Manual OpenWebUI setup checklist exists |
| `operations/doctor.md` | ✅ Strengthened | Read-only Doctor checklist now covers doctrine, single-role/workflow, contract revision, assets, external tools, n8n, Knowledge, Memory and PR hygiene |
| `operations/n8n_email_automation.md` | ✅ Added | n8n email automation guardrails exist; no install or workflow created |
| `operations/n8n_workflows/email_received_operator_notification.md` | ✅ Added | Candidate spec only; no runtime integration |
| Runtime Context Pack endpoint | ✅ First static implementation | `GET /runtime/context-pack` exists, read-only/static |
| API smoke tests | ✅ Added | `tests/test_api_smoke.py` added; local/CI execution still required |
| Hermes `pantheon-os` local skill | ✅ Template added | Template exists under `hermes/templates/pantheon-os/`; not installed locally |
| Hermes context exports | ✅ Added | `hermes/context/*` orientation exports merged; runtime consumption still to verify |
| `domains/general` | ✅ Started | First invariant domain created |
| `domains/architecture_fr` | ✅ Materialized | PR #97 merged: domain package, first candidate skill and first candidate workflow template |
| `quote_vs_cctp_consistency` skill | ✅ Candidate | First post-pivot `architecture_fr` candidate skill exists; no runtime binding |
| `quote_vs_cctp_review` workflow | ✅ Candidate | First post-pivot `architecture_fr` workflow template exists; dependency-graph/adaptive, not active runtime |
| `domains/software` | 🔄 Targeted | Audit/governance domain to verify in repo |
| `adaptive_orchestration` skill | ✅ Candidate | Created under `domains/general/skills/adaptive_orchestration/` |
| `project_context_resolution` skill | ✅ Candidate | Created under `domains/general/skills/project_context_resolution/` |
| `knowledge_selection` skill | ✅ Candidate | Created under `domains/general/skills/knowledge_selection/` |
| OpenWebUI Knowledge Strategy | 🔄 Example + candidate skill added | Registry example and Knowledge Selection candidate exist; live OpenWebUI validation still pending |
| Validated Pantheon memory | 🔄 Model clarified | Levels: session, candidates, project, system; runtime incomplete |
| Legacy FastAPI runtime | ⚠️ Legacy to audit | Existing autonomous runtime components must not be deleted without audit |
| CI / tests | ⚠️ Failing for inherited code drift | PR #97 failures are inherited from `platform/api` and `tests`, not from its Markdown/YAML scope |

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
| Knowledge Registry example | ✅ Added | `knowledge/registry.example.yaml` |
| Knowledge Selection candidate skill | ✅ Candidate | `domains/general/skills/knowledge_selection/` |
| Hermes integration boundary | ✅ Documented | `HERMES_INTEGRATION.md` |
| Hermes `pantheon-os` skill template | ✅ Added | `hermes/templates/pantheon-os/` |
| Hermes context orientation exports | ✅ Added | `hermes/context/*` |
| Pantheon Context Pack | ✅ First static implementation | `GET /runtime/context-pack` |
| Task Contract | ✅ Documented | `TASK_CONTRACTS.md` |
| Task Contract revision | ✅ Documented | `TASK_CONTRACT_REVISIONS.md` |
| Evidence Pack | ✅ Documented | `EVIDENCE_PACK.md` |
| Approval policy | ✅ Documented | `APPROVALS.md` |
| Workflow adaptation doctrine | ✅ Documented | `WORKFLOW_ADAPTATION.md` |
| Execution discipline | ✅ Documented | `EXECUTION_DISCIPLINE.md` |
| Operations Doctor | ✅ Documented | `operations/doctor.md` |
| architecture_fr first workflow | ✅ Candidate | `domains/architecture_fr/workflows/quote_vs_cctp_review/` |
| n8n email automation guardrails | ✅ Documented | `operations/n8n_email_automation.md` + first workflow spec |

Planned or incomplete:

| Component | Status | Target |
|---|---|---|
| OpenWebUI Router Pipe | ⬜ Planned | Route user requests to Hermes Gateway with Pantheon context/contract constraints |
| OpenWebUI Actions | ⬜ Planned | View Evidence, approve, reject, request rerun or clarification |
| OpenWebUI Evidence display | ⬜ Planned | Display Evidence Pack summaries and approval requests |
| ConsultationRequest / ConsultationResult | ⬜ Planned | Govern Pantheon ↔ Hermes delegation |
| Task Contract revision / resume flow | ⬜ Planned | Runtime support later; doctrine only today |
| Run Graph | ⬜ Planned | Display roles, dependencies, consultations, warnings, vetoes and approvals |
| Hermes Result Scorecard | ⬜ Planned | Source, execution, scope, governance and reuse confidence |
| Live Knowledge Registry | ⬜ Planned | Validate the example registry against live OpenWebUI Knowledge names and metadata |
| n8n install | ⬜ Not started | Only documentation/spec exists; no connector, no secret, no workflow runtime |

Not implemented yet:

```text
automatic Pantheon → Hermes task execution
workflow dependency graph runtime
workflow revision/resume runtime
OpenWebUI custom sidebar / Actions
persistent run graph storage
canonical skill promotion runtime
memory promotion runtime
automated PR workflow
Notion connector
live Knowledge Registry sync
Hermes retrieval preflight using knowledge_selection
n8n runtime install or email connector
```

---

## 4. Documentation / code coherence

### 4.1 Documentation

Status: ✅ Stronger, but still requires audit against the tree.

Reliable now:

```text
README.md
CLAUDE.md
docs/assets/README.md
docs/governance/README.md
docs/governance/STATUS.md
docs/governance/ROADMAP.md
docs/governance/ARCHITECTURE.md
docs/governance/MODULES.md
docs/governance/AGENTS.md
docs/governance/MEMORY.md
docs/governance/APPROVALS.md
docs/governance/TASK_CONTRACTS.md
docs/governance/TASK_CONTRACT_REVISIONS.md
docs/governance/EVIDENCE_PACK.md
docs/governance/HERMES_INTEGRATION.md
docs/governance/OPENWEBUI_INTEGRATION.md
docs/governance/OPENWEBUI_DOMAIN_MAPPING.md
docs/governance/MODEL_ROUTING_POLICY.md
docs/governance/EXTERNAL_TOOLS_POLICY.md
docs/governance/EXTERNAL_RUNTIME_OPTIONS.md
docs/governance/EXTERNAL_AI_OPTION_REVIEWS.md
docs/governance/EXECUTION_DISCIPLINE.md
docs/governance/EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md
docs/governance/KNOWLEDGE_TAXONOMY.md
docs/governance/CODE_AUDIT_POST_PIVOT.md
docs/governance/WORKFLOW_SCHEMA.md
docs/governance/WORKFLOW_ADAPTATION.md
docs/governance/SKILL_LIFECYCLE.md
docs/governance/MEMORY_EVENT_SCHEMA.md
knowledge/registry.example.yaml
hermes/context/
domains/general/skills/adaptive_orchestration/
domains/general/skills/project_context_resolution/
domains/general/skills/knowledge_selection/
domains/architecture_fr/domain.md
domains/architecture_fr/rules.md
domains/architecture_fr/knowledge_policy.md
domains/architecture_fr/output_formats.md
domains/architecture_fr/skills/quote_vs_cctp_consistency/
domains/architecture_fr/workflows/quote_vs_cctp_review/
operations/openwebui_hermes_pantheon.md
operations/openwebui_manual_setup.md
operations/doctor.md
operations/n8n_email_automation.md
operations/n8n_workflows/email_received_operator_notification.md
```

Still to align or verify:

```text
ROADMAP.md must stay synchronized after each governance addition.
AGENTS.md should reconcile HEPHAISTOS / HEPHAESTUS spelling across governance docs.
WORKFLOW_SCHEMA.md, TASK_CONTRACTS.md and TASK_CONTRACT_REVISIONS.md must remain aligned with `quote_vs_cctp_review`.
MEMORY.md must keep C3 + Evidence Pack promotion as non-negotiable.
CODE_AUDIT_POST_PIVOT.md must be completed by real tree audit.
Legacy architecture_fr manifests and flat workflows still need classification/migration.
OpenWebUI/Hermes live wiring remains to verify outside the repo docs.
Knowledge Registry example must be validated against live OpenWebUI Knowledge Base names.
Hermes context exports must be tested against actual Hermes consumption.
README diagram PNG exports are still missing from docs/assets/.
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

CI status:

```text
Lint currently fails on ruff format checks in existing platform/api and tests files.
Tests currently fail on existing core.services.storage_service import drift and coverage baseline.
PR #97 did not introduce those failures; it added Markdown/YAML only under domains/architecture_fr and ai_logs.
```

---

## 5. Workflow adaptation and execution discipline

Status: ✅ Doctrine documented, runtime not implemented.

References:

```text
docs/governance/WORKFLOW_ADAPTATION.md
docs/governance/WORKFLOW_SCHEMA.md
docs/governance/EXECUTION_DISCIPLINE.md
docs/governance/TASK_CONTRACT_REVISIONS.md
```

Current rule:

```text
single_role_path before workflow
solo before dependency_graph
workflow templates are reusable examples, not fixed rails
session workflows may be selected, adapted, composed or generated
Hermes executes only the resulting Task Contract
```

Role split:

```text
ATHENA agence les workflows.
HEPHAISTOS / HEPHAESTUS naming must be reconciled.
CHRONOS règle les dépendances.
ZEUS arbitre les options.
THEMIS bloque.
APOLLO valide.
Hermes exécute.
```

Documented concepts:

```text
single_role_task
single_role_task_contract
workflow_template
session_workflow
workflow_override
workflow_candidate
workflow_revision_signal
workflow_patch
task_contract_revision
resume_policy
reset_to_baseline
```

Not implemented yet:

```text
workflow dependency graph runtime
Task Contract revision runtime
pause/resume execution
OpenWebUI workflow adaptation UI
Langflow visual editing
LangGraph Hermes-side execution adapter
```

---

## 6. architecture_fr domain package

Status: ✅ Materialized as documentation/candidate package.

Merged PR:

```text
#97 — docs(architecture_fr): scaffold domain + first candidate skill + first canonical workflow
```

Files now present:

```text
domains/architecture_fr/domain.md
domains/architecture_fr/rules.md
domains/architecture_fr/knowledge_policy.md
domains/architecture_fr/output_formats.md
domains/architecture_fr/templates/README.md
domains/architecture_fr/skills/quote_vs_cctp_consistency/
domains/architecture_fr/workflows/quote_vs_cctp_review/
```

Interpretation:

```text
The domain package is documentation-only.
The skill is candidate-only.
The workflow is candidate/template-only.
No runtime, endpoint, script or automation was added.
No client/project/address/person/chantier data was added.
```

Open items:

```text
Fix stale `domain: architecture` field in legacy domains/architecture_fr/manifest.yaml.
Classify/migrate legacy flat workflows.
Decide HEPHAISTOS vs HEPHAESTUS spelling in governance.
Add first concrete fictional templates only after review.
Validate OpenWebUI Knowledge names against live setup.
```

---

## 7. Memory model

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
OpenConcho/Honcho conclusions are not Pantheon memory.
Workflow candidates are not canonical workflows.
architecture_fr skill/workflow outputs remain candidate-only unless separately reviewed.
```

---

## 8. Knowledge / document strategy

Status: 🔄 Example registry and candidate selection skill added, live wiring incomplete.

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
knowledge/registry.example.yaml
domains/general/skills/knowledge_selection/
domains/architecture_fr/knowledge_policy.md
```

Current status:

```text
knowledge/registry.example.yaml exists.
domains/general/skills/knowledge_selection/ exists as candidate.
architecture_fr declares source tiers and regulatory freshness policy.
live knowledge/registry.yaml is not created yet.
live OpenWebUI Knowledge Base validation is not done yet.
Hermes retrieval preflight mapping is not implemented yet.
```

---

## 9. Candidate skills and workflows

Existing candidate skills:

```text
domains/general/skills/adaptive_orchestration/
domains/general/skills/project_context_resolution/
domains/general/skills/knowledge_selection/
domains/architecture_fr/skills/quote_vs_cctp_consistency/
```

Existing candidate workflows:

```text
domains/architecture_fr/workflows/quote_vs_cctp_review/
```

Status: ✅ Candidate.

Important interpretation:

```text
adaptive_orchestration is governed by WORKFLOW_ADAPTATION.md.
quote_vs_cctp_consistency is review-mode only, never final contractual validation.
quote_vs_cctp_review is a template, not an active runtime workflow.
No skill activation, no memory promotion, no workflow canonization happened.
```

---

## 10. External options and tool governance

Status: ✅ Strongly documented; no integration performed.

Current external classification docs:

```text
EXTERNAL_TOOLS_POLICY.md
EXTERNAL_RUNTIME_OPTIONS.md
EXTERNAL_AI_OPTION_REVIEWS.md
EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md
```

Classified options include:

```text
Stirling-PDF
SearXNG
n8n
OpenWebUI extensions
Hermes plugins
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
Andrej Karpathy Skills
Promptfoo
Instructor
Outlines
Guidance
DSPy
Brainlid LangChain
Recursive-Language-Models
Warp
```

Rules:

```text
Unknown external tools are blocked until classified.
External runtimes may assist Pantheon but must not become Pantheon.
External memory runtimes may be studied but must not become Pantheon Memory.
Evaluation tools may measure but not govern.
Structured-output tools may constrain but not approve.
Developer tools may assist but not become runtime.
n8n may detect and notify, but must not govern, remember, execute Hermes or send externally without approval.
LangChain/LangGraph are only allowed as Hermes-side library options later.
Langflow is lab-only and may not become workflow authority.
OpenClaw is not Pantheon core and would require runtime-contract abstraction before any future switch.
Warp/Oz must not become a parallel cloud-agent runtime for Pantheon.
```

---

## 11. Legacy components

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
legacy architecture_fr manifests
legacy architecture_fr flat workflows
```

Rule:

```text
Do not delete before diagnosis.
Do not reactivate the autonomous runtime path by accident.
```

---

## 12. Immediate action list

### P0 — completed governance base

1. ✅ Governance docs under `docs/governance/`.
2. ✅ AI logs convention under `ai_logs/`.
3. ✅ Static `GET /runtime/context-pack` endpoint created.
4. ✅ Hermes `pantheon-os` local skill template created.
5. ✅ `APPROVALS.md` added.
6. ✅ `TASK_CONTRACTS.md` added.
7. ✅ `TASK_CONTRACT_REVISIONS.md` added.
8. ✅ `EVIDENCE_PACK.md` added.
9. ✅ `HERMES_INTEGRATION.md` added.
10. ✅ `KNOWLEDGE_TAXONOMY.md` added.
11. ✅ `EXTERNAL_TOOLS_POLICY.md` added.
12. ✅ `OPENWEBUI_INTEGRATION.md` added.
13. ✅ `OPENWEBUI_DOMAIN_MAPPING.md` added.
14. ✅ `MODEL_ROUTING_POLICY.md` added.
15. ✅ `EXTERNAL_RUNTIME_OPTIONS.md` added.
16. ✅ `EXTERNAL_AI_OPTION_REVIEWS.md` added and expanded.
17. ✅ `CODE_AUDIT_POST_PIVOT.md` initial register added.
18. ✅ README rewritten around Pantheon Next.
19. ✅ README diagram asset registry added.
20. ✅ API smoke tests added.
21. ✅ `operations/openwebui_manual_setup.md` added.
22. ✅ `operations/doctor.md` strengthened.
23. ✅ `knowledge/registry.example.yaml` added.
24. ✅ `domains/general/skills/knowledge_selection/` added as candidate.
25. ✅ `EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md` added.
26. ✅ Hermes context exports added under `hermes/context/`.
27. ✅ n8n classified and first email notification workflow spec added.
28. ✅ `WORKFLOW_ADAPTATION.md` added.
29. ✅ `EXECUTION_DISCIPLINE.md` added.
30. ✅ `domains/architecture_fr` materialized with first candidate skill/workflow.

### P1 — next documentation/contracts

1. Run the read-only Doctor checklist against the repository tree.
2. Resolve CI/test drift documented by PR #93 and current CI logs.
3. Run `pytest tests/test_api_smoke.py` locally or in CI after CI baseline is repaired.
4. Validate `knowledge/registry.example.yaml` against live OpenWebUI Knowledge Base names, then decide whether to create `knowledge/registry.yaml`.
5. Define Hermes retrieval preflight mapping for `knowledge_selection`.
6. Verify or document `PANTHEON_CONTEXT_URL` consumption by Hermes.
7. Reconcile `HEPHAISTOS` / `HEPHAESTUS` spelling in governance docs.
8. Fix stale `domains/architecture_fr/manifest.yaml` field if confirmed.
9. Classify or migrate legacy `architecture_fr` flat workflows.
10. Complete `CODE_AUDIT_POST_PIVOT.md` from a real tree audit.
11. Define OpenWebUI Router Pipe specification.
12. Define OpenWebUI Actions specification.
13. Draft `EVALUATION.md` around Promptfoo, Instructor and Outlines if evaluation work is prioritized.
14. Export clean colored README diagrams from Lucid, commit them under `docs/assets/`, then embed them in `README.md`.

### P2 — later implementation

1. Implement real ConsultationRequest / ConsultationResult.
2. Implement Task Contract revision and workflow pause/resume.
3. Implement dependency-aware Run Graph storage.
4. Add run event stream.
5. Add Hermes result scorecard.
6. Add controlled PR workflow.
7. Evaluate whether `pantheon_runtime` should be renamed or documented as context export only.
8. Consider a read-only `operations/doctor.py` only after C3 approval.
9. Implement live Knowledge Registry sync only after policy and approval flow are stable.
10. Consider Memory Candidate Review UX only after memory doctrine and approvals are stable.
11. Compare Instructor vs Outlines for Hermes-side structured outputs after runtime boundary is stable.

---

## 13. Risks

| Risk | Status | Guardrail |
|---|---|---|
| Hermes becomes implicit authority | Active risk | Hermes outputs remain candidates |
| OpenWebUI becomes business engine | Active risk | OpenWebUI remains cockpit only |
| Pantheon duplicates Hermes runtime | Active risk | Pantheon governs, Hermes executes |
| Adaptive workflows become hidden runtime | Active risk | `WORKFLOW_ADAPTATION.md`: session changes require trace, approval and Task Contract revision |
| Workflow overuse | Active risk | `EXECUTION_DISCIPLINE.md`: single-role path before workflow |
| Skill duplication | Active risk | Pantheon skill lifecycle + Hermes skill mapping |
| architecture_fr candidate treated as active runtime | Active risk | Skill/workflow are candidate/template only |
| HEPHAISTOS / HEPHAESTUS naming split | Active risk | Dedicated governance reconciliation needed |
| Memory pollution | Active risk | Candidate memory + validation only |
| Cross-project RAG contamination | Active risk | Knowledge Selection + source tiers |
| Legacy runtime confusion | Active risk | Legacy audit before reuse or deletion |
| Over-abstraction | Active risk | Smallest safe path, documented gain required before new modules |
| Approval bypass | Active risk | C0-C5 policy in `APPROVALS.md` |
| Unsupported conclusions | Active risk | Evidence Pack required for consequential outputs |
| OpenWebUI misrouting | Active risk | OpenWebUI must point to Hermes Gateway, not Pantheon API |
| Public Hermes Dashboard exposure | Active risk | Local-only unless auth/VPN and explicit approval |
| Model fallback misuse | Active risk | `MODEL_ROUTING_POLICY.md` forbids silent C4/C5 fallback |
| External runtime drift | Active risk | `EXTERNAL_RUNTIME_OPTIONS.md` + `EXTERNAL_AI_OPTION_REVIEWS.md` |
| External memory drift | Active risk | OpenConcho/Honcho rejected for core; no memory backend added |
| Doctor used as auto-fixer | Active risk | `operations/doctor.md` is read-only and report-only |
| Knowledge Registry treated as live config too early | Active risk | Current file is example-only until live OpenWebUI validation |
| n8n becomes scheduler/runtime | Active risk | n8n may detect and notify only under policy; no execution or external send by default |
| Structured-output tools become authority | Active risk | Instructor/Outlines may constrain outputs but not approve or govern |
| Evaluation tool becomes authority | Active risk | Promptfoo may measure but not canonize skills or workflows automatically |
| Warp/Oz becomes parallel runtime | Active risk | Warp is optional developer terminal only; Oz is blocked for core |
| Recursive-Language-Models becomes runtime | Active risk | Watch/test-only; sandbox only on non-sensitive data |
| README diagram links break | Active risk | Do not embed images until local PNG exports exist |

---

## 14. Final summary

Reliable now:

```text
Pantheon Next product direction
Hermes-backed direction
OpenWebUI / Hermes / Pantheon operating protocol
approval criticality policy
initial task contracts and revision addendum
Evidence Pack doctrine
Hermes integration doctrine
OpenWebUI integration doctrine
OpenWebUI domain mapping
model routing policy
external tools/runtime/AI option policies
external memory runtime option review
n8n external automation policy and first workflow spec
Knowledge taxonomy
Knowledge Registry example
Knowledge Selection candidate skill
Workflow adaptation doctrine
Execution discipline doctrine
README diagram asset registry
architecture_fr domain package
architecture_fr quote_vs_cctp_consistency candidate skill
architecture_fr quote_vs_cctp_review candidate workflow template
adaptive_orchestration candidate skill
project_context_resolution candidate skill
skill lifecycle / XP doctrine
Hermes context exports
static /runtime/context-pack endpoint
API smoke tests
initial code audit post-pivot register
manual OpenWebUI setup checklist
read-only Doctor checklist
```

Partial:

```text
Domain Layer API
Knowledge strategy live wiring
Hermes pantheon-os skill installation
OpenWebUI router/actions
legacy runtime classification
legacy architecture_fr manifest/workflows cleanup
software domain verification
workflow pause/resume runtime
Task Contract revision runtime
Run Graph runtime
Evaluation plan around Promptfoo / Instructor / Outlines
```

Not implemented yet:

```text
real Pantheon ↔ Hermes task execution
OpenWebUI router/actions
run graph runtime
consultation persistence
workflow dependency graph execution
memory promotion runtime
skill promotion runtime
Notion connector
live Knowledge Registry
Hermes retrieval preflight using knowledge_selection
completed post-pivot code audit
Doctor automation
n8n install/runtime/email connector
Promptfoo evaluation suite
Instructor/Outlines Hermes adapter
README local diagram exports
```

Next logical step:

```text
Run a read-only Doctor report on main, then resolve inherited CI drift.
```
