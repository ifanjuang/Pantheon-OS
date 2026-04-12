# Changelog

Toutes les modifications notables du projet ARCEUS sont documentées dans ce fichier.

Le format suit [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) et le projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

---

## Convention de release

| Type de changement | Bump de version | Exemples |
|---|---|---|
| **MAJOR** (`X.0.0`) | Rupture d'API, refonte architecturale, changement de schéma DB non rétrocompatible | Refonte du panthéon, changement de stack LLM, nouvelle version d'API |
| **MINOR** (`0.X.0`) | Nouvelle fonctionnalité, nouveau module, nouveau pattern d'orchestration | Module capture, exploration pattern, contextual retrieval |
| **PATCH** (`0.0.X`) | Correctif, optimisation, refactoring interne sans impact API | Circuit breaker, fix FTS, retry MinIO |

**Quand publier une release :**
- Chaque merge vers `main` d'un lot cohérent de fonctionnalités constitue une release MINOR
- Les correctifs critiques (sécurité, crash) peuvent faire l'objet d'un PATCH immédiat
- Une refonte majeure (ex : nouveau framework d'orchestration, migration breaking) incrémente la MAJOR

---

## [0.5.0] - 2026-04-10

### Added
- **Contextual Retrieval** : enrichissement LLM de chaque chunk au moment de l'ingestion (pattern Anthropic, ~49% d'amélioration de la recherche). Configurable via `CONTEXTUAL_RETRIEVAL=true`
- **Cross-encoder reranking** : reranking post-RRF via `cross-encoder/ms-marco-MiniLM-L-6-v2` (sentence-transformers). Opt-in via `RERANK_ENABLED=true`
- **Module capture (NoobScribe)** : upload audio depuis le chantier, transcription Whisper, traitement par pipeline agent. Routes POST `/capture/upload`, GET `/capture/sessions/{affaire_id}`, GET `/capture/sessions/detail/{id}`
- **Memory consolidation** : job ARQ cron (quotidien 03:00 UTC) qui fusionne les leçons brutes en patterns de haut niveau via LLM, avec chainage `superseded_by`
- **Pattern exploration** dans l'orchestre : pipeline créatif Dionysos (options latérales) -> Promethee (critique) -> Apollon (verification)
- **Migration 0013** : table `capture_sessions`, colonne `chunks.tsv` (TSVECTOR) avec index GIN et trigger auto-update
- `capture_job` et `memory_consolidation_job` dans le worker ARQ

### Changed
- **FTS optimise** : `_search_fts()` utilise la colonne pre-calculee `tsv` avec index GIN au lieu du `LATERAL to_tsvector()` couteux a chaque requete
- **Dionysos SOUL.md** enrichi : mode exploration, relations inter-agents, pre-validation des options creatives
- Module capture enregistre dans `modules.yaml`, `alembic/env.py`, `tests/conftest.py`

---

## [0.4.0] - 2026-04-10

### Added
- **Circuit breaker LLM** : pattern disjoncteur in-process pour Ollama (5 echecs -> open -> 30s recovery -> half_open). Instances `llm_breaker` et `embed_breaker`
- **Health checks** enrichis : verification Redis (ARQ), events pool (LISTEN/NOTIFY), etat du circuit breaker LLM
- **Timeouts agent** : `asyncio.wait_for(timeout=90s)` sur tous les appels LLM de la boucle ReAct
- **Retry MinIO** : decorateur tenacity sur `upload()` et `download()` (3 tentatives, backoff exponentiel)
- **RBAC documents** : verification des permissions affaire lors de la suppression de documents
- **Checkpointer HITL** : appel `setup_checkpointer()` au demarrage pour creer les tables LangGraph
- Hierarchie agents Primary (P) / Secondary (S) dans `AGENTS.md` avec triggers d'invocation
- 8 nouvelles relations inter-agents documentees
- Resolution de conflits intra-famille formalisee
- Protocoles d'ecriture Hestia/Mnemosyne

