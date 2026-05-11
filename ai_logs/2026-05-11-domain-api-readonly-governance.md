# AI LOG ENTRY — 2026-05-11

Branch: `work/claude/domain-api-readonly-governance`

A: Claude

## Objective

Bloc 5 du plan de stabilisation Pantheon Next. Exposer les documents de gouvernance nouvellement canonisés (`ROLE_SIGNALS.md`, `ROLE_SIGNAL_PROFILES.md`, `ROUTING_FOUNDATION.md`) via 4 endpoints `GET` read-only sur la Domain API, plus un index complet de la gouvernance. Aucun POST, aucune exécution, aucune mutation, aucun appel Hermes, aucun runtime OpenWebUI, aucun scheduler.

## Changes

- `platform/api/pantheon_domain/contracts.py`
  - Nouveau modèle Pydantic `GovernanceDocument` avec les 5 champs canoniques : `path`, `title`, `status`, `content`, `last_known_static_source`. Docstring rappelle la lecture-seule et le rôle de `last_known_static_source` comme pointeur stable vers la source de vérité.
- `platform/api/pantheon_domain/governance_docs.py` (nouveau)
  - `GovernanceEntry` dataclass frozen (path / title / status).
  - `GOVERNANCE_INDEX` : 50 entrées alignées sur `docs/governance/README.md`. `AI_LOG.md` classé `LEGACY` (deprecated pointer per le README) ; tous les autres documents en `ACTIVE`.
  - `_read_static_file(relative)` : lecture seule via `Path.read_text(encoding="utf-8")`, retourne `""` en cas d'échec (pas d'exception, pas de mutation).
  - `find_governance_entry(path)` : lookup par chemin canonique.
  - `load_governance_document(entry)` : matérialise un `GovernanceDocument` à la demande.
  - `load_governance_index(*, include_content=False)` : matérialise toute la liste. Par défaut `content=""` pour garder la réponse bornée ; `include_content=True` charge le texte complet.
  - `REPO_ROOT = Path(__file__).resolve().parents[3]` : résolution sans variable d'environnement, sans appel système.
- `platform/api/pantheon_domain/router.py`
  - Import des nouveaux helpers et de `GovernanceDocument`.
  - Helper interne `_load_indexed_doc(relative_path)` qui lève `HTTPException(404)` si le chemin n'est pas dans l'index.
  - 4 nouveaux endpoints **GET only** :
    - `GET /domain/role-signals` → `GovernanceDocument`
    - `GET /domain/role-signal-profiles` → `GovernanceDocument`
    - `GET /domain/routing-foundation` → `GovernanceDocument`
    - `GET /domain/governance-index` → `list[GovernanceDocument]` avec query `include_content` (défaut `false`)
- `tests/test_governance_api.py` (nouveau)
  - 10 tests via `fastapi.testclient.TestClient` (in-process, pas de Postgres, pas de Redis, pas de réseau réel) :
    1. `test_role_signals_endpoint_returns_doctrine` — 200, schéma 5 champs, doctrine présente.
    2. `test_role_signal_profiles_endpoint_returns_iris_doctrine` — 200, IRIS + format_reminder_request + no_decision présents.
    3. `test_routing_foundation_endpoint_returns_routing_doctrine` — 200, vocabulaire routing présent.
    4. `test_per_document_endpoints_use_get_only` — POST/PUT/PATCH/DELETE rejetés (405/404) sur les 3 routes.
    5. `test_governance_index_lists_canonical_docs` — au moins 30 docs, 12 docs canoniques toujours présents.
    6. `test_governance_index_default_omits_content` — index léger par défaut (`content == ""`).
    7. `test_governance_index_include_content_returns_full_text` — `?include_content=true` charge le texte complet.
    8. `test_governance_index_rejects_non_get` — POST/PUT/PATCH/DELETE rejetés.
    9. `test_governance_endpoints_do_not_mutate_source_files` — hash SHA-256 de `docs/governance/` invariant après appel des 4 endpoints.
    10. `test_hermes_is_not_indexed_as_pantheon_role` — aucun titre `Hermes Agent` / `Hermes Role` dans l'index (cohérent avec `hermes_not_in_agents_table` du Doctor).
    11. `test_unknown_governance_endpoint_returns_404` — typo `/domain/role-signal-profile` → 404.

