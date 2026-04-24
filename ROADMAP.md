# ROADMAP — Pantheon OS
> Consolidated roadmap for evolving Pantheon OS into a modular, governed, portable-by-design multi-agent execution system.
>
> Product thesis:
> Pantheon Next is not a chatbot.
> It is a controlled execution environment where specialized agents, explicit workflows, reusable skills, governed tools, and risk policies cooperate like a structured expert team.
---
# 1. Vision
Pantheon OS is a multi-agent system for complex professional work.
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

⸻

4. Domain Overlay Model

Each domain overlay must be able to provide its own value without modifying the core.

Each overlay may contain:

* prompts/
* skills/
* workflows/
* policies/
* trusted_sources/
* templates/
* evaluation_cases/
* domain-specific agents if needed

Activation should be configuration-driven:

* active domain
* enabled overlays
* deterministic runtime injection

Example:

domains/
  architecture/
    prompts/
    skills/
    workflows/
    policies/
    templates/
    trusted_sources/

⸻

5. Agent Pantheon

5.1 Meta / Control Agents

ZEUS

Global orchestration, arbitration, and final coordination.

ATHENA

Planning, classification, decomposition, workflow selection.

METIS

Structured deliberation, hypotheses, conflicts, uncertainty.

PROMETHEUS

Contradiction, critique, adversarial review, anti-consensus pressure.

THEMIS

Procedural legitimacy, rules coherence, process enforcement.

HERA

Post-run supervision, orchestration scoring, coherence verdict.

APOLLO

Final validation, confidence scoring, traceability checks.

HECATE

Missing-information detection, uncertainty scoring, clarification trigger.

5.2 Research and Analysis Agents

HERMES

Precheck, research routing, source strategy.

DEMETER

Document fetching and normalization.

ARGOS

Objective extraction of facts, citations, entities, relations.

ARTEMIS

Relevance filtering, noise reduction, evidence narrowing.

5.3 Memory Agents

HESTIA

Session and project continuity.

MNEMOSYNE

Agency-wide knowledge, reusable patterns, templates.

HADES

Deep retrieval, archives, long-term search.

5.4 Output Agents

KAIROS

Contextual synthesis and level-of-detail control.

DAEDALUS

Document assembly, dossiers, reports, appendices.

IRIS

Formulation, tone adaptation, clarification questions.

HEPHAESTUS

Diagrams, technical visuals, structured artifacts.

APHRODITE

Polish, presentation impact, public-facing refinement.
Never auto-enabled by default.

5.5 System Agents

ARES

Fast degraded mode, fallback execution, guard role.

POSEIDON

Load regulation, parallelism, flow control.

⸻

6. Governance Model

6.1 Criticity C1 to C5

* C1: information
* C2: simple assistance
* C3: local decision support
* C4: consequential decision
* C5: major risk

Criticity must control:

* execution depth
* number of agents
* validation needs
* veto activation
* traceability expectations

6.2 Reversibility

Each action must be classified as:

* internal note
* memory write
* external communication
* critical / irreversible action

6.3 Draft-first

Any serious action must follow:

* generation
* validation
* execution

6.4 Decision Debt

States:

* D0: resolved
* D1: provisional
* D2: conditional
* D3: blocked / critical

Each debt must preserve:

* justification
* lift condition
* optional deadline
* next review phase

6.5 Structured Veto Chain

A veto is not a raw boolean.

Each veto must include:

* verdict
* justification
* severity
* lift_condition

Target chain:

execute_agents
→ veto_check
→ veto_themis
→ veto_zeus
→ zeus_judge

Veto levels:

* warning
* blocking

⸻

7. Memory

7.1 Memory Layers

Session

Short-term run context.

Project

Decisions, constraints, assumptions, debt, project-specific continuity.

Agency / Global

Reusable patterns, templates, reference cases, accumulated knowledge.

7.2 Routing Rules

After each run:

* temporary context → session memory
* validated project decision → Hestia
* reusable pattern detected → proposal to Mnemosyne
* noise → ignored

7.3 Post-run Memory Routing

This must become explicit.

After synthesis:

* validated decision → project memory
* reusable pattern → capitalization proposal
* never dump raw output automatically

