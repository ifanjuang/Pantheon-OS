# ARCEUS — Architecture technique

> Document de référence. Reflète l'état actuel du code, pas une cible future.

---

## Stack

| Composant | Rôle |
|---|---|
| **FastAPI** (async) | API centrale, orchestration, endpoints |
| **PostgreSQL + pgvector** | Données + vecteurs (HNSW, cosine similarity) |
| **LangGraph** | Graphe d'orchestration Zeus (StateGraph, HITL, streaming) |
| **ARQ + Redis** | Queue de jobs background (agents, orchestra) |
| **MinIO** | Stockage fichiers bruts (PDF, images, DOCX) |
| **Ollama** | LLM + embeddings local (`mistral`, `nomic-embed-text`) |
| **OpenAI** | LLM + embeddings cloud (optionnel, `LLM_PROVIDER=openai`) |
| **OpenWebUI** | Interface chat utilisateur |

---

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                     INTERFACES                              │
│  OpenWebUI (chat)      Telegram/WA bot (⬜)   API REST      │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                      FASTAPI                                │
│                                                             │
│  /auth  /affaires  /documents  /agent  /orchestra  /meeting │
└──────┬──────────────┬───────────────┬──────────────┬────────┘
       │              │               │              │
  PostgreSQL       MinIO          Ollama/OpenAI    Redis/ARQ
  + pgvector      (fichiers)     (LLM+embed)     (jobs)
```

---

## Modules actifs

| Module | Prefix | Dépendances | Description |
|---|---|---|---|
| `auth` | `/auth` | — | JWT, RBAC 4 rôles |
| `admin` | `/admin` | — | Config YAML, healthcheck |
| `affaires` | `/affaires` | auth | Dossiers MOE + contexte enrichi |
| `documents` | `/documents` | affaires | Upload, ingest RAG, trigger Thémis |
| `agent` | `/agent` | affaires | Boucle ReAct, mémoire, outils |
| `orchestra` | `/orchestra` | agent, affaires | LangGraph Zeus, C1-C5, HITL |
| `meeting` | `/meeting` | affaires, agent | Analyse CR, actions, OJ |

---

## Le Panthéon — 15 agents + Zeus

```
PERCEPTION          ANALYSE             CADRAGE             CONTINUITÉ
──────────          ───────             ───────             ──────────
Hermès              Athéna              Zeus (orches.)      Hestia
Argos               Héphaïstos ⊗veto    Thémis ⊗veto        Mnémosyne
                    Prométhée           Chronos
                    Apollon             Arès
                    Dionysos

COMMUNICATION       PRODUCTION
─────────────       ──────────
Iris                Dédale
Aphrodite
```

⊗ = droit de veto (bloque l'exécution si C4/C5)

---

## Graphe LangGraph (orchestra)

```
[plan_agents]
     ↓
[zeus_distribute] ←── interrupt() si hitl_enabled
     ↓
[execute_agents]  ←── tous les agents en parallèle (asyncio.gather)
     ↓
[veto_check]      ←── détecte veto Thémis/Héphaïstos, interrupt() si C4+C5
     ↓
[zeus_judge]
     ├─ needs_complement → [execute_complements] → [synthesize]
     └─ complete ──────────────────────────────→ [synthesize]
                                                      ↓
                                                    [END]
```

**Modes d'exécution :**
- `run_orchestra()` — synchrone, bloquant
- `run_orchestra_from_run_id()` — ARQ worker (Redis queue)
- `run_orchestra_hitl()` — avec checkpointing PostgreSQL, reprend sur `resume_orchestra()`
- `stream_orchestra()` — SSE streaming temps réel (événements par nœud)

---

## Criticité C1-C5

```python
CRITICITE_ROUTING = {
    "C1": {"hitl": False, "zeus": False, "veto_check": False},
    "C2": {"hitl": False, "zeus": False, "veto_check": False},
    "C3": {"hitl": False, "zeus": True,  "veto_check": False},
    "C4": {"hitl": True,  "zeus": True,  "veto_check": False},
    "C5": {"hitl": True,  "zeus": True,  "veto_check": True},
}
```

C4+ → HITL automatique (pause avant `execute_agents`)
C5 → HITL + veto check après `execute_agents`

---

## Les 3 mémoires

```
agent_memory (table PostgreSQL)
├── scope='agence'   affaire_id=NULL   → Mnémosyne  [permanente]
└── scope='projet'   affaire_id=<uuid> → Hestia     [durée affaire]

