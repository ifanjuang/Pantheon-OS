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

## [Unreleased]

### Refactored
- **Orchestra — décomposition `service.py` en 5 sous-modules** : le monolithe 1 800 lignes est découpé en modules responsabilité unique. `_shared.py` (260 l) — `OrchestraState`, `CRITICITE_ROUTING`, `VALID_AGENTS`, helpers LLM (`_llm_call`, `_parse_json_response`, `_zeus_system`), helper statique `_get_agent_summary` (LRU), exécuteur isolé `_run_agent_isolated`. `_planner.py` (324 l) — M1 : `preprocess`, `workflow_precheck`, `zeus_distribute` (prompt `_ZEUS_UNIFIED_PROMPT`). `_executor.py` (291 l) — M2 exécution : patterns `_exec_parallel`, `_exec_cascade`, `_exec_arena`, tri topologique `_topological_levels`, nœuds `dispatch_subtasks` et `execute_complements`. `_evaluator.py` (219 l) — M2 évaluation : `zeus_judge` (loop guard intégré), `veto_check` (layer 0 regex + LLM Instructor), `score_decision` (C4/C5 ScoringService). `_synthesizer.py` (167 l) — M4 : `synthesize`, `write_memories` (Hestia/Mnémosyne/wiki/fonctionnelle). `service.py` réduit à 637 l (coordinateur pur) : importe tous les nœuds, enregistre le graphe LangGraph, expose les 4 entry points (`run_orchestra`, `run_orchestra_from_run_id`, `run_orchestra_hitl`, `resume_orchestra`, `stream_orchestra`). La factory `_make_nodes(affaire_id, user_id)` et ses closures sont supprimées — chaque nœud lit `UUID(state["affaire_id"])` / `UUID(state["user_id"])` directement depuis l'état LangGraph.

### Added
- **RAG — RRF SQL natif** : `search_hybrid` remplace les 2 requêtes parallèles (`asyncio.gather` semantic + FTS) + fusion Python (`_rrf_fusion`) par une seule requête CTE PostgreSQL. Structure : `sem_raw` (distance cosine pgvector, 1 calcul/row) → `semantic` (ROW_NUMBER) · `fts_raw` (ts_rank_cd, 1 calcul/row) → `fts` (ROW_NUMBER) · `rrf` (FULL OUTER JOIN + `COALESCE(1/(k+rank), 0)`) → SELECT final trié limité. Fallback sémantique si la CTE échoue. Suppression de `_rrf_score` et `_rrf_fusion` (code mort). `import re` monté au niveau module.

### Added
- **Orchestra — suppression du nœud `plan_agents`** : le nœud intermédiaire qui demandait à chaque agent sélectionné son plan d'action via un appel LLM individuel est supprimé. Remplacé par `_get_agent_summary(agent_name)` — extraction statique et LRU-cachée du titre + premier paragraphe de rôle de chaque `SOUL.md`, 0 appel LLM. `zeus_distribute` reçoit directement ces `agent_summaries` et planifie les sous-tâches en une seule étape Zeus. Gain estimé : -3 à -5 appels LLM par orchestration C3+, -25 % de latence sur le chemin C4/C5. Nouveau prompt `_ZEUS_UNIFIED_PROMPT` (remplace `_ZEUS_PLAN_PROMPT`). Le champ `agent_plans` dans `OrchestraState` / DB est conservé (legacy, toujours `{}`). L'événement SSE `plans_ready` est maintenu mais émis depuis `zeus_distribute` avec les résumés statiques.

