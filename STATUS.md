# Pantheon OS — Project Status

> Source de vérité unique sur l’état actuel du projet.
> Ce fichier consolide ce qui est livré, partiel, à faire et en exploration.
> Les fichiers Markdown de référence pilotent le développement : `README.md`, `ARCHITECTURE.md`, `MODULES.md`, `AGENTS.md`, `ROADMAP.md`, `STATUS.md`.

Dernière mise à jour : 2026-04-26

---

# 1. Légende

- ✅ Fait
- 🔄 Partiellement implémenté
- ⬜ À faire
- 💡 Exploration / veille
- ⚠️ À vérifier dans le code
- ❌ Contradictoire / à corriger

---

# 2. Convention de release

Le projet suit une logique SemVer.

## MAJOR (`X.0.0`)

À utiliser pour : rupture d’API, refonte architecturale, changement de schéma non rétrocompatible, changement majeur du runtime.

## MINOR (`0.X.0`)

À utiliser pour : nouveau module, nouveau workflow, nouveau pattern d’orchestration, nouvelle brique fonctionnelle importante.

## PATCH (`0.0.X`)

À utiliser pour : correctif, optimisation, refactoring interne sans impact API, correction sécurité ou stabilité.

Règles : un lot cohérent mergé sur `main` produit en général une release MINOR ; un correctif critique peut produire un PATCH ; une rupture produit une MAJOR.

---

# 3. Current Baseline

Pantheon OS dispose d’un socle MVP réel : FastAPI, PostgreSQL + pgvector, OpenWebUI, Ollama, Docker Compose, registry d’applications API et manifests API.

## ✅ Confirmé par audit ciblé

- `docker-compose.yml` contient les services `db`, `api`, `openwebui`, `ollama`.
- PostgreSQL utilise `pgvector/pgvector:pg16`.
- L’API FastAPI est définie dans `platform/api/main.py`.
- `ModuleRegistry` charge les applications API activées depuis `modules.yaml`.
- Les apps API disposent de manifests simples dans `platform/api/apps/*/manifest.yaml`.
- `modules.yaml` active le MVP : `auth`, `admin`, `affaires`, `documents`, `agent`, `openai_compat`, `hermes_console`.
- Les tests existants confirment une logique de guards, criticité, veto patterns et promotion mémoire projet/agence.

## 🔄 Partiellement confirmé

- Auto-discovery agents / skills / workflows : `ManifestLoader` indexe les manifests runtime présents dans `/modules` et utilise le contrat commun `ComponentManifest`.
- Workflow definitions : `WorkflowDefinitionLoader` charge `workflow.yaml` et `tasks.yaml` au startup, stocke les définitions dans `app.state.hermes_workflow_definitions`, mais il n’est pas encore branché à un moteur d’exécution.
- Exemple workflow : `modules/workflows/document_analysis/` existe avec `manifest.yaml`, `workflow.yaml`, `tasks.yaml` et test de validation.
- Debug runtime : `/debug/runtime-registry` expose les agents, skills, workflow manifests, workflow definitions et modules API chargés au startup.
- Approval Gate : module API `approvals` présent mais désactivé dans `modules.yaml`. Migration et tests ajoutés, non vérifiés en CI/local dans cette session.
- Installer UI : mini-app locale autonome ajoutée sous `scripts/install/ui/` pour installation NAS + Ollama LAN avec suivi `install_status.json`. Dépendances dédiées et script de lancement ajoutés. Non testée en local dans cette session.
- Mémoire agent : `AgentMemory` et `extract_and_store_memories()` sont utilisés par les tests, avec promotion `promotable` projet → agence. Cette mémoire n’est pas encore alignée avec la doctrine complète `raw_history / candidate_facts / active_facts / summaries / cards / traces`.
- Hermes Console : activée et manifest présent, mais contenu fonctionnel complet non audité.

## ⚠️ À vérifier dans le code

