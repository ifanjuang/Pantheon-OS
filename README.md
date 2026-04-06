# ARCEUS

> Intelligence opérationnelle pour agences MOE — du programme client à la levée des réserves.

Stack : **FastAPI** · **PostgreSQL + pgvector** · **LangGraph** · **MinIO** · **Ollama/OpenAI** · **Docker Compose**

---

## Démarrage rapide

```bash
cp .env.example .env          # configurer DB_PASSWORD, JWT_SECRET_KEY, ADMIN_EMAIL/PASSWORD
docker compose up -d
docker compose exec api alembic upgrade head
# API : http://localhost:8000 | Docs : http://localhost:8000/docs (DEBUG=true)
```

---

## Le Panthéon — 15 agents spécialisés

Organisés en 5 familles fonctionnelles. L'intelligence vient des flux, pas des agents seuls.

### Perception — comprendre le réel brut

| Agent | Rôle |
|---|---|
| **Hermès** | Interface, routage, qualification C1-C5, dispatch vers les bons agents |
| **Argos** | Observation visuelle : photos, plans, défauts — constat objectif sans interprétation |

### Analyse — donner du sens

| Agent | Rôle |
|---|---|
| **Athéna** | Structuration des problèmes, scénarios, vraie question derrière la question |
| **Héphaïstos** | Faisabilité technique, DTU, matériaux, fiches produits, avis techniques, compatibilité |
| **Prométhée** | Contre-analyse, détection des biais, critique logique des décisions |
| **Apollon** | Recherche web + RAG, vérification normative, cohérence et lisibilité du rendu final |
| **Dionysos** | Pensée latérale, rupture créative pour débloquer les situations sans issue |

### Cadrage — trancher et sécuriser

| Agent | Rôle |
|---|---|
| **Thémis** | Réglementation (DTU, RE2020, PLU, ERP, PMR) + contrat MOE + déontologie — **droit de veto** |
| **Chronos** | Temps, délais légaux, impacts planning, priorisation, chemin critique |
| **Arès** | Action terrain rapide, décisions réversibles, déblocage, relances |

### Continuité — maintenir le système

| Agent | Rôle |
|---|---|
| **Hestia** | Mémoire projet : décisions validées, hypothèses, contraintes actées, dettes décisionnelles |
| **Mnémosyne** | Mémoire agence : patterns récurrents, leçons apprises, précédents multi-projets |

### Communication & Production

| Agent | Rôle |
|---|---|
| **Iris** | Emails humains, correspondance client/entreprises/administration, relances délicates |
| **Aphrodite** | Marketing, articles, posts LinkedIn/Instagram, storytelling architectural |
| **Dédale** | Dossiers complets : PC, DCE, DOE, marchés — checklists, cohérence, pièces manquantes |

### Orchestrateur

| Agent | Rôle |
|---|---|
| **Zeus** | Arbitrage stratégique, distribution des rôles, jugement de synthèse, veto global |

---

## Criticité C1-C5

Toute demande est qualifiée par Hermès selon 5 niveaux :

| Niveau | Nature | Mode d'exécution |
|---|---|---|
| **C1** | Information pure | Agent unique, pas de Zeus |
| **C2** | Question | 1-2 agents spécialisés |
| **C3** | Décision locale réversible | Zeus optionnel, Arès peut agir |
| **C4** | Décision engageante | Zeus obligatoire + validation humaine (HITL) |
| **C5** | Risque majeur | Zeus + HITL + veto check (Thémis/Héphaïstos) |

---

## Les 3 mémoires

| Mémoire | Durée | Agent | Contenu |
|---|---|---|---|
| **Agence** | Permanente | Mnémosyne | Patterns, leçons, comportements d'entreprises, erreurs passées |
| **Projet** | Durée affaire | Hestia | Décisions validées, hypothèses, contraintes, dettes décisionnelles D0-D3 |
| **Fonctionnelle** | Session | LangGraph state | Tâches en cours, blocages immédiats, échanges actifs |

---

## Contexte projet injecté automatiquement

Chaque agent reçoit dans son prompt le contexte de l'affaire :

```
Affaire : 2024-001 — École primaire Les Pins
Typologie : ERP scolaire | Région : Occitanie
Budget MOA : 2 400 000 € HT | Honoraires MOE : 142 000 € HT
Phase courante : APD | Fin prévisionnelle : 2025-06-30
Secteur ABF : OUI | Zones à risque : inondation, retrait_gonflement
```

---

## Flux d'une demande (exemple : photo de désordre)

```
Utilisateur → Hermès (qualification C3) → Argos (constat visuel)
                                        → Héphaïstos (interprétation technique)
                                        → Chronos (impact planning)
                                        → Thémis (responsabilité contractuelle)
                                        ↓
                              Zeus (jugement) → veto_check → synthèse
                                        ↓
                              Iris (réponse client) + Hestia (mémorisation)
```

---

## Architecture technique

