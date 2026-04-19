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

### Added
- **FlowManager — gestion dynamique des workflows** : nouveau module `flowmanager` (`GET/POST /flows`, `PATCH/DELETE /flows/{name}`, `POST /flows/{name}/trigger`). Table `workflow_definitions` (migration 0028) stocke nom, version, définition JSON normalisée (`steps` avec flag `parallel`) et source YAML brute. `FlowManagerService.seed_from_disk()` charge automatiquement `config/workflows/*.yaml` absents de la DB. 3 workflows d'exemple fournis : `recherche_documentaire`, `decision_strategique`, `reponse_rapide`.
- **Agents Hécate, Métis, IrisClarifier** : 3 nouveaux agents spécialisés. `HecateResolver` (`uncertainty_resolver`) analyse le contexte avant le pipeline et produit un rapport d'incertitude `{uncertainty_score, blocking, missing_fields, clarification_questions}` — bloquant si score ≥ 0.6. `IrisClarifier` (`clarifier`, partage l'identité IRIS) transforme ce rapport en questions lisibles pour l'utilisateur. `MetisEditor` (`editor`) révise le style et la fluidité du texte synthétisé (post-Kairos, pré-Iris) sans modifier le contenu. Classes, SOUL.md, entrées `agent_registry.yaml` et exports `agents/__init__.py` créés pour les 3.
- **Pantheon OS — registre agent_registry.yaml** : `config/agent_registry.yaml` — source unique de vérité pour les 22 agents. Chaque entrée fige `role` (fonctionnel stable), `layer`, `class` (convention `MythRole`), `soul_dir` (`core` ou `agents`), `triggers`, `veto`, `old_names`. Helpers `get_agent_role()`, `get_agent_meta()` dans `_shared.py` (LRU cached). Convention JSON standard : `{"agent": "ZEUS", "role": "orchestrator"}`.
- **Pantheon OS — restructuration core/ vs agents/** : arborescence séparée entre meta-agents (`core/`) et agents spécialisés (`agents/`). SOUL.md des 6 meta-agents (zeus, hera, artemis, kairos, hermes, athena) déplacés dans `core/{name}/`. 22 classes Python `MythRole` créées : `ZeusOrchestrator`, `HeraSupervisor`, `ArtemisFilter`, `KairosSynthesizer`, `HermesRouter`, `AthenaPlanner` dans `core/` ; `HephaistosValidator`, `ThemisValidator`, `ApollonResearcher` et 13 autres dans `agents/`. `AgentBase` dans `core/_base.py` expose `agent`, `role`, `layer`, `veto`, `triggers`, `soul()`, `identity()`. Résolution SOUL.md via `_resolve_soul_path()` : `core/` prioritaire, `agents/` en fallback.
- **Pantheon OS — convention SSE `agent.event`** : tous les événements SSE renommés pour suivre le pattern `{agent_lowercase}.{event}`. Mapping complet : `plans_ready` → `zeus.plans_ready`, `zeus_decision` → `zeus.decision`, `preprocess_ready` → `hermes.preprocess_ready`, `precheck_verdict` → `hermes.precheck_verdict`, `veto_detected` → `themis.veto_detected` (+`role` dans payload), `hera_verdict` → `hera.verdict`, `run_score` → `hera.run_score`, `score_computed` → `hera.score_computed`, `final_answer` → `kairos.final_answer`, `memories_written` → `hestia.memories_written`, `subtask_done` → `agent.subtask_done`, `agents_done` → `agent.all_done`. Router docstring mis à jour avec la table complète des événements.
- **Pantheon OS — généralisation multi-domaine** : le système n'est plus limité au secteur BTP/MOE. Nouveau champ `domain` (VARCHAR, default `btp`) + `domain_metadata` (JSONB) sur `affaires` (migration 0027). 6 fichiers `agents/domains/{domain}.yaml` créés (btp, droit, audit, conseil, medecine, it) avec `context_injection`, `trusted_sources`, `criticality_keywords` et `veto_patterns` domaine-spécifiques. `_get_domain_context()` (LRU) charge et injecte le contexte dans `_get_soul()` (orchestra) et `_build_system_prompt()` (agent). `fast_veto_check()` fusionne désormais les patterns statiques avec les patterns YAML du domaine actif. Réglage via `DOMAIN=it` dans `.env`.
- **Pantheon OS — 6 nouveaux agents** (SOUL.md) : Héra (supervision cohérence), Artémis (filtrage/recentrage), Hadès (risques & scénarios négatifs), Déméter (optimisation ressources), Poséidon (flux & effets cascade), Kairos (synthèse finale actable). Ajoutés à `VALID_AGENTS` dans `orchestra/_shared.py` et `agent/service.py`.
- **Pantheon OS — améliorations architecturales** : score global multi-critères `run_score` pour tous les runs ; supervision Héra post-synthèse (`hera_verdict` + `hera_feedback`) ; fallback intelligent 3 niveaux (`fallback_level`) ; activation conditionnelle des agents via `AGENT_TRIGGERS` ; limites cognitives par criticité via `COGNITIVE_LIMITS` ; mémoire des erreurs Mnémosyne (`category="erreur"`). Migration 0026 pour les colonnes DB associées.

### Refactored
- **SOUL.md — neutralisation multi-domaine** : 11 fichiers SOUL.md rendus domain-neutral. Thémis et Dédale (critiques) : suppression des références BTP spécifiques (loi MOP, DTU, PC/DCE/DOE, phases ESQ→AOR, Cerfa). Chronos et Héphaïstos (haut) : timelines et normes BTP → références sectorielles génériques. Apollon, Hadès (moyen) : sources BTP → domaine actif, risques généralisés. Arès, Déméter, Poséidon, Hestia, Aphrodite (faible) : terminologie neutralisée. Les SOUL.md définissent l'identité et la méthode ; le domaine actif injecte le contexte sectoriel.

### Added
- **ClawMark runner** : `benchmarks/clawmark_runner.py` — adaptateur ARCEUS pour le benchmark ClawMark (agents coworker multimodaux). Charge des tâches JSON (`task_id`, `type`, `agent`, `instruction`, `expected`), les exécute via `run_agent()` sur une affaire dédiée `CLW-BENCH`, score chaque résultat (contains/not_contains/min_length/min_score), produit un rapport terminal ou JSON (compatible CI). CLI : `list`, `run --dataset`, `run --task cm-001`, `--dry-run`, `--json`. Dataset exemple dans `benchmarks/datasets/clawmark/sample.json` (4 tâches : search RE2020, compliance CCAG, faisabilité bardage, planning PC). Timeout configurable par tâche.
- **OpenSeeker — outil `deep_search`** : nouveau tool `deep_search` dans `modules/agent/tools.py` (pattern OpenSeeker : search → fetch → retour brut). Lance une requête `web_search`, extrait les top N URLs (budget `max_pages` 1-5, défaut 3), lit chaque page en parallèle via `_fetch_url` (3 000 chars/page), timeout global 30s via `asyncio.wait_for`. Retourne les contenus consolidés + toutes les sources. Disponible pour tous les agents (Apollon, Athéna, Thémis). Préférable à `web_search` seul pour les sujets nécessitant plusieurs sources normatives.
- **Dead-Letter Queue ARQ** : décorateur `_dlq_wrap(func)` dans `worker.py` — enveloppe chaque job ARQ pour capturer les exceptions et les pousser dans `arq:dlq` (Redis list, max 1 000 entrées, JSON `{job_id, function, error, failed_at}`). Appliqué à tous les jobs métier (orchestra, agent, memory, telegram, capture, chantier, courrier). Jobs cron (daily_alerts, weekly_summary, memory_consolidation) exclus. Endpoint `GET /control/jobs/failed?limit=N` lit la DLQ directement depuis Redis.
- **Validation secrets au démarrage** : `_check_secrets()` dans `main.py` — appelée en step 0 du lifespan. Refuse le démarrage si `DEBUG=False` et que `JWT_SECRET_KEY`, `ADMIN_PASSWORD` ou `DATABASE_URL` contiennent les valeurs par défaut "changeme". Fail-fast explicite avec message d'erreur listant les variables à corriger. Sans effet en mode `DEBUG=True`.
- **CI/CD GitHub Actions** : `.github/workflows/ci.yml` — pipeline complet sur `push` vers `main`/`claude/**` et `pull_request`. Services : `pgvector/pgvector:pg16` + `redis:7-alpine` avec health checks. Étapes : checkout, Python 3.11 + cache pip, install deps + ruff + pip-audit, lint `ruff check api/ tests/`, audit `pip-audit` (continue-on-error), tests `pytest ../tests/ --cov`. `pyproject.toml` ajouté avec config ruff (`E/F/W`, ignore `E501`/`F401`) et pytest (`asyncio_mode=auto`).
- **Control plane UI** : nouveau module `control` (backend FastAPI) + application `ui/` (Next.js 14 + Tailwind, dark theme). Backend : `GET /control/modules` lit `modules.yaml` + manifests pour l'état de tous les modules ; `GET /control/runs` liste les orchestra runs filtrables par status/criticité ; `GET /control/runs/{id}/trace` reconstruit la timeline d'un run (orchestra.started → hermes.classified → zeus.routing → agents → veto → completion) ; `GET /control/errors` agrège les runs échoués et vetos bloquants ; `WS /control/stream` pousse les mises à jour toutes les 2s (init state + delta runs + refresh erreurs toutes 10s + heartbeat). Frontend 4 panneaux : `ModuleList` (état loaded/disabled, version hover), `RunList` (criticité colorée C1-C5, status icons, sélection), `TraceViewer` (timeline colorée par agent avec payload on hover), `ErrorStream` (severity error/warn, clic → jump trace). Reconnexion WebSocket avec backoff exponentiel. Registre dans `modules.yaml`.
- **OCR fallback GLM-4V** : `core/services/ocr_service.py` — nouveau service OCR utilisant un endpoint OpenAI-compatible (GLM-4V Zhipu ou self-hosted). Déclenché par `RagService.ingest()` quand le texte natif extrait est inférieur à `GLM_OCR_MIN_CHARS` (défaut 100 chars) — typiquement les PDFs scannés et les images. Rendu PDF multi-pages via PyMuPDF (`fitz`) si disponible, sinon tentative envoi PDF direct. Résultat OCR injecté dans les chunks à la place du texte natif, avec méta-données persistées dans `chunks.meta` : `ocr_provider`, `ocr_confidence`, `layout_blocks_count`, `extraction_mode="ocr"`. Nouveaux paramètres `settings.py` : `GLM_OCR_ENDPOINT`, `GLM_OCR_API_KEY`, `GLM_OCR_MODEL` (défaut `glm-4v`), `GLM_OCR_MIN_CHARS` (défaut 100). Fallback silencieux : si l'OCR échoue, le texte natif (même court) est conservé. `.env.example` mis à jour avec les variables commentées.
- **Tests guards + mémoire** : nouveau `tests/test_guards.py` — 20 cas : `criticality_guard` (coût C3/C4/C5, délai C3/C4/C5, sévérité, irréversibilité, règle max), `loop_guard` (première itération, complement_done, complement_count), `MAX_COMPLEMENTS_BY_CRITICITE`, `fast_veto_check` couche 0 (patterns hors mission Thémis, infaisable Héphaïstos, pas de veto). `tests/conftest.py` : imports des nouveaux modèles planning, chantier, communications, finance, decisions pour `Base.metadata.create_all` complet.
- **Mémoire — promotion automatique agence (promotable)** : `extract_and_store_memories()` reçoit un paramètre `scope: str = "projet"`. Le prompt d'extraction demande désormais `"promotable": true/false` sur chaque leçon. Si `promotable=true` ET `affaire_id` présent, une copie `scope='agence'` est créée automatiquement sous le nom `mnemosyne` (agence-level). Les leçons projet-spécifiques restent inchangées. Backward compatible : l'ancien format `list[str]` reçoit `promotable=False` implicitement. Deux nouveaux tests couvrent la promotion et la non-promotion.
- **Hestia SOUL.md — protocole capitalisation projet → agence** : nouvelle section `## Protocole de capitalisation (projet → agence)` avec critères explicites de promotion (règle générale vs spécifique au projet), exemples de leçons promotables/non-promotables, instruction de marquage `"promotable": true`, et signal de capitalisation manuelle `🔁 CAPITALISATION AGENCE` pour les patterns découverts en consultation.
- **Veto séquencé C4/C5 — chaîne Thémis → Héphaïstos explicite** : `veto_check` amélioré pour C4/C5. Pour C3, comportement inchangé : post-analyse des sorties Thémis/Héphaïstos/Apollon si présentes dans `agent_results`. Pour C4/C5 : appels LLM directs et parallèles vers Thémis + Héphaïstos via `_call_veto_explicit` (pas `run_agent` — 0 DB, 0 mémoire, ~1 token/appel) INDÉPENDAMMENT du fait qu'ils aient été sélectionnés par Zeus. Garantit que ces deux gardiens examinent TOUJOURS les décisions engageantes et risquées. Apollon reste post-analysé si présent. Sévérité la plus haute : bloquant > reserve. Prompt `_SEQUENTIAL_VETO_PROMPT` dédié avec soul complète de l'agent comme contexte système. Fast patterns (couche 0 regex) appliqués sur la sortie LLM avant parse JSON. `_get_soul(agent_name)` ajouté à `_shared.py` (LRU cache process lifetime). `orchestra_run_id` ajouté à `OrchestraState` et passé depuis tous les entry points.
- **Hestia post-orchestration — auto-capitalisation des décisions** : `write_memories` (section 3) extrait automatiquement les décisions C3+ de la réponse finale via `_llm_call` + `_parse_json_response` et crée des `ProjectDecision` en DB liées à l'orchestra run (via `run_id`). Prompt `_DECISION_EXTRACT_PROMPT` ciblé : objet, criticité, dette D0-D3, impacts, lot, responsable, réversibilité. Max 5 décisions par orchestration, C3 minimum, fallback silencieux. `agents_impliques` auto-rempli depuis `agent_results.keys()`. Déclenché uniquement pour C3/C4/C5 avec réponse finale ≥ 80 chars.
- **RAG courriers — indexation générique sans document (0025)** : migration 0025 rend `chunks.document_id` nullable et ajoute `source_type VARCHAR(32)` + `source_id UUID` + index composite `(affaire_id, source_type, source_id)`. Nouvelle méthode `RagService.ingest_text_direct(text, affaire_id, source_type, source_id)` : découpe le texte brut via `SentenceSplitter`, embed en batch, INSERT en bulk dans `chunks` sans fichier ni document MinIO. Idempotent : supprime les chunks existants du même `(source_type, source_id)` avant réindexation. Nouvelle méthode `RagService.delete_source(source_type, source_id)` symétrique à `delete_document`. Nouveau job ARQ `ingest_courrier_job` déclenché automatiquement à la création ou à la mise à jour (`objet`/`resume`) d'un courrier — concatène objet + émetteur/destinataire + date + résumé pour construire le corpus. `ingest_courrier(db, courrier_id)` dans `communications/service.py`. Les agents (notamment Apollon, Iris, Hestia) peuvent désormais retrouver le contenu des courriers via `rag_search` exactement comme les documents PDFs. Modèle `Chunk` mis à jour (nullable `document_id`, nouveaux champs `source_type`/`source_id`).
- **Cockpit d'affaire + automatisations métier** : endpoint `GET /affaires/{id}/cockpit` — appels parallèles (`asyncio.gather`) aux services planning, chantier, communications, finance + requête décisions D2/D3 ouvertes. Retourne les 5 dashboards consolidés + liste d'alertes triées par criticité (critical > warning > info) avec module, message et count. Alertes détectées : jalons manqués, arrêt chantier, mises en demeure, décisions D2/D3 ouvertes, dérive budgétaire, NC en retard, courriers hors délai. Deux nouveaux cron ARQ : `daily_alerts_job` (06:00 UTC/jour) parcourt toutes les affaires actives, logge en WARNING les alertes critiques pour remontée observabilité ; `weekly_summary_job` (lundi 07:00 UTC) appelle `run_agent("hestia")` sur chaque affaire active pour capitaliser les points clés actionnables de la semaine (décisions, planning, chantier, comms, finance) dans la mémoire projet.
- **Module finance (0024)** : suivi financier des marchés de travaux. Table `finance_avenants` — modifications contractuelles (plus-value/moins-value), impact délai, statut (en_preparation→soumis→accepte/refuse/annule), lien décision. Table `finance_situations` — situations de travaux par lot/entreprise, montant demandé vs validé, avancement déclaré vs validé MOE, cycle soumise→en_revision→validee→payee. Dashboard `GET /finance/{affaire_id}/dashboard` : agrège budget_moa (affaire), honoraires, montant_marches_initial (somme planning_lots.montant_marche), avenants_acceptes/en_attente, montant_contractuel = initial + acceptés, montant_reclame/valide/paye, taux_engagement (contractuel/budget_moa), taux_realisation (valide/contractuel), derive_ht (dépassement ou économie). Pas de duplication : s'appuie sur affaires.budget_moa et planning_lots.montant_marche déjà en base.
- **Module communications (0023)** : registre probatoire des courriers entrants/sortants. Table `communications_courriers` — sens (entrant/sortant), type_doc (courrier/email/lr/mise_en_demeure/bc/devis/pv/cr/autre), référence, émetteur/destinataire, objet/résumé, storage_key MinIO, dates (émission/réception/délai_réponse/réponse_effective), statut (recu→en_attente_reponse→traite/sans_suite/archive). Liens métier : lot, décision, observation chantier, `reponse_id` (auto-référence courrier sortant→entrant). Pipeline Iris : `POST /communications/courriers/{id}/draft-response` enfile `draft_courrier_job` → `run_agent("iris")` avec contexte type/objet/résumé/délai, instruction spéciale pour les mises en demeure (ton neutre/factuel, pas d'admission de faute). Log warning automatique à la création d'une mise en demeure. Dashboard KPIs : en_attente_reponse, en_retard (délai dépassé), mises_en_demeure, sans_suite.
- **Module chantier (0022)** : observations terrain et non-conformités. Table `chantier_observations` — source (photo/voix/note/mail), localisation textuelle, entreprise, constat Argos, statut (a_analyser→en_cours→analyse). Table `chantier_nonconformites` — gravité (mineure/majeure/critique/arret_chantier), date échéance, statut (ouverte→en_cours→resolue→contestee), diagnostic Héphaïstos, flag `arret_chantier`, lien vers lot/décision/observation. Pipeline Argos : `POST /chantier/observations/{id}/analyze` enfile `analyze_chantier_obs_job` (ARQ) → `run_agent("argos")` → stocke `analyse_argos`. Pipeline Héphaïstos : `POST /chantier/nonconformites/{id}/qualify` enfile `qualify_nc_job` → `run_agent("hephaistos")` → stocke `analyse_hephaistos`, détecte automatiquement les mots-clés d'arrêt de chantier (≥ 20 patterns via `_ARRET_KEYWORDS`), positionne `arret_chantier=True` et escalade la gravité si nécessaire. Dashboard `GET /chantier/{affaire_id}/dashboard` : KPIs observations/NC, flag `alerte_arret_chantier` (NC arret_chantier ouverte), NC en retard. Deux nouveaux jobs ARQ enregistrés dans `worker.py`.
- **Module planning (0021)** : moteur de planification basé sur un graphe de dépendances. Tables `planning_lots` (lot de travaux, entreprise, montant marché), `planning_taches` (dates prévues/réelles, avancement, statut, flag `critique`), `planning_jalons` (administratif/contractuel/technique/livraison, date cible/réelle), `planning_liens` (FS/SS/FF/SF + lag en jours). Service `compute_critical_path()` : tri topologique de Kahn + forward pass (EST/EFT) + backward pass (LFT/LST) → marge totale (float), flag `critique` persisté en base, détection de cycle. Service `propagate_delays(tache_id, delta_jours)` : BFS sur les liens FS sortants, décalage de toutes les dates prévues des successeurs transitifs. Service `get_health()` : score 0-100 (pénalités retard/blocage/jalons manqués), KPIs tâches/jalons/lots. Routes : CRUD lots/tâches/jalons/liens, GET gantt (lots+tâches+jalons+liens en un appel), POST critical-path (calcul + persist), GET health. Chronos peut désormais s'appuyer sur le graphe réel pour raisonner sur les décalages en cascade.
- **ERP — Classification `erp_type` + `erp_categorie` sur les affaires** : migration 0020 ajoute deux colonnes nullable sur `affaires`. `erp_type VARCHAR(10)` — type ERP selon le classement réglementaire français (J, L, M, N, O, P, R, S, T, U, V, W, X, Y, PA, CTS, SG, OA, GA, EF, REF), NULL si l'affaire n'est pas un ERP. `erp_categorie VARCHAR(2)` — catégorie selon l'effectif du public accueilli : 1 (>1500), 2 (701-1500), 3 (301-700), 4 (≤300), 5 (seuil réduit), NULL si non-ERP. Constantes `ERP_TYPES` et `ERP_CATEGORIES` dans `schemas.py`. Validators `@field_validator` dans `AffaireCreate` et `AffaireUpdate` : normalisation uppercase de `erp_type`, rejet de valeurs hors ensemble. `AffaireResponse` expose les deux champs. La nature ERP (type + catégorie) est ainsi disponible dans le contexte projet injecté dans les prompts des agents.

- **C4 — Circuit breaker partagé via Redis** : nouvelle classe `RedisCircuitBreaker` (étend `CircuitBreaker`) dans `core/circuit_breaker.py`. L'état in-process reste la source de vérité pour `check()` (0 latence réseau). `record_failure()` et `record_success()` mettent à jour in-process immédiatement puis fire-and-forget une tâche asyncio `_write_to_redis()` (HSET + EXPIRE, TTL = recovery_timeout × 4). La propriété `state` planifie un refresh en arrière-plan toutes les 5 s via `_refresh_from_redis()` : ne met à jour in-process que si Redis signale un état PLUS dégradé (failures supérieures ou state=open quand local=closed). Fallback silencieux si Redis down — se comporte comme l'ancien `CircuitBreaker`. Les singletons `llm_breaker` et `embed_breaker` sont remplacés par des instances `RedisCircuitBreaker`. Réutilise le client Redis de `FunctionalMemoryService` (singleton partagé, pas de connexion supplémentaire). Gain : les N workers ARQ + l'API FastAPI partagent le même état de circuit — si Ollama est down et détecté par un worker, les autres fail-fast immédiatement sans attendre leur propre timeout de 90s.
- **C5 — Unification mémoire session + persistante** : nouvelle fonction `get_unified_memory(db, agent_name, affaire_id, thread_id)` dans `agent/memory.py` qui agrège les 3 couches mémoire en un seul appel. Couche projet : leçons `agent_memory scope='projet'` pour cet agent sur cette affaire (existant). Couche agence : patterns `agent_memory scope='agence'` (Mnémosyne, toutes affaires — nouveau `_get_agence_memories()`). Couche session : contexte Redis TTL du thread (keys `last_verdict`, `last_answer_excerpt`, `phase_projet`, `domaine` — nouveau `_get_session_context()`). `run_agent()` reçoit un paramètre `thread_id: str = ""` et utilise `get_unified_memory` à la place de `get_agent_memories`. 3 sections distinctes dans le system prompt : `## Mémoire projet`, `## Patterns agence`, `## Contexte session`. `thread_id` propagé de bout en bout : `state["thread_id"]` → `_run_agent_isolated()` → `run_agent()`. Chaîne complète : `dispatch_subtasks`, `execute_complements`, `synthesize` lisent `state.get("thread_id", "")` et le passent aux patterns d'exécution (`_exec_parallel`, `_exec_cascade`, `_exec_arena`).
- **O5 — Outils ReAct en parallèle** : la boucle ReAct exécutait les tool calls séquentiellement même quand le LLM en demandait plusieurs dans un même tour. Remplacé par `asyncio.gather` sur l'ensemble du batch. Les tools DB (`rag_search`, `list_documents`, `get_affaire_info`) utilisent une session `AsyncSessionLocal` isolée quand le batch contient plusieurs calls, pour éviter les accès concurrents sur la même `AsyncSession`. Les tools réseau (`web_search`, `fetch_url`) sont purement parallèles. Un seul tool call : comportement identique à avant (0 overhead). Log `agent.tools_parallel_done` avec count et batch_ms quand > 1 tools s'exécutent en parallèle. Constante `_DB_TOOLS` exportée depuis `tools.py`. Gain estimé : -400 à -1500 ms sur chaque itération ReAct à multi-tools (typique Apollon, Héphaïstos).
- **O4 — Cache sémantique des prétraitements** : nouveau module `preprocessing/cache.py` — `SemanticPreprocessCache`. Avant chaque appel LLM Instructor dans `PreprocessingService.preprocess()`, on embed le message (nomic-embed-text via `RagService.embed`, ~5-15 ms) et on cherche dans Redis (`preprocess:sem:{affaire_id}`, LIST FIFO, max 20 entrées, TTL 3600 s) un `PreprocessedInput` stocké avec similarité cosine ≥ 0.92. Sur hit : retour immédiat sans appel LLM. Sur miss : LLM Instructor + store en pipeline Redis (LPUSH + LTRIM + EXPIRE). Fallback silencieux si Redis down ou embed raté. L'embed n'est calculé que si `affaire_hint` est fourni (tous les runs orchestra). Gain estimé : 0 appel LLM Instructor (~500-1500 ms économisés) sur toute question répétée ou reformulation proche dans la même session affaire.

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