- Présence réelle des agents et skills sous `modules/`.
- État réel de `FlowManager`, `HecateResolver`, `IrisClarifier`, `MetisEditor`, `deep_search`, DLQ ARQ, OCR fallback GLM-4V et cockpit d’affaire.
- État réel des modules métier `planning`, `chantier`, `communications`, `finance`, décrits comme livrés historiquement mais désactivés dans `modules.yaml`.
- Chaîne Alembic réelle : la migration `20260426_0001_add_approval_requests.py` utilise `down_revision = None` faute de visibilité complète du dossier `alembic/versions`. À corriger si une tête Alembic existe déjà.

---

# 4. Delivered Recently

## ✅ Audit initial documentation / code

Livré : `CODE_AUDIT.md`.

Constats :

- le socle MVP est réel ;
- les modules avancés sont majoritairement désactivés ;
- la documentation décrit une cible plus avancée que le runtime actif ;
- la mémoire existe partiellement, mais pas sous la forme complète désormais documentée ;
- la priorité est de renforcer les fondations avant d’ajouter des capacités risquées.

## ✅ Correctif P0 — ManifestLoader runtime

Livré :

- `platform/api/core/registries/__init__.py`
- `platform/api/core/registries/loader.py`
- `tests/test_manifest_loader.py`

Rôle :

- éviter un crash startup lié à l’import `core.registries.loader.ManifestLoader` ;
- charger sans erreur les manifests `agents`, `skills`, `workflows` lorsqu’ils existent ;
- retourner des listes vides lorsque les dossiers sont absents ;
- ignorer les manifests désactivés ;
- rester rétrocompatible avant durcissement strict du schéma.

Statut : ✅ Fait, tests ajoutés. Tests non exécutés dans cette session.

## 🔄 Sprint 2 — Manifest hardening progressif

Livré :

- `platform/api/core/contracts/__init__.py`
- `platform/api/core/contracts/manifest.py`
- intégration du contrat dans `platform/api/core/registry.py`
- intégration du contrat dans `platform/api/core/registries/loader.py`
- `tests/test_manifest_contract.py`

Rôle :

- créer un contrat Pydantic commun `ComponentManifest` ;
- normaliser les anciens manifests API sans casser le MVP ;
- supporter `api_app`, `agent`, `skill`, `tool`, `workflow`, `action`, `provider`, `evaluator`, `service`, `template` ;
- ajouter les notions `enabled`, `priority`, `dependencies`, `inputs`, `outputs`, `risk_profile`, `side_effect_profile`, `approval_required_if` ;
- merger `depends_on` et `dependencies` pour compatibilité ;
- produire des quality issues non bloquantes avant passage à validation stricte.

Statut : 🔄 Partiel avancé. Tests ajoutés, non exécutés dans cette session.

Reste à faire :

- exécuter les tests ;
- corriger les éventuelles erreurs d’import / typing ;
- ajouter un mode strict activable par configuration ;
- enrichir progressivement les manifests existants avec `type`, `risk_profile`, `side_effect_profile`, `inputs`, `outputs` ;
- exposer les quality issues dans la console.

## 🔄 Sprint 3 — Task Contract / Workflow hardening

Livré :

- `platform/api/core/contracts/tasks.py`
- `platform/api/core/registries/workflows.py`
- `platform/api/main.py` branché au loader workflow ;
- `platform/api/core/health.py` avec endpoint debug runtime ;
- `modules/workflows/document_analysis/manifest.yaml`
- `modules/workflows/document_analysis/workflow.yaml`
- `modules/workflows/document_analysis/tasks.yaml`
- `tests/test_task_contracts.py`
- `tests/test_workflow_definition_loader.py`
- `tests/test_document_analysis_workflow.py`

Rôle :

- créer `TaskDefinition` ;
- créer `WorkflowDefinition` ;
- imposer `expected_output` ;
- imposer une affectation cohérente selon `execution_mode` : agent, skill, action, tool, workflow, manual ;
- valider les dépendances entre tâches ;
- détecter les IDs de tâches dupliqués ;
- identifier les tâches critiques C4/C5 et les besoins d’approbation par défaut ;
- charger `workflow.yaml` ;
- charger et fusionner `tasks.yaml` ;
- refuser les définitions invalides sans bloquer les autres workflows ;
- indexer les définitions au startup dans `app.state.hermes_workflow_definitions` ;
- fournir un premier workflow réel `document_analysis` ;
- exposer l’état runtime via `/debug/runtime-registry`.

