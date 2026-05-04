# AI LOG ENTRY — 2026-05-04

Branch: `work/chatgpt/model-routing-ui-policy`

A: ChatGPT

## Objective

Document compute-node/model-routing policy for a future local admin UI and classify recent Hermes UI, memory, search, skill and self-evolution options.

## Changes

- Added `config/compute_nodes.example.yaml`.
- Reworked `config/model_routing.example.yaml` around compute nodes, model registry and role routing.
- Extended `docs/governance/MODEL_ROUTING_POLICY.md` with multi-compute-node mode, compute node registry and future UI boundary.
- Added `operations/model_routing_ui.md` as a future local/admin UI specification.
- Added `docs/governance/EXTERNAL_HERMES_UI_OPTION_REVIEWS.md`.
- Indexed `EXTERNAL_HERMES_UI_OPTION_REVIEWS.md` in `docs/governance/README.md`.

## External options classified

- Hermes Dashboard: `local_admin_only`.
- `nesquena/hermes-webui`: `hermes_ui_lab_candidate`.
- `outsourc-e/hermes-workspace`: `lab_ui_candidate`.
- `joeynyc/hermes-hudui`: `monitor_only_lab`.
- `NousResearch/hermes-agent-self-evolution`: `blocked_for_core`.
- `ksimback/hermes-ecosystem`: `reference_catalog_only`.
- `AxDSan/mnemosyne`: `watch_test_only` / `rejected_for_core_memory`.
- `OnlyTerp/hermes-optimization-guide`: `reference_only`.
- `HuangYuChuh/ComfyUI_Skills_OpenClaw`: `creative_skill_lab_candidate`.
- `Agents365-ai/drawio-skill`: `diagram_skill_candidate`.
- `AMAP-ML/SkillClaw`: `blocked_for_core`.
- `robbyczgw-cla/hermes-web-search-plus`: `search_plugin_candidate`.

## Files Touched

- `config/compute_nodes.example.yaml`
- `config/model_routing.example.yaml`
- `docs/governance/MODEL_ROUTING_POLICY.md`
- `operations/model_routing_ui.md`
- `docs/governance/EXTERNAL_HERMES_UI_OPTION_REVIEWS.md`
- `docs/governance/README.md`
- `ai_logs/2026-05-04-model-routing-ui-and-hermes-options.md`

## Critical files impacted

- `docs/governance/MODEL_ROUTING_POLICY.md`

## Tests

- Not run. Documentation/config-example only.

## Guardrails

- No code changed.
- No runtime behavior changed.
- No endpoint added.
- No dependency added.
- No UI implementation added.
- No Docker/Portainer stack added.
- No Hermes plugin installed.
- No OpenWebUI mutation.
- No model installation.
- No LAN scanning.
- No secret added.
- No memory promotion.
- No skill activation.
- No workflow canonization.
- No private project/client data added.

## Open points

- Decide later whether to build a minimal local/admin model-routing UI.
- Keep `compute_nodes.local.yaml` and `model_routing.local.yaml` local and uncommitted if they contain real LAN IPs or machine names.
- If Hermes WebUI or Hermes Workspace is tested, use a separate lab stack with read-only repo mount first.
- Mnemosyne may be tested only as Hermes local memory sandbox; it must not become Pantheon Memory.
- Self-evolution tools remain blocked for core.

## Next action

- Review and merge PR.
- Then run a read-only Doctor report on main before any runtime installation or UI implementation.
