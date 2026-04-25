# Pantheon OS — Project Status

> Source de vérité unique sur l’état actuel du projet.
> Ce fichier consolide ce qui est livré, partiel, à faire et en exploration.
> Les fichiers Markdown de référence pilotent le développement : `README.md`, `ARCHITECTURE.md`, `MODULES.md`, `AGENTS.md`, `ROADMAP.md`, `STATUS.md`.

Dernière mise à jour : 2026-04-25

---

# 1. Légende

- ✅ Fait
- 🔄 Partiellement implémenté
- ⬜ À faire
- 💡 Exploration / veille
- ⚠️ À vérifier dans le code

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

Pantheon OS est structuré autour d’un noyau modulaire.

## ✅ Baseline actuelle documentée

- `core/` est le framework générique.
- `modules/` porte les composants auto-découverts.
- `platform/` regroupe API, UI, data, storage, infra.
- `domains/` porte les overlays métier.
- Les manifests sont la source de vérité locale des modules.
- L’auto-discovery remplace les registres centralisés codés en dur.

## ✅ Direction d’architecture validée

- séparation control plane / data plane ;
- modularité filesystem-first ;
- agents, skills, tools, workflows séparés ;
- runtime générique ;
- overlays métier hors core ;
- gouvernance explicite ;
- criticité C1-C5 ;
- mémoire multi-couches ;
- RAG hybride ;
- orchestration multi-patterns ;
- observabilité runtime ;
- Approval Gate pour actions sensibles ;
- Browser Tool gouverné seulement après policy, approval et observability.

---

# 4. Delivered Recently

## ✅ Refactoring modulaire majeur

Livré selon l’historique projet :

- passage de `runtime/hermes/` vers `core/` + `modules/` ;
- `modules/agents/{layer}/{myth}_{role}/` ;
- `modules/skills/` ;
- `modules/tools/` ;
- `modules/workflows/` ;
- `platform/api/apps/` à la place de `platform/api/modules/` ;
- configuration simplifiée ;
- auto-discovery via `ManifestLoader`.

## ✅ Orchestration et gouvernance

Livré selon l’historique projet :

- agents normalisés ;
- convention SSE `{agent}.{event}` ;
- activation conditionnelle ;
- limites cognitives par criticité ;
- supervision HERA ;
- score global de run ;
- patterns `solo`, `parallel`, `cascade`, `arena` ;
- exécution topologique par niveaux ;
- sous-tâches explicites ;
- veto C4/C5 explicite.

## ✅ Retrieval hybride

Livré selon l’historique projet :

- FTS PostgreSQL ;
- pgvector ;
- fusion RRF ;
- index GIN ;
- `search_hybrid()` par défaut.

## ✅ Runtime avancé et modules métier

Livré selon l’historique projet :

- `FlowManager` ;
- `HecateResolver` ;
- `IrisClarifier` ;
- `MetisEditor` ;
- `deep_search` ;
- DLQ ARQ ;
- validation des secrets au démarrage ;
- CI/CD GitHub Actions ;
- control plane UI ;
- OCR fallback GLM-4V ;
- promotion mémoire `promotable` ;
- protocole HESTIA projet → agence ;
- auto-capitalisation décisions C3+ ;
- indexation RAG des courriers ;
- cockpit d’affaire consolidé ;
- modules `planning`, `chantier`, `communications`, `finance`.

⚠️ Ces éléments doivent être revérifiés par audit de code complet après la mise à jour documentaire.

---

# 5. Active Backlog

## 5.1 Core and Runtime

### ⬜ Module `decisions`

Déjà indiqué comme partiel : table `project_decisions`, extraction post-orchestration de décisions C3+, dette D0-D3.

Reste à faire : module API complet, endpoints CRUD, filtres par dette, résolution manuelle, alertes D3, dashboard dédié.

### 🔄 Chaîne de veto séquencée

Partiel.

Déjà documenté : veto C4/C5, THEMIS, HEPHAESTUS, parse structuré, hiérarchie de sévérité.

Reste à faire : formalisation complète `veto_zeus`, modèle `verdict / justification / severity / lift_condition`, traçabilité UI.

### ⬜ Approval Gate / HITL

À faire / à vérifier.

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

### 🔄 Mémoire — refactoring de service

Partiel et prioritaire.

Déjà indiqué comme livré : promotion `promotable`, HESTIA post-orchestration, proposition mémoire agence.

Reste à faire :

- clarifier les scopes mémoire ;
- distinguer raw history, candidate facts, active facts, summaries, cards et traces ;
- vérifier si `extract_and_store_memories()` respecte cette séparation ;
- éviter toute promotion massive non sourcée ;
- ajouter ou vérifier le statut `candidate / active / superseded / retracted` ;
- ajouter ou vérifier le context preview ;
- ajouter ou vérifier le dry-run de consolidation ;
- protéger raw messages, documents, traces et tool outputs contre réécriture de consolidation ;
- vérifier que les cards compactes ne deviennent pas des dumps append-only ;
- documenter les owners HESTIA / MNEMOSYNE / HADES / ARGOS / THEMIS / ZEUS dans le code.

### ⬜ Auditable context injection

À faire / à vérifier.

Objectif : pouvoir afficher le contexte réellement injecté ou prévu pour un agent : facts, candidate exclusions, cards, summaries, chunks, documents, décisions, traces pertinentes.

### ⬜ Memory consolidation dry-run

À faire / à vérifier.

