# Pantheon OS — Project context for Claude Code agents

## Overview

**Pantheon OS** is a multi-agent intelligence platform for professional organizations (architecture/MOE, with planned overlays for legal, audit, consulting, medicine, IT). It centralizes document management, semantic RAG, multi-agent orchestration, project tracking, planning, and finance across the full lifecycle of cases.

**Stack (MVP):** FastAPI · PostgreSQL + pgvector · Hermes Runtime (agents/skills/workflows) · OpenWebUI · Ollama/OpenAI · Docker Compose

---

## Architecture

```
pantheon-os/
│
├── core/                          # Pure runtime framework (no domain logic)
│   ├── contracts/                 # AgentBase, SkillBase, ToolBase, WorkflowBase, manifests
│   ├── engine/                    # WorkflowEngine — async step executor
│   ├── routing/                   # HermesRouter — intent → workflow mapping
│   ├── state/                     # SessionState — per-run context
│   ├── registries/                # ManifestLoader — auto-discovery via manifest.yaml
│   ├── validation/                # CompletenessChecker, CoherenceChecker
│   ├── policies/                  # VetoEngine — veto pattern matching
│   ├── observability/             # HermesLogger — structured run logging
│   └── utils/                     # Shared helpers (truncate, Timer)
│
├── agents/                        # 24 agents — auto-discovered via manifest.yaml
│   ├── meta/                      # zeus_orchestrator, athena_planner, apollo_validator,
│   │                              #   themis_guardian, hera_supervisor, chronos_scheduler
│   ├── analysis/                  # hermes_router, demeter_collector, argos_extractor,
│   │                              #   prometheus_challenger, artemis_filter,
│   │                              #   hecate_uncertainty, metis_deliberator
│   ├── memory/                    # hestia_project, mnemosyne_agency, hades_retrieval
│   ├── output/                    # kairos_synthesizer, daedalus_builder, iris_communicator,
│   │                              #   aphrodite_stylist, hephaestus_diagrams, dionysos_creative
│   └── system/                    # ares_executor, poseidon_distributor
│
├── skills/                        # Reusable skill packs
│   └── generic/                   # build_dossier, cross_check, extract_facts,
│                                  #   hybrid_research, summarize
│
├── tools/                         # Atomic capabilities used by skills
│   ├── database/  diagrams/  file/  pdf/  storage/  web/
│
├── workflows/                     # Multi-agent orchestrations
│   ├── base/                      # clarification, dossier_build, research, simple_answer
│   ├── dynamic/                   # deep_research
│   ├── document_analysis/         # Document-driven analysis pipelines
│   └── templates/                 # YAML workflow templates
│
├── platform/
│   ├── api/                       # FastAPI server
│   │   ├── apps/                  # Functional API modules (27 — see modules.yaml)
│   │   │   ├── auth/              # JWT login, register, seed admin
│   │   │   ├── admin/             # Config YAML, setup wizard, healthcheck
│   │   │   ├── affaires/          # Case/project CRUD
│   │   │   ├── documents/         # Upload, RAG ingest
│   │   │   ├── agent/             # ReAct loop, memory, RAG tools
│   │   │   ├── openai_compat/     # OpenAI v1 compatibility (OpenWebUI)
│   │   │   ├── hermes_console/    # Console API: agents/skills/workflows/logs
│   │   │   ├── approvals/         # Approval gate (HITL) — V2 prep
│   │   │   ├── memory/            # Memory candidates / promotion / search — V2 prep
│   │   │   ├── orchestra/         # Multi-agent orchestration runs — V2
│   │   │   ├── flowmanager/       # Workflow definitions store — V2
│   │   │   ├── guards/            # Veto / safety enforcement — V2
│   │   │   └── ...                # capture, chantier, communications, decisions,
│   │   │                          #   evaluation (CI), finance, meeting, planning,
│   │   │                          #   preprocessing, scoring, webhooks, wiki
│   │   ├── core/                  # API-specific: settings, auth, registry, logging, rate_limit
│   │   ├── pantheon_runtime/      # Read-only context-pack endpoint
│   │   ├── pantheon_domain/       # Domain layer repository
│   │   ├── main.py                # Entry point (lifespan, CORS, module registry)
│   │   └── database.py            # SQLAlchemy async engine + Base
│   ├── ui/
│   │   ├── openwebui/             # OpenWebUI config
│   │   └── hermes-console/        # Next.js admin console
│   ├── data/                      # db init SQL, vector data, runtime state, logs
│   ├── storage/                   # nas/, drive-sync/, notion-sync/, exports/
│   └── infra/
│       ├── docker/api/            # Dockerfile for API container
│       ├── compose/               # docker-compose.v2.yml (V2 full stack)
│       ├── migrations/            # Alembic migration copies
│       └── deploy/                # Deployment scripts
│
├── domains/                       # Domain overlays (active: architecture_fr)
│   ├── general/                   # Generic socle — agnostic skills
│   └── architecture_fr/           # BTP/MOE FR overlay (skills, workflows, policies, prompts)
│
├── config/                        # 6 canonical YAML files
│   ├── runtime.yaml               # Hermes mode, thresholds, MVP agent list
│   ├── settings.yaml              # LLM, RAG, API parameters
│   ├── sources.yaml               # Data source adapters (db, NAS, web, Notion)
│   ├── ui.yaml                    # Console and OpenWebUI settings
│   ├── domains.yaml               # Domain overlay mapping (active_domain, overlays)
│   └── policies.yaml              # Veto patterns, safety, rate limits, trusted sources
│
├── docs/
│   └── governance/                # Governance docs (AGENTS, ARCHITECTURE, MODULES,
│                                  #   ROADMAP, STATUS, MEMORY, APPROVALS, ...)
├── ai_logs/                       # AI session journal: README.md (rules) +
│                                  #   YYYY-MM-DD-slug.md per intervention
├── hermes/                        # Hermes integration: skill policy + repo references
├── operations/                    # Operating protocols (OpenWebUI/Hermes/Pantheon)
├── scripts/                       # install/, update/, openclaude-setup.sh
├── legacy/                        # Archived modules and obsolete docs (not loaded)
│
├── tests/                         # Flat pytest suite (test_*.py)
├── alembic/                       # Migrations: 0001 → 0028 → 20260426_0001
├── docker-compose.yml             # MVP stack
├── modules.yaml                   # FastAPI app module registry (enabled/disabled)
├── plugins.yaml                   # Optional service plugins (ollama, portainer, ...)
├── alembic.ini                    # Alembic config
└── .env.example                   # Environment template
```