⸻

8. Documentation Strategy

The system must minimize startup context.

8.1 Auto-loaded documentation nucleus

* AGENTS.md
* ARCHITECTURE.md
* optionally one lightweight operational file

8.2 Not auto-loaded by default

* docs/learnings/
* docs/archive/
* runs/
* sessions/
* older historical material

8.3 Targeted compression

Later, some runtime-facing docs may have:

* a human-readable source version
* a condensed runtime version

Without changing the normal output style of the system.

⸻

9. Implementation Phases

The roadmap is split into 10 major phases.

⸻

10. Phase A — MVP Foundation

Goal

Build one controlled execution loop that works end to end.

Tasks

* FastAPI skeleton
* PostgreSQL + pgvector + async SQLAlchemy
* JWT auth + basic RBAC
* manifests for agents, skills, tools, workflows
* AgentBase, SkillBase, ToolBase, WorkflowBase
* SessionState, RunState, Artifact
* one minimal workflow
* one minimal agent with SOUL.md
* one tool behind a policy gate
* OpenWebUI-compatible route
* SSE streaming
* simple document ingestion
* simple retrieval with citations
* run logging

Git references

Infrastructure and API:

* tiangolo/fastapi
* sqlalchemy/sqlalchemy
* pgvector/pgvector-python

Contracts and runtime:

* All-Hands-AI/OpenHands
* pydantic/pydantic-ai
* instructor-ai/instructor
* guardrails-ai/guardrails

Agent-facing repo rules:

* agentsmd/agents.md

Manifest-first modularity:

* mnfst/manifest

Minimal startup documentation:

* nadimtuhin/claude-token-optimizer

Success criteria

* the API boots cleanly
* manifests are validated at startup
* one end-to-end workflow works
* one streamed response reaches OpenWebUI
* one document can be ingested and cited

⸻

11. Phase B — Controlled Orchestration

Goal

Separate decision from execution.

Tasks

* DecisionContext
* DecisionAction
* DecisionPlan
* DecisionEngine
* control plane / data plane split
* DAG-capable workflow execution
* support for:
    * solo
    * parallel
    * cascade
    * arena
* criticity C1-C5
* HITL checkpoints
* veto nodes
* cognitive limits by criticity
* activation triggers by agent
* structured conflict resolution

Git references

Orchestration and graphs:

* langchain-ai/langgraph

Deliberation:

* beomwookang/deliberate

Planning and routing:

* salesforce-misc/switchplane

Spec-first execution:

* JuliusBrussee/cavekit

Success criteria

* the system produces a plan before execution
* criticity changes runtime behavior
* a workflow can pause, wait for validation, and resume
* vetoes are visible and justified

⸻

12. Phase C — Context, Memory, and Efficiency

Goal

Reduce wasted context, preserve continuity, and lower token waste.

Tasks

* formal session / project / agency memory
* externalize large raw outputs
* retrieve only relevant state
* session checkpoints
* smart_read
* smart_diff
* smart_grep
* persistent cache
* session analytics
* minimal startup context
* recovery after compaction / crash

Git references

Context externalization and continuity:

* mksglu/context-mode

Reading optimization and cache:

* ooples/token-optimizer-mcp

Startup context reduction:

* nadimtuhin/claude-token-optimizer

Targeted document compression:

* JuliusBrussee/caveman

Success criteria

* the system stops injecting large raw content into prompts
* session continuity becomes robust
* repeated reads become cheaper
* the console exposes context and token metrics

⸻

13. Phase D — Policy, Security, and Governance

Goal

Make risky actions governable, auditable, and stoppable.

Tasks

* PolicyEngine
* ActionGate
* allow / block / require_approval
* secret isolation
* approval API
* lineage source → tool → agent → output
* veto severity
* lift conditions
* escalation
* explicit decision debt representation

Git references

Policy engine:

* open-policy-agent/opa

Protection and guardrails:

* wiserautomation/SupraWall
* guardrails-ai/guardrails

Success criteria

* no risky action is executed silently
* approvals are traceable
* each output can be linked to its sources and generation path

⸻

14. Phase E — Evaluation and Deliberation

Goal

Measure quality and reduce weak or overconfident reasoning.

