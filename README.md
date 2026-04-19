# Pantheon OS

> Intelligence opérationnelle multi-agents pour organisations à haute technicité.
> Gestion documentaire, RAG sémantique, orchestration multi-agents, suivi de projet, planification et finances — sur l'ensemble du cycle de vie des dossiers.

**Stack :** FastAPI · PostgreSQL + pgvector · LangGraph · MinIO · Ollama / OpenAI · ARQ / Redis · Docker Compose

→ Développer : [CLAUDE.md](CLAUDE.md) | Changelog : [CHANGELOG.md](CHANGELOG.md)

---

## Démarrage rapide

```bash
cp .env.example .env
# Renseigner : DATABASE_URL, JWT_SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD
# Choisir le domaine actif : DOMAIN=btp|droit|audit|conseil|medecine|it

docker compose up -d
docker compose exec api alembic upgrade head
# API  → http://localhost:8000
# Docs → http://localhost:8000/docs  (DEBUG=true)
```

---

## Le Panthéon — 22 agents

Convention : `{"agent": "ZEUS", "role": "orchestrator"}` — identité (mythe) ≠ responsabilité (rôle).

| Couche | Agent | Classe | Rôle | Veto |
|---|---|---|---|---|
| **Meta** | Zeus | `ZeusOrchestrator` | orchestrator | |
| | Héra | `HeraSupervisor` | supervisor | |
| | Artémis | `ArtemisFilter` | filter | |
| | Kairos | `KairosSynthesizer` | synthesizer | |
| | Apollon | `ApollonValidator` | validator | |
| **Perception** | Hermès | `HermesRouter` | router | |
| **Analyse** | Athéna | `AthenaPlanner` | planner | |
| | Argos | `ArgosExtractor` | extractor | |
| | Prométhée | `PrometheeChallenger` | challenger | |
| | Dionysos | `DionysosCreative` | creative | |
| | Déméter | `DemeterCollector` | collector | |
| | Hécate | `HecateResolver` | uncertainty_resolver | |
| **Cadrage** | Thémis | `ThemisValidator` | legal_validator | ✅ |
| | Chronos | `ChronosPlanner` | time_planner | |
| **Système** | Arès | `AresSecurity` | security_guard | ✅ |
| | Poséidon | `PoseidonDistributor` | distributor | |
| **Continuité** | Hestia | `HestiaMemory` | memory_project | |
| | Mnémosyne | `MnemosyneMemory` | memory_agency | |
| | Hadès | `HadesMemory` | memory_longterm | |
| **Communication** | Iris | `IrisCommunicator` | communicator | |
| | Iris (clarifier) | `IrisClarifier` | clarifier | |
| | Métis | `MetisEditor` | editor | |
| **Production** | Dédale | `DedaleBuilder` | builder | |
| | Héphaïstos | `HephaistosBuilder` | diagram_builder | |
| | Aphrodite | `AphroditeStylist` | stylist | |

Source de vérité : [`config/agent_registry.yaml`](config/agent_registry.yaml)

---

## Criticité C1-C5

| Niveau | Nature | Mode | Max agents |
|---|---|---|---|
| **C1** | Information | Agent unique, pas de Zeus | 1 |
| **C2** | Question | 1-2 agents spécialisés | 2 |
| **C3** | Décision locale réversible | Zeus optionnel, Arès peut agir | 4 |
| **C4** | Décision engageante | Zeus + validation humaine (HITL) | 6 |
| **C5** | Risque majeur | Zeus + HITL + veto obligatoire | 8 |

---

## Les 3 mémoires

| Mémoire | Agent | Scope | Durée |
|---|---|---|---|
| **Agence** | Mnémosyne | `scope='agence'` — patterns, leçons, précédents | Permanente |
| **Projet** | Hestia | `scope='projet'` — décisions, contraintes, dettes D0-D3 | Durée affaire |
| **Fonctionnelle** | Hermès + Chronos | Redis TTL `memory:fn:{thread_id}:*` | Session (1 h) |

