# Pantheon OS — Project Status

> Source de vérité unique sur l’état du projet.
> Ce fichier fusionne :
> - l’historique utile des évolutions
> - le backlog actif
> - les explorations en cours
>
> Il remplace la logique séparée `CHANGELOG.md` + `DEVLIST.md` par une vue consolidée :
> **ce qui est livré**, **ce qui est partiellement en place**, **ce qui reste à faire**.

Dernière mise à jour : 2026-04-21

---

# 1. Légende

- ✅ Fait
- 🔄 Partiellement implémenté
- ⬜ À faire
- 💡 Exploration / veille

---

# 2. Convention de release

Le projet suit une logique SemVer.

## MAJOR (`X.0.0`)
À utiliser pour :
- rupture d’API
- refonte architecturale
- changement de schéma non rétrocompatible
- changement majeur du runtime

## MINOR (`0.X.0`)
À utiliser pour :
- nouveau module
- nouveau workflow
- nouveau pattern d’orchestration
- nouvelle brique fonctionnelle importante

## PATCH (`0.0.X`)
À utiliser pour :
- correctif
- optimisation
- refactoring interne sans impact API
- correction sécurité ou stabilité

Règles :
- un lot cohérent mergé sur `main` produit en général une release MINOR
- un correctif critique peut produire un PATCH immédiat
- une rupture de modèle ou d’architecture produit une MAJOR

---

# 3. Current Baseline

Pantheon OS est maintenant structuré autour d’un noyau modulaire.

## ✅ Baseline actuelle

- `core/` devient le framework pur
- `modules/` porte les composants auto-découverts
- `platform/` regroupe API, UI, data, storage, infra
- `domains/` existe comme couche d’overlays métier
- les manifests deviennent la source de vérité locale des modules
- l’auto-discovery remplace les anciens registres YAML centralisés

## ✅ Direction d’architecture validée

- séparation control plane / data plane
- modularité filesystem-first
- agents, skills, tools, workflows séparés
- runtime générique
- overlays métier hors du core
- gouvernance explicite
- criticité C1–C5
- mémoire multi-couches
- RAG hybride
- orchestration multi-patterns

---

# 4. Delivered Recently

## ✅ Refactoring modulaire majeur

Livré :
- passage de `runtime/hermes/` vers `core/` + `modules/`
- `modules/agents/{layer}/{myth}_{role}/`
- `modules/skills/`
- `modules/tools/`
- `modules/workflows/`
- `platform/api/apps/` à la place de `platform/api/modules/`
- config simplifiée à 5 fichiers
- auto-discovery via `ManifestLoader`

## ✅ Refactoring MVP précédent

Livré :
- architecture MVP simplifiée
- stack réduite pour le MVP
- variables V2 isolées
- simplification du `docker-compose`
- suppression des dépendances V2 non nécessaires dans le MVP
- activation limitée à 7 modules au démarrage

## ✅ Registre agentique et conventions

Livré :
- source de vérité agentique
- normalisation des rôles
- renommages agents
- convention SSE `{agent}.{event}`
- généralisation multi-domaine
- injection de contexte de domaine
- activation conditionnelle des agents
- limites cognitives par criticité
- supervision Héra
- score global de run

## ✅ Orchestration multi-patterns

Livré :
- `solo`
- `parallel`
- `cascade`
- `arena`
- exécution topologique par niveaux
- SSE enrichi
- sous-tâches explicites

## ✅ Retrieval hybride

Livré :
- FTS PostgreSQL
- pgvector
- fusion RRF
- index GIN
- `search_hybrid()` par défaut

## ✅ Skills / tools / runtime avancés déjà ajoutés

Livré :
- `FlowManager`
- `HecateResolver`
- `IrisClarifier`
- `MetisEditor`
- `deep_search`
- DLQ ARQ
- validation des secrets au démarrage
- CI/CD GitHub Actions
- control plane UI
- OCR fallback GLM-4V
- promotion mémoire `promotable`
- protocole Hestia projet → agence
- veto séquencé C4/C5 explicite
- auto-capitalisation des décisions C3+
- indexation RAG des courriers
- cockpit d’affaire consolidé

## ✅ Modules métier déjà livrés

Livré :
- `planning`
- `chantier`
- `communications`
- `finance`

## ✅ Contexte métier enrichi

Livré :
- `erp_type`
- `erp_categorie`
- contexte domaine injecté dans les prompts

---

# 5. Active Backlog

Cette section ne liste que ce qui reste réellement à faire après consolidation avec le changelog.

## 5.1 Core and Runtime

### ⬜ Module `decisions`
Le besoin reste valide.

Déjà en place :
- table `project_decisions`
- extraction post-orchestration de décisions C3+
- dette décisionnelle D0–D3

Reste à faire :
- module API complet `decisions`
- endpoints CRUD explicites
- filtres par dette
- résolution manuelle
- alertes automatiques D3
- tableau de bord dédié

### 🔄 Chaîne de veto séquencée
Partiellement en place.

Déjà livré :
- veto explicite C4/C5
- appels dédiés à Thémis et Héphaïstos
- parse structuré
- hiérarchie de sévérité

Reste à faire :
- formalisation complète de la chaîne cible
- intégration explicite de `veto_zeus`
- enrichissement du modèle `verdict / justification / severity / lift_condition`
- meilleure traçabilité UI

### 🔄 Mémoire — refactoring de service
Partiellement en place.

