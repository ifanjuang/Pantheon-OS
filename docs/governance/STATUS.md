# Pantheon OS — Project Status

> Source of truth for the current project state after the Hermes-backed pivot.
> Reference Markdown files drive development: `README.md`, `ARCHITECTURE.md`, `MODULES.md`, `AGENTS.md`, `MEMORY.md`, `ROADMAP.md`, `STATUS.md`, `APPROVALS.md`, `TASK_CONTRACTS.md`, `EVIDENCE_PACK.md`, `HERMES_INTEGRATION.md`, `KNOWLEDGE_TAXONOMY.md`.

Last update: 2026-04-29

---

# 1. Structural decision

Status: ✅ Documented decision.

Pantheon OS follows a Hermes-backed architecture.

```text
OpenWebUI = user cockpit + knowledge surface
Hermes Agent = privileged operational worker + executable skills + tools
Pantheon OS = governed domain authority + source of truth + domain definitions
```

Design formula:

```text
Pantheon defines and canonizes.
Hermes operates and proposes.
OpenWebUI routes, displays and asks for validation.
```

This replaces the former direction where Pantheon OS would become a full autonomous agent runtime.

---

# 2. Current global status

| Element | Status | Comment |
|---|---|---|
| Hermes-backed pivot | ✅ Done | Direction validated: Pantheon Domain Layer + Hermes + OpenWebUI |
| OpenWebUI / Hermes / Pantheon interaction layer | 🔄 Planned | Protocol documented, API/contracts partially started, not fully implemented |
| `operations/openwebui_hermes_pantheon.md` | ✅ Done | Defines authority model, flows, Context Pack, Evidence Pack, Run Graph, anti-loop |
| `APPROVALS.md` | ✅ Done | Defines C0-C5 criticality and approval levels |
| `TASK_CONTRACTS.md` | ✅ Done | Defines executable task contract schema and first contracts |
| `EVIDENCE_PACK.md` | ✅ Done | Defines evidence schema and mandatory use cases |
| `HERMES_INTEGRATION.md` | ✅ Done | Defines Hermes/Pantheon boundary and context export rules |
| `KNOWLEDGE_TAXONOMY.md` | ✅ Done | Defines Knowledge layers, reliability levels and source tiers |
| `ARCHITECTURE.md` | ✅ Updated | References the OpenWebUI / Hermes / Pantheon operating protocol |
| `domains/general` | ✅ Started | First invariant domain created |
| `adaptive_orchestration` skill | ✅ Candidate | Created under `domains/general/skills/adaptive_orchestration/` |
| `project_context_resolution` skill | ✅ Candidate | Created under `domains/general/skills/project_context_resolution/` |
| Skill XP / levels policy | ✅ Documented | Present in `hermes/skill_policy.md` |
| Runtime Context Pack endpoint | ✅ First static implementation | `GET /runtime/context-pack` exists, read-only/static |
| Hermes `pantheon-os` local skill | ✅ Template added | Template exists under `hermes/templates/pantheon-os/`; not installed locally |
| OpenWebUI Knowledge Strategy | 🔄 Planned | Requires Knowledge Registry, Knowledge Selection, source metadata |
| Validated Pantheon memory | 🔄 Model clarified | Levels: session, candidates, project, system |
| Legacy FastAPI runtime | ⚠️ Legacy to audit | Existing autonomous runtime components must not be deleted without audit |
| Tests | ⚠️ Not executed here | Local/CI execution still required |

---

# 3. OpenWebUI / Hermes / Pantheon interaction layer

Status: 🔄 Planned, partially documented.

Current rule:

```text
Hermes operates.
Pantheon arbitrates.
OpenWebUI pilots and displays.
```

Planned components:

| Component | Status | Target |
|---|---|---|
| OpenWebUI Router Pipe | ⬜ Planned | Route user requests to Pantheon or Hermes Pantheon Operator |
| OpenWebUI Actions | ⬜ Planned | View Evidence, View Run Graph, Approve, Reject, Rerun THEMIS/APOLLO |
| Hermes `pantheon-os` skill | ✅ Template added | Local Hermes skill for Pantheon repository and governance operations |
| Pantheon Context Pack | ✅ First static implementation | `GET /runtime/context-pack` |
| Run Contract | ✅ Documented | See `TASK_CONTRACTS.md` |
| ConsultationRequest / ConsultationResult | ⬜ Planned | Govern Pantheon ↔ Hermes delegation |
| Evidence Pack | ✅ Documented | See `EVIDENCE_PACK.md` |
| Run Graph | ⬜ Planned | Display agents, consultations, warnings, vetoes and approvals |
| Approval policy | ✅ Documented | See `APPROVALS.md` |
| Hermes Result Scorecard | ⬜ Planned | Source, execution, scope, governance and reuse confidence |
| Anti-loop policy | ✅ Documented | Max depth and new-information requirement documented |

Not implemented yet:

- automatic Pantheon → Hermes task execution;
- OpenWebUI custom sidebar;
- persistent run graph storage;
- canonical skill promotion runtime;
- memory promotion runtime;
- automated PR workflow;
- Notion connector;
- dynamic Knowledge Registry.

---

# 4. Documentation / code coherence

## 4.1 Documentation

Status: 🔄 Being realigned.

Reliable now:

- `ARCHITECTURE.md` describes the Hermes-backed anatomy.
- `operations/openwebui_hermes_pantheon.md` defines the three-system operating protocol.
- `APPROVALS.md` defines C0-C5 approval criticality.
- `TASK_CONTRACTS.md` defines bounded Hermes/Pantheon task contracts.
- `EVIDENCE_PACK.md` defines proof requirements.
- `HERMES_INTEGRATION.md` defines how Hermes consumes Pantheon.
- `KNOWLEDGE_TAXONOMY.md` defines OpenWebUI Knowledge layers and reliability.
- `hermes/skill_policy.md` defines skill lifecycle, XP, levels and feedback rules.
- `domains/general/skills/adaptive_orchestration/` exists as a candidate system skill.
- `domains/general/skills/project_context_resolution/` exists as a candidate system skill.

Still to align:

- `ROADMAP.md` must fully reflect the P0 contracts and P1/P2 sequence.
- `AGENTS.md` must explicitly reference approval levels, Evidence Packs and task contracts.
- `MEMORY.md` must explicitly reference Evidence Packs and C3 review for memory promotion.
- `README.md` should stay product/vision oriented and avoid duplicating `MODULES.md`.

## 4.2 Code

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

---

# 5. Memory model

Status: ✅ Doctrine clarified, runtime incomplete.

```text
session    = temporary context
candidates = persisted but not validated
project    = validated project context
system     = validated reusable rules, methods and patterns
```

Cycle:

```text
SESSION → CANDIDATES → validation → PROJECT or SYSTEM
```

No automatic promotion.

Terminology rule:

```text
Use `system memory`, not `agency memory`, for reusable validated rules and patterns.
```

Promotion rule:

```text
Memory promotion is at least C3 and requires Evidence Pack review.
```

---

# 6. Knowledge / document strategy

Status: 🔄 Planned.

Current target:

```text
NAS folders
→ OpenWebUI Knowledge Bases
→ PGVector-backed retrieval
→ Pantheon Knowledge Registry
→ Knowledge Selection
→ Evidence Pack
→ Memory candidates only after validation
```

Reference:

```text
KNOWLEDGE_TAXONOMY.md
```

Planned concepts:

- Knowledge Registry;
- Knowledge Selection skill;
- document metadata;
- source tiers;
- freshness checks;
- no cross-project mixing unless explicitly approved.

Rule:

```text
Documents are knowledge.
Validated reusable facts become memory candidates.
Pantheon alone canonizes memory.
```

---

# 7. Candidate skills and workflows

