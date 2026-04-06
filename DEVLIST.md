# DEVLIST — Backlog de développement ARCEUS

> Ce fichier est la source de vérité du backlog. Mis à jour à chaque session.
> Dernière mise à jour : 2026-04-06

---

## Légende

- ✅ Fait et poussé
- 🔄 Partiellement implémenté
- ⬜ À faire
- 💡 Idée / exploration

---

## Modules à créer

### ⬜ Module `decisions`
Gestion de la dette décisionnelle D0-D3 et des décisions structurées C1-C5.

**Tables déjà créées** (migration 0008) : `project_decisions`

**À implémenter :**
- `api/modules/decisions/` — models, schemas, service, router
- `GET /affaires/{id}/decisions` — liste des décisions d'une affaire
- `GET /affaires/{id}/decisions?dette=D2,D3` — décisions bloquées
- `POST /decisions/` — créer une décision manuellement
- `PATCH /decisions/{id}` — mettre à jour statut, dette
- `POST /decisions/{id}/resolve` — marquer résolue (D0)
- Alertes automatiques sur les D3 (date dépassée sans résolution)

---

### ⬜ Module `planning`
Gantt, lots, dépendances, impacts cascade (Chronos en bénéficiera directement).

**À implémenter :**
- Tables : `lots`, `jalons`, `dependances`
- CRUD lots avec dates, responsables, statuts
- Calcul automatique des impacts en cascade si un lot glisse
- Vue Gantt (JSON exploitable par le front)
- Intégration Chronos : alerte si dérive > seuil configurable
- Trigger depuis `meeting_actions` (action créée → mise à jour lot)

---

### ⬜ Module `webhooks` — Telegram / WhatsApp
Bot conversationnel avec routing @mention et support photos.

**Fonctionnalités demandées :**
- Réception messages Telegram et WhatsApp (webhook entrant)
- Routing par @mention : `@zeus`, `@themis`, `@chronos`, etc.
- Sans @mention → Hermès qualifie et route automatiquement
- Historique de conversation maintenu (Hestia mémorise le fil)
- **Support photos** : envoi photo → Argos analyse → Héphaïstos interprète → réponse au fil
- Réponse dans le même canal (Telegram ou WA)
- Authentification : seuls les numéros/comptes autorisés reçoivent une réponse

**Stack :**
- Telegram : `python-telegram-bot` ou webhook natif
- WhatsApp : Twilio API ou Meta Cloud API
- Photos : stockage MinIO + pipeline Argos → Héphaïstos

---

### ⬜ Module `finance`
Situations de travaux, avenants, budget, alertes de dépassement.

**Tables :** `situations`, `avenants`, `lignes_budget`
- Suivi situation par lot : montant marché, cumul facturé, reste à facturer
- Gestion des avenants (proposés par Thémis si hors contrat)
- Alertes budget (Chronos + Arès si dépassement)
- Tableau de bord financier par affaire

---

### ⬜ Module `communications`
Registre courrier entrant/sortant.

**Tables :** `courriers`
- Enregistrement courriers avec référence, expéditeur, objet, statut
- Upload et ingest RAG des courriers importants
- Relances automatiques (Iris + Chronos)
- Lien avec `meeting_actions` (un courrier peut créer une action)

---

### ⬜ Module `chantier`
Observations terrain, non-conformités, photos de chantier.

**Tables :** `observations`, `non_conformites`
- Upload photos → Argos analyse → Héphaïstos qualifie → statut NC
- Localisation sur plan (point XY sur image de plan)
- Suivi levée des réserves AOR
- Lien avec `meeting_actions` et `planning`

---

## Améliorations techniques

### ⬜ Affaires — mise à jour schemas/router
Les nouveaux champs de contexte (migration 0009) ne sont pas encore exposés dans l'API.

**À faire :**
- `api/modules/affaires/schemas.py` → ajouter typology, region, budget_moa, honoraires, date_debut, date_fin_prevue, phase_courante, abf, zone_risque
- `api/modules/affaires/router.py` → PUT/PATCH pour mettre à jour ces champs
- Validation : phase_courante ∈ {ESQ, APS, APD, PRO, ACT, VISA, DET, AOR}

---

