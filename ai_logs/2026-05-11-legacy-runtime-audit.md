# AI LOG ENTRY — 2026-05-11

Branch: `work/claude/legacy-runtime-audit`

A: Claude

## Objective

Bloc 6 du plan de stabilisation Pantheon Next. Audit read-only des composants legacy post-pivot, sans modifier de code. Production d'un rapport sous `reports/code_audit/` cartographiant chaque composant qui ressemble à `Execution Engine`, `Agent Runtime`, `Tool Runtime`, `Scheduler`, `LangGraph central`, `memory auto-promotion`, `plugin installer non gouverné`, `runtime workflow loader ancien`, `approval API ancienne`, `installer UI ancienne` ou `tests liés à l'ancien runtime`.

## Changes

- `reports/code_audit/2026-05-11-legacy-runtime-audit.md` (nouveau)
  - 11 sections : scope, vocabulaire, résumé, table de classification (par catégorie de hard blocker §7 de `CODE_AUDIT_POST_PIVOT.md`), composants nouveaux non encore inscrits dans l'audit, notes de doctrine, map des hard blockers, conformité aux contraintes, prochaines actions hors scope, Evidence Pack.
  - Vocabulaire brief mappé sur le vocabulaire existant : `keep`, `document`, `move_to_legacy`, `refactor_later`, `delete_candidate`, `blocked_until_review`.
  - Chaque ligne de la table contient : `file`, `current role`, `risk`, `status`, `safe_minimal_action`, `impact_if_removed`, `impact_if_kept`.
  - Trouvaille majeure non documentée jusqu'ici : `platform/api/apps/orchestra/` est un orchestrateur LangGraph central (StateGraph + interrupt + HITL approve endpoint), 10 fichiers, 3 159 lignes. Classification proposée : `blocked_until_review`, risque `critical`. À ajouter à `CODE_AUDIT_POST_PIVOT.md §3` dans une PR `docs:` séparée.
  - 8 lignes additionnelles proposées pour `CODE_AUDIT_POST_PIVOT.md §3` (orchestra, guards, decisions/planning/chantier/communications/finance/flowmanager/scoring/wiki, capture/meeting/preprocessing, admin, webhooks, telegram, V2 worker scaffolding, evaluation).
  - Constat de couverture Doctor : `forbidden_endpoints_absent` couvre seulement `POST /agents/run`, `POST /runtime/execute`, `POST /memory/promote/auto` ; les routes réelles legacy (`POST /agent/run` sans `s`, `POST /orchestra/*`) passent à travers. Recommandation d'extension du Doctor hors scope de cette PR.
- `ai_logs/2026-05-11-legacy-runtime-audit.md` (cette entrée)

## Files Touched

- reports/code_audit/2026-05-11-legacy-runtime-audit.md
- ai_logs/2026-05-11-legacy-runtime-audit.md

## Critical files impacted

- aucun (audit lecture seule ; pas de modification de `platform/api/`, `core/`, `docs/governance/`, `modules.yaml`, `plugins.yaml`, `docker-compose.yml`, `operations/doctor.py`, `operations/doctor.md`, `schemas/`, `tests/`)

## Tests

Aucun test lancé. Audit lecture seule sans exécution. Le Doctor reste à 13 PASS / 0 WARN / 0 FAIL sur main (vérifié au début du Bloc 6 sur la branche fraîche, pas relancé puisque rien n'a changé en code).

## Open points

- Le rapport identifie une violation doctrinale active (`apps/orchestra/` = LangGraph central) qui n'était pas explicitement inscrite dans `CODE_AUDIT_POST_PIVOT.md §3`. Conformément au brief Bloc 6 ("Ne rien supprimer. Ne rien déplacer. Ne rien refactorer."), aucune action corrective n'est appliquée ici ; le rapport propose les actions de suivi.
- Couverture Doctor `forbidden_endpoints_absent` insuffisante par rapport aux routes réelles legacy ; à corriger en PR `feat:` distincte (C3).
- La classification des tests §4.11 est non exhaustive (10 entrées sur ~20). Suffisante pour cibler les fichiers à marquer `legacy_runtime` dans un futur passage de marqueurs pytest.
- `scope=agence` dans `apps/memory/router.py` reproduit la terminologie interdite `agency` (MEMORY_EVENT_SCHEMA.md §2). À renommer en `system` dans une PR `refactor:` séparée.

## Next action

- Ouvrir une PR `docs:` (C3) pour ajouter les lignes manquantes à `CODE_AUDIT_POST_PIVOT.md §3` (orchestra, V2 worker scaffolding, 8 apps MVP business, etc.).
- Une fois cette PR Bloc 6 mergée, ouvrir Bloc 7 (`work/claude/openwebui-hermes-specs`) : specs OpenWebUI / Hermes sans activation.
- Optionnellement, ouvrir une PR `feat:` (C3) qui étend `FORBIDDEN_ENDPOINTS` dans `operations/doctor.py` pour couvrir `/agent/run` et `/orchestra/*` une fois l'audit officialisé.
