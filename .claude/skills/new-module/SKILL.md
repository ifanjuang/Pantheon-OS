---
name: new-module
description: Scaffolde un nouveau module Pantheon OS complet — manifest, models, schemas, service, router, migration
allowed-tools: Write, Read, Bash, Glob, Grep
argument-hint: "[nom-du-module]"
---

Crée le module Pantheon OS "$ARGUMENTS" en suivant exactement les conventions du projet.

## Étapes

### 1. Lire le contexte existant
- Lire `CLAUDE.md` pour les conventions
- Lire `modules.yaml` pour voir l'ordre actuel
- Lire `alembic/env.py` pour voir les imports existants
- Lire `alembic/versions/` pour trouver le dernier numéro de révision

### 2. Créer la structure du module
Créer `platform/api/apps/$ARGUMENTS/` avec :

**`__init__.py`** — vide

**`manifest.yaml`** :
```yaml
name: $ARGUMENTS
version: "1.0.0"
description: "[À compléter]"
prefix: /$ARGUMENTS
depends_on:
  - auth
tools: []
agent: null
```

**`models.py`** — modèle SQLAlchemy avec UUID primary key, timestamps created_at/updated_at, hérite de `database.Base`

**`schemas.py`** — schémas Pydantic Create/Update/Response avec `model_config = {"from_attributes": True}`

**`service.py`** — fonctions async avec `db: AsyncSession`, logique métier sans FastAPI

**`router.py`** — `def get_router(config: dict) -> APIRouter` avec routes CRUD de base

### 3. Créer la migration Alembic
- Numéro = dernier + 1 (format 4 chiffres : 0003, 0004...)
- Fichier : `alembic/versions/000X_$ARGUMENTS.py`
- Implémenter `upgrade()` et `downgrade()`

### 4. Mettre à jour les fichiers existants
- Ajouter l'import du modèle dans `alembic/env.py` : `from apps.$ARGUMENTS.models import ...`
- Ajouter l'entrée dans `modules.yaml` au bon endroit (respecter depends_on)

### 5. Résumé final
Lister les fichiers créés/modifiés et la commande pour appliquer la migration :
```bash
docker compose exec api alembic upgrade head
```