Tasks

* EvaluationRunner
* scorecards
* workflow comparison
* metrics:
    * confidence
    * structure
    * citation quality
    * latency
    * clarification count
    * feedback
* Hera supervision scoring
* Metis deliberation artifacts
* Prometheus contradiction checks
* bullshit risk scoring
* Apollo validation enrichment

Git references

Evaluation:

* langchain-ai/openevals
* promptfoo/promptfoo
* langfuse/langfuse

Deliberation and anti-bullshit:

* beomwookang/deliberate
* jrcruciani/baloney-detection-kit

Success criteria

* candidate workflows can be benchmarked
* weak claims can be rejected
* orchestration gets explicit supervision feedback

⸻

15. Phase F — Structured Skills and Workflow Packs

Goal

Turn repeated patterns into reusable, versioned blocks.

Tasks

* SkillRegistry
* skill manifests
* skill versions
* workflow versions
* statuses:
    * draft
    * candidate
    * active
    * archived
* diff
* rollback
* promotion
* workflow CRUD
* seed YAML → DB
* Hermes Console visibility

Git references

Skills:

* Hermes Skills system
* micpet7514088/skills-manager

Manifests:

* mnfst/manifest

Other references:

* microsoft/semantic-kernel
* JustVugg/distillery

Success criteria

* a skill can be versioned and tested in isolation
* a workflow can be promoted or rolled back
* the runtime knows the active version explicitly

⸻

16. Phase G — Document Intelligence and Knowledge Layer

Goal

Build a strong, traceable, multimodal document layer.

Tasks

* ingest PDF, DOCX, MD, TXT
* preserve metadata:
    * file
    * page
    * section
    * language
    * source id
* hybrid retrieval
* semantic + lexical fusion
* reliable citations
* reusable synthesis cache
* markdown indexing
* later multimodal:
    * images
    * plans
    * sections
    * site photos
    * visual descriptions
    * technical qualification

Git references

Document RAG:

* deepset-ai/haystack
* run-llama/llama_index
* sahilalaknur21/SmartDocs-Multillingual-Agentic-Rag

Markdown and graph knowledge:

* Fusion/mdidx
* ADVASYS/ragraph
* neo4j/neo4j-python-driver

Success criteria

* citations preserve page/section metadata
* hybrid retrieval is more robust
* critical syntheses can be reused
* internal docs become searchable knowledge

⸻

17. Phase H — Architecture Overlay

Goal

Deliver architecture / construction value without polluting the core.

Target submodules

decisions

* decision debt D0-D3
* decision scoring
* debt filters

planning

* lots
* milestones
* dependencies
* slippage
* cascade impacts

chantier

* observations
* non-conformities
* photos
* reservations
* resolution tracking

finance

* payment situations
* change orders
* budget lines
* overrun alerts

communications

* correspondence register
* reminders
* links with actions and meeting records

webhooks

* Telegram / WhatsApp
* mention-based routing
* photo support
* Hestia continuity
* sender authentication

Vitruve

* project exploration agent
* program
* topo
* soil
* PLU
* ABF
* risks
* budget / constraints coherence

Success criteria

* the overlay can be enabled without touching the core
* business skills are visible in the console
* chantier / planning / decision flows remain coherent

⸻

18. Phase I — Observability and Console

Goal

Make Pantheon inspectable and controllable.

Tasks

* prompt traces
* decision traces
* tool call traces
* scores and feedback
* blocked actions
* workflow comparison UI
* run state
* runtime metrics
* agent / skill / workflow toggles
* logs
* errors
* replay later

Git references

Observability:

* langfuse/langfuse
* dagster-io/dagster
* wandb/wandb

Success criteria

* operators can understand why a run produced a result
* blocked actions, scores, paths, and versions are visible
* agents and skills can be controlled cleanly

⸻

19. Phase J — Controlled Learning

Goal

Improve the system without silent mutation.

Tasks

* FeedbackEvent
* explicit feedback:
    * positive
    * negative
    * tags
* implicit signals:
    * copy
    * export
    * continue
    * rewrite
* LearningEngine
* GapAnalyzer
* candidate workflow generation
* human approval before activation
* pattern promotion to Mnemosyne
* later pattern → skill under control