Statut : 🔄 Partiel avancé. Contrats, loader, branchement startup, endpoint debug, exemple réel et tests ajoutés, non exécutés dans cette session.

Reste à faire :

- produire des traces `task_run` ;
- exposer les tâches dans Hermes Console ;
- connecter les définitions au moteur d’exécution lorsqu’il sera audité ou stabilisé.

## 🔄 Approval Gate / HITL minimal

Livré :

- `platform/api/apps/approvals/manifest.yaml`
- `platform/api/apps/approvals/__init__.py`
- `platform/api/apps/approvals/models.py`
- `platform/api/apps/approvals/schemas.py`
- `platform/api/apps/approvals/service.py`
- `platform/api/apps/approvals/router.py`
- `alembic/versions/20260426_0001_add_approval_requests.py`
- `tests/test_approval_contracts.py`
- `modules.yaml` référence `approvals` en `enabled: false`

Rôle :

- créer le modèle `ApprovalRequest` ;
- gérer les statuts `pending / approved / rejected / expired / escalated / cancelled` ;
- fournir les endpoints CRUD et décisions ;
- protéger contre la double décision via update conditionnel `pending / escalated` ;
- préparer l’intégration future avec PolicyGate et pause/resume workflow.

Statut : 🔄 Partiel. Module présent mais désactivé. Migration et tests ajoutés, non exécutés. `down_revision` Alembic à vérifier.

Reste à faire :

- vérifier et corriger `down_revision` ;
- exécuter les tests ;
- ajouter tests de service avec DB async ;
- activer le module après validation migration ;
- brancher PolicyGate ;
- brancher pause/resume workflow ;
- exposer pending approvals dans Hermes Console.

## 🔄 Installer UI — NAS + Ollama LAN

Livré sur branche `feature/approval-gate-activation` :

- `scripts/install/ui/installer_state.py`
- `scripts/install/ui/installer_runner.py`
- `scripts/install/ui/installer_api.py`
- `scripts/install/ui/templates/index.html`
- `scripts/install/ui/static/style.css`
- `scripts/install/ui/README.md`
- `scripts/install/ui/requirements.txt`
- `scripts/install/ui/launch_installer.sh`
- `scripts/install/windows/setup_ollama_windows.ps1`

Rôle :

- lancer une UI autonome sur `http://NAS_IP:8090` ;
- configurer IP Ollama, modèle chat, modèle embeddings, URL API Pantheon ;
- vérifier Docker ;
- vérifier Docker Compose ;
- vérifier Ollama et modèles ;
- préparer `.env` ;
- lancer `docker compose up -d --build` ;
- lancer `alembic upgrade head` ;
- lancer les tests ciblés ;
- vérifier `/health` ;
- vérifier `/debug/runtime-registry` ;
- écrire le suivi dans `install_status.json` ;
- lancer via environnement dédié `.venv-installer`.

Statut : 🔄 Partiel avancé. UI, runner, requirements et script de lancement ajoutés, non testés localement. À garder strictement en LAN administrateur.

Reste à faire :

- tester le lancement `bash scripts/install/ui/launch_installer.sh` ;
- tester l’exécution complète sur NAS ;
- ajouter éventuellement un Dockerfile dédié installer si besoin.

## ✅ Refactoring modulaire majeur

Livré selon l’historique projet, mais à revérifier dans le code complet :

- passage de `runtime/hermes/` vers `core/` + `modules/` ;
- `modules/agents/{layer}/{myth}_{role}/` ;
- `modules/skills/` ;
- `modules/tools/` ;
- `modules/workflows/` ;
- `platform/api/apps/` à la place de `platform/api/modules/` ;
- configuration simplifiée ;
- auto-discovery via `ManifestLoader`.

---

# 5. Active Backlog

## 5.1 Core and Runtime