---

## MVP vs V2

| Component | MVP | V2 |
|---|---|---|
| **OpenWebUI** | ✅ Chat UI + Hermes Console tab | ✅ |
| **FastAPI** | ✅ API server | ✅ |
| **Hermes Runtime** | ✅ Agents/skills/workflows | ✅ |
| **PostgreSQL + pgvector** | ✅ State + vector memory | ✅ |
| **Ollama / OpenAI** | ✅ LLM provider | ✅ |
| **LangGraph** | ❌ (not needed for MVP) | ✅ complex state machines |
| **Redis + ARQ** | ❌ (not needed for MVP) | ✅ background jobs |
| **MinIO** | ❌ (local storage) | ✅ large file S3 storage |
| **Advanced observability** | ❌ | ✅ |

---

## The Pantheon — 24 agents

### Naming convention

```python
class Zeus(AgentBase):
    agent = "@ZEUS"         # @AGENT = meta authority (ALL CAPS)
    role  = "orchestrator"  # stable responsibility (system logic)

class Hermes(AgentBase):
    agent = "@Hermes"       # @Agent = operational agent (PascalCase)
    role  = "router"
```

### MVP agents (enabled at startup)

| Agent | Layer | Role | Description |
|---|---|---|---|
| **@ZEUS** | meta | orchestrator | Global orchestration — execution order, merge/fork/child workflows |
| **@ATHENA** | meta | planner | Planning and decomposition — task analysis, agent selection |
| **@APOLLO** | meta | validator | Final validation — reliability scoring, release decision |
| **@Hermes** | analysis | router | Research router — source selection, skill activation |
| **@Argos** | analysis | extractor | Factual extraction — facts, figures, citations |
| **@Prometheus** | analysis | challenger | Contradiction detection — source comparison, inconsistency flags |
| **@Hecate** | analysis | uncertainty_resolver | Uncertainty detection — missing info, clarification questions |
| **@Hestia** | memory | session_memory | Session memory — immediate context, run continuity |
| **@Hades** | memory | vector_retrieval | Deep memory — pgvector semantic retrieval |
| **@Kairos** | output | synthesizer | Contextual synthesis — information hierarchization |
| **@Daedalus** | output | builder | Deliverable construction — dossiers, briefs, reports |
| **@Iris** | output | communicator | Communication — context reformulation, tone adaptation |

