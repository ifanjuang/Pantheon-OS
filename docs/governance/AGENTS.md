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

Reference for adaptive workflows and request orchestration:

```text
WORKFLOW_ADAPTATION.md
REQUEST_ORCHESTRATION.md
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
REQUEST_ORCHESTRATION.md
```

Rules:

- no persistent mutation without the required C-level approval;
- no external communication without C4 approval;
- no critical, destructive, secret or Docker socket action without C5 policy;
- no memory promotion without C3 review and Evidence Pack;
- no skill activation without candidate review;
- no unsupported consequential output without Evidence Pack;
- no workflow canonization without review;
- no adaptive workflow change that bypasses THEMIS, APOLLO, approvals or tool policy;
- no AGORA consultation may expose raw chain-of-thought;
- no inter-agent agreement may replace THEMIS, APOLLO or required human approval.

---

# 3. Agent responsibilities

| Agent | Function | Governance responsibility |
|---|---|---|
| ZEUS | Global arbitration | Selects, combines, suspends, reroutes or requests workflow refactor; arbitrates variants and inter-agent disagreement without bypassing approval |
| METIS | Request framing and tactical optimization | Classifies the user request, interprets intent, detects implicit needs, selects answer strategy and orients roles/skills before ATHENA arranges the method |
| ATHENA | Planning and workflow arrangement | Breaks task into steps, identifies task contract, arranges workflows and options |
| ARGOS | Observation | Extracts facts, separates facts from assumptions, identifies available inputs and missing sources |
| THEMIS | Rules and responsibility | Classifies approval level, vetoes unsafe actions and unsafe workflow transitions |
| APOLLO | Final validation | Checks coherence, completeness, confidence, evidence, unsupported claims and adherence to the initial brief |
| PROMETHEUS | Alternatives and contradiction | Finds flaws, blind spots, counterarguments and alternative workflow paths; proposes variants when useful |
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

AGORA is not an agent.

AGORA is a bounded consultation mode used when several roles need to compare variants, state risks, request revision or help ZEUS arbitrate.

---

# 4. Request framing responsibilities

METIS is the primary role for request framing.

METIS intervenes when a request is:

```text
vague
ambiguous
multi-domain
technical
regulatory
contractual
financial
legal-sensitive
project-context-dependent
likely to need current sources
likely to need several interpretations
likely to be answered wrongly by a short direct response
```

METIS may use or request the following candidate skills:

```text
request_classification
request_intent_enrichment
context_scope_expansion
knowledge_selection
```

METIS must choose one of these answer strategies:

```text
answer_directly
answer_with_assumptions
ask_targeted_question
expand_context
route_to_workflow
```

METIS must not:

```text
answer as final authority
invent missing context
search everywhere by default
turn every question into a workflow
bypass HECATE uncertainty review when ambiguity is material
bypass THEMIS when risk is material
bypass APOLLO final coherence review
```

Example:

```text
Question: Combien d’UP il me faut ?
METIS interpretation: The user likely asks about ERP evacuation units of passage.
METIS implicit needs: type ERP, activity, occupancy, level, exits, available widths, main/accessory exit.
METIS answer strategy: answer_with_assumptions or ask_targeted_question depending on missing data.
```

---

# 5. AGORA consultation mode

AGORA is a bounded, structured forum of roles.

It is used for:

```text
variant comparison
inter-agent disagreement
revision requests
brief adherence disputes
risk versus usefulness trade-offs
workflow path selection
answer strategy selection
```

AGORA participants depend on the task.

Common participants:

```text
METIS for initial intent
ATHENA for structure and method
PROMETHEUS for alternatives
THEMIS for risk and veto
APOLLO for coherence and evidence
IRIS for clarity
ZEUS for arbitration
```

AGORA outputs visible structured summaries, not raw reasoning.

Allowed AGORA outputs:

```text
agent_revision_request
variant_set
agent_forum_review
decision_arbitration
brief_adherence_review
zeus_arbitration
```

Forbidden AGORA behavior:

```text
open-ended agent debate
raw chain-of-thought
majority vote overriding THEMIS
majority vote overriding APOLLO
workflow canonization
memory promotion
skill activation
file mutation
external communication
```

Default AGORA limit:

```text
max_rounds: 1
public_summary_only: true
zeus_arbitrates: true
```

---

# 6. Workflow adaptation responsibilities

Pantheon workflows are governed dependency graphs, not fixed linear chains.

Reference:

```text
WORKFLOW_ADAPTATION.md
REQUEST_ORCHESTRATION.md
```

Canonical split:

```text
METIS cadre la demande.
ATHENA agence les workflows.
HEPHAESTUS forge les skills.
CHRONOS règle les dépendances.
PROMETHEUS propose des variantes.
AGORA compare les options quand nécessaire.
ZEUS arbitre les options.
THEMIS bloque.
APOLLO valide.
Hermes exécute.
```

ZEUS may consult roles before or during execution.

Roles may emit structured signals such as:

```text
role_need_statement
agent_revision_request
workflow_option
variant_set
agent_forum_review
workflow_revision_signal
workflow_patch_candidate
```

They must not emit raw chain-of-thought.

---

# 7. Agent limits

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
- replace human approval where `APPROVALS.md` requires it;
- use AGORA as a hidden autonomous runtime;
- treat inter-agent agreement as final approval.

---

# 8. Approval role by agent

