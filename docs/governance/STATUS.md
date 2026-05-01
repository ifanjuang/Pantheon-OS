# Pantheon Next — Project Status

> Source of truth for the current project state after the Hermes-backed pivot.
> Governance Markdown files drive development under `docs/governance/`.

Last update: 2026-05-01

---

## 1. Structural decision

Status: ✅ Documented decision.

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

---

## 2. Current global status

| Element | Status | Comment |
|---|---|---|
| Pantheon Next naming | ✅ Updated | README now uses Pantheon Next as product name |
| Hermes-backed pivot | ✅ Done | Direction validated: Pantheon governance + Hermes runtime + OpenWebUI cockpit |
| `docs/governance/` | ✅ Canonical | Governance documents live under `docs/governance/` |
| `ai_logs/` | ✅ Canonical | AI intervention logs use one file per session |
| README | ✅ Updated | Product entry point rewritten for Pantheon Next |
| OpenWebUI / Hermes / Pantheon interaction layer | 🔄 Planned | Protocol documented, API/contracts partially started, not fully implemented |
| `OPENWEBUI_INTEGRATION.md` | ✅ Added | Defines OpenWebUI cockpit, Knowledge and validation boundary |
| `HERMES_INTEGRATION.md` | ✅ Done | Defines Hermes/Pantheon boundary and context export rules |
| `EXTERNAL_TOOLS_POLICY.md` | ✅ Done | Defines external tool classification and allowlist policy |
| `CODE_AUDIT_POST_PIVOT.md` | ✅ Added | Initial register for legacy/runtime component classification |
| `operations/openwebui_hermes_pantheon.md` | ✅ Done | Defines authority model, flows, Context Pack, Evidence Pack, Run Graph, anti-loop |
| `APPROVALS.md` | ✅ Done | Defines C0-C5 criticality and approval levels |
| `TASK_CONTRACTS.md` | ✅ Done | Defines task contract schema and first contracts |
| `EVIDENCE_PACK.md` | ✅ Done | Defines evidence schema and mandatory use cases |
| `KNOWLEDGE_TAXONOMY.md` | ✅ Done | Defines Knowledge layers, reliability levels and source tiers |
| `ARCHITECTURE.md` | ✅ Updated | References the OpenWebUI / Hermes / Pantheon operating protocol |
| `domains/general` | ✅ Started | First invariant domain created |
| `domains/architecture_fr` | 🔄 Targeted | Main business domain, first workflows still to create |
| `domains/software` | 🔄 Targeted | Audit/governance domain to verify in repo |
| `adaptive_orchestration` skill | ✅ Candidate | Created under `domains/general/skills/adaptive_orchestration/` |
| `project_context_resolution` skill | ✅ Candidate | Created under `domains/general/skills/project_context_resolution/` |
| Runtime Context Pack endpoint | ✅ First static implementation | `GET /runtime/context-pack` exists, read-only/static |
| Hermes `pantheon-os` local skill | ✅ Template added | Template exists under `hermes/templates/pantheon-os/`; not installed locally |
| OpenWebUI Knowledge Strategy | 🔄 Planned | Requires Knowledge Registry, Knowledge Selection, source metadata |
| Validated Pantheon memory | 🔄 Model clarified | Levels: session, candidates, project, system |
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

Planned components:

| Component | Status | Target |
|---|---|---|
| OpenWebUI Router Pipe | ⬜ Planned | Route user requests to Hermes Gateway with Pantheon context/contract constraints |
| OpenWebUI Actions | ⬜ Planned | View Evidence, approve, reject, request rerun or clarification |
| OpenWebUI Evidence display | ⬜ Planned | Display Evidence Pack summaries and approval requests |
| Hermes `pantheon-os` skill | ✅ Template added | Local Hermes skill for Pantheon repository and governance operations |
| Pantheon Context Pack | ✅ First static implementation | `GET /runtime/context-pack` |
| Task Contract | ✅ Documented | See `TASK_CONTRACTS.md` |
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

## 4. Documentation / code coherence

### 4.1 Documentation

Status: 🔄 Being realigned.

Reliable now:

- `README.md` presents Pantheon Next and the Hermes-backed operating model.
- `ARCHITECTURE.md` describes the Hermes-backed anatomy.
- `operations/openwebui_hermes_pantheon.md` defines the three-system operating protocol.
- `OPENWEBUI_INTEGRATION.md` defines OpenWebUI as cockpit, Knowledge surface and validation boundary.
- `APPROVALS.md` defines C0-C5 approval criticality.
- `TASK_CONTRACTS.md` defines bounded Hermes/Pantheon task contracts.
- `EVIDENCE_PACK.md` defines proof requirements.
- `HERMES_INTEGRATION.md` defines how Hermes consumes Pantheon.
- `KNOWLEDGE_TAXONOMY.md` defines OpenWebUI Knowledge layers and reliability.
- `EXTERNAL_TOOLS_POLICY.md` defines external tool governance.
- `CODE_AUDIT_POST_PIVOT.md` defines the first legacy audit register.
- `hermes/skill_policy.md` defines skill lifecycle, XP, levels and feedback rules.
- `domains/general/skills/adaptive_orchestration/` exists as a candidate system skill.
- `domains/general/skills/project_context_resolution/` exists as a candidate system skill.

Still to align:

- `ROADMAP.md` should reflect that `EXTERNAL_TOOLS_POLICY.md`, `OPENWEBUI_INTEGRATION.md` and `CODE_AUDIT_POST_PIVOT.md` now exist.
- `AGENTS.md` must explicitly reference approval levels, Evidence Packs and task contracts.
- `MEMORY.md` must explicitly reference Evidence Packs and C3 review for memory promotion.
- `ARCHITECTURE.md` may be renamed textually from Pantheon OS to Pantheon Next without changing the repository name.
- Code package names such as `pantheon_runtime` must be audited before any rename.

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

## 6. Knowledge / document strategy

Status: 🔄 Planned.

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
```

Rule:

```text
Documents are knowledge.
Validated reusable facts become memory candidates.
Pantheon Next alone canonizes memory.
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

## 8. Legacy components

Status: ⚠️ Present, not deleted.

Reference:

```text
CODE_AUDIT_POST_PIVOT.md
```

Legacy elements still need audit:

- old dynamic module registry;
- `modules.yaml`;
- previous workflow loader;
- initial approval API;
- Alembic approval migration;
- Installer UI;
- old tests tied to autonomous runtime assumptions;
- naming and purpose of `platform/api/pantheon_runtime/`.

Rule:

```text
Do not delete before diagnosis.
Do not reactivate the autonomous runtime path by accident.
```

---

## 9. Immediate action list

### P0 — documentation base

1. ✅ Governance docs moved under `docs/governance/`.
2. ✅ AI logs convention moved to `ai_logs/`.
3. ✅ Static `GET /runtime/context-pack` endpoint created.
4. ✅ Hermes `pantheon-os` local skill template created.
5. ✅ `APPROVALS.md` added.
6. ✅ `TASK_CONTRACTS.md` added.
7. ✅ `EVIDENCE_PACK.md` added.
8. ✅ `HERMES_INTEGRATION.md` added.
9. ✅ `KNOWLEDGE_TAXONOMY.md` added.
10. ✅ `EXTERNAL_TOOLS_POLICY.md` added.
11. ✅ `OPENWEBUI_INTEGRATION.md` added.
12. ✅ `CODE_AUDIT_POST_PIVOT.md` initial register added.
13. ✅ README rewritten around Pantheon Next.

### P1 — next documentation/contracts

1. Update `ROADMAP.md` to reflect completed P0 files.
2. Create OpenWebUI Router Pipe specification.
3. Create OpenWebUI Actions specification.
4. Create `knowledge/registry.yaml`.
5. Create Knowledge Selection candidate skill.
6. Create Hermes context exports.
7. Create domain package rule files: `rules.md`, `knowledge_policy.md`, `output_formats.md`.
8. Create first quality gates under `domains/general/skills/`.
9. Add tests for `/runtime/context-pack`.
10. Run `code_audit_post_pivot` and complete the audit register.

### P2 — later implementation

1. Implement real ConsultationRequest / ConsultationResult.
2. Implement Run Graph storage.
3. Add run event stream.
4. Add Hermes result scorecard.
5. Add controlled PR workflow.
6. Evaluate whether `pantheon_runtime` should be renamed or documented as context export only.

---

## 10. Risks

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
| OpenWebUI misrouting | Active risk | OpenWebUI must point to Hermes Gateway, not Pantheon API |
| Public Hermes Dashboard exposure | Active risk | Local-only unless auth/VPN and explicit approval |

---

## 11. Final summary

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
External tools policy
Knowledge taxonomy
adaptive_orchestration candidate skill
project_context_resolution candidate skill
skill lifecycle / XP doctrine
static /runtime/context-pack endpoint
initial code audit post-pivot register
```

Partial:

```text
Domain Layer API
Knowledge strategy
Hermes pantheon-os skill installation
OpenWebUI router/actions
legacy runtime classification
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
```

Next logical step:

```text
Update ROADMAP.md, then run the code_audit_post_pivot review against the repository tree.
```
