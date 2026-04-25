# Pantheon OS — Architecture
> Reference architecture document.
> This file describes the target structure and stable architectural principles of Pantheon Next.
>
> It is not a changelog.
> It is not a roadmap.
> It is not a snapshot of legacy implementation details.
---
# 1. Overview
Pantheon Next is a modular multi-agent execution system built around a strict separation between:
- control plane
- data plane
The system is designed for complex professional work where reasoning, execution, validation, memory, and governance must remain explicit, inspectable, and controlled.
Pantheon Next is not a chatbot.
It is a governed execution environment in which agents, skills, tools, workflows, policies, and memory cooperate as a structured expert system.
---
# 2. High-Level Architecture
```text
User / External Channel
        ↓
OpenWebUI / API Adapters
        ↓
FastAPI API Layer
        ↓
Session Manager
        ↓
Manifest Loader / Registries
        ↓
Workflow Engine
        ↓
Decision Engine (Control Plane)
        ↓
Execution Engine (Data Plane)
        ↓
Agents / Skills / Tools
        ↓
Memory / Documents / Knowledge
        ↓
Artifacts / Outputs

⸻

3. Architectural Principles

3.1 Domain-agnostic core

The core/ layer must remain generic.

It provides:

* contracts
* registries
* state management
* workflow coordination
* decision engine
* execution engine
* policy enforcement
* evaluation
* learning
* observability
* memory abstractions
* document services
* provider abstractions

No business-specific logic should live in the core.

3.2 Filesystem-driven modularity

Pantheon loads runtime building blocks dynamically from the filesystem.

This applies to:

* agents
* skills
* tools
* workflows
* prompts
* templates

Each runtime block is defined by a manifest and validated at startup.

3.3 Domain overlays stay outside the core

Domain-specific behavior lives in domains/{domain}/.

An overlay may define:

* prompts
* skills
* workflows
* policies
* trusted sources
* templates
* evaluation cases
* domain-specific agents if needed

Examples:

* domains/architecture/
* domains/legal/
* domains/software/

3.4 Control plane and data plane remain separate

The system must preserve a strict split between:

* the layer that decides what should happen
* the layer that executes validated decisions

This prevents hidden side effects, unclear reasoning boundaries, and prompt-driven execution drift.

3.5 Governance is a runtime concern

Criticity, reversibility, policy, vetoes, approvals, escalation, and traceability belong to runtime governance.
They must not exist only as prompt instructions.

⸻

4. Repository Structure

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

⸻

5. Core Layers

5.1 Core

The core/ layer contains the runtime engine and generic system logic.

Responsibilities:

* contracts and interfaces
* registries and manifest loading
* state management
* workflow engine
* decision engine
* execution engine
* policy engine
* evaluation
* learning
* observability
* memory routing
* document intelligence services
* LLM abstraction

The core must remain portable across domains.

5.2 Modules

The modules/ layer contains reusable runtime building blocks.

Components:

* agents
* skills
* tools
* workflows
* prompts
* templates

These are reusable execution blocks, not the place for business-specific value.

5.3 Domains

The domains/ layer contains business overlays.

This is where domain-specific behavior lives.

Examples:

* architecture decision scoring
* legal citation policies
* software review workflows
* trusted source lists
* métier-specific templates

5.4 Platform

The platform/ layer handles delivery and infrastructure.

Components:

* FastAPI services
* OpenWebUI integration
* persistence
* background jobs
* deployment
* streaming adapters
* admin console

⸻

6. Control Plane

The control plane is responsible for reasoning, planning, and governance before execution.

Main responsibilities:

* task classification
* decomposition
* deliberation
* contradiction detection
* uncertainty detection
* clarification decisions
* policy-aware routing
* escalation decisions
* final orchestration judgment

Main objects:

* DecisionContext
* DecisionAction
* DecisionPlan

Typical control-plane agents:

* ZEUS
* ATHENA
* METIS
* PROMETHEUS
* THEMIS
* APOLLO
* HECATE
* HERMES as precheck and source strategy

The control plane decides what should happen before the data plane executes it.

⸻

7. Data Plane

The data plane executes validated decisions.

Main responsibilities:

* run agents
* inject tools and skills
* execute tasks
* manage sequential and parallel execution
* produce artifacts
* persist results
* log execution traces

Main objects:

* ExecutionState
* ExecutionResult

The data plane must never bypass the governance and policy layers.

⸻

8. Workflow Engine

The Workflow Engine coordinates the execution of a workflow pack.

A workflow is an explicit execution structure, not an implicit prompt chain.

Capabilities:

* solo
* parallel
* cascade
* arena
* conditional routing
* clarification checkpoints
* pause and resume
* merge and fork flows
* child workflows later

The Workflow Engine orchestrates both the control plane and the data plane.

Future extensions may include:

* LangGraph adapter
* checkpoint-backed resume
* graph-based execution for complex workflows

⸻

9. Manifest Loader and Registries

Pantheon relies on manifests and registries as the runtime source of truth.

Responsibilities:

* discover agents, skills, tools, and workflows from disk
* validate manifests at startup
* register identities and metadata
* expose enabled and disabled state
* support version-aware loading later

Typical registries:

* AgentRegistry
* SkillRegistry
* ToolRegistry
* WorkflowRegistry

Typical manifest fields include:

* id
* name
* type
* version
* enabled
* domain
* inputs
* outputs
* dependencies
* constraints
* policy
* activation
* tags

⸻

10. Governance Layer

Pantheon governs execution through explicit runtime controls.

10.1 Criticity

Criticity levels C1-C5 control:

* execution depth
* number of agents
* approval requirements
* veto activation
* clarification thresholds
* traceability requirements

10.2 Reversibility

Actions are classified by reversibility, for example:

* internal note
* memory write
* external communication
* critical or irreversible action

10.3 Draft-first

Serious outputs must follow:

* generate
* validate
* execute

10.4 Decision debt

Pantheon tracks provisional or blocked decisions through explicit decision debt states.

10.5 Escalation

High-risk or unresolved cases trigger escalation rather than silent continuation.

⸻

11. Policy Layer

All tool calls and side-effectful actions pass through a policy gate.

Policy decisions:

* allow
* block
* require_approval

The policy layer ensures:

* safety
* auditability
* compliance
* bounded execution

Risky actions must never be silently executed.

Examples include:

* sending emails
* modifying persistent records
* external API actions with side effects
* destructive file operations
* irreversible workflow mutations

⸻

12. Veto Chain

Pantheon uses a structured veto chain.

A veto is not a raw boolean.
It is a structured runtime decision containing:

* verdict
* justification
* severity
* lift condition

Typical flow:

execute_agents
→ veto_check
→ veto_themis
→ veto_zeus
→ zeus_judge

Veto levels:

* warning
* blocking

This allows the system to stop unsafe or procedurally invalid runs in a traceable way.

⸻

13. Memory System

Pantheon uses multiple memory layers.

13.1 Session Memory

Short-term runtime continuity.

Contents:

* current run context
* recent clarifications
* intermediate artifacts
* current workflow state

13.2 Project Memory

Project-specific continuity.

Contents:

* decisions
* constraints
* assumptions
* decision debt
* validated project history

Primary owner:

* HESTIA

13.3 Agency / Global Memory

Reusable long-term knowledge.

Contents:

* reusable patterns
* templates
* reference cases
* internal know-how
* validated cross-project lessons

Primary owner:

* MNEMOSYNE

13.4 Functional Memory

Temporary execution state.

Contents:

* in-flight task state
* ephemeral task progress
* short-lived runtime continuity

This should not be confused with durable project or agency memory.

13.5 Graph Memory (later)

Future structured relational memory.

Possible contents:

* entities
* relations
* contradictions
* dependency links

Memory must remain selective.
Not everything should be stored.

⸻

14. Post-Run Memory Routing

Pantheon should explicitly route results after synthesis.

Examples:

* validated project decision → project memory
* reusable pattern → agency/global memory proposal
* temporary context → session only
* noise → ignored

This keeps memory useful and avoids uncontrolled accumulation.

A mature implementation should also support:

* candidate memory scoring
* memory hygiene checks
* stale-memory trimming
* condensation of verbose memory into pointers
* governed proposals for wiki pages, templates, or skills

⸻

15. Knowledge Layer

The knowledge layer is distinct from runtime memory.

It may contain:

* prompts
* templates
* indexed markdown
* documentation
* examples
* trusted source corpora

This layer supports retrieval, not just continuity.

⸻

16. Document Intelligence Layer

This layer handles document processing and retrieval.

Responsibilities:

* ingestion
* parsing
* chunking
* indexing
* hybrid retrieval
* citation tracking
* synthesis cache
* multilingual support

Target metadata:

* file
* page
* section
* language
* source id

Later multimodal extension:

* images
* plans
* sections
* site photos
* visual descriptions
* technical qualification

⸻

17. Evaluation and Learning

17.1 Evaluation

Pantheon evaluates:

* structure
* confidence
* citation quality
* latency
* clarification count
* workflow quality
* supervision quality

Core mechanisms:

* scorecards
* regression tests
* workflow comparison
* Hera scoring
* Apollo validation

17.2 Learning

Pantheon improves through controlled learning.

Mechanisms:

* feedback collection
* gap analysis
* candidate workflow generation
* reusable pattern proposals
* controlled promotion

Learning must remain reviewed and explicit.
No silent self-mutation.

⸻

18. Observability

Pantheon tracks:

* agent execution
* tool calls
* prompts
* decisions
* workflow versions
* scores
* feedback
* blocked actions
* approvals
* vetoes
* cost
* latency

The system must remain inspectable in production.

⸻

19. External Interfaces

OpenWebUI is the main user-facing interface, not the runtime engine.

Other interfaces may be added later:

* Telegram
* WhatsApp
* voice input/output
* external API triggers

All external channels should route through the same governed runtime.

⸻

20. Design Constraints

* no business logic in core/
* no uncontrolled tool execution
* no hidden workflow mutation
* no silent risky actions
* no runtime dependency on the UI layer
* no collapse of agent / skill / tool / workflow roles
* no uncontrolled memory growth

⸻

21. Relationship to the Roadmap

This document describes the target structure and stable architectural principles.

Implementation sequencing is defined in ROADMAP.md.

The roadmap controls:

* MVP order
* orchestration phases
* context and memory upgrades
* policy and governance rollout
* evaluation and learning phases
* domain overlay delivery
* durable execution and scaling

⸻

22. Relationship to Legacy ARCEUS

Legacy ARCEUS implementation details, current stack snapshots, old endpoint maps, and historical orchestration graphs should be preserved separately as legacy implementation references.

This document defines Pantheon Next architecture.
It should not be overloaded with old implementation snapshots.

⸻

23. Key Outcome

Pantheon Next becomes a controlled multi-agent system where reasoning, execution, validation, memory, and governance are explicit, modular, portable, and testable.