## Files Touched

- platform/api/pantheon_domain/contracts.py
- platform/api/pantheon_domain/router.py
- platform/api/pantheon_domain/governance_docs.py
- tests/test_governance_api.py
- ai_logs/2026-05-11-domain-api-readonly-governance.md

## Critical files impacted

- aucun (additions uniquement ; pas de modification de `docs/governance/`, `modules.yaml`, `pyproject.toml`, `.env.example`, `docker-compose.yml`, `operations/doctor.py`, `operations/doctor.md`, `operations/validate_governance.py`, `schemas/`)

## Tests

```text
PYTHONPATH=platform/api python3 -c "from fastapi.testclient import TestClient; from main import app; ..."
  → /domain/role-signals          → 200 (19 511 bytes)
  → /domain/role-signal-profiles  → 200 (14 132 bytes)
  → /domain/routing-foundation    → 200 (10 250 bytes)
  → /domain/governance-index      → 200 (9 082 bytes, métadonnées seulement)

PYTHONPATH=platform/api python3 -m pytest tests/test_governance_api.py
  → 10 passed

PYTHONPATH=platform/api python3 -m pytest \
    tests/test_governance_api.py tests/test_api_smoke.py tests/test_doctor_readonly.py
  → 22 passed

ruff check platform/api/ tests/                    → All checks passed!
ruff format --check platform/api/pantheon_domain/ tests/test_governance_api.py
                                                   → 6 files already formatted

python3 operations/doctor.py --no-write --print    → 13 PASS, 0 WARN, 0 FAIL
```

## Doctrine respectée

- `OpenWebUI expose. Hermes Agent exécute. Pantheon Next gouverne.`
- GET only sur les 4 nouveaux endpoints (vérifié par test).
- Aucune mutation de fichier source (vérifié par hash SHA-256 de `docs/governance/` avant/après).
- Aucun appel réseau, aucun subprocess, aucun appel Hermes, aucune écriture OpenWebUI.
- Aucune activation de skill, aucune promotion mémoire, aucun scheduler, aucun agent loop.
- HERMES n'est pas indexé comme rôle Pantheon (test dédié).
- Path resolution via `parents[3]` sans variable d'environnement, sans secret.

## Open points

- L'index renvoie 50 entrées (avec `AI_LOG.md` flaggé `LEGACY`). Si un document est ajouté à `docs/governance/`, la liste statique dans `governance_docs.py` doit être mise à jour dans le même PR — c'est documenté dans la docstring du module.
- Pour `/domain/governance-index?include_content=true`, la réponse atteint ~250-500 KB selon la taille des docs. C'est borné par `docs/governance/` ; un opt-in `metadata_only` par catégorie pourrait être ajouté plus tard si besoin.
- Le chemin de résolution `parents[3]` suppose que `platform/api/pantheon_domain/` reste à 3 niveaux du repo root. Tout changement structurel devra mettre à jour cette constante et le test de path.
- Aucun endpoint ne renvoie un document hors index : `/domain/role-signal-profile` (sans `s`) renvoie 404 — vérifié.
- Pas de branchement aux flags CI : les tests roulent dans pytest standard et passent en CI grâce aux services existants (Postgres/Redis pour les autres tests). Les 10 nouveaux tests ne touchent pas la DB.

## Next action

- Une fois la PR mergée, ouvrir Bloc 6 (`work/claude/legacy-runtime-audit`) — audit read-only des composants legacy post-pivot, rapport sous `reports/code_audit/`.
- Optionnellement, ajouter un endpoint similaire pour `EVIDENCE_PACK`, `TASK_CONTRACTS`, `WORKFLOW_SCHEMA` si la roadmap exige une exposition individuelle d'autres docs (à valider en C3 hors scope Bloc 5).