| Approval area | Primary agent | Secondary agents |
|---|---|---|
| C0 read / diagnostic | ATHENA | METIS, ARGOS, APOLLO |
| C1 draft / suggestion | ATHENA | METIS, IRIS, APOLLO |
| C2 reversible low-risk action | THEMIS | ZEUS, APOLLO |
| C3 persistent internal change | THEMIS | ZEUS, APOLLO |
| C4 external / contractual / responsibility action | THEMIS | IRIS, APOLLO, human user |
| C5 critical / irreversible / secrets / destructive action | THEMIS | ZEUS, APOLLO, human user |
| Request classification / intent framing | METIS | HECATE, ATHENA, ARGOS |
| Context expansion | METIS | ARGOS, HESTIA, MNEMOSYNE, knowledge_selection |
| Brief adherence review | APOLLO | METIS, ATHENA, IRIS, THEMIS |
| Variant generation | PROMETHEUS | ATHENA, IRIS |
| Variant review / AGORA | ZEUS | METIS, ATHENA, PROMETHEUS, THEMIS, APOLLO, IRIS |
| Workflow session adaptation | ZEUS | ATHENA, CHRONOS, THEMIS, APOLLO |
| Workflow candidate promotion | THEMIS | ZEUS, ATHENA, APOLLO |
| Skill candidate / skill improvement | HEPHAESTUS | THEMIS, APOLLO, ZEUS |

THEMIS can veto.

APOLLO can refuse final validation.

ZEUS can reroute but cannot bypass approval.

---

# 9. Interaction with task contracts

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
- task contract revision or resume after pause;
- structured AGORA consultation for consequential output;
- decision arbitration that affects the final output or risk level.

METIS classifies the request and answer strategy when needed.

ATHENA identifies or arranges the task contract frame.

THEMIS checks approval level.

ZEUS arbitrates execution trajectory.

APOLLO validates output.

Hermes executes the approved frame.

---

# 10. Interaction with Evidence Packs

Evidence Pack review is mandatory for consequential outputs.

METIS records when applicable:

- interpreted intent;
- request classification;
- implicit needs;
- answer strategy;
- context expansion requirement.

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

- brief adherence;
- limitations;
- completeness issues;
- proof quality;
- next safe action.

ZEUS records when applicable:

- AGORA result;
- variant selected;
- variant rejected;
- workflow option selected;
- workflow option rejected;
- workflow patch approved or rejected;
- reason for pause, resume or reset.

---

# 11. Interaction with memory

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
- METIS may identify memory relevance, but must route to HESTIA or MNEMOSYNE.
- AGORA may propose memory candidates only through the normal Memory Candidate flow.

Terminology:

```text
Use system memory, not agency memory.
```

---

# 12. Interaction with skills

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

General request-orchestration skill candidates:

```text
request_classification
request_intent_enrichment
context_scope_expansion
agent_revision_request
variant_generation
agent_forum_review
decision_arbitration
brief_adherence_review
```

Rules:

- every new skill starts as `candidate`;
- no automatic level-up;
- no active skill mutation without review;
- no skill promotion without Evidence Pack;
- Hermes local skills are not Pantheon canonical skills by default;
- HEPHAESTUS may forge or propose a skill candidate, not activate it directly.

---

# 13. Interaction with Hermes

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

# 14. Typical orchestration

## 14.1 Vague or consequential request

```text
METIS → classify and enrich intent
HECATE → expose ambiguity and hidden risks
ARGOS → inventory available facts and missing sources
ATHENA → choose response method or workflow
THEMIS → classify risk and approval
APOLLO → validate coherence and evidence
IRIS → formulate final answer
```

## 14.2 Repo consistency audit

```text
METIS → classify request and expected output
ATHENA → scope and task contract
ARGOS → files and facts
PROMETHEUS → contradictions
THEMIS → approval and policy risks
APOLLO → final diagnostic
ZEUS → final routing
```

## 14.3 Quote versus CCTP review

```text
METIS → interpret user intent and needed comparison level
ATHENA → review plan / workflow arrangement
ARGOS → quote/CCTP extraction
HEPHAESTUS → technical coherence / skill robustness
DEMETER → quantities/costs
THEMIS → contractual/responsibility risks
PROMETHEUS → missing scope and contradictions
APOLLO → final review
IRIS → client-readable wording if needed
```

## 14.4 Client message review

```text
METIS → intent and sensitivity
ATHENA → structure
IRIS → wording
THEMIS → liability and C4 validation
APOLLO → clarity, brief adherence and completeness
```

## 14.5 Variant and arbitration flow

```text
METIS → confirm true request
PROMETHEUS → generate variants
AGORA → collect bounded role opinions
THEMIS → risk/veto
APOLLO → brief adherence/evidence
ZEUS → select, combine or reject
IRIS → final wording
```

## 14.6 Adaptive workflow design

```text
ZEUS → requests consultation
METIS → frames intent and answer strategy
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

# 15. Evolution rule

A new agent must:

- represent a universal cognitive function;
- not be domain-specific;
- not duplicate an existing agent;
- have a clear governance role or reasoning value;
- be documented before use.

A new consultation mode must:

- be bounded;
- define participants;
- define outputs;
- avoid raw chain-of-thought;
- avoid runtime behavior;
- preserve THEMIS, APOLLO and human approval gates.

---

# 16. Summary

```text
Pantheon Roles = reasoning and governance roles
Hermes agents = runtime executors
Skills = reusable governed capabilities
Workflows = adaptive governed dependency graphs
AGORA = bounded consultation mode, not an agent
Task contracts = executable frames
Approvals = C0-C5 control rules
Evidence Packs = proof and audit trail
Memory = validated durable context
Hermes = execution
OpenWebUI = cockpit
Pantheon = authority
```