LangGraph state / Redis
└── mémoire fonctionnelle               → Hermès + Chronos [session]
```

Injection automatique dans chaque prompt agent via `run_agent()` :
1. Contexte affaire (typology, region, budget, phase, ABF, zones)
2. Mémoire dynamique (leçons de l'affaire, scope='projet')

---

## Pipeline RAG

```
Upload fichier
     ↓
StorageService → MinIO (brut)
     ↓
RagService.chunk_and_embed()
  ├── Extraction texte (PDF/DOCX/TXT)
  ├── Découpe en chunks (~512 tokens, overlap 50)
  ├── Embedding (Ollama nomic-embed-text ou OpenAI)
  └── Stockage PostgreSQL chunks (vector(768), HNSW index)
     ↓
Disponible pour rag_search (cosine similarity)
     ↓
[BackgroundTask] → run_agent("themis") → analyse conformité du document
```

**Recherche :**
```sql
SELECT ... 1 - (embedding <=> :vec::vector) AS score
FROM chunks
WHERE affaire_id = :aid
ORDER BY score DESC LIMIT :k
```

---

## Outils agents (`agent/tools.py`)

| Outil | Description |
|---|---|
| `rag_search` | Recherche sémantique dans les documents du projet |
| `web_search` | DuckDuckGo avec filtre sites MOE prioritaires |
| `fetch_url` | Lecture HTML (trafilatura) + PDF (pypdf) |

Retourne `tuple[str, list[dict]]` — résultat + sources pour citation.

---

## Flux complet : question utilisateur

```
1. Utilisateur → OpenWebUI → POST /agent/run
                              { instruction, affaire_id, agent="athena" }

2. run_agent()
   ├── Charge SOUL.md de l'agent
   ├── Injecte contexte affaire (typology, region, budget, phase...)
   ├── Injecte mémoire dynamique (leçons scope='projet')
   └── Boucle ReAct (max 10 itérations)
       ├── LLM → outil ? → execute_tool() → résultat injecté
       └── LLM → réponse finale

3. Persisté dans agent_runs
4. [Arrière-plan] extract_and_store_memories() → agent_memory
```

## Flux complet : orchestration multi-agents

```
1. POST /orchestra/run { instruction, agents=[...], criticite="C3" }

2. run_orchestra()
   ├── CRITICITE_ROUTING → hitl=False (C3)
   ├── Persiste OrchestraRun (status=running, criticite=C3)
   └── LangGraph graph.invoke()
       ├── plan_agents     → chaque agent déclare son plan
       ├── zeus_distribute → Zeus distribue les rôles (JSON)
       ├── execute_agents  → tous les agents en parallèle
       ├── veto_check      → détection veto (si C4+)
       ├── zeus_judge      → complet ou complément ?
       └── synthesize      → réponse finale structurée

3. OrchestraRun mis à jour (final_answer, agent_results, duration_ms)
```

---

## Schéma DB simplifié

```
users ──────────────────────────── affaires ─────────────────────────────┐
  │ (created_by)                    │ code, nom, typology, region         │
  │                                 │ budget_moa, honoraires, phase        │
  │                                 │ date_debut, date_fin_prevue          │
  │                                 │ abf, zone_risque (JSONB)             │
  │                        ┌────────┴──────────────────────────────┐      │
  │                        │                                       │      │
  │                   documents                              agent_runs   │
  │                   chunks (vector768)                     orchestra_runs│
  │                   affaire_permissions                    agent_memory  │
  │                   meeting_crs                            project_decisions│
  │                   meeting_actions                                      │
  │                   meeting_agendas                                      │
  └────────────────────────────────────────────────────────────────────────┘
```

---

## Migrations Alembic — séquence

```
0001 → users, affaires, permissions, documents, chunks
0002 → agent_runs
0003 → orchestra_runs (plans, assignments, results, synthesis_agent)
0004 → agent_memory
0005 → agent_runs.sources (JSONB)
0006 → orchestra_runs HITL (hitl_enabled, hitl_payload, checkpoint_thread_id)
0007 → meeting (meeting_crs, meeting_actions, meeting_agendas)
0008 → agent_memory.scope + orchestra_runs.criticite + project_decisions
0009 → affaires contexte enrichi (typology, region, budget, phase, abf, zones)
```

Toujours exécuter : `docker compose exec api alembic upgrade head`