### Extended agents (V2, disabled by default)

| Agent | Layer | Role |
|---|---|---|
| **@THEMIS** | meta | Process integrity guardian (veto) |
| **@HERA** | meta | Global coherence supervisor |
| **@CHRONOS** | meta | Scheduling and temporal coordination |
| **@Demeter** | analysis | Data collection and ingestion |
| **@Artemis** | analysis | Filtering and focus (signal/noise) |
| **@Metis** | analysis | Tactical optimization |
| **@Mnemosyne** | memory | Structured knowledge library |
| **@Aphrodite** | output | Polish and presentation |
| **@Hephaestus** | output | Diagrams and technical production |
| **@Dionysos** | output | Creative variation and ideation |
| **@Ares** | system | Fast execution / fallback mode |
| **@Poseidon** | system | Load management and flow control |

Source of truth: `agents/{layer}/{myth}_{role}/manifest.yaml`

---

## Data model (MVP tables)

| Table | Description |
|---|---|
| `users` | User accounts, RBAC role |
| `affaires` | Project cases + context (domain, typology, region, budget, phase) |
| `affaire_permissions` | Per-case role override |
| `documents` | Uploaded files (PDF/DOCX/TXT/images) |
| `chunks` | RAG fragments, `vector(768)`, HNSW index |
| `agent_runs` | Agent execution traces (steps, RAG sources, duration) |
| `agent_memory` | Learned lessons — `scope`: `agence` or `projet` |

---

## Module structure

### Agent module (`agents/{layer}/{myth}_{role}/`)

```
zeus_orchestrator/
├── agent.py          # AgentBase subclass
├── manifest.yaml     # id, name, layer, role, enabled, veto, description
├── config.yaml       # max_tokens, temperature, timeout_s
├── SOUL.md           # System prompt (brand identity)
└── tests/
    └── test_agent.py
```

```python
from pathlib import Path
from core.contracts.agent import AgentBase


class Zeus(AgentBase):
    agent = "@ZEUS"
    role = "orchestrator"
    layer = "meta"
    veto = False
    _soul_dir = Path(__file__).parent
```

### FastAPI app module (`platform/api/apps/{name}/`)

```
auth/
├── __init__.py
├── manifest.yaml     # name, version, prefix, depends_on
├── models.py         # SQLAlchemy models (inherit database.Base)
├── schemas.py        # Pydantic request/response schemas
├── service.py        # Business logic
└── router.py         # def get_router(config: dict) -> APIRouter
```

---