Git references

Learning and improvement:

* stanfordnlp/dspy
* micpet7514088/autogap
* swapedoc/hermes2anti

Success criteria

* negative feedback produces process improvements
* the system proposes candidate versions, never silent mutations
* Mnemosyne receives useful patterns, not noise

⸻

20. Phase K — Software / Code Branch

Goal

Add a software specialization without making it universal.

Tasks

* minimal_code_context
* change_impact_analysis
* architecture_map
* review workflows
* debug workflows
* repo onboarding
* pre-merge checks

Git references

* tirth8205/code-review-graph

Success criteria

* the software branch improves code workflows
* it remains a domain branch
* it does not become a universal dependency

⸻

21. Phase L — Durable Execution and Portability

Goal

Prepare for long runs, recovery, and migration.

Tasks

* checkpoints
* retries
* replay runner
* memory export/import
* workflow bundles
* server-to-server migration
* durable orchestration later only if justified

Git references

* samuelcolvin/arq
* temporalio/temporal
* awizemann/scarf

Success criteria

* long workflows can resume
* project and agency memory are exportable
* runs are replayable for debugging and validation

⸻

22. Phased Optimization Strategy

Example-driven optimization must remain disciplined.

Phase 1

Instrumentation only.

Phase 2

Optimize only stable, structured tasks:

* criticity classification
* action extraction
* metadata extraction
* repeatable transformations

Phase 3

Possibly extend to Hermes or Zeus if examples become sufficient.

Rules

* never blindly optimize SOUL.md
* avoid optimizing highly identity-defining or creative agents first
* never sacrifice system character for shallow optimization

⸻

23. External Channels and Voice

This belongs as an extension, not in the initial kernel.

Targets

* Telegram
* WhatsApp
* voice
* TTS
* STT
* authenticated sender mapping
* mention-based routing
* Hermes fallback
* Hestia continuity across channels

⸻

24. Git Repo Governance

Recommended branching model:

* main: stable
* develop: integration
* experiment/*: exploratory work
* overlay/*: domain overlays

Rules:

* every schema change requires a migration
* every critical block requires regression tests
* V3 experiments remain isolated

⸻

25. External Inspiration Map

Adopt now

agentsmd/agents.md

Use it as the model for AGENTS.md as the root agent-facing file.

Hermes Skills system

Use it for skills as documented, categorized, activatable units.

mnfst/manifest

Use it for strong declarative manifests and enriched contracts.

nadimtuhin/claude-token-optimizer

Use it for minimal startup context.

Claude Cowork rules

Use them for:

* hard rules
* retros
* final-pass gates
* read-in-full discipline
* crash resilience

V2

mksglu/context-mode

Use it for:

* raw context externalization
* session continuity
* targeted state retrieval
* code-based analysis instead of context overload

micpet7514088/autogap

Use it for:

* gap analysis
* goal hypothesis
* top blockers
* macro-step planning

ooples/token-optimizer-mcp

Use it for:

* smart reads
* persistent cache
* session analytics

JuliusBrussee/cavekit

Use it for:

* spec-first execution
* acceptance criteria
* dependency graphs
* build/check loops

V3

swapedoc/hermes2anti

Use it for:

* learning loops
* pattern promotion
* failure/success memory

JuliusBrussee/caveman

Use it for:

* runtime document compression
* not for the system’s response style

Domain-specific code branch

tirth8205/code-review-graph

Use it for:

* blast radius
* minimal code context
* targeted review

Watchlist

All-Hands-AI/OpenHands

Watch for:

* public/private packaging
* loading order
* runtime patterns

OpenHands/software-agent-sdk

Watch for:

* runtime SDK
* contracts
* registry ideas

⸻

26. Final Target

Pantheon Next must become an execution environment where:

* agents remain replaceable
* workflows remain versioned
* skills remain reusable
* tools remain governed
* memory remains structured
* evaluation drives improvement
* human validation controls risk
* domain overlays carry business value
* the core stays thin, portable, and generic

Final thesis:

Turn AI from a chat interface into a structured working team for complex professional tasks.

If you want, the next clean step is `domains/architecture/ROADMAP.md` in English as well.