---
name: migration
description: Génère une migration Alembic pour les changements de schéma détectés dans les modèles SQLAlchemy
allowed-tools: Read, Write, Glob, Grep, Bash
argument-hint: "[description-courte]"
---

Génère la migration Alembic pour "$ARGUMENTS".

## Contexte actuel
Migrations existantes : !`ls alembic/versions/ | grep -v __pycache__ | sort`
Dernier numéro : !`ls alembic/versions/ | grep -v __pycache__ | grep "^[0-9]" | sort | tail -1 | cut -c1-4`

## Étapes

### 1. Analyser les changements
- Lire les fichiers `models.py` modifiés récemment
- Identifier les tables/colonnes ajoutées, modifiées ou supprimées
- Vérifier `alembic/env.py` pour confirmer que les modèles sont importés

### 2. Calculer le prochain numéro
Format : 4 chiffres zéro-padded. Ex : si le dernier est `0002`, créer `0003`.

### 3. Créer le fichier de migration
`alembic/versions/000X_$ARGUMENTS.py` avec :
```python
revision = "000X"
down_revision = "XXXX"   # révision précédente
```

### 4. Implémenter upgrade() et downgrade()
- `op.create_table()` / `op.drop_table()`
- `op.add_column()` / `op.drop_column()`
- `op.create_index()` / `op.drop_index()`
- Pour colonnes vector pgvector : utiliser `op.execute("ALTER TABLE ... TYPE vector(768) USING NULL")`

### 5. Vérifier alembic/env.py
S'assurer que tous les nouveaux modèles sont importés dans `alembic/env.py`.

### 6. Commande d'application
```bash
docker compose exec api alembic upgrade head
```
