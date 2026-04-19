# Pantheon OS

> Multi-agent operational intelligence for high-expertise organizations.
> Document management, semantic RAG, multi-agent orchestration, project tracking, planning and finance — across the full lifecycle of cases.

**Stack:** FastAPI · PostgreSQL + pgvector · LangGraph · MinIO · Ollama / OpenAI · ARQ / Redis · Docker Compose

→ Develop: [CLAUDE.md](CLAUDE.md) | Changelog: [CHANGELOG.md](CHANGELOG.md)

---

## Quick Start

```bash
cp .env.example .env
# Fill in: DATABASE_URL, JWT_SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD
# Choose the active domain: DOMAIN=btp|droit|audit|conseil|medecine|it

docker compose up -d
docker compose exec api alembic upgrade head
# API  → http://localhost:8000
# Docs → http://localhost:8000/docs  (DEBUG=true)
```

---

## The Pantheon — 22 Agents

Convention: `{"agent": "ZEUS", "role": "orchestrator"}` — identity (myth) ≠ responsibility (role).

| Layer | Agent | Class | Role | Veto |
|---|---|---|---|---|
| **Meta** | Zeus | `ZeusOrchestrator` | orchestrator | |
| | Hera | `HeraSupervisor` | supervisor | |
| | Artemis | `ArtemisFilter` | filter | |
| | Kairos | `KairosSynthesizer` | synthesizer | |
| | Apollo | `ApollonValidator` | validator | |
| **Perception** | Hermes | `HermesRouter` | router | |
| **Analysis** | Athena | `AthenaPlanner` | planner | |
| | Argos | `ArgosExtractor` | extractor | |
| | Prometheus | `PrometheeChallenger` | challenger | |
| | Dionysus | `DionysosCreative` | creative | |
| | Demeter | `DemeterCollector` | collector | |
| | Hecate | `HecateResolver` | uncertainty_resolver | |
| **Framing** | Themis | `ThemisValidator` | legal_validator | ✅ |
| | Chronos | `ChronosPlanner` | time_planner | |
| **System** | Ares | `AresSecurity` | security_guard | ✅ |
| | Poseidon | `PoseidonDistributor` | distributor | |
| **Continuity** | Hestia | `HestiaMemory` | memory_project | |
| | Mnemosyne | `MnemosyneMemory` | memory_agency | |
| | Hades | `HadesMemory` | memory_longterm | |
| **Communication** | Iris | `IrisCommunicator` | communicator | |
| | Iris (clarifier) | `IrisClarifier` | clarifier | |
| | Metis | `MetisEditor` | editor | |
| **Production** | Daedalus | `DedaleBuilder` | builder | |
| | Hephaestus | `HephaistosBuilder` | diagram_builder | |
| | Aphrodite | `AphroditeStylist` | stylist | |

Source of truth: [`config/agent_registry.yaml`](config/agent_registry.yaml)

---

## Criticality C1-C5

| Level | Nature | Mode | Max agents |
|---|---|---|---|
| **C1** | Information | Single agent, no Zeus | 1 |
| **C2** | Question | 1-2 specialized agents | 2 |
| **C3** | Reversible local decision | Zeus optional, Ares can act | 4 |
| **C4** | Binding decision | Zeus + human validation (HITL) | 6 |
| **C5** | Major risk | Zeus + HITL + mandatory veto | 8 |

---

## The 3 Memories

| Memory | Agent | Scope | Duration |
|---|---|---|---|
| **Agency** | Mnemosyne | `scope='agence'` — patterns, lessons, precedents | Permanent |
| **Project** | Hestia | `scope='projet'` — decisions, constraints, debts D0-D3 | Case lifetime |
| **Functional** | Hermes + Chronos | Redis TTL `memory:fn:{thread_id}:*` | Session (1 h) |

---

## Domains

The active domain is selected via `.env`:

```bash
DOMAIN=btp        # btp | droit | audit | conseil | medecine | it
DOMAIN_LABEL="Architecture & Project Management"
```

Each domain automatically injects into all SOUL.md files: business context, priority web sources, criticality keywords, and domain-specific veto patterns (`agents/domains/{domain}.yaml`).

---

## Architecture

```
ARCEUS/
├── core/                   # Meta-agents (Zeus, Hera, Artemis, Kairos, Hermes, Athena)
│   ├── _base.py            # AgentBase — common contract (agent ≠ role)
│   └── {myth}/SOUL.md      # Personality of each meta-agent
├── agents/                 # 16 specialized agents
│   ├── domains/            # Domain overlays (btp|droit|audit|conseil|medecine|it)
│   └── {myth}/SOUL.md
├── config/
│   └── agent_registry.yaml # Single registry: role, layer, class, triggers, veto
├── api/
│   ├── main.py
│   └── modules/
│       ├── auth/           # JWT, RBAC (admin/moe/collaborateur/lecteur)
│       ├── affaires/       # Cases + enriched context + domain
│       ├── documents/      # Upload, RAG ingest
│       ├── agent/          # ReAct loop, memory, RAG+web tools
│       ├── orchestra/      # LangGraph Zeus, C1-C5, HITL, SSE streaming
│       ├── meeting/        # Meeting analysis, action extraction, agenda
│       ├── guards/         # Criticality / reversibility / loop / veto
│       ├── memory/         # Functional memory Redis TTL
│       ├── monitoring/     # KPIs (duration, cost, vetos, scoring)
│       └── control/        # WebSocket dashboard — runs, trace, errors
├── alembic/versions/       # Migrations 0001→0027
└── ui/                     # Next.js dashboard (RunList, TraceViewer)
```

---

## Modules

| Module | Status | Description |
|---|---|---|
| `auth` | ✅ | JWT, RBAC 4 roles |
| `admin` | ✅ | YAML config, setup wizard, healthcheck |
| `affaires` | ✅ | CRUD + enriched context + multi-sector domain |
| `documents` | ✅ | Upload + RAG + Themis trigger |
| `agent` | ✅ | ReAct, dynamic memory, tools |
| `orchestra` | ✅ | LangGraph Zeus, C1-C5, HITL, veto, SSE |
| `meeting` | ✅ | Meeting analysis, actions, agenda |
| `guards` | ✅ | Criticality, reversibility, structured veto |
| `memory` | ✅ | Functional memory Redis TTL |
| `monitoring` | ✅ | Observability KPIs, decision scoring |
| `control` | ✅ | Real-time WebSocket dashboard |
| `evaluation` | ✅ | OpenClaw — reproducible evaluation harness |
| `decisions` | ⬜ | CRUD project_decisions, debt D0-D3 |
| `planning` | ⬜ | Gantt, work packages, cascade impacts |
| `finance` | ⬜ | Progress billing, amendments, budget |
| `communications` | ⬜ | Mail registry |

---

## Key Environment Variables

```bash
DATABASE_URL=postgresql+asyncpg://arceus:password@db:5432/arceus
LLM_PROVIDER=ollama           # or "openai"
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=mistral:7b
EMBEDDING_PROVIDER=ollama
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIM=768
REDIS_URL=redis://redis:6379/0
DOMAIN=btp                    # active domain
DOMAIN_LABEL="Architecture & Project Management"
ADMIN_EMAIL=admin@agency.com
ADMIN_PASSWORD=changeme
```