## 7.1 Existing candidate skills

```text
domains/general/skills/adaptive_orchestration/
domains/general/skills/project_context_resolution/
```

Status: ✅ Candidate.

## 7.2 First business-domain target

Use case:

```text
quote_vs_cctp_analysis / quote_vs_cctp_review
```

Status: ⬜ Not created yet.

Target domain:

```text
domains/architecture_fr/
```

---

# 8. Legacy components

Status: ⚠️ Present, not deleted.

Legacy elements still need audit:

- old dynamic module registry;
- `modules.yaml`;
- previous workflow loader;
- initial approval API;
- Alembic approval migration;
- Installer UI;
- old tests tied to autonomous runtime assumptions.

Rule:

```text
Do not delete before diagnosis.
Do not reactivate the autonomous runtime path by accident.
```

---

# 9. Immediate action list

## P0 — completed documentation base

1. ✅ Add `OpenWebUI / Hermes / Pantheon interaction layer — planned` to `STATUS.md`.
2. ✅ Update `MODULES.md` with consultation, evidence pack and run graph modules.
3. ✅ Add `AI_LOG.md` entries after interventions.
4. ✅ Create first static `GET /runtime/context-pack` endpoint.
5. ✅ Create Hermes `pantheon-os` local skill template.
6. ✅ Add `APPROVALS.md`.
7. ✅ Add `TASK_CONTRACTS.md`.
8. ✅ Add `EVIDENCE_PACK.md`.
9. ✅ Add `HERMES_INTEGRATION.md`.
10. ✅ Add `KNOWLEDGE_TAXONOMY.md`.

## P1 — next documentation/contracts

1. Create OpenWebUI Router Pipe specification.
2. Create OpenWebUI Actions specification.
3. Create `knowledge/registry.yaml`.
4. Create Knowledge Selection candidate skill.
5. Create Hermes context exports.
6. Create domain package rule files: `rules.md`, `knowledge_policy.md`, `output_formats.md`.
7. Create first quality gates under `domains/general/skills/`.
8. Add tests for `/runtime/context-pack`.

## P2 — later implementation

1. Implement real ConsultationRequest / ConsultationResult.
2. Implement Run Graph storage.
3. Add run event stream.
4. Add Hermes result scorecard.
5. Add controlled PR workflow.
6. Create `CODE_AUDIT_POST_PIVOT.md`.

---

# 10. Risks

| Risk | Status | Guardrail |
|---|---|---|
| Hermes becomes implicit authority | Active risk | Hermes outputs remain candidates |
| OpenWebUI becomes business engine | Active risk | OpenWebUI remains cockpit only |
| Pantheon duplicates Hermes runtime | Active risk | Pantheon governs, Hermes executes |
| Skill duplication | Active risk | Pantheon skill policy + Hermes skill check |
| Memory pollution | Active risk | Candidate memory + validation only |
| Cross-project RAG contamination | Active risk | Knowledge Selection + source tiers |
| Legacy runtime confusion | Active risk | Legacy audit before reuse or deletion |
| Over-abstraction | Active risk | Documented gain required before new modules |
| Approval bypass | Active risk | C0-C5 policy in `APPROVALS.md` |
| Unsupported conclusions | Active risk | Evidence Pack required for consequential outputs |

---

# 11. Final summary

Reliable now:

```text
Hermes-backed direction
OpenWebUI / Hermes / Pantheon operating protocol
approval criticality policy
initial task contracts
Evidence Pack doctrine
Hermes integration doctrine
Knowledge taxonomy
adaptive_orchestration candidate skill
project_context_resolution candidate skill
skill lifecycle / XP doctrine
static /runtime/context-pack endpoint
```

Partial:

```text
Domain Layer API
Knowledge strategy
Hermes pantheon-os skill installation
OpenWebUI router/actions
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
```

Next logical step:

```text
Create knowledge/registry.yaml, knowledge_selection skill and Hermes context exports.
```