### Changed
- **RAG hybrid search** : `asyncio.gather` avec `return_exceptions=True` pour resilience FTS
- **FTS sanitization** : nettoyage regex des caracteres speciaux avant `plainto_tsquery`
- **DB pool** : `pool_size=15`, `max_overflow=25`, `pool_recycle=1800`

### Fixed
- `setup_checkpointer()` jamais appele — tables LangGraph HITL jamais creees (C4/C5 casses silencieusement)
- Doublon `meeting` dans `modules.yaml` (enabled=true puis enabled=false)
- FTS crash sur caracteres speciaux (@, !, etc.) dans les requetes

---

## [0.3.0] - 2026-04-08

### Added
- **Migration 0012** : champs tracabilite sur `orchestra_runs` et `agent_runs`
- **Memoire temporelle** : `valid_until`, `superseded_by`, `category` sur `agent_memory`
- **Scope memoire** : `agence` (global) vs `projet` (par affaire) dans `agent_memory`
- Extraction categorisee des lecons (technique, planning, budget, contractuel, general)
- `memory_job` ARQ pour extraction asynchrone des lecons

### Changed
- Refactoring production : fiabilite, tracabilite, memoire temporelle
- Events PostgreSQL : correction fuite de connexions dans `events.py`
- Worker : signature `criticite` compatible avec les jobs deja en queue

---

## [0.2.0] - 2026-04-07

### Added
- **Module orchestra** : orchestration multi-agents LangGraph avec Zeus
- **Patterns d'execution** : solo, parallel, cascade, arena dans `dispatch_subtasks`
- **RAG hybride** : recherche semantique (pgvector cosine) + FTS PostgreSQL + fusion RRF (k=60)
- **SSE streaming** pour les orchestrations longues
- **Background queue ARQ** : execution asynchrone des orchestrations et runs agent
- **HITL (Human-In-The-Loop)** : validation humaine obligatoire pour C4/C5 via LangGraph checkpointer
- **Module meeting** : analyse de comptes-rendus, extraction d'actions, generation d'ordres du jour
- **Apollon** : agent recherche & verification (web_search + fetch_url)
- **Bot Telegram** : session par chat, routing intelligent, mentions @agent, analyse photo via Argos
- **Suite de tests** : auth, affaires, documents, webhooks

### Changed
- **Pantheon complet** : 15 agents + Zeus, architecture rhizomatique
  - Hephaistos, Dionysos, Dedale, Iris, Aphrodite integres avec SOUL.md
  - Refonte de la hierarchie et des flux inter-agents
- Optimisations multi-fichiers : performance et robustesse

---

## [0.1.0] - 2026-04-01

### Added
- **Infrastructure & kernel** : FastAPI async, PostgreSQL + pgvector, SQLAlchemy 2.0, Alembic
- **Module auth** : JWT, RBAC (admin/moe/collaborateur/lecteur), seed admin
- **Module documents** : upload PDF/DOCX/TXT, ingestion RAG, stockage MinIO S3
- **Module affaires** : dossiers MOE avec contexte projet (typologie, region, budget, phase, ABF, zones)
- **Module agent** : boucle ReAct (Reason + Act) avec function calling, memoire dynamique
- **Module openai_compat** : endpoint compatible OpenAI pour Open WebUI
- **RagService** : chunking adaptatif (SentenceWindow pour CCTP/DTU), embedding batch, pgvector HNSW
- **LlmService** : chat + extraction structuree, support Ollama et OpenAI
- **StorageService** : abstraction MinIO S3
- **5 premiers agents** : Athena, Themis, Hermes, Promethee, Apollon (SOUL.md)
- **Docker Compose** : DB + API + MinIO + Redis + Ollama + Open WebUI
- **Migration 0001** : users, affaires, permissions, documents, chunks
- **CLAUDE.md** : contexte projet pour agents Claude Code
- **4 Claude Code skills** pour le developpement

---

## [0.0.1] - 2026-03-21

### Added
- Initial commit
- DEVPLAN.md : plan de developpement complet
- Architecture modulaire plugin
- Documentation : README, ARCHITECTURE, INSTALL
- Roadmap 5 phases : Fondation / Memoire / Pilote / Agents / Plateforme