---

## Domaines

Le domaine actif est sélectionné via `.env` :

```bash
DOMAIN=btp        # btp | droit | audit | conseil | medecine | it
DOMAIN_LABEL="Architecture & Maîtrise d'Œuvre"
```

Chaque domaine injecte automatiquement dans tous les SOUL.md : contexte métier, sources web prioritaires, mots-clés de criticité et patterns de veto spécifiques (`agents/domains/{domain}.yaml`).

---

## Architecture

```
ARCEUS/
├── core/                   # Meta-agents (Zeus, Héra, Artémis, Kairos, Hermès, Athéna)
│   ├── _base.py            # AgentBase — contrat commun (agent ≠ role)
│   └── {myth}/SOUL.md      # Personnalité de chaque meta-agent
├── agents/                 # 16 agents spécialisés
│   ├── domains/            # Overlays domaine (btp|droit|audit|conseil|medecine|it)
│   └── {myth}/SOUL.md
├── config/
│   └── agent_registry.yaml # Registre unique : role, layer, class, triggers, veto
├── api/
│   ├── main.py
│   └── modules/
│       ├── auth/           # JWT, RBAC (admin/moe/collaborateur/lecteur)
│       ├── affaires/       # Dossiers + contexte enrichi + domaine
│       ├── documents/      # Upload, ingest RAG
│       ├── agent/          # Boucle ReAct, mémoire, outils RAG+web
│       ├── orchestra/      # LangGraph Zeus, C1-C5, HITL, SSE streaming
│       ├── meeting/        # Analyse CR, extraction actions, OJ
│       ├── guards/         # Criticité / réversibilité / boucle / veto
│       ├── memory/         # Mémoire fonctionnelle Redis TTL
│       ├── monitoring/     # KPIs (durée, coût, vetos, scoring)
│       └── control/        # Dashboard WebSocket — runs, trace, erreurs
├── alembic/versions/       # Migrations 0001→0027
└── ui/                     # Dashboard Next.js (RunList, TraceViewer)
```

---

## Modules

| Module | Statut | Description |
|---|---|---|
| `auth` | ✅ | JWT, RBAC 4 rôles |
| `admin` | ✅ | Config YAML, setup wizard, healthcheck |
| `affaires` | ✅ | CRUD + contexte enrichi + domaine multi-secteur |
| `documents` | ✅ | Upload + RAG + trigger Thémis |
| `agent` | ✅ | ReAct, mémoire dynamique, outils |
| `orchestra` | ✅ | LangGraph Zeus, C1-C5, HITL, veto, SSE |
| `meeting` | ✅ | Analyse CR, actions, ordre du jour |
| `guards` | ✅ | Criticité, réversibilité, veto structuré |
| `memory` | ✅ | Mémoire fonctionnelle Redis TTL |
| `monitoring` | ✅ | KPIs observabilité, scoring décisionnel |
| `control` | ✅ | Dashboard WebSocket temps réel |
| `evaluation` | ✅ | OpenClaw — harness d'éval reproductible |
| `decisions` | ⬜ | CRUD project_decisions, dette D0-D3 |
| `planning` | ⬜ | Gantt, lots, impacts cascade |
| `finance` | ⬜ | Situations, avenants, budget |
| `communications` | ⬜ | Registre courrier |

---

## Variables d'environnement clés

```bash
DATABASE_URL=postgresql+asyncpg://arceus:password@db:5432/arceus
LLM_PROVIDER=ollama           # ou "openai"
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=mistral:7b
EMBEDDING_PROVIDER=ollama
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIM=768
REDIS_URL=redis://redis:6379/0
DOMAIN=btp                    # domaine actif
DOMAIN_LABEL="Architecture & Maîtrise d'Œuvre"
ADMIN_EMAIL=admin@agence.fr
ADMIN_PASSWORD=changeme
```
