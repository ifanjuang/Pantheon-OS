Pantheon OS

Multi-agent operational intelligence platform for high-expertise environments
(architecture, project management, legal, consulting, audit, IT)

Pantheon OS combines structured data, document intelligence (RAG), and multi-agent orchestration into a single execution layer.

⸻

Core Idea

This is not a chatbot.

Pantheon OS is a runtime system where:

* agents are modular execution units
* workflows define reasoning pipelines
* tools and skills extend capabilities
* OpenWebUI is only the interface layer

The system executes controlled reasoning, not free-form prompting.

⸻

Stack

* FastAPI (API + runtime host)
* PostgreSQL + pgvector (data + semantic memory)
* OpenWebUI (chat interface)
* Ollama or OpenAI (LLM provider)
* Docker Compose (deployment)

Optional (V2):

* Redis / ARQ (async jobs)
* MinIO (object storage)
* LangGraph (complex orchestration)

⸻

Quick Start

cp .env.example .env
# Configure:
# - DB_PASSWORD
# - JWT_SECRET_KEY
# - LLM_PROVIDER (ollama or openai)
docker compose up -d
docker compose exec api alembic upgrade head

Access:

* API → http://localhost:8000
* Docs → http://localhost:8000/docs
* UI (OpenWebUI) → http://localhost:3000

⸻

Architecture

The system is split into three layers:

core/        → runtime engine (no business logic)
modules/     → agents, skills, tools, workflows (plug-and-play)
platform/    → API, UI, infrastructure

1. Core (Hermes Runtime)

Pure execution engine:

* AgentBase, SkillBase, ToolBase, WorkflowBase
* WorkflowEngine (async execution)
* HermesRouter (intent → workflow)
* SessionState (context per run)
* ManifestLoader (auto-discovery)
* VetoEngine (risk control)
* Observability (logs, traces)

No domain logic lives here.

⸻

2. Modules (Execution Units)

All intelligence is defined as self-contained modules.

modules/
├── agents/
├── skills/
├── tools/
└── workflows/

Each module is:

* isolated
* discoverable
* configurable
* optionally enabled/disabled

Agent structure

modules/agents/meta/zeus_orchestrator/
├── agent.py
├── manifest.yaml
├── config.yaml
├── SOUL.md

Example manifest

id: zeus
name: "@ZEUS"
layer: meta
role: orchestrator
enabled: true
veto: false
class: modules.agents.meta.zeus_orchestrator.agent.Zeus

Agents are loaded automatically at startup.

⸻

3. Platform

platform/
├── api/        → FastAPI (modular apps)
├── ui/         → OpenWebUI + admin console
├── data/       → database + runtime state
├── infra/      → docker, deployment

⸻

Runtime Model

Agent

An agent is defined by:

* identity (@ZEUS)
* role (orchestrator)
* layer (meta, analysis, memory, output, system)
* behavior (SOUL.md)

Base contract:

class AgentBase:
    agent: str
    role: str
    layer: str

⸻

Workflow

A workflow is a deterministic pipeline of agents.

Example:

id: research
steps:
  - hecate
  - hermes
  - argos
  - prometheus
  - kairos
  - iris
fallback: simple_answer

Workflows define execution logic, not agents.

⸻

Skills and Tools

* Skills = reusable reasoning capabilities (extraction, validation, synthesis)
* Tools = external actions (PDF, web, DB, storage)

They are injected dynamically during execution.

⸻

API Modules

FastAPI is modular via modules.yaml.

Example:

modules:
  - name: auth
    enabled: true
  - name: agent
    enabled: true
  - name: hermes_console
    enabled: true

Each module is a self-contained app:

platform/api/apps/{module}/
├── manifest.yaml
├── models.py
├── schemas.py
├── service.py
└── router.py

⸻

OpenWebUI Integration

OpenWebUI connects via OpenAI-compatible API:

OPENAI_API_BASE_URL=http://api:8000/v1
OPENAI_API_KEY=<JWT_SECRET_KEY>

This allows:

* chat interface
* tool usage
* multi-agent execution

Without exposing internal complexity.

⸻

Data Model (MVP)

Core tables:

* users → authentication
* affaires → projects / cases
* documents → uploaded files
* chunks → vectorized content
* agent_runs → execution traces
* agent_memory → learned knowledge

⸻

Auditable Memory

Pantheon OS uses structured memory to preserve continuity across affairs, agents, workflows and documents.

Memory is not an opaque summary layer. It must distinguish raw sources, validated facts, candidate facts, summaries, compact cards and orchestration traces.

The operating rule is simple: any information injected into an agent context must be inspectable, source-linked, revisable and retractable. Raw documents, raw messages, tool outputs and execution traces remain the verification base. Cards, summaries and promoted facts are derived layers, not independent truth.

The system must therefore support memory preview, source labels, candidate promotion, explicit consolidation and dry-run review before risky memory mutation.

⸻

Configuration

Single source of truth:

config/
├── runtime.yaml
├── settings.yaml
├── sources.yaml
├── ui.yaml
├── domains.yaml

Modules contain their own local config.

⸻

Design Principles

1. Modularity first
    Everything is a module (agent, skill, tool, workflow)
2. Runtime > prompts
    Execution logic replaces prompt engineering
3. Separation of concerns
    * core = engine
    * modules = intelligence
    * platform = delivery
4. Deterministic orchestration
    Workflows control reasoning, not LLM improvisation
5. Scalable architecture
    MVP runs without Redis or LangGraph
    V2 enables distributed execution
6. Auditable memory
    Context injection must be inspectable, source-linked and governed.

⸻

Roadmap

MVP (current)

* Core runtime
* Modular agents
* Basic workflows
* RAG
* OpenWebUI integration

V2

* Dynamic workflow generation
* Strategy engine
* Observability + scoring
* Async execution (Redis / ARQ)
* Multi-tenant + domain overlays
* Auditable memory lifecycle: raw history, candidate facts, active facts, summaries, compact cards, dry-run consolidation

⸻

License

Private / internal use (adapt as needed)

⸻