## Hermes Console API (`/console`)

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/console/dashboard` | user | Summary stats |
| GET | `/console/agents` | user | List all agents |
| POST | `/console/agents/{name}/toggle` | admin/moe | Enable/disable agent |
| GET | `/console/skills` | user | List all skills |
| POST | `/console/skills/{id}/toggle` | admin/moe | Enable/disable skill |
| GET | `/console/workflows` | user | List all workflows |
| POST | `/console/workflows/{id}/toggle` | admin/moe | Enable/disable workflow |
| GET | `/console/settings` | user | Get runtime settings |
| POST | `/console/settings` | admin | Update runtime settings |
| GET | `/console/logs` | user | Get recent logs |

---

## Config files (6 canonical, source of truth)

| File | Purpose |
|---|---|
| `config/runtime.yaml` | Hermes mode, max_agents, thresholds, MVP agent list |
| `config/settings.yaml` | LLM, embeddings, RAG, API parameters |
| `config/sources.yaml` | Data source adapters (pgvector, NAS, web, Notion) |
| `config/ui.yaml` | Console and OpenWebUI settings |
| `config/domains.yaml` | Active domain, overlay paths, trusted sources |
| `config/policies.yaml` | Veto patterns, safety, rate limits, domain trusted sources |

Agent/skill/workflow enable state lives in each `{agents|skills|workflows}/{path}/config.yaml`.
FastAPI app enable state lives in `modules.yaml` at the repo root.

---

## Important rules

- Always inherit `database.Base` for SQLAlchemy models
- Always declare new tables in `alembic/env.py`
- Always create an Alembic migration for schema changes
- Circular imports → late imports inside functions
- Shared services (`RagService`, `LlmService`) → classmethods
- Auth: `Depends(get_current_user)`, `Depends(require_role("admin", "moe"))`
- **No LangGraph in MVP** — use simple async pipelines
- **No Redis/ARQ in MVP** — use FastAPI `BackgroundTasks` if needed
- Agent source of truth: `agents/{layer}/{myth}_{role}/` — not YAML registries
- Archived code and obsolete docs live under `legacy/` — never imported by the runtime

---

## Code patterns

### SQLAlchemy 2.0
```python
result = await db.execute(select(Model).where(Model.field == value))
items = result.scalars().all()
```

### pgvector (cosine similarity)
```python
rows = await db.execute(
    text("SELECT ... 1 - (embedding <=> :vec::vector) AS score FROM chunks WHERE ..."),
    {"vec": str(embedding_list), ...}
)
```

---

## Launch

```bash
cp .env.example .env
# Edit .env — change DB_PASSWORD and JWT_SECRET_KEY at minimum
docker compose up -d
docker compose exec api alembic upgrade head
# API docs:  http://localhost:8000/docs  (DEBUG=true only)
# Chat UI:   http://localhost:3000
# Console:   http://localhost:3000 → Hermes Console tab
```

### V2 stack
```bash
docker compose -f docker-compose.yml -f platform/infra/compose/docker-compose.v2.yml up -d
```

---

## Key environment variables

```bash
# Database
DATABASE_URL=postgresql+asyncpg://pantheon:password@db:5432/pantheon
DATABASE_URL_SYNC=postgresql://pantheon:password@db:5432/pantheon

# Auth
JWT_SECRET_KEY=your-secret-min-32-chars
ADMIN_EMAIL=admin@yourorg.com
ADMIN_PASSWORD=strongpassword

# LLM (choose one)
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=mistral:7b
# or: LLM_PROVIDER=openai  OPENAI_API_KEY=sk-...

# Embeddings
EMBEDDING_PROVIDER=ollama
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIM=768

# Domain (only architecture_fr is active in MVP; general is the shared base layer)
DOMAIN=architecture_fr
DOMAIN_LABEL="Architecture & Maîtrise d'Œuvre (FR)"

# Runtime
DEBUG=true
```

---

## Alembic migrations

Run `alembic upgrade head` after each schema change.

| Migration | Content |
|---|---|
| 0001 | users, affaires, permissions, documents, chunks |
| 0002 | agent_runs |
| 0003 | orchestra_runs |
| 0004 | agent_memory |
| 0005–0028 | V2 features (guards, wiki, scoring, workflow_definitions, etc.) |
| 20260426_0001 | approval_requests (HITL approval gate) |

---

## Changelog

`CHANGELOG.md` at root documents all notable changes.

**Rule**: every functional commit must add an entry in `[Unreleased]`. On release, rename with version + date.

SemVer:
- **MAJOR**: breaking API or non-retrocompatible DB schema change
- **MINOR**: new feature, module, or pattern
- **PATCH**: bug fix, optimization, internal refactoring
