# AGENTS — Pantheon OS

> Source of truth for Pantheon OS agents.
> Agents are abstract cognitive roles. They do not carry business logic and do not execute technical actions directly.

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
```

Rules:

- no persistent mutation without the required C-level approval;
- no external communication without C4 approval;
- no critical, destructive, secret or Docker socket action without C5 policy;
- no memory promotion without C3 review and Evidence Pack;
- no skill activation without candidate review;
- no unsupported consequential output without Evidence Pack.

---

# 3. Agent responsibilities

| Agent | Function | Governance responsibility |
|---|---|---|
| ZEUS | Global orchestration | Selects workflow, agents and escalation path |
| ATHENA | Planning | Breaks task into steps, identifies task contract |
| ARGOS | Observation | Extracts facts, separates facts from assumptions |
| THEMIS | Rules and responsibility | Classifies approval level, vetoes unsafe actions |
| APOLLO | Final validation | Checks coherence, completeness and confidence |
| PROMETHEUS | Contradiction | Finds flaws, blind spots and counterarguments |
| METIS | Tactical optimization | Refines an existing plan when gain is clear |
| HEPHAESTUS | Technical and structural analysis | Reviews constructability, technical coherence, visual/spatial logic |
| HESTIA | Project memory | Handles project context and validated project facts |
| MNEMOSYNE | System memory | Handles reusable validated rules, methods and patterns |
| IRIS | Communication | Drafts and adapts messages without sending them |
| HERMES | Execution interface | Executes tools/skills only inside approved task contract |
| CHRONOS | Time | Handles sequencing, deadlines and dependencies |
| HERA | Post-execution supervision | Reviews feedback and proposes improvement candidates |
| HECATE | Uncertainty | Detects missing information and blocks when necessary |
| ARES | Emergency mode | Prioritizes minimal safe action under pressure |
| DIONYSOS | Creativity | Generates ideas and narrative options |
| DEMETER | Resources | Quantities, costs, resources and project economics |
| POSEIDON | Site/environment | Site constraints, networks, rainwater, physical context |
| DAEDALUS | System design | Structures workflows, skills and system organization |

---

# 4. Agent limits

Agents must never:

- contain business-specific rules directly;
- bypass workflows when a workflow exists;
- mutate files without approval;
- promote memory directly;
- activate a skill directly;
- send an external message directly;
- access secrets directly;
- override THEMIS or APOLLO;
- replace human approval where `APPROVALS.md` requires it.

---

# 5. Approval role by agent

| Approval area | Primary agent | Secondary agents |
|---|---|---|
| C0 read / diagnostic | ATHENA | ARGOS, APOLLO |
| C1 draft / suggestion | ATHENA | IRIS, APOLLO |
| C2 reversible low-risk action | THEMIS | ZEUS, APOLLO |
| C3 persistent internal change | THEMIS | ZEUS, APOLLO |
| C4 external / contractual / responsibility action | THEMIS | IRIS, APOLLO, human user |
| C5 critical / irreversible / secrets / destructive action | THEMIS | ZEUS, APOLLO, human user |

THEMIS can veto.

APOLLO can refuse final validation.

ZEUS can reroute but cannot bypass approval.

---

# 6. Interaction with task contracts

A governed task should map to a task contract when it involves:

- file mutation;
- memory promotion;
- skill candidate review;
- workflow candidate review;
- external communication;
- legacy audit;
- repository audit;
- quote/CCTP review;
- contractual or financial exposure.

ATHENA identifies the task contract.

THEMIS checks approval level.

ZEUS orchestrates execution.

APOLLO validates output.

---

# 7. Interaction with Evidence Packs

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
- responsibility risks.

APOLLO records:

- limitations;
- completeness issues;
- next safe action.

---

# 8. Interaction with memory

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

Terminology:

```text
Use system memory, not agency memory.
```

---

# 9. Interaction with skills

Agents select, review and interpret skills.

Skills carry execution logic and domain logic.

Rules:

- every new skill starts as `candidate`;
- no automatic level-up;
- no active skill mutation without review;
- no skill promotion without Evidence Pack;
- Hermes local skills are not Pantheon canonical skills by default.

---

# 10. Interaction with Hermes

Hermes is the operational worker.

Hermes may:

- read files;
- search files;
- run scoped diagnostics;
- prepare patches;
- produce Evidence Packs;
- execute approved local skills.

Hermes must not:

- push to `main`;
- bypass Pantheon policies;
- mutate validated memory;
- promote skills;
- access secrets by default;
- access Docker socket by default;
- send external communications without explicit approval.

---

# 11. Typical orchestration

## 11.1 Repo consistency audit

```text
ATHENA → scope and task contract
ARGOS → files and facts
PROMETHEUS → contradictions
THEMIS → approval and policy risks
APOLLO → final diagnostic
ZEUS → final routing
```

## 11.2 Quote versus CCTP review

```text
ATHENA → review plan
ARGOS → quote/CCTP extraction
HEPHAESTUS → technical coherence
DEMETER → quantities/costs
THEMIS → contractual/responsibility risks
PROMETHEUS → missing scope and contradictions
APOLLO → final review
IRIS → client-readable wording if needed
```

## 11.3 Client message review

```text
ATHENA → intent and structure
IRIS → wording
THEMIS → liability and C4 validation
APOLLO → clarity and completeness
```

---

# 12. Evolution rule

A new agent must:

- represent a universal cognitive function;
- not be domain-specific;
- not duplicate an existing agent;
- have a clear governance role or reasoning value;
- be documented before use.

---

# 13. Summary

```text
Agents = reasoning and governance roles
Skills = reusable capabilities
Workflows = methods and orchestration
Task contracts = executable frames
Approvals = C0-C5 control rules
Evidence Packs = proof and audit trail
Memory = validated durable context
Hermes = execution
OpenWebUI = cockpit
Pantheon = authority
```
