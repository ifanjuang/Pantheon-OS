# Pantheon OS — Contexte projet pour agents Claude Code

## Vue d'ensemble

**Pantheon OS** est un système d'intelligence opérationnelle multi-agents pour organisations professionnelles à haute technicité (MOE/BTP, droit, audit, conseil, médecine, IT…). Il centralise la gestion documentaire, le RAG sémantique, l'orchestration multi-agents, le suivi de projet, la planification et les finances sur l'ensemble du cycle de vie des dossiers.

Stack : **FastAPI** (async) · **PostgreSQL + pgvector** · **LangGraph** · **MinIO** · **Ollama/OpenAI** · **ARQ/Redis** · **Docker Compose**

---

## Architecture

```
ARCEUS/
├── api/
│   ├── main.py                     # Startup, lifespan, seed admin
│   ├── database.py                 # SQLAlchemy async engine + Base
│   ├── worker.py                   # ARQ worker (jobs background)
│   ├── core/
│   │   ├── auth.py                 # JWT, RBAC (admin/moe/collaborateur/lecteur)
│   │   ├── settings.py             # Pydantic Settings (.env)
│   │   ├── checkpointer.py         # LangGraph PostgreSQL checkpointer (HITL)
│   │   ├── queue.py                # ARQ Redis job queue
│   │   ├── registry.py             # Chargeur dynamique de modules
│   │   └── services/
│   │       ├── rag_service.py      # Chunking + embedding + pgvector search
│   │       ├── llm_service.py      # Chat + extraction structurée
│   │       └── storage_service.py  # MinIO S3
│   └── modules/
│       ├── auth/                   # Login, register, seed admin
│       ├── admin/                  # Config YAML, setup wizard, healthcheck
│       ├── affaires/               # Dossiers projet + contexte enrichi + domaine
│       ├── documents/              # Upload, ingest RAG, trigger Thémis
│       ├── agent/                  # Boucle ReAct, mémoire, outils RAG+web
│       ├── orchestra/              # LangGraph Zeus, C1-C5, HITL, SSE streaming
│       ├── meeting/                # Analyse CR, extraction actions, OJ
│       ├── preprocessing/          # Hermès++ : cleaning, intent, precheck gate
│       ├── guards/                 # Criticality / reversibility / loop / veto
│       ├── memory/                 # Mémoire fonctionnelle Redis TTL (session)
│       ├── monitoring/             # KPIs observabilité (durée, coût, vetos, scoring)
│       └── evaluation/             # OpenClaw — harness d'éval reproductible
├── core/                           # Meta-agents (layer: meta + perception)
│   ├── _base.py                    # AgentBase — contrat commun (agent ≠ role)
│   ├── __init__.py                 # Exports: ZeusOrchestrator, HeraSupervisor, …
│   ├── zeus_orchestrator.py        # class ZeusOrchestrator
│   ├── hera_supervisor.py          # class HeraSupervisor
│   ├── artemis_filter.py           # class ArtemisFilter
│   ├── kairos_synthesizer.py       # class KairosSynthesizer
│   ├── hermes_router.py            # class HermesRouter
│   ├── athena_planner.py           # class AthenaPlanner
│   └── zeus/ hera/ artemis/ …     # SOUL.md de chaque meta-agent
├── agents/                         # Agents spécialisés (analysis → production)
│   ├── __init__.py                 # Exports: HephaistosValidator, ThemisValidator, …
│   ├── hephaistos_validator.py     # class HephaistosValidator
│   ├── themis_validator.py         # class ThemisValidator
│   ├── apollon_researcher.py       # … (16 classes au total)
│   ├── argos/ hephaistos/ …        # SOUL.md de chaque agent spécialisé
│   └── domains/                    # Overlays domaine (btp|droit|audit|conseil|medecine|it)
├── config/
│   └── agent_registry.yaml         # Registre unique : role, layer, class, triggers, veto
├── alembic/versions/               # Migrations séquentielles 0001→0027
├── modules.yaml                    # Registre modules actifs
└── docker-compose.yml              # DB + API + MinIO + Redis + Ollama + OpenWebUI
```