### 🔄 Manifest hardening

Partiel avancé.

Le contrat `ComponentManifest` existe et est branché dans les deux mécanismes de chargement : API apps et runtime manifests agents/skills/workflows.

Reste à faire :

- exécuter `pytest tests/test_manifest_loader.py tests/test_manifest_contract.py` ;
- ajouter un mode strict configurable ;
- enrichir les manifests API existants ;
- enrichir les manifests runtime lorsqu’ils seront audités ;
- exposer les erreurs et warnings dans Hermes Console.

Priorité : P1.

### 🔄 Task Contract / Workflow hardening

Partiel avancé.

Les contrats `TaskDefinition` et `WorkflowDefinition` existent. Le loader `WorkflowDefinitionLoader` lit `workflow.yaml` et `tasks.yaml`. Le startup charge ces définitions dans `app.state.hermes_workflow_definitions`. Le workflow `document_analysis` fournit le premier exemple réel. L’endpoint `/debug/runtime-registry` permet de vérifier ce qui est chargé.

Reste à faire :

- exécuter `pytest tests/test_task_contracts.py tests/test_workflow_definition_loader.py tests/test_document_analysis_workflow.py` ;
- ajouter `task_run` dans l’observability ;
- exposer les tâches dans Hermes Console ;
- connecter les définitions au moteur d’exécution.

Priorité : P1.

### 🔄 Approval Gate / HITL

Partiel.

Le module `approvals` existe mais reste désactivé dans `modules.yaml`.

Reste à faire :

- vérifier et corriger `down_revision` Alembic ;
- exécuter `pytest tests/test_approval_contracts.py` ;
- ajouter tests de service avec DB async ;
- activer le module après validation migration ;
- brancher PolicyGate ;
- brancher pause/resume workflow ;
- exposer pending approvals dans Hermes Console.

Priorité : P1.

### ⬜ Module `decisions`

Documenté mais désactivé.

`modules.yaml` indique `decisions.enabled=false`.

Reste à faire : module API complet, endpoints CRUD, filtres par dette, résolution manuelle, alertes D3, dashboard dédié.

Priorité : P1 après Task Contract et Approval Gate minimal.

### 🔄 Chaîne de veto séquencée

Partiel.

Les tests confirment des patterns de veto et une criticité C1-C5. Reste à confirmer l’orchestration complète `veto_check → veto_themis → veto_zeus → zeus_judge`.

Reste à faire : formalisation complète `veto_zeus`, modèle `verdict / justification / severity / lift_condition`, traçabilité UI.

Priorité : P2.

### 🔄 Mémoire — refactoring de service

Partiel.

Confirmé par tests :

- `extract_and_store_memories()` existe ;
- `AgentMemory` existe ;
- promotion `promotable` projet → agence testée.

Reste à faire :

- clarifier les scopes mémoire ;
- distinguer raw history, candidate facts, active facts, summaries, cards et traces ;
- éviter toute promotion massive non sourcée ;
- ajouter ou vérifier le statut `candidate / active / superseded / retracted` ;
- ajouter context preview ;
- ajouter dry-run de consolidation ;
- protéger raw messages, documents, traces et tool outputs contre réécriture de consolidation ;
- vérifier que les cards compactes ne deviennent pas des dumps append-only ;
- documenter les owners HESTIA / MNEMOSYNE / HADES / ARGOS / THEMIS / ZEUS dans le code.

Priorité : P1.

### ⬜ Auditable context injection

À faire.

Objectif : pouvoir afficher le contexte réellement injecté ou prévu pour un agent : facts, candidate exclusions, cards, summaries, chunks, documents, décisions, traces pertinentes.

Priorité : P1.

### ⬜ Memory consolidation dry-run

À faire.

Toute promotion, rétractation, supersession, fusion ou condensation doit pouvoir être prévisualisée avant application.

Priorité : P2.

### ⬜ Affaires — exposition complète des nouveaux champs

Reste à faire : schemas, router, enums métier.

Priorité : P2.

### 🔄 Tests automatisés

Partiel.

