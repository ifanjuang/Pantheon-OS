# HERMES_EXECUTION_MODEL.md

## Purpose

This document defines the execution model used by Pantheon Next.

Pantheon Next does not execute tools directly and does not operate as an autonomous runtime platform.

Core doctrine:

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

This file defines:

- runtime boundaries;
- execution responsibilities;
- subagent model;
- workflow supervision;
- approval interruptions;
- Evidence Pack production;
- LangGraph scope limits;
- prohibited architectural patterns.

---

# Runtime boundaries

## OpenWebUI

OpenWebUI is the user-facing cockpit.

Responsibilities:

- chat interface;
- Knowledge Collections;
- retrieval;
- validation UI;
- approval UI;
- Evidence Pack display;
- session continuity.

OpenWebUI does not:

- execute workflows;
- canonize memory;
- route tools directly;
- operate as the orchestration runtime;
- replace Hermes.

---

## Hermes Agent

Hermes is the execution runtime.

Responsibilities:

- execute tools;
- execute workflows;
- manage subagents;
- generate Evidence Packs;
- execute Task Contracts;
- supervise runtime orchestration;
- execute approval interrupts;
- interact with local or remote inference providers.

Hermes may internally use:

- LangGraph;
- subagents;
- tool routing;
- workflow supervisors;
- runtime memory;
- retries and execution recovery.

Hermes does not:

- redefine governance;
- canonize project memory;
- bypass approvals;
- mutate governance Markdown without validation.

---

## Pantheon Next

Pantheon is the governance and domain layer.

Responsibilities:

- define doctrine;
- define workflows;
- define approvals;
- define abstract agents;
- define memory rules;
- define Task Contracts;
- define Evidence Packs;
- define governance policies;
- define execution overlays.

Pantheon does not:

- become a runtime;
- execute tools;
- orchestrate execution directly;
- become a scheduler platform;
- become a distributed agent mesh;
- become a provider routing platform;
- become a LangGraph server.

---

# Declarative cognitive agents

Pantheon defines declarative cognitive agents.

These agents are not persistent autonomous services.

They are execution roles that may be instantiated by Hermes during runtime.

Example:

```yaml
athena:
  role: planning and decomposition
  outputs:
    - plan
    - workflow_candidate
    - risks
```

Pantheon declares the role.

Hermes may instantiate the role as:

- a prompt specialization;
- a subagent;
- a LangGraph node;
- a runtime execution context.

---

# Current execution model

Current state:

```text
Pantheon snapshot
    ↓
Hermes runtime context injection
    ↓
Single runtime execution
```

The current system does not yet implement:

- real multi-agent runtime execution;
- persistent subagent orchestration;
- autonomous routing graphs;
- persistent inter-agent memory.

---

# Future execution model

Future execution should remain runtime-centralized inside Hermes.

Target pattern:

```text
OpenWebUI
    ↓
Hermes Supervisor
    ├── ATHENA
    ├── ARGOS
    ├── THEMIS
    ├── APOLLO
    ├── HEPHAESTUS
    └── IRIS
            ↓
Workflow Supervisor
            ↓
LangGraph (limited scope)
```

---

# Supervisor pattern

ZEUS acts as runtime supervisor.

Responsibilities:

- select execution roles;
- arbitrate contradictions;
- terminate workflows safely;
- request human validation;
- maintain execution boundaries.

ZEUS is not:

- a distributed orchestrator;
- a permanent daemon;
- a god-object runtime.

---

# Subagent model

Subagents are stateless execution roles.

Subagents:

- receive bounded context;
- execute a constrained task;
- produce structured outputs;
- do not persist independently;
- do not communicate freely outside runtime supervision.

Subagents should remain:

- deterministic where possible;
- auditable;
- interruptible;
- disposable.

---

# Approval interrupts

THEMIS governs approval interrupts.

Approval interrupts may:

- pause execution;
- request human validation;
- block dangerous actions;
- require explicit resume.

Approval interrupts are mandatory for:

- destructive operations;
- external communications;
- repository mutations;
- memory promotion;
- infrastructure mutations;
- financial or contractual actions.

OpenWebUI is responsible for displaying and validating approval requests.

---

# Evidence Packs

Critical workflows should generate Evidence Packs.

Evidence Packs may contain:

- workflow steps;
- sources;
- extracted facts;
- generated outputs;
- uncertainties;
- approval history;
- execution metadata;
- residual risks.

Evidence Packs are not optional for critical workflows.

---

# LangGraph policy

LangGraph may be used inside Hermes only.

Allowed uses:

- workflow supervision;
- approval interrupts;
- long-running execution;
- Evidence Pack traceability;
- recovery and replay;
- structured execution graphs.

Disallowed uses:

- Pantheon runtime orchestration;
- autonomous governance execution;
- distributed agent mesh;
- global scheduler platform;
- persistent autonomous execution.

LangGraph scope must remain limited to critical workflows.

---

# Memory boundaries

Runtime memory belongs to Hermes.

Canonical memory belongs to Pantheon governance.

Memory promotion requires:

- identifiable sources;
- validation rules;
- approval classification;
- conflict checking.

Automatic self-promotion is prohibited.

---

# Anti-patterns

The following architectures are explicitly prohibited:

- Pantheon autonomous runtime;
- Pantheon execution scheduler;
- Pantheon distributed agent mesh;
- Pantheon LangGraph server;
- persistent autonomous gods;
- unrestricted inter-agent communication;
- self-modifying governance;
- automatic canonical memory promotion;
- OpenWebUI runtime orchestration;
- duplicated execution runtimes.

---

# Architectural principle

The architecture must always preserve:

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```
