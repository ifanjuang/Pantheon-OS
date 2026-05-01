# AI LOG ENTRY — 2026-04-29

Branch: `claude/audit-repository-EnYEU`

A: Claude (Opus 4.7)

## Objective

Run a full repository audit, fix critical inconsistencies, archive legacy code, reconcile documentation with reality, and unify the AI coordination journal under a single convention.

## Changes

Seven commits pushed on `claude/audit-repository-EnYEU`:

1. **`d9e3e03` — fix: reconnect approval migration and scope domains to MVP**
   - `alembic/versions/20260426_0001_add_approval_requests.py` : `down_revision = None` → `"0028"` (resolves the detached-head known issue).
   - `config/domains.yaml` : drop `legal_fr` / `medical_fr` (no overlay folders), add `general` as base layer.
   - `config/policies.yaml` : drop `legal_fr` / `medical_fr` `trusted_sources`, comment narrowed to MVP scope.
   - `platform/api/pantheon_runtime/router.py` : drop orphan `domains/software` from context-pack.

2. **`fc7ebb1` — chore: archive legacy modules and obsolete docs**
   - Move to `legacy/` : `apps/control/`, `apps/monitoring/`, `benchmarks/`, `INSTALL.md`.
   - Convention : `legacy/` never imported by the runtime (see `legacy/README.md`).
   - `modules.yaml` : drop `control` and `monitoring` entries.
   - `pyproject.toml` Ruff exclude switched from `benchmarks/` to `legacy/`.
   - **Kept active despite initial flag** : `apps/evaluation/` (used by `.github/workflows/ci.yml`), `operations/openwebui_hermes_pantheon.md` (referenced by 5+ docs and 1 skill), `approvals` / `flowmanager` / `openai_compat` (V2 in active prep or MVP minimal).

3. **`3f34fb3` — docs(claude): align CLAUDE.md with current repo structure**
   - Drop the inexistent `modules/` wrapper.
   - Pantheon count : 22 → 24, add `@CHRONOS` and `@Dionysos` to Extended agents.
   - Domains : `architecture/legal/medical` → `architecture_fr` (active) + `general` (base).
   - 27 FastAPI apps acknowledged, 6 config files, table Alembic refreshed.

4. **`9e7923b` — docs(governance): move 15 governance docs to docs/governance/**
   - Pulled AGENTS, AI_LOG, APPROVALS, ARCHITECTURE, EVIDENCE_PACK, EXTERNAL_TOOLS_POLICY, EXTERNAL_WATCHLIST, HERMES_INTEGRATION, KNOWLEDGE_TAXONOMY, MEMORY, MODULES, ROADMAP, STATUS, TASK_CONTRACTS, VERSIONS out of the repo root.
   - Stayed at root : README.md, CLAUDE.md, CHANGELOG.md, VERSION.
   - Updated references : `pantheon_runtime/router.py` truth_files, 2 skill manifests, CLAUDE.md tree.

5. **`c02dc1f` — chore: refresh changelog, declare PEP 621 metadata, fix Dockerfile**
   - `pyproject.toml` : add `[project]` section with explicit deps copied from `platform/api/requirements.txt`.
   - `platform/infra/docker/api/Dockerfile` : replace `COPY modules/` (path no longer exists) with `COPY agents/ skills/ tools/ workflows/`. **Unblocks API image build.**
   - `CHANGELOG.md` : populate `[Unreleased]`.

6. **`2e11272` — Merge remote-tracking branch 'origin/main'**
   - Auto-resolved : main's `TASK_CONTRACTS.md` mods applied onto `docs/governance/TASK_CONTRACTS.md` (rename followed by Git's `ort` strategy), main's new `ai_logs/2026-04-29-external-tools-governance.md` integrated as-is. No manual conflict resolution required.

7. **`fbf96d7` — docs(ai-logs): unify AI_LOG.md into ai_logs/ folder convention**
   - Two competing journal formats reconciled around `ai_logs/`.
   - `ai_logs/README.md` : rules, critical files, branch conventions, entry template.
   - `ai_logs/0000-historical-archive.md` : 10 historical entries preserved (git rename).
   - `docs/governance/AI_LOG.md` removed.
   - Reference updates : router.py truth_files, 2 Hermes templates, operations doc (3 occurrences), 5 governance docs, CLAUDE.md, CHANGELOG.

## Files Touched

- Migrations : `alembic/versions/20260426_0001_add_approval_requests.py`.
- Config : `config/domains.yaml`, `config/policies.yaml`, `modules.yaml`, `pyproject.toml`.
- Runtime : `platform/api/pantheon_runtime/router.py`.
- Build : `platform/infra/docker/api/Dockerfile`.
- Docs root : `CLAUDE.md`, `CHANGELOG.md`.
- Docs governance (moves + content updates) : 15 files into `docs/governance/`, plus `docs/governance/README.md` (new).
- AI logs (new convention) : `ai_logs/README.md` (new), `ai_logs/0000-historical-archive.md` (rename + header).
- Hermes templates : `hermes/templates/pantheon-os/SKILL.md`, `examples/audit_repo.md`.
- Operations : `operations/openwebui_hermes_pantheon.md`.
- Skill manifests : `domains/general/skills/{adaptive_orchestration,project_context_resolution}/manifest.yaml`.
- Legacy moves : `apps/control/*`, `apps/monitoring/*`, `benchmarks/*`, `INSTALL.md`.
- Legacy README : `legacy/README.md` (new).

## Critical files impacted

- `modules.yaml`, `pyproject.toml`, `platform/api/main.py` (indirectly via Dockerfile fix).
- `alembic/versions/*` (one revision relinked).
- All governance Markdown sources of truth (relocated, not modified in content).
- `platform/api/pantheon_runtime/router.py` (truth_files structure).

## Tests

- Not executed. Validations limited to :
  - `python3 -m py_compile` on edited Python files (OK).
  - `python3 -c "import yaml; yaml.safe_load(...)"` on edited YAML files (OK).
  - `python3 -c "import tomllib; tomllib.load(...)"` on `pyproject.toml` (OK).
  - `grep` sweeps to confirm zero residual references to moved/removed items.
- The CI pipeline (`.github/workflows/ci.yml`) was preserved : `apps/evaluation/` was deliberately not archived because it is invoked there.

## Open points

- `alembic upgrade head` not run on a real DB ; the chain is logically connected (0001→…→0028→20260426_0001) but should be applied locally before activating `approvals`.
- Test coverage of the platform remains at ~16 %. Several V2 apps (decisions, scoring, finance, planning, wiki, chantier, communications) carry 600-1300 LOC each without any test.
- `apps/openai_compat` is MVP-enabled but stub-like (296 LOC, no service/models layer). Critical for OpenWebUI integration — deserves a dedicated review.
- `apps/admin` and `apps/agent` are the two largest MVP modules (1411 and 1620 LOC) and do not follow the standard `models / schemas / service / router` pattern.
- `README.md` was not audited in this session.
- `pyproject.toml` deps now duplicate `platform/api/requirements.txt`. Source of truth for the Docker build remains the requirements file ; consider migrating to a single source via `dynamic = ["dependencies"]` in a later iteration.

## Next action

1. Run `alembic upgrade head` on a test database to confirm the relinked migration applies cleanly.
2. Merge the PR for `claude/audit-repository-EnYEU` into `main` (no conflicts remaining).
3. Optionally activate `approvals` (`enabled: true` in `modules.yaml`) once the migration is verified and a test is in place.
4. Schedule a separate pass on `apps/openai_compat` and on test coverage for V2 modules.
