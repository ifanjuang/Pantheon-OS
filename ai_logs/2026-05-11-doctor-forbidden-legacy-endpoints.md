# AI LOG ENTRY — 2026-05-11

Branch: `work/claude/doctor-forbidden-legacy-endpoints`

A: Claude

## Objective

Étendre le Doctor C0 read-only pour détecter les surfaces POST legacy révélées par le Bloc 6 (`reports/code_audit/2026-05-11-legacy-runtime-audit.md`) et désormais inscrites dans `CODE_AUDIT_POST_PIVOT.md §3` (PR #144). Aucune modification du runtime, aucune suppression de route, aucun nouveau endpoint, aucun branchement CI.

## Changes

- `operations/doctor.py`
  - Ajout du registre `LEGACY_RUNTIME_ENDPOINTS` (5 entrées : `(module, local_route, exposed_path, reason)`) listant `/agent/run`, `/orchestra/run`, `/orchestra/run-hitl`, `/orchestra/stream`, `/orchestra/runs/{run_id}/approve`.
  - Nouveau check `check_legacy_runtime_surfaces(repo, report)` :
    - lit `platform/api/apps/{module}/router.py` pour chaque entrée ;
    - cherche un décorateur `@router.post("local_route")` (regex tolérante guillemets simples/doubles) ;
    - rapporte `PASS` si aucune route trouvée, `WARN` (risk `high`) si au moins une est encore définie, `NOT_APPLICABLE` si `platform/api/apps/` n'existe pas ;
    - lecture seule (`Path.read_text` uniquement) ; pas de réseau, pas de subprocess, pas de mutation.
  - Choix `WARN` (et pas `FAIL`) délibéré : ces surfaces sont présentes par design pendant la transition vers Hermes Gateway et sont classées `legacy` / `to_verify` dans `CODE_AUDIT_POST_PIVOT.md §3`. Les hard-blockers (`POST /agents/run`, `POST /runtime/execute`, `POST /memory/promote/auto`) conservent leur sévérité `FAIL` dans `check_forbidden_endpoints` — les deux checks restent distincts.
  - Le check est inséré dans `CHECKS` juste après `check_forbidden_endpoints`.
  - `main()` continue de retourner `0` par défaut ; aucune option CLI ni comportement runtime n'est modifié.
- `tests/test_doctor_readonly.py`
  - `test_doctor_exposes_expected_checks` étendu pour inclure `check_legacy_runtime_surfaces`.
  - 7 nouveaux tests :
    - `test_legacy_runtime_surfaces_detected_on_real_tree` — sur le repo réel, les 5 paths attendus apparaissent en `WARN`.
    - `test_legacy_runtime_surfaces_pass_on_clean_tree` — repo synthétique sans les routes → `PASS`.
    - `test_legacy_runtime_surfaces_not_applicable_without_apps` — `platform/api/apps/` absent → `NOT_APPLICABLE`.
    - `test_legacy_runtime_surfaces_match_full_set` — repo synthétique avec les 5 routes → `WARN` avec evidence complète.
    - `test_legacy_runtime_surfaces_ignores_governance_get_endpoints` — `/domain/role-signals`, `/domain/role-signal-profiles`, `/domain/routing-foundation`, `/domain/governance-index` ne doivent pas apparaître dans l'evidence.
    - `test_legacy_runtime_surfaces_check_remains_read_only` — `mtime_ns` + bytes du router synthétique invariants après le check.
    - `test_doctor_main_still_exits_zero_with_warn` — `main(['--no-write'])` retourne `0` même quand le nouveau check produit un WARN.

## Files Touched

- operations/doctor.py
- tests/test_doctor_readonly.py
- ai_logs/2026-05-11-doctor-forbidden-legacy-endpoints.md

## Critical files impacted

- aucun (pas de modification de `platform/api/apps/agent/*`, `platform/api/apps/orchestra/*`, `platform/api/main.py`, `modules.yaml`, `docker-compose.yml`, `.env.example`, `docs/governance/*`, `schemas/*`, ni d'endpoints API)

## Tests

```text
PYTHONPATH=platform/api python3 -m pytest tests/test_doctor_readonly.py
  → 15 passed in 0.56s

PYTHONPATH=platform/api python3 -m pytest \
    tests/test_doctor_readonly.py tests/test_api_smoke.py \
    tests/test_governance_api.py tests/test_governance_schemas.py
  → 41 passed in 1.24s

ruff check operations/doctor.py tests/test_doctor_readonly.py
  → All checks passed!

ruff format --check operations/doctor.py tests/test_doctor_readonly.py
  → 2 files already formatted

python3 operations/doctor.py --no-write --print
  → exit 0
  → forbidden_endpoints_absent           PASS
  → legacy_runtime_surfaces_absent       WARN (5 surfaces détectées)
```

État Doctor après cette PR : 12 PASS + 1 WARN sur les 13 checks. Le WARN est le nouveau `legacy_runtime_surfaces_absent` qui flagge les 5 routes connues — comportement attendu et documenté.

## Doctrine respectée

- `OpenWebUI expose. Hermes Agent exécute. Pantheon Next gouverne.`
- C0 read-only : aucun fichier modifié hors de cette PR. Le check lui-même utilise uniquement `read_text`.
- Aucun runtime modifié, aucune route supprimée, aucune route désactivée.
- Aucun appel réseau, aucun subprocess, aucun Docker, aucun secret.
- Doctor reste un observateur : exit 0 par défaut, aucun fix automatique.
- Séparation `FAIL` (hard-blockers) / `WARN` (legacy transitionnel) préservée.

## Non-objectifs

- Pas de modification de `apps/agent/router.py` ni `apps/orchestra/router.py`.
- Pas de retrait des routes legacy ; elles restent telles qu'elles sont sur main.
- Pas de désactivation de modules dans `modules.yaml`.
- Pas de branchement du Doctor dans la CI (toujours opt-in).
- Pas de nouveau validateur, pas de nouveau endpoint, pas de nouveau schéma.
- Pas de modification de `docs/governance/`.

## Open points

- Le check ne couvre pour l'instant que `apps/agent/` et `apps/orchestra/`. Si d'autres apps exposent des surfaces équivalentes (e.g. `apps/webhooks/`), elles seront à ajouter dans une PR suivante après audit.
- La detection est purement syntaxique (regex sur `@*.post("X")`). Une obfuscation (assignment dynamique de route, monkey-patch) passerait à travers. Acceptable pour le périmètre lecture-seule actuel.
- Le check repose sur les routes locales (sans préfixe) ; le préfixe `/agent` / `/orchestra` est rappelé dans l'evidence pour aider la lecture.

## Next action

- Une fois mergée, ouvrir la prochaine étape de doctrine selon priorité d'`ifanjuang` :
  - soit Bloc 7 original (`work/claude/openwebui-hermes-specs`) — specs OpenWebUI / Hermes sans activation ;
  - soit traitement explicite du gel de `apps/orchestra/` (déclassement de `modules.yaml`, etc., en PR C3+ dédiée).
