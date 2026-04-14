# ARCEUS — Contexte projet pour agents Claude Code

## Vue d'ensemble

ARCEUS est un système d'intelligence opérationnelle pour agences MOE (Maîtrise d'Œuvre). Il centralise la gestion documentaire, le RAG sémantique, l'orchestration multi-agents, le suivi de chantier, la planification et les finances sur l'ensemble du cycle de vie des projets de construction.

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
│       ├── affaires/               # Dossiers MOE + contexte projet enrichi
│       ├── documents/              # Upload, ingest RAG, trigger Thémis
│       ├── agent/                  # Boucle ReAct, mémoire, outils RAG+web
│       ├── orchestra/              # LangGraph Zeus, C1-C5, HITL, SSE streaming
│       └── meeting/                # Analyse CR, extraction actions, OJ
├── agents/                         # SOUL.md de chaque agent du panthéon
│   ├── zeus/ hermes/ argos/
│   ├── athena/ hephaistos/ promethee/ apollon/ dionysos/
│   ├── themis/ chronos/ ares/
│   ├── hestia/ mnemosyne/
│   └── iris/ aphrodite/ dedale/
├── alembic/versions/               # Migrations séquentielles 0001→0009
├── modules.yaml                    # Registre modules actifs
└── docker-compose.yml              # DB + API + MinIO + Redis + Ollama + OpenWebUI
```

---

## Le Panthéon — 15 agents + Zeus

| Famille | Agent | Rôle |
|---|---|---|
| **Perception** | Hermès | Interface, routage, qualification C1-C5 |
| | Argos | Observation visuelle, constat objectif (photos, plans) |
| **Analyse** | Athéna | Structuration des problèmes, scénarios |
| | Héphaïstos | Faisabilité technique, DTU, matériaux, fiches produits — **veto technique** |
| | Prométhée | Contre-analyse, détection biais, critique logique |
| | Apollon | Recherche web + RAG, vérification normative, cohérence finale |
| | Dionysos | Pensée latérale, rupture créative |
| **Cadrage** | Thémis | Réglementation + contrat MOE + déontologie — **veto contractuel** |
| | Chronos | Temps, planning, délais légaux, impacts cascade |
| | Arès | Action terrain rapide, décisions réversibles C3 |
| **Continuité** | Hestia | Mémoire projet (décisions, hypothèses, dettes D0-D3) |
| | Mnémosyne | Mémoire agence (patterns, leçons, précédents) |
| **Communication** | Iris | Emails humains, correspondance, relances |
| | Aphrodite | Marketing, réseaux sociaux, storytelling |
| **Production** | Dédale | Dossiers complets (PC, DCE, DOE, marchés) |
| **Orchestrateur** | Zeus | Arbitrage stratégique, distribution, jugement, veto global |

---

## Modèles de données

| Table | Description |
|---|---|
| `users` | Comptes utilisateurs, rôle RBAC |
| `affaires` | Dossiers MOE + contexte (typology, region, budget, phase, ABF, zones) |
| `affaire_permissions` | Override de rôle par affaire |
| `documents` | Fichiers uploadés (PDF/DOCX/TXT/images) |
| `chunks` | Fragments RAG, vecteur `vector(768)`, index HNSW |
| `agent_runs` | Traces d'exécution agent (steps, sources RAG, durée) |
| `agent_memory` | Leçons apprises — `scope` : `agence` ou `projet` |
| `orchestra_runs` | Orchestrations Zeus : plans, assignments, résultats, HITL, criticité |
| `project_decisions` | Décisions structurées C1-C5 avec dette D0-D3 |
| `meeting_crs` | Comptes-rendus analysés |
| `meeting_actions` | Actions extraites avec priorité, statut, échéance |
| `meeting_agendas` | Ordres du jour générés |

---

## Criticité C1-C5

| Niveau | Nature | Mode |
|---|---|---|
| C1 | Information | Agent unique, pas de Zeus |
| C2 | Question | 1-2 agents |
| C3 | Décision locale réversible | Zeus optionnel, Arès peut agir |
| C4 | Décision engageante | Zeus + HITL humain |
| C5 | Risque majeur | Zeus + HITL + veto check |

---

## Les 3 mémoires

| Mémoire | Scope DB | Agent | Durée |
|---|---|---|---|
| **Agence** | `scope='agence'`, `affaire_id=NULL` | Mnémosyne | Permanente |
| **Projet** | `scope='projet'`, `affaire_id=<uuid>` | Hestia | Durée affaire |
| **Fonctionnelle** | LangGraph state / Redis | Hermès + Chronos | Session |

---

## Conventions de code

### Créer un nouveau module

```
api/modules/{nom}/
├── __init__.py
├── manifest.yaml       # name, version, description, prefix, depends_on
├── models.py           # Modèles SQLAlchemy (héritent de database.Base)
├── schemas.py          # Schémas Pydantic request/response
├── service.py          # Logique métier pure
└── router.py           # def get_router(config: dict) -> APIRouter
```

Le `registry.py` charge automatiquement `router.get_router(config)` et monte le router sur le `prefix` du manifest.

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

---

## Changelog & Releases

Le fichier `CHANGELOG.md` à la racine documente toutes les modifications notables.

**Règle obligatoire** : tout commit contenant un changement fonctionnel (feat, fix, refactor impactant) doit ajouter une entrée dans la section `[Unreleased]` du CHANGELOG. Lors d'une release (merge vers main d'un lot cohérent), la section `[Unreleased]` est renommée avec le nouveau numéro de version et la date.

Convention SemVer :
- **MAJOR** : rupture d'API ou changement de schéma DB non rétrocompatible
- **MINOR** : nouvelle fonctionnalité, nouveau module, nouveau pattern
- **PATCH** : correctif, optimisation, refactoring interne