### Added
- **Guards — veto hybride couche 0 + couche 1** : nouveau fichier `veto_patterns.py` implémentant `fast_veto_check(agent, output)` — détection déterministe par regex de ~20 patterns critiques (Thémis : hors mission, litige, mise en demeure, avenant requis ; Héphaïstos : non-conforme DTU, infaisable, danger structurel ; Apollon : contradiction normative ; génériques : opposition formelle, veto explicite, expert externe requis). `structured_veto` appelle d'abord `fast_veto_check` (couche 0, 0 token LLM) puis bascule sur LLM Instructor uniquement si aucun pattern n'a conclu. Gain estimé : ~80 % des vetos bloquants évidents sans appel LLM, latence divisée par 3 sur ces cas.
- **Guards — `MAX_COMPLEMENTS_BY_CRITICITE`** : constante dict exportée depuis `guards/service.py` — `{C1: 0, C2: 0, C3: 1, C4: 2, C5: 3}`. Le nœud `zeus_judge` dans le graphe Zeus utilise désormais ce seuil en fonction de la criticité de la demande (plus `max_complements=1` hardcodé global). C1/C2 ne déclenchent plus jamais de boucle d'enrichissement.

### Changed
- **Orchestra `zeus_judge`** : `GuardsService.loop_guard()` reçoit maintenant `max_complements=MAX_COMPLEMENTS_BY_CRITICITE.get(criticite, 1)` au lieu de la valeur fixe `1`.
- **Guards `structured_veto`** : désormais pipeline à deux couches explicites (couche 0 déterministe → couche 1 LLM).