Déjà livré :
- promotion `promotable`
- Hestia post-orchestration
- proposition mémoire agence

Reste à faire :
- nettoyage explicite des scopes
- refonte de `extract_and_store_memories()`
- purge des mémoires fonctionnelles expirées
- clarification définitive des rôles Hestia / Mnemosyne / mémoire fonctionnelle

### ⬜ Affaires — exposition complète des nouveaux champs
Reste à faire :
- exposer tous les nouveaux champs de contexte dans `schemas.py`
- exposer leur mise à jour propre dans le router
- valider strictement les enums métier

### 🔄 Tests automatisés
Partiellement en place.

Déjà livré :
- CI GitHub Actions
- `tests/test_guards.py`
- base pytest
- couverture de plusieurs guards et patterns critiques

Reste à faire :
- tests unitaires plus larges sur tools
- tests d’intégration `orchestra/service.py`
- tests E2E RAG
- tests mémoire
- tests workflows critiques C1–C5

### 🔄 Monitoring agents / runs
Partiellement en place.

Déjà livré :
- control plane UI
- runs list
- traces
- errors stream
- websocket refresh

Reste à faire :
- dashboards synthétiques de performance
- durée moyenne par agent
- taux d’échec par workflow
- fréquence d’activation par agent
- métriques d’usage consolidées

---

## 5.2 Interfaces and Channels

### ⬜ Module `webhooks` — Telegram / WhatsApp
Toujours à faire.

Cible :
- réception Telegram / WhatsApp
- routing par `@mention`
- fallback Hermes
- mémoire de fil par Hestia
- support photo
- réponse dans le même canal
- auth expéditeur

### ⬜ OpenWebUI Pipelines
Toujours à faire.

Objectif :
- déclencher directement Zeus / orchestra depuis OpenWebUI
- réduire la friction UI → runtime

### 💡 Voix
À explorer plus tard.

Périmètre possible :
- transcription
- TTS
- voix dans OpenWebUI
- voix dans webhooks

---

## 5.3 Document and Retrieval Layer

### ⬜ Retrieval multimodal
Toujours à faire.

Objectif :
- intégrer plans, coupes, photos, images
- chunk image + description générée
- pipeline Argos + qualification technique
- fusion dans le retrieval

### 🔄 OCR / extraction avancée
Partiellement en place.

Déjà livré :
- fallback OCR GLM-4V
- remplacement du texte natif si OCR meilleur

Reste à faire :
- industrialisation
- scoring qualité OCR plus visible
- monitoring des modes d’extraction

---

## 5.4 Optimization and Learning

### 🔄 DSPy — plan phasé
Partiellement prêt conceptuellement, non réellement industrialisé.

Phase 1 :
- instrumentation des runs
- structuration des exemples

Phase 2 :
- optimisation sur tâches très structurées
- extraction d’actions
- classification de criticité
- extraction de métadonnées documentaires

Phase 3 :
- éventuellement Hermès et Zeus si volume d’exemples suffisant

Règles :
- ne pas optimiser les `SOUL.md`
- ne pas optimiser les agents créatifs / identitaires trop tôt

### 🔄 Hestia / Mnemosyne learning loop
Partiellement en place.

Déjà livré :
- promotion `promotable`
- protocole de capitalisation

Reste à faire :
- gouvernance plus explicite de la promotion
- outillage de revue avant promotion forte
- tableau de bord de capitalisation

---

# 6. Architecture Overlay Backlog

## 💡 `Vitruve`
Toujours en exploration.

But :
- agent de démarrage projet
- programme
- sol
- topo
- PLU
- ABF
- risques
- cohérence budget / contraintes

Sortie cible :
- fiche synthèse contraintes avant conception

---

# 7. Explorations and Watchlist

## 💡 Hindsight / TEMPR
Piste de mémoire agentique enrichie.
À tester sur une affaire pilote avant toute migration.

## 💡 Neo4j
À envisager seulement si la complexité relationnelle dépasse ce que PostgreSQL + SQL récursif peuvent couvrir proprement.

## 💡 Micro-services
Pas un objectif.
À considérer seulement si la charge ou l’équipe le justifie.

## 💡 Branch software / code
Toujours pertinente comme branche de domaine future :
- review
- blast radius
- minimal code context
- repo onboarding

---

# 8. Repo Governance

Branchements recommandés :

- `main` → stable
- `develop` → intégration
- `experiment/*` → exploration
- `overlay/*` → overlays métier

Règles :

- toute migration de schéma doit être versionnée
- toute brique critique doit avoir un test de non-régression
- toute exploration V3 reste isolée

---

# 9. Immediate Priorities

Ordre recommandé de travail maintenant :

1. finaliser `AGENTS.md`
2. finaliser `ARCHITECTURE.md`
3. créer `MODULES.md`
4. créer ou finaliser le module `decisions`
5. compléter la refonte mémoire
6. compléter les tests d’intégration
7. renforcer le monitoring consolidé
8. lancer `webhooks`
9. préparer le retrieval multimodal
10. instrumenter sérieusement pour DSPy plus tard

---

# 10. Final Rule

Ce fichier doit rester la vue consolidée de la vérité projet.

Il ne doit pas seulement raconter ce qui a changé.
Il doit dire clairement :

- ce qui est livré
- ce qui est partiel
- ce qui reste à faire
- ce qui est seulement en exploration

Pantheon OS doit rester :

- modulaire
- gouverné
- portable
- testable
- exploitable en production