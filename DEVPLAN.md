# OS CHANTIER — Plan de développement technique

> Document de référence pour Claude. À relire au début de chaque session.

---

## 0. TL;DR

Système de pilotage intelligent de chantier pour une agence d'architecture (MOE).
Stack : **FastAPI + PostgreSQL/pgvector + OpenWebUI + Notion**.
Objectif : un "OS chantier" capable de générer des plannings, simuler des scénarios, extraire des actions de réunion et assister la MOE en continu.

---

## 1. ORGANISATION DU REPO

```
ARCEAG/
├── DEVPLAN.md                  ← ce fichier
├── docker-compose.yml          ← orchestration complète
├── .env.example
├── .gitignore
│
├── api/                        ← FastAPI (LoongFlow API)
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                 ← point d'entrée
│   ├── config.py               ← settings pydantic
│   ├── database.py             ← connexion SQLAlchemy async
│   │
│   ├── models/                 ← ORM SQLAlchemy
│   │   ├── __init__.py
│   │   ├── affaire.py
│   │   ├── chantier_event.py
│   │   ├── budget.py
│   │   ├── planning_task.py
│   │   ├── decision.py
│   │   ├── alert.py
│   │   ├── event.py
│   │   ├── notion_chunk.py
│   │   ├── project_memory.py   ← mémoire validée
│   │   └── user_preferences.py ← config comportement mémoire
│   │
│   ├── schemas/                ← Pydantic schemas (I/O)
│   │   ├── __init__.py
│   │   ├── affaire.py
│   │   ├── chantier_event.py
│   │   ├── planning.py
│   │   ├── scenario.py
│   │   ├── meeting.py
│   │   ├── rag.py
│   │   └── memory.py           ← candidate, save, query schemas
│   │
│   ├── routers/                ← endpoints FastAPI
│   │   ├── __init__.py
│   │   ├── chantier.py         ← /chantier/*
│   │   ├── budget.py           ← /budget/*
│   │   ├── planning.py         ← /planning/*
│   │   ├── scenario.py         ← /scenario/*
│   │   ├── meeting.py          ← /meeting/*
│   │   ├── rag.py              ← /rag/*
│   │   ├── events.py           ← /events/*
│   │   └── memory.py           ← /memory/*
│   │
│   ├── engines/                ← logique métier pure
│   │   ├── __init__.py
│   │   ├── planning_engine.py  ← tri topologique + calcul dates
│   │   ├── scenario_engine.py  ← simulation retards / météo
│   │   ├── event_engine.py     ← priorités + alertes
│   │   ├── meeting_engine.py   ← analyse CR + extraction actions
│   │   ├── rag_engine.py       ← embedding + recherche pgvector
│   │   └── memory_engine.py    ← mémoire projet : dédup, classification, validation
│   │
│   └── services/               ← intégrations externes
│       ├── __init__.py
│       ├── notion_sync.py      ← sync Notion ↔ DB
│       └── openai_client.py    ← appels LLM (embeddings, etc.)
│
├── db/                         ← migrations et seeds
│   ├── migrations/             ← Alembic
│   │   └── versions/
│   ├── alembic.ini
│   ├── seeds/
│   │   ├── seed_lots.py        ← lots standards BTP
│   │   └── seed_examples.py    ← exemples plannings
│   └── init.sql                ← extensions pgvector + schéma initial
│
├── openwebui/                  ← configuration OpenWebUI
│   ├── agents/
│   │   ├── planning_agent.yaml
│   │   ├── meeting_agent.yaml
│   │   └── chantier_agent.yaml
│   ├── tools/
│   │   ├── planning_tools.py   ← tools OpenWebUI → API
│   │   ├── chantier_tools.py
│   │   ├── rag_tools.py
│   │   └── memory_tools.py     ← candidate, save, query mémoire
│   └── knowledge/
│       └── README.md           ← instructions ingestion docs
│
└── docs/
    ├── architecture.md
    ├── api_reference.md
    └── lot_dependencies.md     ← référentiel dépendances inter-lots
```

---

## 2. MODÈLE DE DONNÉES

### 2.1 Tables principales

#### `affaires` — projets
```sql
CREATE TABLE affaires (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code        VARCHAR(50) UNIQUE NOT NULL,   -- ex: "AFF-2024-001"
    nom         VARCHAR(255) NOT NULL,
    type_projet VARCHAR(100),                  -- "maison individuelle", "ERP", etc.
    surface_m2  DECIMAL(10,2),
    adresse     TEXT,
    statut      VARCHAR(50) DEFAULT 'en_cours', -- en_cours, termine, archive
    metadata    JSONB DEFAULT '{}',
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);
```

