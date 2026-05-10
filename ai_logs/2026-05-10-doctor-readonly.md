# AI LOG ENTRY — 2026-05-10

Branch: `work/claude/doctor-readonly`

A: Claude

## Objective

Matérialiser le Doctor C0 read-only décrit par `operations/doctor.md` sous forme d'un script Python autonome, ajouter une suite de tests vérifiant son comportement et déposer un premier rapport sous `reports/doctor/`. Aucun fix automatique, aucun appel réseau, aucune mutation hors `reports/doctor/`.

## Changes

- `operations/doctor.py`
  - Script Python 3.11 read-only, stdlib uniquement (no external dependency).
  - 12 checks structurés en `Finding` dataclasses, regroupés par catégorie (root, ai_logs, governance, doctrine, runtime_boundary, canonical_paths, hygiene).
  - Checks exécutés :
    - `root_entry_points` : présence de `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `VERSION`.
    - `ai_logs_readme_present` : `ai_logs/README.md` présent.
    - `governance_docs_present` : 27 docs gouvernance requises par `operations/doctor.md` §6.
    - `role_signal_docs_present` : `ROLE_SIGNALS.md`, `ROLE_SIGNAL_PROFILES.md`, `ROUTING_FOUNDATION.md`.
    - `doctrine_lines_present` : triplet canonique français dans `README.md`, `CLAUDE.md`, `STATUS.md`.
    - `architecture_doctrine_layers` : `ARCHITECTURE.md` mentionne OpenWebUI / Hermes Agent / Pantheon (lenient, doc paraphrase).
    - `hermes_not_in_agents_table` : aucune ligne `| HERMES |` ou `| Hermes |` dans `AGENTS.md`.
    - `governance_index_coverage` : chaque `*.md` sous `docs/governance/` est référencé dans `docs/governance/README.md`.
    - `governance_dead_links` : chaque référence `docs/governance/<NAME>.md` résout vers un fichier existant.
    - `forbidden_endpoints_absent` : aucune route `@router.post`/`@app.post` vers `/agents/run`, `/runtime/execute`, `/memory/promote/auto` dans `platform/api/`.
    - `forbidden_paths_absent` : `domains/architecture/`, `workflows/generic/`, `memory/agency/` absents.
    - `legacy_paths_classified` : si `skills/generic/` existe, il doit être référencé dans `CODE_AUDIT_POST_PIVOT.md`.
    - `critical_todos_absent` : aucun `TODO!`, `FIXME!`, `XXX!` dans `docs/`, `operations/`, `platform/api/`, `ai_logs/`.
  - CLI : `--repo`, `--output`, `--print`, `--no-write`, `--date`.
  - Code de sortie toujours `0` (Doctor observe, ne casse pas la CI).
  - Aucun appel réseau, aucun shell, aucun Docker, aucun secret lu ou imprimé.
- `tests/test_doctor_readonly.py`
  - 7 tests :
    - vocabulaire `CHECKS` exposé et complet ;
    - exécution complète sur le dépôt réel ;
    - 8 checks canoniques (root, ai_logs, gov docs, role signal docs, doctrine, hermes-not-pantheon, forbidden endpoints, forbidden paths) doivent PASS sur main ;
    - sections obligatoires du rapport (`# Pantheon Doctor Report`, `Mode: C0 read-only`, `## Summary`, `## Findings`, `## Required approvals before fix`, `## Evidence Pack references`) ;
    - `--no-write` ne crée pas le fichier par défaut ;
    - `--output` écrit un Markdown valide dans le chemin donné ;
    - importer le module n'a pas d'effet de bord sur le système de fichiers.
- `reports/doctor/.gitkeep`
  - Garde le dossier de rapport sous Git sans contenu sensible.
- `reports/doctor/2026-05-10-doctor-report.md`
  - Premier rapport généré par `python3 operations/doctor.py`.
  - 13 findings : 10 PASS, 3 WARN, 0 FAIL.
  - Les 3 WARN correspondent à de vraies observations à arbitrer hors Bloc 3 :
    - `governance_index_coverage` : 2 docs non référencés dans `docs/governance/README.md`.
    - `governance_dead_links` : 3 références mortes (`AI_LOG.md`, `EVALUATION.md`, `EXTERNAL_RUNTIME_REVIEW_TEMPLATE.md`).
    - `legacy_paths_classified` : `skills/generic/` non classifié dans `CODE_AUDIT_POST_PIVOT.md`.

## Files Touched

- operations/doctor.py
- tests/test_doctor_readonly.py
- reports/doctor/.gitkeep
- reports/doctor/2026-05-10-doctor-report.md
- ai_logs/2026-05-10-doctor-readonly.md

## Critical files impacted

- aucun (additions read-only ; pas de modification de `platform/api`, `core/`, `docs/governance/`, `modules.yaml`, `pyproject.toml`, `.env.example`, `docker-compose.yml`)

## Tests

```text
ruff check platform/api/ tests/ operations/doctor.py             → All checks passed!  EXIT 0
ruff format --check operations/doctor.py tests/test_doctor_readonly.py
                                                                 → 2 files already formatted
PYTHONPATH=platform/api python3 -m pytest tests/test_doctor_readonly.py
                                                                 → 7 passed in 0.38s
PYTHONPATH=platform/api python3 -m pytest tests/test_api_smoke.py
                                                                 → 3 passed
python3 operations/doctor.py
                                                                 → reports/doctor/2026-05-10-doctor-report.md écrit
                                                                 → 10 PASS, 3 WARN, 0 FAIL
```

`ruff format --check platform/api/ tests/` signale encore 2 fichiers de test à reformater (`test_manifest_loader.py`, `test_workflow_definition_loader.py`). Ces 2 fichiers sont déjà couverts par la PR #132 (Bloc 2) — hors scope ici.

## Open points

- Le Doctor n'inspecte pas les services live (API, OpenWebUI, Hermes, Docker) ; la section `Evidence Pack references` du rapport mentionne explicitement cette limitation.
- 3 WARN détectés ne sont pas corrigés par cette PR (par doctrine : Doctor observe, ne répare pas). Ils méritent une PR dédiée C3 (`feat: address doctor warnings`) après revue.
- L'absence de répertoire `memory/` est cohérente avec STATUS.md (runtime mémoire incomplet) ; le Doctor ne le réclame pas.

## Next action

- Une fois la PR mergée, ouvrir le Bloc 4 (`work/claude/governance-schema-validation`).
- Optionnellement, traiter les 3 WARN dans une PR dédiée à part (hors scope C0 du Doctor).
