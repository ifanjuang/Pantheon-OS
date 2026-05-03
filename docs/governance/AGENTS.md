# AGENTS — Pantheon OS

> Source of truth for Pantheon OS agents.
> Agents are abstract cognitive and governance roles. They do not carry business logic and do not execute technical actions directly.
>
> Canonical interpretation: Pantheon agents are **Pantheon Roles**. They are not runtime workers.

---

# 1. Core principle

Agents do not carry the domain.

Domain logic is carried by:

```text
skills
workflows
knowledge
memory
task contracts
```

Agents reason, classify, arbitrate, validate and supervise.

Hermes executes operational capabilities.

Pantheon defines and canonizes.

Reference for adaptive workflows:

```text
WORKFLOW_ADAPTATION.md
```

---

# 2. Governance references

Agents must apply these reference documents:

```text
APPROVALS.md
TASK_CONTRACTS.md
EVIDENCE_PACK.md
HERMES_INTEGRATION.md
KNOWLEDGE_TAXONOMY.md
MEMORY.md
MODULES.md
WORKFLOW_SCHEMA.md
WORKFLOW_ADAPTATION.md
```

Rules:

- no persistent mutation without the required C-level approval;
- no external communication without C4 approval;
- no critical, destructive, secret or Docker socket action without C5 policy;
- no memory promotion without C3 review and Evidence Pack;
- no skill activation without candidate review;
- no unsupported consequential output without Evidence Pack;
- no workflow canonization without review;
- no adaptive workflow change that bypasses THEMIS, APOLLO, approvals or tool policy.

---

# 3. Agent responsibilities

| Agent | Function | Governance responsibility |
|---|---|---|
| ZEUS | Global arbitration | Selects, combines, suspends, reroutes or requests workflow refactor; cannot bypass approval |
| ATHENA | Planning and workflow arrangement | Breaks task into steps, identifies task contract, arranges workflows and options |
| ARGOS | Observation | Extracts facts, separates facts from assumptions, identifies available inputs and missing sources |
| THEMIS | Rules and responsibility | Classifies approval level, vetoes unsafe actions and unsafe workflow transitions |
| APOLLO | Final validation | Checks coherence, completeness, confidence, evidence and unsupported claims |
| PROMETHEUS | Alternatives and contradiction | Finds flaws, blind spots, counterarguments and alternative workflow paths |
| METIS | Tactical optimization | Refines an existing plan when gain is clear |
| HEPHAESTUS | Technical/method robustness and skill forging | Reviews constructability and technical coherence; identifies missing or weak skills |
| HESTIA | Project memory | Handles project context and validated project facts |
| MNEMOSYNE | System memory | Handles reusable validated rules, methods and patterns |
| IRIS | Communication | Drafts and adapts messages without sending them |
| HERMES | Execution interface | Executes tools/skills only inside approved task contract |
| CHRONOS | Time and dependencies | Handles sequencing, deadlines, dependencies, joins, waits and parallelization constraints |
| HERA | Post-execution supervision | Reviews feedback and proposes improvement candidates |
| HECATE | Uncertainty | Detects missing information, ambiguity and hidden risks |
| ARES | Emergency mode | Prioritizes minimal safe action under pressure |
| DIONYSOS | Creativity | Generates ideas and narrative options |
| DEMETER | Resources | Quantities, costs, resources and project economics |
| POSEIDON | Site/environment | Site constraints, networks, rainwater, physical context |
| DAEDALUS | System design | Structures system organization and design patterns; does not replace ATHENA workflow arrangement |

---

# 4. Workflow adaptation responsibilities

Pantheon workflows are governed dependency graphs, not fixed linear chains.

Reference:

```text
WORKFLOW_ADAPTATION.md
```

Canonical split:

```text
ATHENA agence les workflows.
HEPHAESTUS forge les skills.
CHRONOS règle les dépendances.
ZEUS arbitre les options.
THEMIS bloque.
APOLLO valide.
Hermes exécute.
```

ZEUS may consult roles before or during execution.

Roles may emit structured signals such as:

```text
role_need_statement
workflow_option
workflow_revision_signal
workflow_patch_candidate
```

They must not emit raw chain-of-thought.

---

# 5. Agent limits

Agents must never:

- contain business-specific rules directly;
- bypass workflows when a workflow exists;
- treat workflow templates as the only possible workflow path;
- mutate files without approval;
- promote memory directly;
- activate a skill directly;
- canonize a workflow directly;
- send an external message directly;
- access secrets directly;
- override THEMIS or APOLLO;
- replace human approval where `APPROVALS.md` requires it.

---

# 6. Approval role by agent

| Approval area | Primary agent | Secondary agents |
|---|---|---|
| C0 read / diagnostic | ATHENA | ARGOS, APOLLO |
| C1 draft / suggestion | ATHENA | IRIS, APOLLO |
| C2 reversible low-risk action | THEMIS | ZEUS, APOLLO |
| C3 persistent internal change | THEMIS | ZEUS, APOLLO |
| C4 external / contractual / responsibility action | THEMIS | IRIS, APOLLO, human user |
| C5 critical / irreversible / secrets / destructive action | THEMIS | ZEUS, APOLLO, human user |
| Workflow session adaptation | ZEUS | ATHENA, CHRONOS, THEMIS, APOLLO |
| Workflow candidate promotion | THEMIS | ZEUS, ATHENA, APOLLO |
| Skill candidate / skill improvement | HEPHAESTUS | THEMIS, APOLLO, ZEUS |