Confirmé :

- `tests/test_guards.py` ;
- `tests/test_manifest_loader.py` ;
- `tests/test_manifest_contract.py` ;
- `tests/test_task_contracts.py` ;
- `tests/test_workflow_definition_loader.py` ;
- `tests/test_document_analysis_workflow.py` ;
- `tests/test_approval_contracts.py`.

Reste à faire : tests tools, `orchestra/service.py`, E2E RAG, mémoire complète, approvals DB/service, workflows C1-C5, context preview, consolidation dry-run.

Priorité : P1.

### 🔄 Monitoring agents / runs

Partiel / à vérifier.

Reste à faire : dashboards performance, durée par agent, taux d’échec, fréquence d’activation, métriques d’usage, changements mémoire, contexte injecté, approvals, browser action traces.

Priorité : P2.

---

## 5.2 Interfaces and Channels

### 🔄 Installer UI autonome

Partiel avancé.

Disponible sous `scripts/install/ui/`. Elle permet d’installer et diagnostiquer Pantheon OS avant que le runtime principal soit opérationnel. Elle dispose maintenant d’un `requirements.txt` dédié et d’un script `launch_installer.sh`.

Reste à faire : test local/NAS, éventuel Dockerfile dédié.

Priorité : P1 pour self-hosting.

### ⬜ Module `webhooks` — Telegram / WhatsApp

Désactivé dans `modules.yaml`.

Cible : réception Telegram / WhatsApp, routing par mention, fallback HERMES, mémoire de fil par HESTIA, support photo, réponse canal, auth expéditeur.

Priorité : P3.

### ⬜ OpenWebUI Pipelines

Objectif : déclencher directement ZEUS / orchestra depuis OpenWebUI et réduire friction UI → runtime.

Priorité : P3.

### 💡 Browser Tool gouverné

Intéressant mais non prioritaire.

Statut : à intégrer seulement après PolicyEngine, Approval Gate et Observability.

À retenir : primitives browser simples, screenshots comme preuve d’état, action trace avant/après, domain browser skills, HTTP direct quand possible.

À rejeter : agent libre sur le Chrome personnel par défaut, auto-modification de helpers, actions sans Approval Gate.

Priorité : P4.

### 💡 Voix

À explorer plus tard : transcription, TTS, OpenWebUI, webhooks.

Priorité : P4.

---

## 5.3 Document and Retrieval Layer

### ⬜ Retrieval multimodal

Objectif : plans, coupes, photos, images, chunk image + description, pipeline ARGOS, qualification technique, fusion retrieval.

Priorité : P3.

### 🔄 OCR / extraction avancée

Partiel / à vérifier.

Reste à faire : industrialisation, scoring qualité OCR, monitoring extraction.

Priorité : P3.

---

## 5.4 Optimization and Learning

### 🔄 DSPy — plan phasé

Conceptuellement prêt, non industrialisé.

Phase 1 : instrumentation.

Phase 2 : optimisation tâches structurées : criticité, actions, métadonnées documentaires.

Phase 3 : éventuellement HERMES ou ZEUS si volume suffisant.

Règles : ne pas optimiser les `SOUL.md`, ne pas optimiser les agents identitaires trop tôt.

Priorité : P4.

### 🔄 HESTIA / MNEMOSYNE learning loop

Partiel.

Déjà confirmé par tests : promotion `promotable` projet → agence.

Reste à faire : gouvernance plus explicite, revue avant promotion forte, dashboard de capitalisation.

Priorité : P2.

---

# 6. Architecture Overlay Backlog

## 💡 VITRUVE

Exploration.

But : agent de démarrage projet, programme, sol, topo, PLU, ABF, risques, budget, contraintes.

Sortie cible : fiche synthèse contraintes avant conception.

Priorité : P3.

---

# 7. Explorations and Watchlist

## 💡 Hermes Local Memory

À intégrer dans la doctrine mémoire : séparation raw history / candidate facts / active facts / summaries / cards / traces, contexte injecté inspectable, dry-run, cards non souveraines, consolidation explicite.