#### `planning_tasks` — tâches planning
```sql
CREATE TABLE planning_tasks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    lot             VARCHAR(100) NOT NULL,      -- "Maçonnerie", "Charpente"...
    phase           VARCHAR(100),               -- "Gros oeuvre", "Second oeuvre"...
    task            VARCHAR(255) NOT NULL,
    duration_days   INTEGER NOT NULL,
    depends_on      UUID[] DEFAULT '{}',        -- IDs des tâches précédentes
    start_date      DATE,
    end_date        DATE,
    statut          VARCHAR(50) DEFAULT 'planned', -- planned, in_progress, done, blocked
    entreprise_id   UUID,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `chantier_events` — journal chantier
```sql
CREATE TABLE chantier_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    type_event      VARCHAR(50) NOT NULL,  -- observation|action|avancement|jalon|blocage
    lot             VARCHAR(100),
    description     TEXT NOT NULL,
    statut          VARCHAR(50) DEFAULT 'ouvert', -- ouvert|en_cours|clos
    priorite        VARCHAR(20) DEFAULT 'normal', -- low|normal|high|critical
    auteur          VARCHAR(100),
    photos          TEXT[] DEFAULT '{}',
    date_evenement  TIMESTAMPTZ DEFAULT NOW(),
    date_echeance   TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `budgets`
```sql
CREATE TABLE budgets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    lot             VARCHAR(100) NOT NULL,
    entreprise      VARCHAR(255),
    montant_marche  DECIMAL(12,2),
    montant_depense DECIMAL(12,2) DEFAULT 0,
    montant_reste   DECIMAL(12,2) GENERATED ALWAYS AS (montant_marche - montant_depense) STORED,
    statut          VARCHAR(50) DEFAULT 'actif',
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `decisions`
```sql
CREATE TABLE decisions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id),
    titre           VARCHAR(255) NOT NULL,
    description     TEXT,
    decideur        VARCHAR(100),
    date_decision   DATE,
    impacts         TEXT[],
    statut          VARCHAR(50) DEFAULT 'active',
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `notion_chunks` — RAG
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE notion_chunks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id),
    source_type     VARCHAR(100),   -- "cctp", "ccap", "cr_reunion", "norme", "exemple"
    source_ref      VARCHAR(255),   -- nom du document
    contenu         TEXT NOT NULL,
    embedding       VECTOR(1024),   -- pgvector
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON notion_chunks USING ivfflat (embedding vector_cosine_ops);
```

#### `alerts`
```sql
CREATE TABLE alerts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id),
    type_alert      VARCHAR(100) NOT NULL,  -- "deadline_depassee", "dependance_non_respectee", etc.
    severite        VARCHAR(20) NOT NULL,   -- warning|critical
    message         TEXT NOT NULL,
    entite_ref      UUID,           -- ID de la tâche / event concerné
    acquittee       BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `project_memory` — mémoire projet validée
```sql
CREATE TABLE project_memory (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    type_memory     VARCHAR(50) NOT NULL,   -- decision|risk|insight|coordination
    content         TEXT NOT NULL,
    importance      VARCHAR(20) NOT NULL DEFAULT 'info', -- info|warning|critical
    source          VARCHAR(50) NOT NULL,   -- chat|cr|chantier|notion|planning|simulation
    source_ref      UUID,                   -- ID de l'entité source (chantier_event, etc.)
    embedding       VECTOR(1024),           -- pour dédup sémantique
    validated_by    VARCHAR(100),           -- utilisateur ayant validé
    validated_at    TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Index cosine pour dédup et retrieval
CREATE INDEX ON project_memory USING ivfflat (embedding vector_cosine_ops);
-- Index filtrage rapide par affaire + type
CREATE INDEX ON project_memory (affaire_id, type_memory, importance);
```