---

## Le Panthéon — 22 agents

Convention de nommage : `{"agent": "ZEUS", "role": "orchestrator"}` — identité ≠ responsabilité.

| Layer | Agent | Classe Python | Rôle fonctionnel | Veto |
|---|---|---|---|---|
| **Meta** | Zeus | `ZeusOrchestrator` | orchestrator | — |
| | Héra | `HeraSupervisor` | supervisor | — |
| | Artémis | `ArtemisFilter` | filter | — |
| | Kairos | `KairosSynthesizer` | synthesizer | — |
| **Perception** | Hermès | `HermesRouter` | router | — |
| | Argos | `ArgosObserver` | observer | — |
| **Analyse** | Athéna | `AthenaPlanner` | planner | — |
| | Héphaïstos | `HephaistosValidator` | technical_validator | ✅ |
| | Prométhée | `PrometheeChallenger` | challenger | — |
| | Apollon | `ApollonResearcher` | researcher | — |
| | Dionysos | `DionysosCreative` | creative | — |
| | Hadès | `HadesAnalyst` | risk_analyst | — |
| | Poséidon | `PoseidonAnalyst` | cascade_analyst | — |
| **Cadrage** | Thémis | `ThemisValidator` | legal_validator | ✅ |
| | Chronos | `ChronosPlanner` | time_planner | — |
| | Arès | `AresExecutor` | executor | — |
| | Déméter | `DemeterOptimizer` | optimizer | — |
| **Continuité** | Hestia | `HestiaMemory` | memory_project | — |
| | Mnémosyne | `MnemosyneMemory` | memory_agency | — |
| **Communication** | Iris | `IrisCommunicator` | communicator | — |
| | Aphrodite | `AphroditeMarketer` | marketer | — |
| **Production** | Dédale | `DedaleBuilder` | builder | — |

Source de vérité : `config/agent_registry.yaml`

---

## Modèles de données

| Table | Description |
|---|---|
| `users` | Comptes utilisateurs, rôle RBAC |
| `affaires` | Dossiers projet + contexte (typology, region, budget, phase, ABF, zones) + `domain` |
| `affaire_permissions` | Override de rôle par affaire |
| `documents` | Fichiers uploadés (PDF/DOCX/TXT/images) |
| `chunks` | Fragments RAG, vecteur `vector(768)`, index HNSW |
| `agent_runs` | Traces d'exécution agent (steps, sources RAG, durée) |
| `agent_memory` | Leçons apprises — `scope` : `agence` ou `projet` |
| `orchestra_runs` | Orchestrations Zeus : plans, assignments, résultats, HITL, criticité, `run_score`, `hera_verdict` |
| `project_decisions` | Décisions structurées C1-C5 avec dette D0-D3 |
| `meeting_crs` | Comptes-rendus analysés |
| `meeting_actions` | Actions extraites avec priorité, statut, échéance |
| `meeting_agendas` | Ordres du jour générés |

---

## Criticité C1-C5

| Niveau | Nature | Mode | Max agents | Max subtasks |
|---|---|---|---|---|
| C1 | Information | Agent unique, pas de Zeus | 1 | 1 |
| C2 | Question | 1-2 agents | 2 | 2 |
| C3 | Décision locale réversible | Zeus optionnel, Arès peut agir | 4 | 3 |
| C4 | Décision engageante | Zeus + HITL humain | 6 | 5 |
| C5 | Risque majeur | Zeus + HITL + veto check | 8 | 6 |

---

## Les 3 mémoires

| Mémoire | Scope DB | Agent | Durée |
|---|---|---|---|
| **Agence** | `scope='agence'`, `affaire_id=NULL` | Mnémosyne | Permanente |
| **Projet** | `scope='projet'`, `affaire_id=<uuid>` | Hestia | Durée affaire |
| **Fonctionnelle** | Redis TTL (`memory:fn:{thread_id}:*`) | Hermès + Chronos | Session (TTL 1h) |

