# AI LOG ENTRY — 2026-05-10

Branch: `work/claude/ci-lint-tests-repair`

A: Claude

## Objective

Réparer le drift CI/lint/tests hérité (PR #55, refactor `modules/` → `apps/`, 2026-04-28) sans modifier l'architecture, sans baisser la couverture et sans toucher la doctrine. Aucun runtime, dépendance ou endpoint ajouté.

## Diagnostic

Trois drifts détectés dans `tests/`, tous imputables au renommage `modules/` → `apps/` (PR #55) puis à la consolidation des veto patterns :

1. **Format ruff** (CI scope `platform/api/ tests/`) — 2 fichiers de tests utilisaient des string concats multi-lignes que `ruff format 0.15.x` veut compacter en chaîne unique.
2. **Patch paths obsolètes** — `tests/*.py` patchaient `modules.X.Y.Z` alors que le code vit dans `apps.X.Y.Z` depuis PR #55. 28 occurrences sur 6 fichiers.
3. **Doctrine veto patterns** — `test_hephaistos_infaisable_detected` testait un pattern qui a été déplacé vers `_ARES` quand Hephaistos a été clarifié comme `diagram_builder` sans veto technique propre (`apps/guards/veto_patterns.py:82-85`).

## Changes

- `tests/test_manifest_loader.py`, `tests/test_workflow_definition_loader.py`
  - `ruff format` : compactage automatique des chaînes concaténées (whitespace seul).
- `tests/test_capture.py`, `tests/test_guards.py`, `tests/test_meeting.py`, `tests/test_memory.py`, `tests/test_orchestra.py`, `tests/test_webhooks.py`
  - Renommage des chemins de patch : `"modules.X` → `"apps.X` (28 remplacements).
  - Aucun module Python `modules.*` n'existe ; `modules.yaml` (fichier YAML à la racine) n'est PAS touché.
- `tests/test_guards.py`
  - `test_hephaistos_infaisable_detected` → `test_ares_infaisable_detected` : doctrine actuelle clarifie qu'Héphaïstos est diagram_builder ; les patterns DTU/sécurité (dont `infaisable`) sont portés par Arès. Comment court ajouté pointant `apps/guards/veto_patterns.py`.

## Files Touched

- tests/test_capture.py
- tests/test_guards.py
- tests/test_manifest_loader.py
- tests/test_meeting.py
- tests/test_memory.py
- tests/test_orchestra.py
- tests/test_webhooks.py
- tests/test_workflow_definition_loader.py
- ai_logs/2026-05-10-ci-lint-tests-repair.md

## Critical files impacted

- aucun (changements limités à `tests/`)
- pas de modification de `pyproject.toml`, `conftest.py`, `platform/api/main.py`, `core/`, `apps/`, ni de `modules.yaml`

## Tests

Toutes commandes lancées localement (Python 3.11.15, ruff 0.15.8, pytest 9.0.3) :

```text
ruff check platform/api/ tests/             → All checks passed!  EXIT 0
ruff format --check platform/api/ tests/    → 186 files already formatted  EXIT 0
ruff check .                                → All checks passed!  EXIT 0
PYTHONPATH=platform/api python3 -m pytest tests/test_api_smoke.py
                                            → 3 passed in 0.09s
PYTHONPATH=platform/api python3 -m pytest tests/ --no-cov -q --tb=no
                                            → 90 passed, 107 errors in 2.21s
```

État avant cette PR :

```text
ruff format --check platform/api/ tests/    → 2 files would be reformatted
PYTHONPATH=platform/api python3 -m pytest tests/ --no-cov -q --tb=no
                                            → 8 failed, 82 passed, 107 errors
```

Évolution : 8 failures → 0 failure, +8 tests passants (90 vs 82).

## Open points

- Les 107 ERROR restants sont tous `socket.gaierror` (impossibilité de joindre PostgreSQL/Redis depuis ce sandbox). En CI, le job `test` provisionne `pgvector/pgvector:pg16` et `redis:7-alpine` et ces tests passeront.
- `ruff format --check .` (scope dépôt complet) signale 56 fichiers à reformater dans `core/`, `legacy/`, `alembic/versions/`, `scripts/install/ui/`, `skills/generic/`. Le `[tool.ruff.lint] exclude` du `pyproject.toml` exclut `legacy/` et `alembic/versions/` du linter mais pas du formatter. Hors scope CI actuel ; à reprendre dans un Bloc dédié si la doctrine décide d'élargir le scope.
- `tests/conftest.py:129` référence le fichier `modules.yaml` (YAML à la racine consommé par `ModuleRegistry`) — c'est un chemin de fichier, pas un module Python, donc volontairement non touché.
- 2 tests `TestMemoryPromotion` dans `test_guards.py` requièrent les fixtures DB (`db`, `affaire`) ; ils erroreront dans tout sandbox sans Postgres mais passeront en CI.

## Next action

- Une fois la PR mergée, reprendre Bloc 3 (Doctor read-only) sur `work/claude/doctor-readonly`.
- Optionnellement, ouvrir un Bloc dédié pour aligner `[tool.ruff.format]` avec le scope `lint exclude` (legacy/, alembic/versions/) afin que `ruff format --check .` repo-wide devienne propre — mais hors scope CI actuel.