Toute promotion, rétractation, supersession, fusion ou condensation doit pouvoir être prévisualisée avant application.

### ⬜ Affaires — exposition complète des nouveaux champs

Reste à faire : schemas, router, enums métier.

### 🔄 Tests automatisés

Partiel.

Déjà indiqué : CI, `tests/test_guards.py`, base pytest.

Reste à faire : tests tools, `orchestra/service.py`, E2E RAG, mémoire, approvals, workflows C1-C5, context preview, consolidation dry-run.

### 🔄 Monitoring agents / runs

Partiel.

Déjà indiqué : control plane UI, runs list, traces, errors stream, websocket refresh.

Reste à faire : dashboards performance, durée par agent, taux d’échec, fréquence d’activation, métriques d’usage, changements mémoire, contexte injecté, approvals, browser action traces.

---

## 5.2 Interfaces and Channels

### ⬜ Module `webhooks` — Telegram / WhatsApp

Cible : réception Telegram / WhatsApp, routing par mention, fallback HERMES, mémoire de fil par HESTIA, support photo, réponse canal, auth expéditeur.

### ⬜ OpenWebUI Pipelines

Objectif : déclencher directement ZEUS / orchestra depuis OpenWebUI et réduire friction UI → runtime.

### 💡 Browser Tool gouverné

Intéressant mais non prioritaire.

Source d’inspiration analysée : `browser-use/browser-harness`.

À retenir :

- primitives browser simples ;
- screenshots comme preuve d’état ;
- action trace avant/après ;
- domain browser skills ;
- HTTP direct quand possible.

À rejeter :

- agent libre sur le Chrome personnel par défaut ;
- auto-modification des helpers pendant un run ;
- clics coordonnées sans trace ;
- actions sur compte connecté sans Approval Gate.

Statut : à intégrer seulement après PolicyEngine, Approval Gate et Observability.

### 💡 Voix

À explorer plus tard : transcription, TTS, OpenWebUI, webhooks.

---

## 5.3 Document and Retrieval Layer

### ⬜ Retrieval multimodal

Objectif : plans, coupes, photos, images, chunk image + description, pipeline ARGOS, qualification technique, fusion retrieval.

### 🔄 OCR / extraction avancée

Partiel : fallback OCR GLM-4V indiqué.

Reste à faire : industrialisation, scoring qualité OCR, monitoring extraction.

---

## 5.4 Optimization and Learning

### 🔄 DSPy — plan phasé

Conceptuellement prêt, non industrialisé.

Phase 1 : instrumentation.

Phase 2 : optimisation tâches structurées : criticité, actions, métadonnées documentaires.

Phase 3 : éventuellement HERMES ou ZEUS si volume suffisant.

Règles : ne pas optimiser les `SOUL.md`, ne pas optimiser les agents identitaires trop tôt.

### 🔄 HESTIA / MNEMOSYNE learning loop

Partiel.

Déjà indiqué : promotion `promotable`, protocole capitalisation.

Reste à faire : gouvernance plus explicite, revue avant promotion forte, dashboard de capitalisation.

---

# 6. Architecture Overlay Backlog

## 💡 VITRUVE

Exploration.

But : agent de démarrage projet, programme, sol, topo, PLU, ABF, risques, budget, contraintes.

Sortie cible : fiche synthèse contraintes avant conception.

---

# 7. Explorations and Watchlist

## 💡 Hermes Local Memory

Analyse réalisée comme source externe utile pour Pantheon OS.

À intégrer maintenant dans la documentation : séparation raw history / candidate facts / active facts / summaries / cards / traces, contexte injecté inspectable, dry-run, cards non souveraines, consolidation explicite.

À rejeter : remplacement PostgreSQL/pgvector par SQLite, suppression FastAPI, worker mémoire opaque, copie mécanique.

## 💡 LangGraph Approval Hub

Analyse réalisée comme source externe utile pour Pantheon OS.

À intégrer maintenant dans la documentation : modèle Approval Gate, queue pending approvals, statut d’approbation, décision humaine avec note, audit log, expiration, escalation.

À rejeter : dépendance Vercel/Supabase, dashboard séparé comme source de vérité, SDK externe comme cœur du système.

## 💡 Browser Harness

Analyse réalisée comme source externe utile mais risquée.

À intégrer dans la documentation : screenshots before/after, action trace, Browser Tool gouverné, domain browser skills, HTTP direct fallback.

À rejeter : agent libre sur Chrome personnel, auto-modification de helpers, actions sans Approval Gate.

## 💡 Hindsight / TEMPR

Piste de mémoire agentique enrichie. À tester sur une affaire pilote avant migration.

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

1. Auditer le code contre `README.md`, `ARCHITECTURE.md`, `MODULES.md`, `AGENTS.md`, `ROADMAP.md`, `STATUS.md`.
2. Vérifier l’état réel de la mémoire : raw history, candidate facts, active facts, cards, summaries, traces.
3. Finaliser ou cadrer le module `decisions`.
4. Compléter la refonte mémoire.
5. Ajouter ou vérifier context preview.
6. Ajouter ou vérifier dry-run de consolidation.
7. Ajouter ou vérifier Approval Gate / HITL.
8. Compléter tests mémoire, approvals et workflows C1-C5.
9. Renforcer monitoring consolidé : approvals, contexte injecté, traces d’action.
10. Lancer `webhooks`.
11. Préparer retrieval multimodal.
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