À rejeter : remplacement PostgreSQL/pgvector par SQLite, suppression FastAPI, worker mémoire opaque, copie mécanique.

## 💡 LangGraph Approval Hub

À intégrer dans l’Approval Gate : queue pending approvals, statut d’approbation, décision humaine avec note, audit log, expiration, escalation.

À rejeter : dépendance Vercel/Supabase, dashboard séparé comme source de vérité, SDK externe comme cœur du système.

## 💡 Browser Harness

À intégrer plus tard : screenshots before/after, action trace, Browser Tool gouverné, domain browser skills, HTTP direct fallback.

À rejeter : agent libre sur Chrome personnel, auto-modification de helpers, actions sans Approval Gate.

## 💡 ElizaOS

À intégrer : contrat actions / providers / evaluators / services, dépendances et priorités de modules, event handlers plus tard.

À rejeter : remplacement du runtime Pantheon, characters/personas, stack TypeScript/Bun/Express.

## 💡 CrewAI

À intégrer : Task Contract, expected_output, Crew Pattern comme workflow multi-agent, Flow Pattern comme orchestration contrôlée.

À rejeter : CrewAI runtime, rôle/goal/backstory comme modèle central.

## 💡 Agents / Skills Standards

À intégrer : `AGENTS.md` opérationnel pour agents coding, `SKILL.md`, skill contract, skill security scan.

À rejeter : import massif de catalogues d’agents.

## 💡 Neo4j

À envisager seulement si PostgreSQL + SQL récursif ne suffisent plus pour la complexité relationnelle.

## 💡 Micro-services

Pas un objectif. À considérer uniquement si charge ou équipe le justifie.

## 💡 Branch software / code

Pertinente comme branche de domaine future : review, blast radius, minimal code context, repo onboarding.

---

# 8. Repo Governance

Branches recommandées :

- `main` → stable ;
- `develop` → intégration ;
- `experiment/*` → exploration ;
- `overlay/*` → overlays métier.

Règles :

- toute migration de schéma doit être versionnée ;
- toute brique critique doit avoir un test de non-régression ;
- toute exploration V3 reste isolée ;
- les Markdown de référence font foi ;
- si le code est plus pertinent que les Markdown, proposer d’abord la mise à jour documentaire ;
- si le code contredit les Markdown sans justification, corriger le code après audit.

---

# 9. Immediate Priorities

Ordre recommandé :

1. Tester l’installer UI : `bash scripts/install/ui/launch_installer.sh` puis `http://NAS_IP:8090`.
2. Exécuter les tests ajoutés : `pytest tests/test_manifest_loader.py tests/test_manifest_contract.py tests/test_task_contracts.py tests/test_workflow_definition_loader.py tests/test_document_analysis_workflow.py tests/test_approval_contracts.py` puis suite existante pertinente.
3. Vérifier la chaîne Alembic et corriger `down_revision` de la migration approvals si nécessaire.
4. Corriger les éventuels échecs liés aux contrats.
5. Finaliser l’audit code/docs avec inspection complète locale ou CI.
6. Enrichir progressivement les manifests API et runtime.
7. Activer `approvals` après validation migration + tests.
8. Brancher PolicyGate / Approval Gate.
9. Compléter la mémoire : raw/candidate/active/summaries/cards/traces.
10. Ajouter context preview.
11. Ajouter dry-run de consolidation.
12. Compléter tests mémoire, approvals DB/service et workflows C1-C5.
13. Renforcer monitoring consolidé : approvals, contexte injecté, traces d’action.
14. Reporter Browser Tool après PolicyEngine, Approval Gate et Observability.
15. Instrumenter DSPy plus tard.

---

# 10. Final Rule

Ce fichier reste la vue consolidée de vérité projet.

Il doit dire clairement :

- ce qui est livré ;
- ce qui est partiel ;
- ce qui reste à faire ;
- ce qui est en exploration ;
- ce qui doit être vérifié dans le code.

Pantheon OS doit rester modulaire, gouverné, portable, testable, observable, exploitable et piloté par ses Markdown de référence.
