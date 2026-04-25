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
- Mémoire agent : `AgentMemory` et `extract_and_store_memories()` sont utilisés par les tests, avec promotion `promotable` projet → agence. Cette mémoire n’est pas encore alignée avec la doctrine complète `raw_history / candidate_facts / active_facts / summaries / cards / traces`.
- Hermes Console : activée et manifest présent, mais contenu fonctionnel complet non audité.

## ⚠️ À vérifier dans le code

- Présence réelle des agents, skills et workflows sous `modules/`.
- État réel de `FlowManager`, `HecateResolver`, `IrisClarifier`, `MetisEditor`, `deep_search`, DLQ ARQ, OCR fallback GLM-4V et cockpit d’affaire.
- État réel des modules métier `planning`, `chantier`, `communications`, `finance`, décrits comme livrés historiquement mais désactivés dans `modules.yaml`.

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

### ⬜ Task Contract / Workflow hardening

À faire.

Objectif : formaliser les tâches comme unités assignables et vérifiables.

À intégrer :

- `TaskDefinition` ;
- `WorkflowDefinition` ;
- `tasks.yaml` ;
- `expected_output` obligatoire ;
- `assigned_agent` ou `assigned_role` ;
- `dependencies` ;
- `tools_allowed` ;
- `approval_required_if` ;
- `success_criteria` ;
- traces `task_run`.

Priorité : P1.

### ⬜ Module `decisions`

Documenté mais désactivé.

`modules.yaml` indique `decisions.enabled=false`.

Reste à faire : module API complet, endpoints CRUD, filtres par dette, résolution manuelle, alertes D3, dashboard dédié.

Priorité : P1 après Manifest hardening.

### 🔄 Chaîne de veto séquencée

Partiel.

Les tests confirment des patterns de veto et une criticité C1-C5. Reste à confirmer l’orchestration complète `veto_check → veto_themis → veto_zeus → zeus_judge`.

Reste à faire : formalisation complète `veto_zeus`, modèle `verdict / justification / severity / lift_condition`, traçabilité UI.

Priorité : P2.

### ⬜ Approval Gate / HITL

Documenté mais non confirmé dans le code.

Source d’inspiration analysée : `suryamr2002/langgraph-approval-hub`.

À intégrer :

- modèle `ApprovalRequest` ;
- statuts `pending / approved / rejected / expired / escalated / cancelled` ;
- assignee personne / équipe ;
- `decision_note` ;
- audit log ;
- expiration ;
- escalation ;
- pause/resume workflow ;
- protection contre double décision concurrente ;
- console pending approvals.

À rejeter :

- dépendance directe à Vercel / Supabase ;
- dashboard externe séparé comme source de vérité ;
- SDK externe comme couche principale.

Priorité : P1.

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
- `tests/test_manifest_contract.py`.

Reste à faire : tests tools, `orchestra/service.py`, E2E RAG, mémoire complète, approvals, workflows C1-C5, context preview, consolidation dry-run.

Priorité : P1.

### 🔄 Monitoring agents / runs

Partiel / à vérifier.

Reste à faire : dashboards performance, durée par agent, taux d’échec, fréquence d’activation, métriques d’usage, changements mémoire, contexte injecté, approvals, browser action traces.

Priorité : P2.

---

## 5.2 Interfaces and Channels

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

À rejeter : agent libre sur le Chrome personnel par défaut, auto-modification des helpers pendant un run, clics coordonnées sans trace, actions sur compte connecté sans Approval Gate.

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

1. Exécuter les tests ajoutés : `pytest tests/test_manifest_loader.py tests/test_manifest_contract.py` puis suite existante pertinente.
2. Corriger les éventuels échecs liés au contrat manifest.
3. Finaliser l’audit code/docs avec inspection complète locale ou CI.
4. Enrichir progressivement les manifests API et runtime.
5. Formaliser Task Contract + `tasks.yaml`.
6. Ajouter ou vérifier Approval Gate / HITL.
7. Compléter la mémoire : raw/candidate/active/summaries/cards/traces.
8. Ajouter context preview.
9. Ajouter dry-run de consolidation.
10. Compléter tests mémoire, approvals et workflows C1-C5.
11. Renforcer monitoring consolidé : approvals, contexte injecté, traces d’action.
12. Reporter Browser Tool après PolicyEngine, Approval Gate et Observability.
13. Instrumenter DSPy plus tard.

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
