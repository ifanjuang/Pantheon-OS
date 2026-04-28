# Pantheon OS — Project Status

> Source of truth for the current project state after the Hermes-backed pivot.
> Reference Markdown files drive development: `README.md`, `ARCHITECTURE.md`, `MODULES.md`, `AGENTS.md`, `MEMORY.md`, `ROADMAP.md`, `STATUS.md`.

Last update: 2026-04-28

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
| `ARCHITECTURE.md` | ✅ Updated | References the OpenWebUI / Hermes / Pantheon operating protocol |
| `domains/general` | ✅ Started | First invariant domain created |
| `adaptive_orchestration` skill | ✅ Candidate | Created under `domains/general/skills/adaptive_orchestration/` |
| Skill XP / levels policy | ✅ Documented | Present in `hermes/skill_policy.md` |
| Runtime Context Pack endpoint | 🔄 Planned / first implementation in progress | Target: `GET /runtime/context-pack` |
| Hermes `pantheon-os` local skill | 🔄 Planned / template in progress | Must remain local/experimental until installed manually in Hermes |
| OpenWebUI Knowledge Strategy | 🔄 Planned | Requires Knowledge Registry, Knowledge Selection, Evidence Pack, source tiers |
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
| Hermes `pantheon-os` skill | 🔄 Template in progress | Local Hermes skill for Pantheon repository and governance operations |
| Pantheon Context Pack | 🔄 First static endpoint in progress | `GET /runtime/context-pack` |
| Run Contract | ⬜ Planned | Frame allowed/forbidden actions and expected outputs |
| ConsultationRequest / ConsultationResult | ⬜ Planned | Govern Pantheon ↔ Hermes delegation |
| Evidence Pack | ⬜ Planned | Track files read, commands, tests, sources, diffs, errors, limitations |
| Run Graph | ⬜ Planned | Display agents, consultations, warnings, vetoes and approvals |
| Hermes Result Scorecard | ⬜ Planned | Source, execution, scope, governance and reuse confidence |
| Anti-loop policy | ✅ Documented | Max depth and new-information requirement documented |

Not implemented yet:

- automatic Pantheon → Hermes task execution;
- OpenWebUI custom sidebar;
- persistent run graph storage;
- canonical skill promotion runtime;
- memory promotion runtime;
- automated PR workflow.

---

# 4. Documentation / code coherence

## 4.1 Documentation

Status: 🔄 Being realigned.

Reliable now:

- `ARCHITECTURE.md` describes the Hermes-backed anatomy.
- `operations/openwebui_hermes_pantheon.md` defines the three-system operating protocol.
- `hermes/skill_policy.md` defines skill lifecycle, XP, levels and feedback rules.
- `domains/general/skills/adaptive_orchestration/` exists as a candidate system skill.

Still to align:

- `MODULES.md` must include consultation, run graph and evidence pack modules.
- `MEMORY.md` must remain aligned with session / candidates / project / system.
- `ROADMAP.md` must reflect the OpenWebUI / Hermes / Pantheon interaction layer.
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

Known endpoints before this intervention:

```text
/health
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

Target new endpoint:

```text
/runtime/context-pack
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

Planned concepts:

- Knowledge Registry;
- Knowledge Selection skill;
- Evidence Pack for RAG responses;
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

## 7.1 Existing candidate skill

```text
domains/general/skills/adaptive_orchestration/
```

Status: ✅ Candidate.

Purpose:

```text
Before execution: select or adapt.
During execution: reevaluate and adjust.
After execution: propose candidate improvement when useful.
```

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

## P0

1. Add `OpenWebUI / Hermes / Pantheon interaction layer — planned` to `STATUS.md`.
2. Update `MODULES.md` with consultation, evidence pack and run graph modules.
3. Add an `AI_LOG.md` entry for this intervention.
4. Create first static `GET /runtime/context-pack` endpoint.
5. Create Hermes `pantheon-os` local skill template.

## P1

1. Create OpenWebUI Router Pipe specification.
2. Create OpenWebUI Actions specification.
3. Create Knowledge Registry.
4. Create Knowledge Selection candidate skill.
5. Create Evidence Pack templates.
6. Add tests for `/runtime/context-pack`.

## P2

1. Implement real ConsultationRequest / ConsultationResult.
2. Implement Run Graph storage.
3. Add run event stream.
4. Add Hermes result scorecard.
5. Add controlled PR workflow.

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

---

# 11. Final summary

Reliable now:

```text
Hermes-backed direction
OpenWebUI / Hermes / Pantheon operating protocol
adaptive_orchestration candidate skill
skill lifecycle / XP doctrine
```

Partial:

```text
Domain Layer API
Context Pack endpoint
MODULES alignment
Knowledge strategy
Hermes pantheon-os skill
```

Not implemented yet:

```text
real Pantheon ↔ Hermes task execution
OpenWebUI router/actions
run graph runtime
consultation persistence
memory promotion runtime
skill promotion runtime
```

Next logical step:

```text
Finish P0: MODULES.md, AI_LOG.md, /runtime/context-pack, Hermes pantheon-os skill template.
```