---

## Conventions de nommage — Pantheon OS

### Agents : identité ≠ responsabilité

```python
# Classe Python — convention MythRole
class ZeusOrchestrator(AgentBase):
    agent = "ZEUS"          # identité (stable, branding)
    role  = "orchestrator"  # responsabilité (stable, logique système)

# JSON standard (logs, events, API)
{"agent": "ZEUS", "role": "orchestrator"}
```

### SSE Events — convention `{agent}.{event}`

| Event | Emetteur | Payload clé |
|---|---|---|
| `hermes.preprocess_ready` | Hermès | intent, suggested_criticite |
| `hermes.precheck_verdict` | Hermès | verdict, criticite |
| `zeus.plans_ready` | Zeus | plans par agent |
| `zeus.decision` | Zeus | subtasks, assignments |
| `zeus.verdict` | Zeus | complete \| needs_complement |
| `agent.subtask_done` | (tout agent) | task_id, results |
| `agent.all_done` | (tout agent) | results tronqués |
| `themis.veto_detected` | Thémis | agent, role, motif, severity |
| `hera.run_score` | Héra | quality, coherence, confidence, risk |
| `hera.score_computed` | Héra | score_id, verdict, total |
| `hera.verdict` | Héra | aligned \| misaligned \| degraded |
| `kairos.final_answer` | Kairos | answer, run_id |
| `hestia.memories_written` | Hestia | count, wiki_page_id |

Events système (non agentiques) : `run_created`, `phase_start`, `done`, `error`

### Résolution SOUL.md

`_resolve_soul_path(name)` cherche dans l'ordre :
1. `core/{name}/SOUL.md` — meta-agents (zeus, hera, artemis, kairos, hermes, athena)
2. `agents/{name}/SOUL.md` — agents spécialisés

### DB — convention `agent_name`

Les colonnes `agent_name` en DB utilisent le **lowercase** (`"zeus"`, `"hephaistos"`).
La correspondance uppercase↔lowercase est garantie par `old_names` dans `agent_registry.yaml`.

---

## Généralisation multi-domaine

Le domaine actif est configuré via `.env` :

```bash
DOMAIN=btp        # btp | droit | audit | conseil | medecine | it
DOMAIN_LABEL="Architecture & Maîtrise d'Œuvre"
```

Chaque domaine a un fichier `agents/domains/{domain}.yaml` avec :
- `context_injection` — injecté automatiquement dans tous les SOUL.md
- `trusted_sources` — sources web prioritaires pour Apollon
- `criticality_keywords` — mots-clés haussant la criticité
- `veto_patterns` — patterns regex par agent (fusionnés avec les patterns statiques)

---

## Conventions de code

### Créer un nouvel agent

```
core/   (meta-agents)          agents/   (agents spécialisés)
  {myth}_{role}.py               {myth}_{role}.py
  {myth}/SOUL.md                 {myth}/SOUL.md
```

```python
from core._base import AgentBase

class MythRole(AgentBase):
    agent    = "MYTH"
    role     = "role_stable"
    layer    = "meta|analysis|framing|continuity|communication|production"
    veto     = False
    triggers = ["C3", "C4", "C5"]
    _soul_dir = Path(__file__).parent / "myth"
```

Puis ajouter dans `config/agent_registry.yaml` et `api/modules/orchestra/_shared.py:VALID_AGENTS`.

### Créer un nouveau module API

```
api/modules/{nom}/
├── __init__.py
├── manifest.yaml       # name, version, description, prefix, depends_on
├── models.py           # Modèles SQLAlchemy (héritent de database.Base)
├── schemas.py          # Schémas Pydantic request/response
├── service.py          # Logique métier pure
└── router.py           # def get_router(config: dict) -> APIRouter
```

### Règles importantes

