# Pantheon OS — Versions

Ce fichier suit les versions cibles et les composants sensibles du runtime.

Les mises à jour ne doivent pas être automatiques et aveugles. Toute évolution doit passer par : audit, changelog, tests, migration si nécessaire, puis mise à jour documentaire.

---

## Version projet

| Élément | Valeur |
|---|---|
| Version actuelle | `0.5.0-alpha.1` |
| Fichier source | `VERSION` |
| Statut | alpha, non stable |
| Branche de travail | `feature/approval-gate-activation` |

---

## Runtime cible

| Composant | Version / tag cible | Statut | Notes |
|---|---:|---|---|
| Python | 3.12 | cible | À garder aligné avec Dockerfile API |
| FastAPI | `requirements.txt` | à verrouiller | Version exacte à figer plus tard |
| PostgreSQL | 16 | actif | Via `pgvector/pgvector:pg16` |
| pgvector | image `pgvector/pgvector:pg16` | actif | Extension DB requise |
| OpenWebUI | `ghcr.io/open-webui/open-webui:main` | risqué | À figer avant release stable |
| Ollama | PC LAN | externe | Non géré par Docker NAS |
| Docker Compose | local NAS | requis | Vérifié par Installer UI |

---

## Modèles Ollama recommandés

| Usage | Modèle | Statut | Notes |
|---|---|---|---|
| Chat principal | `qwen2.5:7b` | recommandé | Bon compromis local |
| Chat puissant | `qwen2.5:14b` | optionnel | Pour PC GPU solide |
| Chat alternatif | `mistral` | optionnel | Fallback courant |
| Embeddings | `nomic-embed-text` | requis | Modèle embeddings local recommandé |

---

## Images Docker sensibles

| Image | Tag actuel | Décision |
|---|---|---|
| `pgvector/pgvector` | `pg16` | OK pour MVP |
| `ghcr.io/open-webui/open-webui` | `main` | À figer avant stable |

---

## Politique d’update

### Autorisé automatiquement

- vérifier la version locale ;
- vérifier la branche ;
- vérifier le commit ;
- vérifier s’il existe des commits distants ;
- afficher les commits entrants ;
- écrire `update_status.json`.

### Interdit sans validation explicite

- `git pull` ;
- changement de branche ;
- migration DB ;
- rebuild Docker ;
- modification `.env` ;
- update de modèle Ollama ;
- update d’image Docker vers `latest` ou `main` sans test.

### Séquence safe update

```bash
git fetch origin
git status --short
git log HEAD..origin/main --oneline
docker compose pull
docker compose up -d --build
docker compose exec -T api alembic upgrade head
docker compose exec -T api pytest
curl http://localhost:8000/health
curl http://localhost:8000/debug/runtime-registry
```

---

## Règle release

Une release Pantheon OS doit avoir :

- `VERSION` mis à jour ;
- `CHANGELOG.md` mis à jour ;
- `STATUS.md` mis à jour ;
- migrations vérifiées ;
- tests ciblés passants ;
- `/health` OK ;
- `/debug/runtime-registry` OK ;
- note des known issues.
