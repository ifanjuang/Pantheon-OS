# AI Logs — Pantheon OS

Dossier des journaux d'intervention des assistants IA (ChatGPT, Claude, autres) sur le dépôt.

Objectif : éviter les doublons, conflits de branches, modifications contradictoires et incohérences entre code et documentation.

## Format

- **Une entrée = un fichier** : `YYYY-MM-DD-slug.md` (par exemple `2026-04-29-external-tools-governance.md`).
- L'entrée existante `2026-04-29-external-tools-governance.md` sert de référence canonique.
- Les anciennes entrées (avant cette unification) sont conservées dans `0000-historical-archive.md`.

## Règles

1. **Lire** les entrées récentes du dossier avant toute modification.
2. **Lire** les Markdown de référence (sous `docs/governance/`) avant toute modification structurante :
   - `docs/governance/STATUS.md`
   - `docs/governance/ROADMAP.md`
   - `docs/governance/ARCHITECTURE.md`
   - `docs/governance/AGENTS.md`
   - `docs/governance/MODULES.md`
   - `docs/governance/MEMORY.md`
   - `README.md`
3. **Ne jamais** pousser directement sur `main`.
4. **Travailler** sur une branche dédiée.
5. **Créer** une nouvelle entrée datée pour chaque intervention significative.
6. **Signaler** clairement tout impact sur un fichier critique.
7. Les Markdown de référence restent la base du développement.
8. Si le code est plus pertinent que les Markdown, proposer ou appliquer d'abord la mise à jour documentaire.
9. **Ne jamais** inscrire dans le dépôt des informations issues de conversations privées, projets réels, clients, entreprises, adresses, chantiers ou personnes identifiables.

## Fichiers critiques (impact à signaler)

- `docs/governance/STATUS.md`, `ROADMAP.md`, `ARCHITECTURE.md`, `AGENTS.md`, `MODULES.md`, `MEMORY.md`
- `README.md`, `CLAUDE.md`, `CHANGELOG.md`
- `hermes/skill_policy.md`, `hermes/external_skill_repos.md`
- `modules.yaml`, `plugins.yaml`
- `platform/api/main.py`
- `platform/api/core/registries/*`, `platform/api/core/contracts/*`
- `platform/api/apps/*`
- `alembic/versions/*`
- `docker-compose.yml`, `.env.example`
- `pyproject.toml`

## Conventions de branches

- ChatGPT : `work/chatgpt/*` ou `feature/chatgpt/*`
- Claude : `work/claude/*` ou `feature/claude/*` ou `claude/*`
- `main` : stable uniquement (jamais de push direct).

## Template d'entrée

Créer un fichier `ai_logs/YYYY-MM-DD-slug.md` avec le contenu suivant :

```md
# AI LOG ENTRY — YYYY-MM-DD

Branch: `<branch-name>`

A: <ChatGPT | Claude | autre>

## Objective

<une phrase>

## Changes

- <liste à puces>

## Files Touched

- <liste des chemins>

## Critical files impacted

- <liste ou "none">

## Tests

- <commande(s) lancée(s) ou "non lancé">

## Open points

- <à vérifier>

## Next action

- <recommandation>
```