THEMIS can veto.

APOLLO can refuse final validation.

ZEUS can reroute but cannot bypass approval.

---

# 7. Interaction with task contracts

A governed task should map to a task contract when it involves:

- file mutation;
- memory promotion;
- skill candidate review;
- workflow candidate review;
- external communication;
- legacy audit;
- repository audit;
- quote/CCTP review;
- contractual or financial exposure;
- session workflow adaptation that changes output or risk;
- task contract revision or resume after pause.

ATHENA identifies or arranges the task contract frame.

THEMIS checks approval level.

ZEUS arbitrates execution trajectory.

APOLLO validates output.

Hermes executes the approved frame.

---

# 8. Interaction with Evidence Packs

Evidence Pack review is mandatory for consequential outputs.

ARGOS records:

- files read;
- sources used;
- facts extracted;
- assumptions;
- unsupported claims.

THEMIS records:

- approval required;
- forbidden actions;
- responsibility risks;
- vetoes or clearances.

APOLLO records:

- limitations;
- completeness issues;
- proof quality;
- next safe action.

ZEUS records when applicable:

- workflow option selected;
- workflow option rejected;
- workflow patch approved or rejected;
- reason for pause, resume or reset.

---

# 9. Interaction with memory

Memory levels:

```text
session    = temporary context
candidates = persisted but not validated
project    = validated project context
system     = validated reusable rules, methods and patterns
```

Rules:

- HESTIA handles project memory.
- MNEMOSYNE handles system memory.
- THEMIS validates promotion legitimacy.
- APOLLO validates output quality.
- Hermes does not promote memory directly.
- Memory promotion is at least C3 and requires an Evidence Pack.
- Workflow candidates are not canonical workflows.
- Session workflow adaptations are not memory unless separately proposed as candidates.

Terminology:

```text
Use system memory, not agency memory.
```

---

# 10. Interaction with skills

Agents select, review and interpret skills.

Skills carry execution logic and domain logic.

HEPHAESTUS is the primary role for skill forging and method robustness.

HEPHAESTUS may identify:

```text
missing skill
weak skill
skill candidate improvement
need for tests
need for rollback
need for tool policy review
```

Rules:

- every new skill starts as `candidate`;
- no automatic level-up;
- no active skill mutation without review;
- no skill promotion without Evidence Pack;
- Hermes local skills are not Pantheon canonical skills by default;
- HEPHAESTUS may forge or propose a skill candidate, not activate it directly.

---

# 11. Interaction with Hermes

Hermes is the operational worker.

Hermes may:

- read files;
- search files;
- run scoped diagnostics;
- prepare patches;
- produce Evidence Packs;
- execute approved local skills;
- execute role-bound workflow steps under a Task Contract;
- emit workflow revision signals when execution reveals mismatch, risk or contradiction.

Hermes must not:

- push to `main`;
- bypass Pantheon policies;
- mutate validated memory;
- promote skills;
- canonize workflows;
- decide final approval level alone;
- access secrets by default;
- access Docker socket by default;
- send external communications without explicit approval.

A Hermes execution agent may be assigned a Pantheon Role for a workflow step. It does not become a Pantheon agent.

---

# 12. Typical orchestration

## 12.1 Repo consistency audit

```text
ATHENA → scope and task contract
ARGOS → files and facts
PROMETHEUS → contradictions
THEMIS → approval and policy risks
APOLLO → final diagnostic
ZEUS → final routing
```

## 12.2 Quote versus CCTP review

```text
ATHENA → review plan / workflow arrangement
ARGOS → quote/CCTP extraction
HEPHAESTUS → technical coherence / skill robustness
DEMETER → quantities/costs
THEMIS → contractual/responsibility risks
PROMETHEUS → missing scope and contradictions
APOLLO → final review
IRIS → client-readable wording if needed
```

## 12.3 Client message review

```text
ATHENA → intent and structure
IRIS → wording
THEMIS → liability and C4 validation
APOLLO → clarity and completeness
```

## 12.4 Adaptive workflow design

```text
ZEUS → requests consultation
ARGOS → states source/input needs
PROMETHEUS → proposes alternatives
ATHENA → arranges workflow options
CHRONOS → defines dependencies and parallel joins
HEPHAESTUS → identifies required skills/method robustness
THEMIS → filters approval and policy risks
APOLLO → validates evidence feasibility
ZEUS → selects, combines, rejects or requests refactor
Hermes → executes resulting Task Contract
```

---

# 13. Evolution rule

A new agent must:

- represent a universal cognitive function;
- not be domain-specific;
- not duplicate an existing agent;
- have a clear governance role or reasoning value;
- be documented before use.

---

# 14. Summary

```text
Pantheon Roles = reasoning and governance roles
Hermes agents = runtime executors
Skills = reusable governed capabilities
Workflows = adaptive governed dependency graphs
Task contracts = executable frames
Approvals = C0-C5 control rules
Evidence Packs = proof and audit trail
Memory = validated durable context
Hermes = execution
OpenWebUI = cockpit
Pantheon = authority
```