### ⬜ Chaîne de veto séquencée dans LangGraph
Actuellement : veto_check détecte les mots-clés. Amélioration : chaîne formelle.

**Architecture cible :**
```
execute_agents → veto_check → [si C4+] veto_themis → [si C5] veto_hephaistos → veto_zeus → zeus_judge
```
Chaque nœud veto appelle l'agent avec une instruction structurée et attend `{"verdict": "approved"|"vetoed", "justification": "..."}`.

---

### ⬜ Mémoire — refactoring service
`api/modules/agent/memory.py` à améliorer :

- `extract_and_store_memories()` → accepter le `scope` explicitement (agence ou projet)
- `get_agent_memories()` → interroger aussi `scope='agence'` pour Mnémosyne et Hestia
- Tâche de purge périodique : nettoyer les mémoires fonctionnelles expirées

---

### ⬜ Retrieval hybride (BM25 + sémantique)
Améliorer la précision RAG en combinant cosine similarity pgvector + full-text `pg_trgm`.

**Approche :**
- Activer `pg_trgm` (déjà dans `db/init.sql`)
- Modifier `rag_service.py` : requête hybride avec RRF (Reciprocal Rank Fusion)
- Gain attendu : meilleure précision sur les requêtes avec entités spécifiques (noms, références, numéros d'article)

---

### ⬜ Hestia — intégration post-orchestration
Après chaque `synthesize` dans LangGraph, Hestia devrait automatiquement :
1. Décider si la synthèse contient une décision mémorisable
2. La stocker en `scope='projet'`
3. Si pattern agence → proposer capitalisation en `scope='agence'`

**Impact :** mémoire projet auto-alimentée sans action manuelle.

---

### 💡 Hindsight (vectorize-io) — exploration
Système de mémoire agentique avec TEMPR (sémantique + BM25 + graphe entités + temporel).
Pertinent pour remplacer `agent_memory` à terme.
**Évaluation :** tester sur une affaire pilote avant migration.

---

## Agents — améliorations SOUL.md

### ⬜ IDENTITY.md — nettoyage
Les anciens `IDENTITY.md` de Thémis, Hermès, Mnémosyne, Athéna sont obsolètes.
→ Soit les supprimer (SOUL.md contient tout), soit les aligner sur le nouveau format.

### ⬜ Hestia — protocole de capitalisation
Ajouter dans `agents/hestia/SOUL.md` le protocole exact de décision :
quand passer de mémoire projet → mémoire agence (critères : récurrence, généricité, valeur apprise).

---

## Infrastructure

### ⬜ Variables d'environnement WEBHOOK_SECRET
Documenter dans `.env.example` les variables pour les bots Telegram/WA.

### ⬜ Tests automatisés
Aucun test en place. Priorité :
- Tests unitaires sur `agent/tools.py` (execute_tool)
- Tests d'intégration sur `orchestra/service.py` (run_orchestra C1-C5)
- Tests sur `meeting/service.py` (analyse_cr)

### ⬜ Monitoring agents
Tableau de bord des runs agents : durée moyenne, taux d'échec, agents les plus sollicités.
Peut être simple (requêtes sur `agent_runs` + `orchestra_runs`).

---

## Idées à explorer

### 💡 Vitruve — Analyse programme & contexte initial
Agent dédié au démarrage de projet :
- Analyse programme client → surfaces, usages, relations fonctionnelles
- Lecture étude de sol (G1/G2) → portance, fondations, nappe
- Relevé topo → pente, orientation, NGF, voisinage
- Synthèse contraintes PLU → emprise, hauteur, prospect
- Secteur ABF → prescriptions
- Zones à risque → inondation, sismique, archéo, bruit, retrait-gonflement
- Budget MOA → cohérence programme/budget ESQ
- **Sortie :** fiche synthèse contraintes avant conception

### 💡 Retrieval multimodal
Intégrer les images (plans, coupes, photos) dans le RAG.
Un chunk peut être une image + sa description générée par Argos.

### 💡 DSPy — Optimisation des prompts
Compiler les prompts Hermès et Zeus avec DSPy MIPROv2 à partir des runs annotés.
Gain : meilleure qualité de routing sans changer le code.

### 💡 OpenWebUI — Pipelines
Créer des pipelines OpenWebUI pour déclencher directement zeus/orchestra depuis le chat.
