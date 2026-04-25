# ROADMAP — Pantheon Next

> Consolidated roadmap for evolving Pantheon OS into a modular, governed, portable-by-design multi-agent execution system.
>
> Product thesis:
> Pantheon Next is not a chatbot.
> It is a controlled execution environment where specialized agents, explicit workflows, reusable skills, governed tools, and risk policies cooperate like a structured expert team.

---

# 1. Vision

Pantheon Next is a multi-agent system for complex professional work.

It targets environments with high density of rules, documents, coordination, and accountability:

- architecture
- project management
- compliance
- legal work
- audit
- consulting
- IT
- research and documentation-heavy work

The system must remain:

- modular
- explainable
- inspectable
- governed
- portable across domains

The runtime must stay generic.
Business value must live in domain overlays.

---

# 2. Preservation Rules

This is the most important section.
Every refactor, optimization, or new capability must preserve these rules.

## 2.1 The core remains domain-agnostic

The core provides:

- contracts
- execution
- routing
- state
- registries
- policies
- evaluation
- observability
- memory
- document services

The core must not contain architecture-specific, legal-specific, or business-specific logic.

## 2.2 Filesystem-driven modularity remains

Adding an agent, skill, tool, or workflow must remain as simple as:

- creating a folder
- declaring a manifest
- exposing a valid contract

The runtime discovers modules.
The core code should not need to change for every new block.

## 2.3 Agent, skill, tool, and workflow remain distinct

- an agent reasons
- a skill applies a reusable capability
- a tool performs a technical or external action
- a workflow structures global execution

These layers must not collapse into each other.

## 2.4 Workflows remain explicit

Execution must remain:

- structured
- visible
- traceable
- testable

The system must not drift toward an implicit chain of prompts.

## 2.5 Governance remains explicit

Pantheon must preserve:

- criticity
- reversibility
- draft-first
- veto
- escalation
- human validation for risky actions
- decision debt

## 2.6 Memory remains multi-layered and selective

Pantheon must preserve:

- session memory
- project memory
- agency/global memory

Memory must never become a context dump.

## 2.7 Structured outputs remain mandatory

For serious runs, outputs must continue to expose:

- context
- findings
- analysis
- certainty
- impacts
- options
- validation required
- memory target

## 2.8 Domain overlays remain outside the core

Business value must be carried by:

- `domains/architecture/`
- `domains/legal/`
- `domains/software/`
- future overlays

Not by the runtime kernel.

---

# 3. Target Architecture

```text
platform/
  api/              FastAPI apps
  ui/               OpenWebUI integration + admin console
  data/             persistence and runtime state
  infra/            Docker, deployment, scripts

core/
  contracts/        base types and interfaces
  registry/         agent, skill, tool, workflow registries
  decision/         control plane
  execution/        data plane
  state/            session and run state
  policies/         policy engine and action gate
  evaluation/       scorecards and tests
  learning/         controlled improvement loop
  observability/    traces, logs, runs
  memory/           session, project, agency adapters
  documents/        ingestion, indexing, retrieval, citation
  packaging/        context and artifact bundles
  llm/              provider abstraction, budget, routing

modules/
  agents/           modular agents
  skills/           reusable reasoning skills
  tools/            external actions and connectors
  workflows/        workflow packs
  prompts/          prompt libraries
  templates/        output templates

domains/
  architecture/
  legal/
  software/
  consulting/