#### `memory_candidates` — mémoire en attente de validation
```sql
CREATE TABLE memory_candidates (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affaire_id      UUID REFERENCES affaires(id) ON DELETE CASCADE,
    type_memory     VARCHAR(50) NOT NULL,
    content         TEXT NOT NULL,
    importance      VARCHAR(20) NOT NULL DEFAULT 'info',
    source          VARCHAR(50) NOT NULL,
    source_ref      UUID,
    embedding       VECTOR(1024),
    similarity_score DECIMAL(5,4),          -- similarité avec mémoire existante (si proche)
    duplicate_of    UUID REFERENCES project_memory(id), -- si doublon détecté
    statut          VARCHAR(30) DEFAULT 'pending', -- pending|validated|rejected|merged
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `user_preferences` — configuration comportement mémoire
```sql
CREATE TABLE user_preferences (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         VARCHAR(100) UNIQUE NOT NULL,  -- identifiant OpenWebUI
    auto_save       BOOLEAN DEFAULT FALSE,
    ask_validation  BOOLEAN DEFAULT TRUE,
    sensitivity     VARCHAR(20) DEFAULT 'medium',  -- low|medium|high
    -- low    : enregistre tout automatiquement
    -- medium : demande validation pour warning + critical
    -- high   : demande validation pour tout, même info
    notify_on_duplicate BOOLEAN DEFAULT TRUE,
    min_importance_to_save VARCHAR(20) DEFAULT 'info', -- seuil minimum pour proposer
    metadata        JSONB DEFAULT '{}',
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 3. PLANNING ENGINE

### Algorithme

1. Recevoir liste de tâches avec `depends_on` (IDs)
2. Tri topologique (Kahn's algorithm)
3. Pour chaque tâche dans l'ordre : `start_date = max(end_date des dépendances)`
4. `end_date = start_date + duration_days` (jours ouvrés)
5. Détecter cycles → erreur 400
6. Sauvegarder en DB

### Dépendances inter-lots référentielles

```python
LOT_DEPENDENCIES = {
    "Terrassement":       [],
    "Fondations":         ["Terrassement"],
    "Maçonnerie":         ["Fondations"],
    "Charpente":          ["Maçonnerie"],
    "Couverture":         ["Charpente"],
    "Menuiseries ext.":   ["Couverture"],
    "Isolation":          ["Menuiseries ext."],
    "Plâtrerie":          ["Menuiseries ext.", "Isolation"],
    "Électricité":        ["Plâtrerie"],      # rough-in avant plâtre fini
    "Plomberie":          ["Plâtrerie"],
    "Chauffage":          ["Plomberie"],
    "Carrelage":          ["Électricité", "Plomberie"],
    "Peinture":           ["Plâtrerie", "Électricité"],
    "Menuiseries int.":   ["Peinture"],
    "VRD":                ["Terrassement"],
    "Espaces verts":      ["VRD"],
}

JALONS = {
    "Hors d'eau":         ["Couverture"],
    "Hors d'air":         ["Menuiseries ext."],
    "Support prêt":       ["Plâtrerie"],
    "Réception":          ["Peinture", "Menuiseries int.", "Carrelage"],
}
```

### Format JSON entrée/sortie planning

**Entrée :**
```json
{
  "affaire_id": "uuid",
  "start_date": "2024-04-01",
  "tasks": [
    {
      "id": "t1",
      "lot": "Terrassement",
      "task": "Décapage terrain",
      "duration_days": 3,
      "depends_on": [],
      "phase": "Gros oeuvre"
    },
    {
      "id": "t2",
      "lot": "Fondations",
      "task": "Semelles filantes",
      "duration_days": 5,
      "depends_on": ["t1"],
      "phase": "Gros oeuvre"
    }
  ]
}
```

**Sortie :**
```json
{
  "affaire_id": "uuid",
  "duree_totale_jours": 87,
  "date_fin_estimee": "2024-07-15",
  "critical_path": ["t1", "t2", "t5", "t12"],
  "jalons": {
    "hors_eau": "2024-05-20",
    "hors_air": "2024-06-01",
    "reception": "2024-07-15"
  },
  "tasks": [
    {
      "id": "t1",
      "lot": "Terrassement",
      "task": "Décapage terrain",
      "start_date": "2024-04-01",
      "end_date": "2024-04-04",
      "duration_days": 3,
      "depends_on": [],
      "phase": "Gros oeuvre",
      "on_critical_path": false
    }
  ]
}
```

---

## 4. SCENARIO ENGINE

### Scénarios supportés

| Type | Paramètres | Impact calculé |
|------|-----------|----------------|
| `retard_lot` | lot, jours_retard | cascade sur dépendances |
| `absence_entreprise` | entreprise, date_debut, date_fin | tâches bloquées, alternatives |
| `meteo` | type (pluie/gel/canicule), duree_jours | lots impactés, report |
| `blocage_livraison` | materiau, jours_retard | tâches dépendantes |

### Format sortie scénario

```json
{
  "scenario": "retard_lot",
  "parametres": {"lot": "Maçonnerie", "jours_retard": 10},
  "impact": {
    "duree_supplementaire_jours": 10,
    "nouvelle_date_fin": "2024-07-25",
    "taches_impactees": ["t5", "t6", "t12"],
    "jalons_decales": {"reception": "+10j"},
    "cout_estime_retard": 15000
  },
  "alternatives": [
    {
      "action": "Avancer lot Menuiseries int. en parallèle",
      "gain_jours": 5,
      "faisabilite": "haute"
    }
  ],
  "planning_simule": [/* liste complète des tâches recalculées */]
}
```

---

## 5. ENDPOINTS API

### `/chantier`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/chantier/create` | Créer une affaire |
| GET | `/chantier/{id}` | Détail affaire |
| GET | `/chantier/{id}/events` | Journal chantier |
| POST | `/chantier/{id}/events` | Ajouter événement |
| PATCH | `/chantier/{id}/events/{event_id}` | Mettre à jour événement |

### `/planning`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/planning/generate` | Générer planning depuis liste tâches |
| GET | `/planning/{affaire_id}` | Récupérer planning |
| POST | `/planning/simulate` | Simuler scénario |
| POST | `/planning/update` | Recalculer après modification |
| GET | `/planning/{affaire_id}/gantt` | Export format Gantt |

### `/meeting`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/meeting/analyze` | Analyser CR brut → actions |
| POST | `/meeting/cr` | Générer CR formaté |
| GET | `/meeting/{affaire_id}/actions` | Lister actions ouvertes |
| PATCH | `/meeting/actions/{action_id}` | Mettre à jour action |

### `/rag`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/rag/ingest` | Ingérer document → chunks + embeddings |
| POST | `/rag/query` | Recherche sémantique |
| GET | `/rag/{affaire_id}/sources` | Lister sources indexées |

### `/budget`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/budget/create` | Créer ligne budgétaire |
| GET | `/budget/{affaire_id}` | Budget complet affaire |
| PATCH | `/budget/{id}` | Mettre à jour dépenses |
| GET | `/budget/{affaire_id}/alert` | Dépassements détectés |

### `/events` (event engine)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/events/process` | Traiter événements → alertes |
| GET | `/events/{affaire_id}/alerts` | Alertes actives |
| PATCH | `/events/alerts/{id}/ack` | Acquitter alerte |

### `/memory`
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/memory/candidate` | Soumettre info → dédup + classification → candidate |
| GET | `/memory/{affaire_id}/candidates` | Lister candidats en attente |
| POST | `/memory/save` | Valider et persister une candidate |
| DELETE | `/memory/candidate/{id}` | Rejeter une candidate |
| PATCH | `/memory/candidate/{id}` | Modifier contenu avant validation |
| GET | `/memory/{affaire_id}` | Lister mémoire validée (filtres: type, importance) |
| POST | `/memory/query` | Recherche sémantique dans la mémoire |
| DELETE | `/memory/{id}` | Supprimer une mémoire validée |
| GET | `/memory/{affaire_id}/context` | Contexte enrichi pour une question (memory + events + decisions) |
| GET | `/memory/preferences/{user_id}` | Lire préférences utilisateur |
| PUT | `/memory/preferences/{user_id}` | Mettre à jour préférences |

---

## 6. EVENT ENGINE — Règles métier

```python
RULES = [
    # Deadline dépassée → CRITICAL
    {
        "condition": "planning_task.end_date < today AND statut != 'done'",
        "type": "deadline_depassee",
        "severite": "critical",
        "message": "Tâche '{task}' ({lot}) deadline dépassée de {delta} jours"
    },
    # Dépendance non respectée → WARNING
    {
        "condition": "planning_task.statut == 'in_progress' AND any(dep.statut != 'done' for dep in depends_on)",
        "type": "dependance_non_respectee",
        "severite": "warning",
        "message": "Tâche '{task}' démarrée mais dépendance '{dep}' non terminée"
    },
    # Budget dépassé → CRITICAL
    {
        "condition": "budget.montant_depense > budget.montant_marche * 0.95",
        "type": "budget_critique",
        "severite": "critical",
        "message": "Lot '{lot}' : budget à {pct}% du marché"
    },
    # Blocage sans résolution > 7j → WARNING
    {
        "condition": "chantier_event.type == 'blocage' AND event.age_days > 7 AND statut == 'ouvert'",
        "type": "blocage_prolonge",
        "severite": "warning",
        "message": "Blocage ouvert depuis {age} jours : {description}"
    },
]
```

---

## 7. MEETING ENGINE

### Pipeline d'analyse CR

```
Texte brut CR
    ↓
1. LLM extraction structurée
    ↓
2. Classification par type : décision | action | observation | blocage
    ↓
3. Attribution lot + responsable + échéance
    ↓
4. Insertion chantier_events (type=action/blocage)
    ↓
5. Génération CR formaté Markdown
    ↓
6. [optionnel] Sync Notion
```

### Prompt système meeting engine

```
Tu es un assistant MOE expert en pilotage de chantier.
Analyse ce compte-rendu de réunion de chantier.

Extrais :
1. DÉCISIONS : ce qui a été décidé (avec décideur si mentionné)
2. ACTIONS : tâches à réaliser (avec responsable et échéance si disponibles)
3. OBSERVATIONS : constats sur l'avancement
4. BLOCAGES : problèmes bloquants identifiés

Pour chaque élément, précise :
- lot concerné (Maçonnerie, Charpente, Électricité, etc.)
- description claire et actionnable
- priorité (low/normal/high/critical)
- échéance si mentionnée

Retourne un JSON structuré.
```

---

## 8. RAG ENGINE

### Pipeline ingestion

```
Document (PDF/TXT/MD)
    ↓
1. Extraction texte (pypdf2 / python-docx)
    ↓
2. Chunking (500 tokens, overlap 50)
    ↓
3. Embedding (text-embedding-3-large ou nomic-embed)
    ↓
4. Stockage notion_chunks avec VECTOR(1024)
    ↓
5. Index ivfflat
```

### Pipeline requête

```
Question utilisateur
    ↓
1. Embedding question
    ↓
2. Recherche cosine similarity (top-k=5)
    ↓
3. Reranking contextuel
    ↓
4. Injection dans prompt LLM
    ↓
5. Réponse augmentée
```

---

## 9. OPENWEBUI — Agents et Tools

### Agent Planning

**Système prompt :**
```
Tu es un expert planning chantier BTP avec 20 ans d'expérience.
Tu connais parfaitement les dépendances inter-lots et les contraintes terrain.

Quand on te demande de générer un planning :
1. Interroge le RAG pour trouver des exemples similaires
2. Applique les dépendances standard (voir référentiel)
3. Génère le JSON de tâches
4. Appelle l'API /planning/generate
5. Présente le résultat de façon lisible avec jalons critiques

Tu dois TOUJOURS utiliser les tools disponibles avant de répondre.
Ne génère jamais de planning de mémoire sans interroger l'API.
```

**Tools disponibles :**
- `generate_planning(affaire_id, tasks_json, start_date)`
- `simulate_scenario(affaire_id, scenario_type, params)`
- `get_planning(affaire_id)`
- `rag_query(query, affaire_id, source_type)`

### Agent Meeting

**Système prompt :**
```
Tu es un assistant MOE spécialisé dans l'analyse de réunions de chantier.
Quand on te soumet un CR ou des notes de réunion :
1. Extrais toutes les actions, décisions et blocages
2. Classe par lot et priorité
3. Propose un CR structuré
4. Enregistre les actions via l'API

Sois précis, actionnable. Chaque action doit avoir un responsable et une date.
```

**Tools disponibles :**
- `analyze_meeting(affaire_id, raw_text)`
- `get_open_actions(affaire_id)`
- `update_action(action_id, statut)`
- `create_event(affaire_id, type, lot, description, priorite, echeance)`

### Agent Chantier (assistant général)

**Système prompt :**
```
Tu es l'OS Chantier, assistant intelligent de pilotage pour une MOE.
Tu as accès à toutes les données du chantier en temps réel.

Tu peux :
- Répondre aux questions sur l'avancement
- Détecter les incohérences et alertes
- Proposer des optimisations planning
- Analyser les risques
- Consulter les documents (CCTP, normes) via RAG

Toujours baser tes réponses sur les données réelles via les tools.
Signale clairement quand tu utilises le RAG vs les données temps réel.
```

---

## 10. DOCKER COMPOSE

```yaml
version: '3.9'

services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: arceag
      POSTGRES_USER: arceag
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U arceag"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: ./api
    environment:
      DATABASE_URL: postgresql+asyncpg://arceag:${DB_PASSWORD}@db:5432/arceag
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      NOTION_TOKEN: ${NOTION_TOKEN}
      SECRET_KEY: ${SECRET_KEY}
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./api:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  openwebui:
    image: ghcr.io/open-webui/open-webui:main
    environment:
      OPENAI_API_BASE_URL: ${OPENAI_API_BASE_URL}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    volumes:
      - openwebui_data:/app/backend/data
    ports:
      - "3000:8080"
    depends_on:
      - api

  # optionnel : adminer pour inspecter la DB
  adminer:
    image: adminer
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  postgres_data:
  openwebui_data:
```

---

## 11. ORDRE DE DÉVELOPPEMENT

### Phase 1 — Fondations (priorité maximale)
- [ ] Structure repo + docker-compose
- [ ] `db/init.sql` + migrations Alembic
- [ ] `api/database.py` + connexion async
- [ ] Modèles SQLAlchemy (affaires, planning_tasks, chantier_events)
- [ ] Schemas Pydantic
- [ ] Router `/chantier` (CRUD basique)

### Phase 2 — Planning Engine
- [ ] `engines/planning_engine.py` (tri topo + calcul dates)
- [ ] Router `/planning/generate`
- [ ] Router `/planning/simulate` (scénarios)
- [ ] Tests unitaires planning engine

### Phase 3 — Event + Alert Engine
- [ ] `engines/event_engine.py`
- [ ] Router `/events`
- [ ] Tâche background (APScheduler ou Celery) pour run engine périodiquement

### Phase 4 — Meeting Engine + RAG + Memory Engine
- [ ] `engines/rag_engine.py` (embedding + pgvector)
- [ ] Router `/rag/ingest` + `/rag/query`
- [ ] `engines/meeting_engine.py`
- [ ] Router `/meeting`
- [ ] Tables `project_memory`, `memory_candidates`, `user_preferences`
- [ ] `engines/memory_engine.py` (pipeline complet)
- [ ] Router `/memory` (tous les endpoints)
- [ ] Tests déduplication (similarité cosine)

### Phase 5 — OpenWebUI
- [ ] Configuration agents (YAML)
- [ ] Tools Python (wrappers API)
- [ ] Ingestion knowledge (CCTP exemples, normes)
- [ ] Tests agents en conversationnel

### Phase 6 — Intégrations
- [ ] `services/notion_sync.py`
- [ ] Webhooks Notion → API
- [ ] Export Gantt

---

## 12. VARIABLES D'ENVIRONNEMENT

```env
# DB
DB_PASSWORD=changeme
DATABASE_URL=postgresql+asyncpg://arceag:changeme@db:5432/arceag

# LLM
OPENAI_API_KEY=sk-...
OPENAI_API_BASE_URL=https://api.openai.com/v1
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIM=1024
LLM_MODEL=gpt-4o

# Notion
NOTION_TOKEN=secret_...
NOTION_DATABASE_AFFAIRES=...
NOTION_DATABASE_ACTIONS=...

# API
SECRET_KEY=changeme-secret
API_PORT=8000
DEBUG=true
```

---

## 13. RÈGLES DE DEV (à respecter absolument)

1. **Toute logique métier dans `engines/`** — jamais dans les routers
2. **Routers = validation + appel engine + retour HTTP** uniquement
3. **SQLAlchemy async** partout (asyncpg driver)
4. **Pydantic v2** pour tous les schemas
5. **OpenWebUI ne contient aucune logique** — tout passe par l'API
6. **pgvector** pour tout ce qui est sémantique (pas d'index texte brut)
7. **UUID** comme clé primaire partout
8. **JSONB** pour les données flexibles (metadata)
9. Aucune valeur hardcodée — tout passe par `config.py` (pydantic-settings)
10. Tests dans `api/tests/` pour les engines critiques (planning, scenario)

---

## 14. QUESTIONS OUVERTES / DÉCISIONS À PRENDRE

| # | Question | Décision par défaut |
|---|----------|---------------------|
| 1 | Modèle embedding : OpenAI vs local (nomic) ? | OpenAI text-embedding-3-large |
| 2 | Auth API : JWT vs API key simple ? | API key simple en v1 |
| 3 | Sync Notion : webhook ou polling ? | Polling 5min en v1 |
| 4 | Jours ouvrés : calendrier FR ou configurable ? | Configurable par affaire |
| 5 | Multi-tenant (plusieurs agences) ? | Non en v1, prévu en v2 |
| 6 | Export Gantt : format MS Project ou CSV ? | CSV + JSON en v1 |

---

---

## 15. MEMORY ENGINE — Mémoire Projet Intelligente

### 15.1 Architecture à 3 niveaux

```
┌─────────────────────────────────────────────────────────────┐
│  Niveau 1 — MÉMOIRE BRUTE (non persistée)                   │
│  Discussion chat, analyses en cours, hypothèses temporaires  │
│  → Vie = durée de la session OpenWebUI                      │
└─────────────────────────┬───────────────────────────────────┘
                          │ détection automatique
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Niveau 2 — MÉMOIRE CANDIDATE (memory_candidates)           │
│  Information détectée comme potentiellement importante       │
│  → Dédup vérifié, classification faite, attente validation  │
└─────────────────────────┬───────────────────────────────────┘
                          │ validation utilisateur (ou auto)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Niveau 3 — MÉMOIRE VALIDÉE (project_memory)                │
│  Décisions, risques, insights, coordination                  │
│  → Persistée, indexée pgvector, exploitable par tous agents │
└─────────────────────────────────────────────────────────────┘
```

### 15.2 Pipeline de création d'une mémoire candidate

```
Information produite (chat / CR / analyse / simulation)
    │
    ▼
1. CLASSIFICATION LLM
   → type_memory  : decision | risk | insight | coordination
   → importance   : info | warning | critical
   → lot concerné (si applicable)
    │
    ▼
2. GÉNÉRATION EMBEDDING (text-embedding-3-large)
    │
    ▼
3. DÉDUPLICATION (pgvector cosine similarity)
   ┌─────────────────────────────────────────────────────┐
   │ Rechercher dans project_memory WHERE affaire_id = X  │
   │ ORDER BY embedding <=> query_embedding LIMIT 5       │
   │                                                      │
   │  similarity >= 0.92  →  DOUBLON — ne pas créer      │
   │  0.75 <= sim < 0.92  →  PROCHE — signaler + proposer│
   │  similarity < 0.75   →  NOUVEAU — créer candidate   │
   └─────────────────────────────────────────────────────┘
    │
    ▼
4. VÉRIFICATION CROSS-TABLES
   → chantier_events (descriptions similaires ?)
   → decisions (déjà arbitré ?)
   → alerts (déjà alerté ?)
    │
    ▼
5. CRÉATION memory_candidates
   → statut = 'pending'
   → similarity_score + duplicate_of si proche
    │
    ▼
6. DÉCISION SELON user_preferences
   (voir section 15.4)
```

### 15.3 Classification automatique

**Prompt système classifieur :**
```
Tu es un assistant MOE expert en pilotage de chantier.
Analyse cette information extraite d'un échange chantier.

Classifie selon :
TYPE (un seul) :
- decision    : une décision a été prise ou doit être prise
- risk        : un risque, problème ou danger identifié
- insight     : observation utile, retour d'expérience, constat important
- coordination: information de coordination entre acteurs / lots

IMPORTANCE (un seul) :
- critical : impact direct sur délai, coût, sécurité ou réception
- warning  : impact possible, à surveiller
- info     : utile à conserver, pas d'urgence

Réponds UNIQUEMENT avec ce JSON :
{
  "type_memory": "...",
  "importance": "...",
  "lot": "...",          // lot BTP concerné, null si transversal
  "resume": "...",       // résumé en 1 phrase claire et actionnable (max 120 chars)
  "raison": "..."        // justification courte de la classification
}
```

**Exemples de classification :**

| Information brute | type | importance |
|---|---|---|
| "réservation PAC mal positionnée de 30cm" | risk | warning |
| "décision : changer entreprise lot plomberie" | decision | critical |
| "prévoir 2 semaines de délai livraison charpente métal" | insight | warning |
| "BET structure attend validation plans avant semaine 3" | coordination | warning |
| "prise de conscience : éviter joints en fond de tableau" | insight | info |
| "retard coulage dalle dû aux gelées, impact -7j planning" | risk | critical |

### 15.4 Comportement selon user_preferences

```python
def should_auto_save(candidate: MemoryCandidate, prefs: UserPreferences) -> str:
    """
    Retourne : 'auto_save' | 'ask_user' | 'skip'
    """
    # Mode auto total
    if prefs.auto_save and not prefs.ask_validation:
        return 'auto_save'

    # Seuil importance non atteint → ignorer
    importance_rank = {'info': 0, 'warning': 1, 'critical': 2}
    if importance_rank[candidate.importance] < importance_rank[prefs.min_importance_to_save]:
        return 'skip'

    # Mode intelligent (défaut)
    if not prefs.auto_save and prefs.ask_validation:
        match prefs.sensitivity:
            case 'low':
                # Auto-save sauf critical → demander
                return 'ask_user' if candidate.importance == 'critical' else 'auto_save'
            case 'medium':
                # Demander pour warning + critical
                return 'ask_user' if candidate.importance in ('warning', 'critical') else 'auto_save'
            case 'high':
                # Toujours demander
                return 'ask_user'

    return 'ask_user'
```

### 15.5 Format de la proposition à l'utilisateur (OpenWebUI)

L'agent doit présenter la candidature de façon structurée et concise.

**Template réponse agent :**
```
---
📋 **Nouvelle information détectée**

**Type :** `{type_memory}` | **Importance :** `{importance}`
**Lot :** {lot}

> {resume}

{si_proche}
⚠️ Information proche déjà enregistrée :
> "{contenu_existant}" (similarité: {similarity_score:.0%})

---
Souhaitez-vous l'enregistrer ?
**[Oui]** · **[Non]** · **[Modifier]**
---
```

**Comportement des actions :**

| Action | Effet |
|--------|-------|
| `[Oui]` | Appelle `/memory/save` → statut `validated` → insert `project_memory` |
| `[Non]` | Appelle `DELETE /memory/candidate/{id}` → statut `rejected` |
| `[Modifier]` | Affiche l'information éditable → `PATCH /memory/candidate/{id}` → repropose |

### 15.6 Recherche et utilisation en contexte

**Avant chaque analyse (meeting, planning, simulation) le système doit :**

```python
async def build_project_context(affaire_id: UUID, question: str) -> ProjectContext:
    """
    Construit le contexte enrichi pour l'IA avant toute analyse.
    Fusionne mémoire, events et décisions sans doublon.
    """
    embedding = await embed(question)

    # 1. Mémoire projet (top 8 par similarité)
    memories = await db.execute("""
        SELECT * FROM project_memory
        WHERE affaire_id = :aid
        ORDER BY embedding <=> :emb
        LIMIT 8
    """, {"aid": affaire_id, "emb": embedding})

    # 2. Events récents / ouverts critiques
    events = await db.execute("""
        SELECT * FROM chantier_events
        WHERE affaire_id = :aid
          AND statut != 'clos'
          AND priorite IN ('high', 'critical')
        ORDER BY date_evenement DESC
        LIMIT 10
    """, {"aid": affaire_id})

    # 3. Décisions récentes
    decisions = await db.execute("""
        SELECT * FROM decisions
        WHERE affaire_id = :aid
          AND statut = 'active'
        ORDER BY date_decision DESC
        LIMIT 5
    """, {"aid": affaire_id})

    # 4. Alertes actives
    alerts = await db.execute("""
        SELECT * FROM alerts
        WHERE affaire_id = :aid AND acquittee = FALSE
        ORDER BY created_at DESC LIMIT 5
    """, {"aid": affaire_id})

    return ProjectContext(
        memories=memories,
        events=events,
        decisions=decisions,
        alerts=alerts
    )
```

**Endpoint dédié :**
`GET /memory/{affaire_id}/context?question={question}`

Retourne le contexte fusionné, injecté dans le prompt système des agents.

### 15.7 Tools OpenWebUI — memory_tools.py

```python
"""
Tools mémoire pour les agents OpenWebUI.
Ces fonctions sont appelées par l'agent quand il détecte une information importante.
"""

async def detect_and_candidate_memory(
    affaire_id: str,
    raw_content: str,
    source: str = "chat"
) -> dict:
    """
    Soumettre une information pour évaluation mémoire.
    L'API classe, déduplique et crée la candidate.
    Retourne la candidate avec recommandation (auto_save | ask_user | skip).
    """
    response = await api_post("/memory/candidate", {
        "affaire_id": affaire_id,
        "content": raw_content,
        "source": source
    })
    return response


async def validate_memory(candidate_id: str, user_id: str) -> dict:
    """Valider et persister une candidate."""
    return await api_post("/memory/save", {
        "candidate_id": candidate_id,
        "validated_by": user_id
    })


async def reject_memory(candidate_id: str) -> dict:
    """Rejeter une candidate."""
    return await api_delete(f"/memory/candidate/{candidate_id}")


async def query_project_memory(
    affaire_id: str,
    question: str,
    type_filter: str = None,
    importance_filter: str = None
) -> dict:
    """Recherche sémantique dans la mémoire validée."""
    return await api_post("/memory/query", {
        "affaire_id": affaire_id,
        "question": question,
        "type_filter": type_filter,
        "importance_filter": importance_filter
    })


async def get_project_context(affaire_id: str, question: str) -> dict:
    """Contexte enrichi : mémoire + events + décisions + alertes."""
    return await api_get(f"/memory/{affaire_id}/context", {"question": question})
```

### 15.8 Intégration dans les autres engines

**Meeting engine** — après extraction des actions :
```python
# Pour chaque décision et blocage extrait du CR
for item in extracted_items:
    if item.type in ('decision', 'blocage'):
        candidate = await memory_engine.create_candidate(
            affaire_id=affaire_id,
            content=item.description,
            source="cr",
            source_ref=meeting_id
        )
        # Le router retourne les candidats avec la réponse meeting
        # L'agent OpenWebUI les présente à l'utilisateur
```

**Planning engine** — après simulation scénario :
```python
# Si impact critique détecté
if scenario_result.duree_supplementaire_jours > 7:
    await memory_engine.create_candidate(
        affaire_id=affaire_id,
        content=f"Risque planning : {scenario.type} sur {scenario.lot} → +{delta}j sur réception",
        source="simulation",
        importance_hint="critical"  # suggestion, la classification LLM peut overrider
    )
```

**Event engine** — sur nouvelle alerte critique :
```python
if alert.severite == 'critical':
    await memory_engine.create_candidate(
        affaire_id=affaire_id,
        content=alert.message,
        source="chantier",
        source_ref=alert.entite_ref,
        importance_hint="critical"
    )
```

### 15.9 Règles de qualité mémoire (invariants)

1. **Jamais de doublon** — seuil cosine `>= 0.92` = rejet automatique sans proposition
2. **Mémoire actionnable** — le `content` doit toujours être une phrase complète et autonome (comprise hors contexte)
3. **Traçabilité obligatoire** — tout enregistrement doit avoir `source` + `source_ref` si possible
4. **Pas d'embedding null** — toute entrée `project_memory` doit avoir son embedding (contrôle DB)
5. **Nettoyage périodique** — les `memory_candidates` rejetées ou `pending` depuis > 7 jours sont archivées
6. **Importance non dégradable** — une `critical` ne peut pas être reclassifiée `info` sans justification explicite
7. **Cohérence cross-affaire** — `insights` génériques (pas liés à un lot spécifique) peuvent être tagués `global` pour réutilisation

### 15.10 Seuils de similarité cosine — calibration

| Seuil | Interprétation | Action |
|-------|---------------|--------|
| >= 0.92 | Quasi-identique | Rejet silencieux (doublon certain) |
| 0.80 – 0.91 | Très similaire | Proposer fusion ou mise à jour |
| 0.65 – 0.79 | Thème proche | Signaler l'existant, laisser choisir |
| < 0.65 | Nouveau | Créer candidate directement |

---

*Dernière mise à jour : 2026-03-21*
*Auteur : Claude (session OS Chantier)*
