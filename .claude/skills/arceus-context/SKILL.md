---
name: arceus-context
description: Contexte architectural ARCEUS — conventions, patterns, structure des modules
user-invocable: false
---

Tu travailles sur **ARCEUS**, un système d'intelligence opérationnelle pour agences d'architecture (MOE).

## Stack
FastAPI async · PostgreSQL + pgvector · MinIO · Ollama/OpenAI · LlamaIndex · Docker Compose

## Conventions absolues

### Créer un module
```
api/modules/{nom}/
├── __init__.py
├── manifest.yaml       # name, version, description, prefix, depends_on
├── models.py           # SQLAlchemy hérite de database.Base
├── schemas.py          # Pydantic request/response
├── service.py          # logique métier pure
└── router.py           # def get_router(config: dict) -> APIRouter
```

### Règles SQLAlchemy 2.0
- Hériter de `database.Base` — toujours
- Mapped columns avec `Mapped[type]` et `mapped_column()`
- UUID primary key : `mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)`
- Toute nouvelle table → import dans `alembic/env.py` + nouvelle migration

### Règles migration Alembic
- Fichier : `alembic/versions/000X_description.py`
- `revision` = "000X", `down_revision` = révision précédente
- Toujours implémenter `upgrade()` ET `downgrade()`
- Extensions pgvector activées dans 0001 — ne pas les réactiver

### Auth FastAPI
- `Depends(get_current_user)` — utilisateur connecté
- `Depends(require_role("admin", "moe"))` — rôle requis
- Import depuis `core.auth`

### Services partagés (classmethods, pas d'instanciation)
- `RagService.search(db, query, affaire_id, top_k)`
- `RagService.ingest(db, document_id, file_bytes, ...)`
- `StorageService.upload(affaire_id, module, filename, content)`
- `LlmService.chat(messages)` / `LlmService.extract(messages, ResponseModel)`

### modules.yaml
Tout nouveau module activé doit être ajouté dans `modules.yaml` dans le bon ordre (respecter depends_on).

## Agents du panthéon grec
`agents/themis/` ⚖️ · `agents/argus/` 👁️ · `agents/hermes/` ⚡ · `agents/mnemosyne/` 🏛️ · `agents/athena/` 🦉
Chaque agent a SOUL.md + IDENTITY.md + MEMORY.md. Ne pas modifier SOUL.md sans raison.
