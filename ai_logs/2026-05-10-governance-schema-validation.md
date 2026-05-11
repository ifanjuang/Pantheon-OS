# AI LOG ENTRY — 2026-05-10

Branch: `work/claude/governance-schema-validation`

A: Claude

## Objective

Matérialiser les schémas statiques pour les objets de gouvernance canoniques de Pantheon Next (Bloc 4) et ajouter un validateur read-only + tests. Aucun runtime, aucune exécution de workflow, aucune mutation de fichier, aucune promotion mémoire, aucune activation de skill, aucune auto-correction.

## Changes

- `schemas/README.md`
  - Décrit le format YAML des schémas (sous-ensemble JSON-Schema lisible), le périmètre doctrinal et les `Supported keywords`. Précise que les Markdown sous `docs/governance/` restent source de vérité (les schémas n'introduisent pas de doctrine).
- `schemas/*.schema.yaml` (13 fichiers)
  - `role_signal.schema.yaml` — enveloppe canonique (ROLE_SIGNALS.md §8), enum des 20 rôles, types de signal et statuts. `forbidden_keys` : `raw_chain_of_thought`, `hidden_prompt`, `secret`, `api_key`, `private_key`, `tool_call`.
  - `addressed_role_signal.schema.yaml` — `mediator_role: IRIS` strict, `sender_substance` et `mediated_message` avec leurs `forbidden_keys` propres.
  - `role_consultation.schema.yaml` — `id` au format `RC-YYYY-...`, `max_rounds` requis.
  - `format_reminder_request.schema.yaml` — `from_role: IRIS` strict, `constraints.{no_decision,no_approval,no_execution,no_memory_promotion,no_tool_call,no_external_send}: true` enforcés via `enum: [true]`. `forbidden_keys` : `decision`, `approval`, `final_wording`, `risk_level`, `tool_call`, `secret`.
  - `format_reminder_response.schema.yaml` — `to_role: IRIS` strict, `no_decision: true` strict. `forbidden_keys` ciblent les fuites de décision.
  - `format_blocked.schema.yaml` — `from_role: IRIS`, `escalation_required: true` strict, `blocked_action` enum.
  - `task_contract.schema.yaml` — 16 champs requis (TASK_CONTRACTS.md §3+§4), `mode` enum, `remediation_policy.auto_fix_allowed: false` strict.
  - `single_role_task_contract.schema.yaml` — `approval_level` plafonné à C0/C1/C2, `mode` ∈ `{read_only, suggest, draft}`, `escalation_conditions` non vide. `forbidden_keys` interdisent `external_send`, `memory_promotion`, `file_mutation`.
  - `task_contract_revision.schema.yaml` — `resume_policy` requis avec `mode` enum (TASK_CONTRACT_REVISIONS.md §7).
  - `evidence_pack.schema.yaml` — minimum + champ optionnel `role_signal_traceability` aligné sur EVIDENCE_PACK.md §6b.
  - `memory_candidate.schema.yaml` — `forbidden_keys` interdit `agency` / `agency_scope` / `auto_promoted` (MEMORY_EVENT_SCHEMA.md §2).
  - `skill_manifest.schema.yaml` — `lifecycle` + `hermes_mapping` en `one_of` (`wrap_hermes_skill` ou `none_found`). `forbidden_keys` : `auto_activate`, `auto_levelup`, `auto_promote_memory`.
  - `workflow_manifest.schema.yaml` — 13 champs requis (WORKFLOW_SCHEMA.md §4). `forbidden_keys` : `auto_canonize`, `auto_activate`, `silent_mutation`.
- `schemas/examples/<schema>/`
  - 1 ou 2 exemples valides + 1 exemple invalide par schéma (28 instances totales).
  - Chaque invalide porte un commentaire qui désigne la règle violée et la référence canonique.
  - Exemples invalides clés :
    - `role_signal/invalid/unknown_role.yaml` — `from_role: HERMES` rejeté (AGENTS.md §3).
    - `role_signal/invalid/raw_chain_of_thought_present.yaml` — clé interdite.
    - `task_contract/invalid/auto_fix_allowed_true.yaml` — auto_fix interdit.
    - `single_role_task_contract/invalid/c4_disallowed.yaml` — C4 doit escalader vers un workflow.
    - `memory_candidate/invalid/agency_scope_used.yaml` — terminologie `agency` interdite.
- `operations/validate_governance.py`
  - Validateur stdlib + PyYAML (déjà dépendance Pantheon).
  - Charge `schemas/*.schema.yaml`, contrôle la version `$pantheon_schema: 1`, rejette les mots-clés inconnus.
  - Valide récursivement les instances avec : `object/array/string/integer/number/boolean/null/any`, `required`, `properties`, `forbidden_keys`, `items`, `enum`, `pattern`, `min_items/max_items`, `min_length/max_length`, `nullable`, `one_of`.
  - CLI `--repo`, `--schema-dir`, `--instance`, `--instances`, `--exit-on-error`. Code de sortie 0 par défaut (gouvernance, pas CI gate). Pas de mutation, pas de réseau, pas de shell.
  - Choix de localisation : sous `operations/` (à côté de `doctor.py`) plutôt que `tools/` car `tools/` est déjà un package Python legacy de la stack runtime.
- `tests/test_governance_schemas.py`
  - 11 tests : chargement, présence des 11 schémas canoniques, validation des exemples valides, échec des exemples invalides, exit 0 par défaut, exit 1 sur `--exit-on-error`, rejet des `forbidden_keys`, rejet de `HERMES` comme rôle Pantheon, rejet de `auto_fix_allowed: true`, absence d'effet de bord à l'import.

## Files Touched

- schemas/README.md
- schemas/role_signal.schema.yaml
- schemas/addressed_role_signal.schema.yaml
- schemas/role_consultation.schema.yaml
- schemas/format_reminder_request.schema.yaml
- schemas/format_reminder_response.schema.yaml
- schemas/format_blocked.schema.yaml
- schemas/task_contract.schema.yaml
- schemas/single_role_task_contract.schema.yaml
- schemas/task_contract_revision.schema.yaml
- schemas/evidence_pack.schema.yaml
- schemas/memory_candidate.schema.yaml
- schemas/skill_manifest.schema.yaml
- schemas/workflow_manifest.schema.yaml
- schemas/examples/<13 dossiers>/valid_*.yaml et invalid/*.yaml (28 fichiers)
- operations/validate_governance.py
- tests/test_governance_schemas.py
- ai_logs/2026-05-10-governance-schema-validation.md

## Critical files impacted

- aucun (additions uniquement ; pas de modification de `platform/api/`, `core/`, `docs/governance/`, `modules.yaml`, `pyproject.toml`, `.env.example`, `docker-compose.yml`, `operations/doctor.py`, `operations/doctor.md`)

## Tests

```text
python3 operations/validate_governance.py
  → 28 ok, 0 unexpected outcome(s) over 28 instances.

PYTHONPATH=platform/api python3 -m pytest tests/test_governance_schemas.py -q --no-cov
  → 11 passed

PYTHONPATH=platform/api python3 -m pytest \
    tests/test_governance_schemas.py \
    tests/test_doctor_readonly.py \
    tests/test_api_smoke.py -q --no-cov
  → 22 passed

ruff check platform/api/ tests/ operations/
  → All checks passed!

ruff format --check operations/validate_governance.py tests/test_governance_schemas.py
  → 2 files already formatted

python3 operations/doctor.py --no-write --print
  → 13 PASS, 0 WARN, 0 FAIL (Doctor regression check)
```

Note : `ruff format --check operations/doctor.py` reste signalé sur main (pré-existant, hors scope Bloc 4 ; le CI ne vérifie que `platform/api/ tests/`).

## Open points

- Le validateur n'est pas branché à la CI : exit code 0 par défaut. Une PR ultérieure C3 pourrait l'ajouter à `.github/workflows/ci.yml` avec `--exit-on-error`, après revue.
- Couverture des schémas : 11 objets canoniques + 2 variantes (`single_role_task_contract`, `task_contract_revision`). Si la doctrine introduit de nouveaux types (par exemple `consultation_request`, `consultation_result`, `agora_round`), il faudra ajouter les schémas et exemples correspondants.
- Format `one_of` : implémentation minimale (exactly-one). Suffisant pour `evidence_pack.approval_required` et `skill_manifest.hermes_mapping` ; extensions futures à prévoir si une union ouverte est nécessaire.
- HEPHAISTOS / HEPHAESTUS : les enums acceptent les deux orthographes pour ne pas forcer la réconciliation dans cette PR.
- Tous les exemples sont fictifs ; aucun nom de client, projet, personne, adresse ou chantier réel.

## Next action

- Une fois la PR mergée, ouvrir Bloc 5 (`work/claude/domain-api-readonly-governance`).
- Optionnellement, brancher `python3 operations/validate_governance.py --exit-on-error` dans CI (PR C3 séparée).
- Optionnellement, ajouter des exemples invalides supplémentaires couvrant les autres `forbidden_keys` (un par règle) lorsque la couverture devient prioritaire.
