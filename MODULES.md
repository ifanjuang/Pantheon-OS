# MODULES — Pantheon OS

> Functional reference for Pantheon OS modules after the Hermes-backed pivot.
> Pantheon OS is not the agent runtime. It is the governed domain layer that defines skills, workflows, memory, knowledge, rules and validation.

---

# 1. Principle

Pantheon OS must remain simpler than the runtime it governs.

```text
OpenWebUI = cockpit and knowledge surface
Hermes Agent = operational runtime and executable skills
Pantheon OS = governed domain authority and source of truth
```

Pantheon modules define:

- agents;
- domains;
- skills;
- workflows;
- memory;
- knowledge;
- Hermes integration;
- consultation;
- evidence packs;
- run graphs;
- operations.

A module must be:

- readable;
- isolated;
- maintainable;
- traceable;
- aligned with the reference Markdown files.

---

# 2. Core modules

## 2.1 Agents

Path:

```text
agents/
```

Role:

- define universal cognitive functions;
- structure analysis;
- orchestrate workflows;
- validate outputs;
- detect risk and uncertainty.

Agents are abstract and not business-specific.

They must not:

- contain domain-specific business logic;
- execute technical actions directly;
- mutate files without validation;
- bypass THEMIS, APOLLO or human validation when required.

---

## 2.2 Domains

Path:

```text
domains/
  general/
  architecture_fr/
  software/
```

Role:

- group domain-specific skills, workflows and templates;
- inject professional rules and constraints;
- prevent business logic from leaking into agents.

Current structure:

```text
domains/{domain}/
  domain.md
  skills/
  workflows/
  templates/
```

Rules:

- `general` contains invariant system capabilities.
- `architecture_fr` contains French-speaking architecture-domain capabilities.
- `software` contains repository, documentation and code governance capabilities.
- The French architecture domain must not be recreated as `domains/architecture/`.

---

## 2.3 Skills

Path:

```text
domains/{domain}/skills/{skill_id}/
```

Minimal structure:

```text
SKILL.md
manifest.yaml
examples.md
tests.md
UPDATES.md
```

Role:

- represent reusable capabilities;
- define inputs, outputs, limits and risks;
- carry domain logic;
- provide outputs usable by workflows or humans.

Lifecycle:

```text
candidate
active
probation
quarantine
archived
rejected
```

XP and level metadata live in `manifest.yaml`.

Rule:

```text
A new skill starts as candidate.
No level-up is automatic.
No active skill is modified directly without review.
```

---

## 2.4 Workflows

Path:

```text
domains/{domain}/workflows/*.yaml
```

Role:

- define structured procedures;
- orchestrate agents and skills;
- define validation points;
- expose expected outputs and fallback paths.

Rules:

- a workflow must be a method, not a long prompt;
- workflows may be adaptive if `adaptive_orchestration` authorizes it;
- every durable workflow change starts as a candidate update;
- risky workflow changes require validation.

---

## 2.5 Adaptive orchestration

Path:

```text
domains/general/skills/adaptive_orchestration/
```

Status: candidate.

Role:

- run workflow preflight;
- choose, adapt, simplify or switch workflows;
- insert subworkflows when prerequisites are missing;
- add or remove agents when justified;
- expand context when uncertainty remains;
- ask the user only when required;
- propose candidate skill/workflow updates after useful patterns.

Core rule:

```text
Before execution: select or adapt.
During execution: reevaluate and adjust.
After execution: propose candidate improvement when useful.
```

---

## 2.6 Memory

Path:

```text
memory/
  session/
  candidates/
  project/
  system/
```

Role:

- preserve validated context;
- separate temporary context from durable knowledge;
- prevent raw documents from becoming memory automatically.

Memory levels:

```text
session    = temporary context
candidates = persisted but not validated
project    = validated project context
system     = validated reusable rules, methods and patterns
```

Rule:

```text
No automatic promotion.
```

Terminology rule:

```text
Use system memory, not agency memory.
```

---

## 2.7 Knowledge

Path:

```text
knowledge/
```

Role:

- define document strategy;
- describe OpenWebUI Knowledge Bases;
- define source policy;
- prevent cross-project contamination;
- support RAG without turning documents into memory.

Planned components:

```text
knowledge/registry.yaml
knowledge/source_tiers.md
knowledge/freshness_policy.md
knowledge/openwebui_collections.md
```

Rule:

```text
Documents are knowledge.
Validated reusable facts become memory candidates.
Pantheon alone canonizes memory.
```

---

## 2.8 Knowledge selection

Status: planned.

Role:

- select relevant OpenWebUI Knowledge Bases based on the request;
- avoid consulting all bases by default;
- prevent mixing project documents without explicit approval;
- request user validation when the source choice is ambiguous or sensitive;
- record consulted bases in the Evidence Pack.

Planned location:

```text
domains/general/skills/knowledge_selection/
```

---

## 2.9 Hermes integration

Path:

```text
hermes/
```

Role:

- define how Pantheon exposes controlled context to Hermes;
- define Hermes skill policy;
- classify external Hermes skill repositories;
- prepare local Hermes skill templates.

Current files:

```text
hermes/skill_policy.md
hermes/external_skill_repos.md
```

Planned context exports:

```text
hermes/context/
  pantheon_context.md
  agents_context.md
  memory_context.md
  rules_context.md
  architecture_fr_context.md
  software_context.md
```

Rule:

```text
Hermes executes operational work.
Pantheon defines, validates and canonizes.
```

---

## 2.10 Consultation

Status: planned.

Role:

- govern Pantheon ↔ Hermes delegation;
- define allowed and forbidden actions;
- prevent recursive consultation loops;
- make every Hermes result reviewable by Pantheon.

Planned code structure:

```text
core/consultation/
  contracts.py
  router.py
  hermes_client.py
  policy.py
  events.py
```

Planned contracts:

```text
RunContract
ConsultationRequest
ConsultationResult
EvidencePack
HermesScorecard
```

Rules:

```text
Hermes outputs candidates.
Pantheon canonizes.
Consultations must bring new information.
max_consultation_depth = 2.
```

---

## 2.11 Evidence Pack

Status: planned.

Role:

- make outputs auditable;
- record sources and limits;
- prevent unsupported conclusions;
- support THEMIS and APOLLO review.

Required fields:

```text
files_read
commands_run
tests_run
sources_used
knowledge_bases_consulted
documents_used
diffs_created
errors
limitations
confidence
```

Rule:

```text
Any Hermes output intended for Pantheon must include an Evidence Pack.
Any RAG-based answer should expose the consulted sources when the answer is consequential.
```

---

## 2.12 Run Graph

Status: planned.

Role:

- expose workflow progress;
- show active agents;
- show Hermes consultations;
- show warnings, vetoes, approvals and blockers;
- provide a base for future OpenWebUI visual trace.

Minimal event types:

```text
run.created
run.started
agent.started
agent.completed
consultation.requested
consultation.completed
skill.candidate_created
memory.candidate_created
decision.candidate_created
veto.warning
veto.blocking
approval.required
artifact.created
run.completed
run.failed
```

Rule:

```text
Display state, summaries, evidence and decisions.
Never display raw chain-of-thought.
```

---

## 2.13 Runtime Context Pack

Status: first static endpoint planned.

Endpoint:

```http
GET /runtime/context-pack
```

Role:

- give Hermes a compact operational view of Pantheon;
- list truth files;
- list active rules;
- list domain packages;
- list known blockers;
- recommend the correct entrypoint.

Rule:

```text
The Context Pack is orientation only.
It does not replace the reference Markdown files.
```

---

## 2.14 Operations

Path:

```text
operations/
```

Role:

- document operating protocols;
- document deployment assumptions;
- document NAS/OpenWebUI/Hermes setup;
- document maintenance and upgrade procedures.

Current protocol:

```text
operations/openwebui_hermes_pantheon.md
```

---

# 3. Legacy modules

Status: to audit.

Legacy elements include:

- previous autonomous FastAPI runtime;
- dynamic module registry;
- previous workflow loader;
- initial approval API;
- Alembic approval migration;
- Installer UI;
- old tests coupled to the previous runtime direction.

Rules:

```text
Do not delete without audit.
Do not reactivate the autonomous runtime accidentally.
Do not keep duplicate workflow/skill definitions.
```

---

# 4. What is not a Pantheon module

The following are not Pantheon modules:

- business-specific agents;
- a full agent runtime duplicated from Hermes;
- an OpenWebUI frontend fork;
- a hidden database of business truth;
- raw document storage pretending to be memory;
- unreviewed local Hermes skills;
- community skills installed directly into production.

---

# 5. Global flow

```text
User
→ OpenWebUI
→ Pantheon Router / adaptive orchestration
→ optional Hermes consultation
→ Evidence Pack
→ THEMIS / APOLLO review when needed
→ OpenWebUI display / approval
→ memory candidate only if validated
```

---

# 6. Summary

```text
agents       → cognitive roles
domains      → professional/context boundaries
skills       → reusable capabilities
workflows    → methods and orchestration
memory       → validated durable context
knowledge    → document retrieval and source policy
hermes       → execution integration
consultation → controlled delegation
evidence     → auditability
run graph    → trace and visibility
operations   → deployment and maintenance
```
