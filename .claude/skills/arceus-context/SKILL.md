---
name: arceus-context
description: Contexte architectural Pantheon OS — conventions, patterns, structure des modules
user-invocable: false
---

Tu travailles sur **Pantheon OS**, une plateforme d'intelligence multi-agent pour organisations professionnelles (architecture/MOE, juridique, médical, IT).

## Stack
FastAPI async · PostgreSQL + pgvector · Hermes Runtime (agents/skills/workflows) · OpenWebUI · Ollama/OpenAI · Docker Compose

## Structure clé

```
core/contracts/agent.py    # AgentBase (import depuis ici)
modules/agents/{layer}/{myth}_{role}/  # 22 agents auto-découverts
platform/api/apps/{nom}/   # modules FastAPI
config/runtime.yaml        # 5 fichiers canoniques
```

## Conventions absolues

### Créer un module FastAPI
```
platform/api/apps/{nom}/
├── __init__.py
├── manifest.yaml       # name, version, description, prefix, depends_on
├── models.py           # SQLAlchemy hérite de database.Base
├── schemas.py          # Pydantic request/response
├── service.py          # logique métier pure
└── router.py           # def get_router(config: dict) -> APIRouter
```

### Créer un agent
```
modules/agents/{layer}/{myth}_{role}/
├── agent.py            # hérite de core.contracts.agent.AgentBase
├── manifest.yaml       # id, name, layer, role, enabled, veto
├── config.yaml         # max_tokens, temperature, timeout_s
├── SOUL.md             # system prompt
└── tests/test_agent.py
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

### Services partagés (classmethods)
- `RagService.search(db, query, affaire_id, top_k)`
- `RagService.ingest(db, document_id, file_bytes, ...)`
- `LlmService.chat(messages)` / `LlmService.extract(messages, ResponseModel)`

### modules.yaml
Tout nouveau module activé doit être ajouté dans `modules.yaml` dans le bon ordre (respecter depends_on).

## Agents du panthéon (22 agents)
`@ZEUS` (meta) · `@ATHENA` (meta) · `@APOLLO` (meta) · `@Hermes` (analysis) · `@Argos` (analysis) · `@Prometheus` (analysis) · `@Hecate` (analysis) · `@Hestia` (memory) · `@Hades` (memory) · `@Kairos` (output) · `@Daedalus` (output) · `@Iris` (output)
SOUL.md dans `modules/agents/{layer}/{myth}_{role}/SOUL.md`. Ne pas modifier SOUL.md sans raison.
