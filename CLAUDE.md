# ARCEUS — Contexte projet pour agents Claude Code

## Vue d'ensemble

ARCEUS est un système d'intelligence opérationnelle pour agences MOE (Maîtrise d'Œuvre). Il centralise la gestion documentaire, le RAG sémantique, le suivi de chantier, la planification et les finances sur l'ensemble du cycle de vie des projets de construction.

Stack : **FastAPI** (async) · **PostgreSQL + pgvector** · **MinIO** · **Ollama/OpenAI** · **LlamaIndex** · **Docker Compose**

## Architecture

```
ARCEUS/
├── api/                        # FastAPI — tout le backend
│   ├── main.py                 # Startup, lifespan, seed admin
│   ├── database.py             # SQLAlchemy async engine + Base
│   ├── core/
│   │   ├── auth.py             # JWT, RBAC (admin/moe/collaborateur/lecteur)
│   │   ├── settings.py         # Pydantic Settings (.env)
│   │   ├── events.py           # Bus événements PostgreSQL LISTEN/NOTIFY
│   │   ├── registry.py         # Chargeur dynamique de modules
│   │   ├── base_engine.py      # Classe de base pour les engines de module
│   │   └── services/
│   │       ├── rag_service.py  # Chunking + embedding + recherche pgvector
│   │       ├── llm_service.py  # Chat + extraction structurée (Instructor)
│   │       └── storage_service.py  # MinIO S3
│   └── modules/
│       ├── auth/               # Login, register, seed admin
│       ├── admin/              # Config YAML, setup wizard
│       ├── affaires/           # Modèle Affaire (dossier MOE)
│       └── documents/          # Upload, ingest RAG, recherche sémantique
├── alembic/                    # Migrations DB
│   └── versions/
│       └── 0001_initial_schema.py  # users, affaires, permissions, documents, chunks
├── db/init.sql                 # Extensions PostgreSQL (pgvector, uuid-ossp, pg_trgm)
├── modules.yaml                # Registre modules actifs (ordre = ordre de chargement)
└── docker-compose.yml          # DB + API + MinIO + Ollama + OpenWebUI + Portainer
```

## Modèles de données

| Table | Description |
|---|---|
| `users` | Comptes utilisateurs, rôle RBAC |
| `affaires` | Dossiers MOE (projets) |
| `affaire_permissions` | Override de rôle par affaire |
| `documents` | Fichiers uploadés (PDF/DOCX/TXT) |
| `chunks` | Fragments RAG avec vecteur `vector(768)` |

## Conventions de code

### Créer un nouveau module

Chaque module suit ce pattern :

```
api/modules/{nom}/
├── __init__.py
├── manifest.yaml       # name, version, description, prefix, depends_on
├── models.py           # Modèles SQLAlchemy (héritent de database.Base)
├── schemas.py          # Schémas Pydantic request/response
├── service.py          # Logique métier pure (pas de FastAPI ici)
└── router.py           # def get_router(config: dict) -> APIRouter
```

Le `registry.py` charge automatiquement `router.get_router(config)` et monte le router sur le `prefix` du manifest.

### Règles importantes

- **Toujours** hériter de `database.Base` pour les modèles SQLAlchemy
- **Toujours** déclarer les nouvelles tables dans `alembic/env.py` (imports en haut du fichier)
- **Toujours** créer une migration Alembic pour tout changement de schéma
- Les **imports circulaires** entre modules sont évités via des imports tardifs (`from modules.x.models import Y` dans les fonctions)
- Les services partagés (`RagService`, `LlmService`, `StorageService`) sont des **classmethods** — pas d'instanciation
- Les **dépendances FastAPI** pour l'auth : `Depends(get_current_user)`, `Depends(require_role("admin", "moe"))`

### Patterns SQLAlchemy 2.0

```python
# Requête async
result = await db.execute(select(Model).where(Model.field == value))
items = result.scalars().all()

# Recherche pgvector (cosine)
rows = await db.execute(
    text("SELECT ... 1 - (embedding <=> :vec::vector) AS score FROM chunks WHERE ..."),
    {"vec": str(embedding_list), ...}
)
```

## Lancer le projet

```bash
# 1. Copier et configurer l'environnement
cp .env.example .env
# Éditer .env : DB_PASSWORD, JWT_SECRET_KEY, ADMIN_EMAIL, ADMIN_PASSWORD

# 2. Démarrer la stack
docker compose up -d

# 3. Appliquer les migrations (première fois)
docker compose exec api alembic upgrade head

# 4. L'API est disponible sur http://localhost:8000
# Docs Swagger : http://localhost:8000/docs (DEBUG=true uniquement)
```

## Endpoints principaux

```
POST /auth/login           → JWT { access_token }
POST /auth/register        → Créer utilisateur (admin)
GET  /auth/me              → Profil courant
GET  /auth/users           → Liste utilisateurs (admin)

POST /documents/upload     → Upload fichier + ingest RAG (multipart)
POST /documents/search     → Recherche sémantique { query, affaire_id, top_k }
GET  /documents/?affaire_id=... → Liste documents

GET  /admin/setup/status   → Santé de tous les services
GET  /health               → Healthcheck API
```

## Variables d'environnement clés

```bash
DATABASE_URL=postgresql+asyncpg://arceus:password@db:5432/arceus
LLM_PROVIDER=ollama          # ou "openai"
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=mistral:7b
EMBEDDING_PROVIDER=ollama
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIM=768
ADMIN_EMAIL=admin@agence.fr
ADMIN_PASSWORD=changeme      # À changer en prod
```

## Utiliser OpenClaude sur ce projet

Pour travailler sur ARCEUS avec un LLM local (Ollama) au lieu des modèles Anthropic :

```bash
# 1. Installer OpenClaude
npm install -g @gitlawb/openclaude

# 2. Configurer (voir scripts/openclaude-setup.sh)
source scripts/openclaude-setup.sh

# 3. Lancer
openclaude
```

Le script pointe OpenClaude vers l'Ollama du docker-compose (port 11434).
Modèle recommandé pour du code : `qwen2.5-coder:14b` ou `deepseek-coder-v2:16b`.

```bash
# Pull du modèle dans Ollama
docker compose exec ollama ollama pull qwen2.5-coder:14b
```

## Roadmap modules

| Module | Statut | Description |
|---|---|---|
| `auth` | ✅ v0 | Login JWT, RBAC 4 rôles |
| `admin` | ✅ v0 | Config YAML, setup wizard |
| `documents` | ✅ v0 | Upload + RAG |
| `affaires` | ⬜ next | CRUD dossiers MOE |
| `planning` | ⬜ v1 | Gantt, lots, impacts cascade |
| `meeting` | ⬜ v1 | Analyse CR → actions |
| `finance` | ⬜ v2 | Situations, avenants, budget |
| `communications` | ⬜ v2 | Registre courrier |
| `notifications` | ⬜ v1 | SMTP, Telegram, WhatsApp |