```
ARCEUS/
├── api/
│   ├── main.py                     # Startup FastAPI, lifespan, seed admin
│   ├── database.py                 # SQLAlchemy async engine
│   ├── core/
│   │   ├── auth.py                 # JWT, RBAC (admin/moe/collaborateur/lecteur)
│   │   ├── settings.py             # Pydantic Settings (.env)
│   │   ├── checkpointer.py         # LangGraph PostgreSQL checkpointer (HITL)
│   │   ├── queue.py                # ARQ Redis job queue
│   │   └── services/
│   │       ├── rag_service.py      # Chunking + embedding + pgvector search
│   │       ├── llm_service.py      # Chat + extraction structurée
│   │       └── storage_service.py  # MinIO S3
│   ├── modules/
│   │   ├── auth/                   # Login, register, JWT
│   │   ├── admin/                  # Config YAML, setup wizard
│   │   ├── affaires/               # Dossiers MOE (code, nom, typology, budget, phase…)
│   │   ├── documents/              # Upload + ingest RAG + trigger Thémis
│   │   ├── agent/                  # Boucle ReAct, mémoire dynamique, outils
│   │   ├── orchestra/              # LangGraph Zeus, C1-C5, HITL, SSE streaming
│   │   └── meeting/                # Analyse CR + actions + génération OJ
│   └── worker.py                   # ARQ worker (jobs background)
├── agents/                         # SOUL.md de chaque agent
│   ├── zeus/ hermes/ argos/
│   ├── athena/ hephaistos/ promethee/ apollon/ dionysos/
│   ├── themis/ chronos/ ares/
│   ├── hestia/ mnemosyne/
│   └── iris/ aphrodite/ dedale/
├── alembic/versions/               # Migrations séquentielles 0001→0009
└── docker-compose.yml              # DB + API + MinIO + Redis + Ollama + OpenWebUI
```

---

## Base de données

| Table | Description |
|---|---|
| `users` | Comptes, rôles RBAC |
| `affaires` | Dossiers MOE + contexte (typology, region, budget, phase, ABF, zones) |
| `affaire_permissions` | Override de rôle par affaire |
| `documents` | Fichiers uploadés (PDF/DOCX/TXT/images) |
| `chunks` | Fragments RAG, vecteur `vector(768)`, index HNSW |
| `agent_runs` | Traces d'exécution par agent (steps, sources, durée) |
| `agent_memory` | Leçons apprises par scope : `agence` / `projet` |
| `orchestra_runs` | Orchestrations Zeus : plans, assignments, résultats, HITL |
| `project_decisions` | Décisions structurées avec criticité C1-C5 et dette D0-D3 |
| `meeting_crs` | Comptes-rendus analysés par Hermès |
| `meeting_actions` | Actions extraites avec priorité, statut, échéance |
| `meeting_agendas` | Ordres du jour générés par Athéna |

---

## Endpoints principaux

```
POST /auth/login                    → JWT
POST /auth/register                 → Créer utilisateur (admin)
GET  /auth/me                       → Profil courant

POST /affaires/                     → Créer affaire (avec contexte)
GET  /affaires/                     → Lister affaires

POST /documents/upload              → Upload + ingest RAG (trigger Thémis)
POST /documents/search              → Recherche sémantique

POST /orchestra/run                 → Lancer orchestration Zeus (ARQ)
POST /orchestra/stream              → SSE streaming temps réel
POST /orchestra/run-hitl            → Avec HITL (pause avant exécution)
POST /orchestra/runs/{id}/approve   → Reprendre ou annuler après HITL

POST /meeting/crs/upload            → Analyser un CR
GET  /meeting/crs/{id}/actions      → Actions extraites
POST /meeting/agendas/generate      → Générer un ordre du jour

GET  /admin/setup/status            → Santé de tous les services
GET  /health                        → Healthcheck
```

---

## Variables d'environnement clés

```bash
DATABASE_URL=postgresql+asyncpg://arceus:password@db:5432/arceus
LLM_PROVIDER=ollama                 # ou "openai"
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=mistral:7b
EMBEDDING_PROVIDER=ollama
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIM=768
REDIS_URL=redis://redis:6379/0
ADMIN_EMAIL=admin@agence.fr
ADMIN_PASSWORD=changeme
```

---

## Roadmap

| Module | Statut | Description |
|---|---|---|
| `auth` | ✅ | JWT, RBAC 4 rôles |
| `admin` | ✅ | Config YAML, setup wizard |
| `documents` | ✅ | Upload + RAG + trigger automatique |
| `affaires` | ✅ | CRUD + contexte projet enrichi |
| `agent` | ✅ | ReAct, mémoire, outils, streaming |
| `orchestra` | ✅ | LangGraph Zeus, C1-C5, HITL, veto |
| `meeting` | ✅ | Analyse CR, actions, ordre du jour |
| `planning` | ⬜ | Gantt, lots, impacts cascade (Chronos) |
| `decisions` | ⬜ | CRUD project_decisions, dette décisionnelle |
| `webhooks` | ⬜ | Telegram, email entrant |
| `finance` | ⬜ | Situations, avenants, budget |
| `communications` | ⬜ | Registre courrier |