### Added
- **Module evaluation — OpenClaw (M4)** : harness d'éval reproductible. Datasets YAML (`datasets/openclaw-*.yaml`) décrivant cas + attendus (`expected_criticite`, `expected_intent`, `expected_precheck`, `expected_agents`, `forbidden_agents`, `expected_veto`, `must_contain`, `must_not_contain`, `max_duration_ms`). `EvaluationService.run_eval(dataset_id)` invoque le graphe Zeus sur chaque cas. Scoring d'éval distinct du scoring décisionnel : 3 axes pondérés (completeness 40%, relevance 35%, security 25%) + passage conditionné à `total ≥ 0.6 AND security ≥ 0.5`. Routes `GET /evaluation/datasets`, `GET /evaluation/datasets/{id}`, `POST /evaluation/run/{id}`. CLI `python -m modules.evaluation.cli run openclaw-devis [--max-cases N] [--dry-run] [--json]`. 5 datasets par défaut : devis, chantier, photo, litige, courrier (15 cas au total)
- **Module memory (M3)** : mémoire fonctionnelle Redis TTL (session). Comble le chaînon entre Mnémosyne (agence, permanente) et Hestia (projet, durée affaire). `FunctionalMemoryService.set_context` / `get_context` / `delete_context` / `promote_to_project`. Fallback silencieux si Redis down. Routes `GET|POST|DELETE /memory/context/{thread_id}` + `POST /memory/promote`
- **Module monitoring (M3)** : observabilité ARCEUS — KPIs agrégés depuis `orchestra_runs`, `agent_runs`, `decision_scores`. 4 familles : OrchestraKPIs (durée p50/p95/mean, distribution criticité, taux enrichissement, HITL), AgentKPIs (taux erreur, itérations, top 10 agents), ScoringKPIs (verdicts, scores, axes), GuardsKPIs (veto bloquant/reserve, verdicts précheck, shortcircuit rate). Fenêtres 24h/7d/30d/90d. Routes `GET /monitoring/kpis[/{orchestra|agents|scoring|guards}]`
- **Intégration mémoire fonctionnelle dans le graphe Zeus** : `preprocess` lit le contexte session Redis (affaire_id, phase, domaine) et persiste `last_preprocessed` ; `write_memories` persiste `last_verdict` + `last_answer_excerpt` pour continuité conversationnelle sur N runs
- **OrchestraState** : nouveau champ `thread_id` pour la mémoire fonctionnelle (par défaut = run_id)
- **Module guards (M2)** : gardes-fous explicites — `criticality_guard` (règle pure C1-C5 dérivée de impact_cout/impact_delai/severity/intent), `reversibility_guard` (LLM, distingue actions réversibles/irréversibles, force HITL si nécessaire), `loop_guard` (anti-boucle d'enrichissement), `structured_veto` (LLM Instructor, remplace la détection keyword fragile, retourne `severity: bloquant|reserve|information` + `condition_levee`). Routes de preview `/guards/veto/preview`, `/guards/reversibility/preview`, `/guards/criticality/preview`
- **Refactor `veto_check`** : utilise `GuardsService.structured_veto` au lieu de `_VETO_KEYWORDS`. Évalue Thémis > Héphaïstos > Apollon par ordre de priorité, ne déclenche HITL que sur veto bloquant + criticité C4/C5 (C3 trace le veto sans interrompre)
- **Loop guard dans `zeus_judge`** : remplace `if state.get("complement_done")` inline par `GuardsService.loop_guard(state, max_complements=1)` — extensible à un compteur futur
- **Événement SSE** `veto_detected` : émet agent, severity, motif, condition_levee dès qu'un veto est détecté
- **Migration 0019** : colonnes `condition_levee` + `reversible` sur `project_decisions`, colonnes `veto_severity` + `veto_condition_levee` sur `orchestra_runs`
- **Module preprocessing (Hermès++)** : normalisation d'entrée (cleaned_question, reformulated_question, intent, phase/domaine, missing_information, confidence, suggested_criticite) + gate Precheck (approved|trim|upgrade|clarification|blocked). Routes de preview `/preprocessing/preview` et `/preprocessing/precheck`
- **Nœud `preprocess`** en tête du graphe Zeus : reformulation LLM via LlmService.extract() avant plan_agents, avec fallback silencieux si LLM down
- **Nœud `workflow_precheck`** entre `zeus_distribute` et `dispatch_subtasks` : évalue le dimensionnement du plan Zeus (trim sur-dimensionné, upgrade criticité sous-estimée), court-circuite vers END sur clarification/blocked avec message utilisateur
- **Événements SSE** `preprocess_ready` + `precheck_verdict` pour suivi temps réel du gate
- **Migration 0018** : colonnes `preprocessed_input` (JSONB), `precheck_verdict` (String 32), `precheck_reasoning` (Text) sur `orchestra_runs`
- **Module wiki (synthesis-cache)** : pages markdown navigables depuis les décisions validées, recherche hybride cosine+LIKE, précédents agence (+5 scoring). Routes CRUD `/wiki/pages/`, promotion `/wiki/pages/from-decision/{id}`, recherche `/wiki/search`, check précédents `/wiki/precedents`
- **Module scoring** : scoring décisionnel 100 pts / 5 axes (technique, contractuel, planning, cohérence, logique) avec bonus/malus automatiques. Modes manuel et auto (LLM via Instructor). Routes `/scoring/manual`, `/scoring/auto`, `/scoring/stats`
- **Module decisions (dashboard)** : CRUD décisions/tâches/observations, 5 vues dashboard (critiques, dettes, non-validées, par lot, timeline), KPIs agrégés. Routes `/decisions/kpis`, `/decisions/views/{view}`
- **Nœud `score_decision`** dans le graphe Zeus : scoring automatique pour C4/C5 via ScoringService.score_auto() après le jugement Zeus
- **Nœud `write_memories`** dans le graphe Zeus : mémoire Hestia (projet) + Mnémosyne (agence) après synthèse, promotion wiki automatique pour C4/C5
- **Migration 0014** : table `wiki_pages` avec vector pgvector + HNSW cosine
- **Migration 0015** : table `decision_scores` avec index composite (decision_id, computed_at DESC)
- **Migration 0016** : enrichissement `project_decisions` + tables `project_tasks` / `project_observations`
- **Migration 0017** : colonnes scoring + mémoires sur `orchestra_runs`

### Changed
- **Graphe Zeus** : flow étendu `preprocess → plan_agents → zeus_distribute → workflow_precheck → dispatch_subtasks → veto_check → zeus_judge → [execute_complements] → score_decision → synthesize → write_memories → END`
- **OrchestraState** : nouveaux champs `preprocessed_input`, `precheck_verdict`, `precheck_reasoning`, `veto_severity`, `veto_condition_levee`, `thread_id`
- **CRITICITE_ROUTING** : `veto_check` activé sur C3 et C4 (avant : uniquement C5). Le HITL reste réservé aux vetos bloquants C4/C5.
- **modules.yaml** : activation de `memory` (précédemment placeholder désactivé), ajout de `monitoring` et `evaluation`.

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