- **Toujours** hériter de `database.Base` pour les modèles SQLAlchemy
- **Toujours** déclarer les nouvelles tables dans `alembic/env.py`
- **Toujours** créer une migration Alembic pour tout changement de schéma
- Imports circulaires → imports tardifs dans les fonctions
- Services partagés (`RagService`, `LlmService`, `StorageService`) → classmethods
- Auth : `Depends(get_current_user)`, `Depends(require_role("admin", "moe"))`

### Pattern SQLAlchemy 2.0

```python
result = await db.execute(select(Model).where(Model.field == value))
items = result.scalars().all()
```

### Pattern pgvector (cosine)

```python
rows = await db.execute(
    text("SELECT ... 1 - (embedding <=> :vec::vector) AS score FROM chunks WHERE ..."),
    {"vec": str(embedding_list), ...}
)
```

---

## Lancer le projet

```bash
cp .env.example .env
docker compose up -d
docker compose exec api alembic upgrade head
# API : http://localhost:8000 | Docs : http://localhost:8000/docs (DEBUG=true)
```

---

## Variables d'environnement clés

```bash
DATABASE_URL=postgresql+asyncpg://arceus:password@db:5432/arceus
LLM_PROVIDER=ollama          # ou "openai"
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=mistral:7b
EMBEDDING_PROVIDER=ollama
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIM=768
REDIS_URL=redis://redis:6379/0
AGENTS_DIR=/agents
DOMAIN=btp                   # domaine actif (btp|droit|audit|conseil|medecine|it)
DOMAIN_LABEL="Architecture & Maîtrise d'Œuvre"
ADMIN_EMAIL=admin@agence.fr
ADMIN_PASSWORD=changeme
```

---

## Migrations Alembic — séquence

| Migration | Contenu |
|---|---|
| 0001 | users, affaires, permissions, documents, chunks |
| 0002 | agent_runs |
| 0003 | orchestra_runs |
| 0004 | agent_memory |
| 0005 | agent_runs.sources |
| 0006 | orchestra_runs HITL |
| 0007 | meeting (crs, actions, agendas) |
| 0008 | agent_memory.scope + orchestra_runs.criticite + project_decisions |
| 0009 | affaires contexte enrichi (typology, region, budget, phase, ABF, zones) |
| 0010 | index GIN full-text sur chunks.contenu (hybrid search RRF) |
| 0011 | webhook_sessions (canal externe → affaire) |
| 0012 | traçabilité orchestra (subtasks, veto) + agent error_message + memory category |
| 0013 | capture_sessions + chunks.tsv tsvector + trigger auto-update |
| 0014 | wiki_pages (synthesis cache, vector pgvector, HNSW cosine) |
| 0015 | decision_scores (scoring décisionnel 100 pts / 5 axes) |
| 0016 | enrichissement project_decisions + project_tasks + project_observations |
| 0017 | orchestra_runs scoring + mémoires (score_id, score_verdict, memories_written, wiki_page_id) |
| 0018 | orchestra_runs preprocessing + precheck (preprocessed_input JSONB, precheck_verdict, precheck_reasoning) |
| 0019 | guards : project_decisions (condition_levee, reversible) + orchestra_runs (veto_severity, veto_condition_levee) |
| 0026 | orchestra_runs intelligence : run_score JSONB, hera_verdict, hera_feedback, fallback_level |
| 0027 | affaires.domain VARCHAR + affaires.domain_metadata JSONB |

---

## Changelog & Releases

Le fichier `CHANGELOG.md` à la racine documente toutes les modifications notables.

**Règle obligatoire** : tout commit contenant un changement fonctionnel (feat, fix, refactor impactant) doit ajouter une entrée dans la section `[Unreleased]` du CHANGELOG. Lors d'une release (merge vers main d'un lot cohérent), la section `[Unreleased]` est renommée avec le nouveau numéro de version et la date.

Convention SemVer :
- **MAJOR** : rupture d'API ou changement de schéma DB non rétrocompatible
- **MINOR** : nouvelle fonctionnalité, nouveau module, nouveau pattern
- **PATCH** : correctif, optimisation, refactoring interne
