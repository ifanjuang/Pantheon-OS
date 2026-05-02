# AI LOG ENTRY — 2026-05-02

Branch: `work/claude/ci-repair-diagnostic`

A: Claude Code

## Objective

Diagnose CI failures observed on PR #92 (and inherited from `main`):
Lint and Tests jobs fail on every branch. Apply the safe mechanical
lint fix; document the Tests breakage without applying an architectural
fix.

## Operating context

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

This work belongs to the `software` audit/refactor domain.
Reference: `docs/governance/CODE_AUDIT_POST_PIVOT.md`,
`hermes/context/software_context.md` (PR #92, in flight).

## Coordination check

- `git fetch --all --prune`: done.
- No other branch on `origin/` is currently working on CI repair.
- No collision with `work/chatgpt/knowledge-selection-skill` (touches only
  `domains/general/skills/knowledge_selection/*`).
- `docs/governance/STATUS.md` and `docs/governance/ROADMAP.md` not touched
  (reserved for ChatGPT in-flight work; the new STATUS / ROADMAP entries
  about CI will be added in a follow-up sync PR).
- `docs/governance/CODE_AUDIT_POST_PIVOT.md` was already in scope of this
  domain register and is the natural home for the new section.

## Reproduction

Reproduced both failures locally on a fresh worktree built from
`origin/main` (HEAD `362ad41`).

### Lint

```bash
pip install ruff==0.8.0
ruff check        platform/api/ tests/   # passes
ruff format --check platform/api/ tests/ # 4 files would be reformatted
```

Files flagged:

```text
platform/api/apps/approvals/router.py
platform/api/core/contracts/manifest.py
platform/api/pantheon_domain/repository.py
tests/test_manifest_loader.py
```

The `--diff` output confirms cosmetic-only changes (line-length wraps).
No semantic change.

### Tests

```bash
pip install -r platform/api/requirements.txt --ignore-installed PyYAML
PYTHONPATH=platform/api python -m pytest tests/ --collect-only -q
# 197 tests collected
PYTHONPATH=platform/api python -m pytest tests/ -q --no-cov -x
# Fails on tests/test_guards.py::TestCriticalityGuardHybrid::test_c5_from_rules_skips_ai
# ModuleNotFoundError: No module named 'modules'
```

Searched for stale `modules.*` references:

```bash
grep -rn "^from modules\|^import modules\|modules\." tests/ platform/api/
```

Found `modules.<path>` patch strings across 7 test files. Mapped each
target to the new `apps.<path>` location (all mappings exist in the
current tree, except `apps.capture.service.run_agent` which is imported
**inside** `process_capture()` rather than at module top-level — this
case requires an architectural decision, not a mechanical rename).

Full mapping table is now in
`docs/governance/CODE_AUDIT_POST_PIVOT.md` §10.

## Decision

| Failure | Decision | Reason |
|---|---|---|
| Lint | apply `ruff format` (4 files) | mechanical, safe, no behavior change |
| Tests | document, do **not** patch in this PR | requires per-symbol mapping; one case (`test_capture.py::run_agent`) is architectural |
| Security audit | no action | passing |
| OpenClaw regression | no action | skipped by design on non-main/develop |

The lint patch is C3 (file mutation, candidate patch on a branch). It
preserves the AST: every change is whitespace / newline placement only.

## Changes

- `platform/api/apps/approvals/router.py` — `ruff format` reformat
- `platform/api/core/contracts/manifest.py` — `ruff format` reformat
- `platform/api/pantheon_domain/repository.py` — `ruff format` reformat
- `tests/test_manifest_loader.py` — `ruff format` reformat
- `docs/governance/CODE_AUDIT_POST_PIVOT.md` — new §10 "CI / test
  breakage diagnostic (2026-05-02)" with per-job classification, full
  mapping table for stale `modules.*` test patches, and proposed next
  actions
- `ai_logs/2026-05-02-ci-repair-diagnostic.md` — this log

## Files Touched

- `platform/api/apps/approvals/router.py`
- `platform/api/core/contracts/manifest.py`
- `platform/api/pantheon_domain/repository.py`
- `tests/test_manifest_loader.py`
- `docs/governance/CODE_AUDIT_POST_PIVOT.md`
- `ai_logs/2026-05-02-ci-repair-diagnostic.md`

## Critical files impacted

- `docs/governance/CODE_AUDIT_POST_PIVOT.md` — additive only (new §10).
  No change to existing sections.

## Tests

After applying `ruff format`:

```bash
ruff check        platform/api/ tests/   # All checks passed!
ruff format --check platform/api/ tests/ # 186 files already formatted
```

Lint job will now pass on this branch.

The Tests job will still fail on this branch — the diagnostic explicitly
keeps that out of scope.

## Validation

- Read `ai_logs/README.md`.
- Read `docs/governance/STATUS.md`.
- Read `docs/governance/CODE_AUDIT_POST_PIVOT.md`.
- Read `.github/workflows/ci.yml`.
- Verified each `apps.*` symbol target exists at module level (except
  one `tests/test_capture.py::run_agent` case — recorded as
  architectural).
- Verified `modules.yaml` (the YAML config file at root) is **not**
  affected by the reorg.
- Verified `ruff format` produced no semantic diff (only whitespace).
- No code added.
- No endpoint added.
- No script added.
- No external tool integrated.
- No autonomous runtime path reactivated.
- No private project / client / address / person data introduced.

## Doctrine alignment

- `software` domain rules respected (`hermes/context/software_context.md`):
  patch candidate on a dedicated branch, no direct `main` push, no
  legacy reactivation, AI log entry produced.
- `Detect → document → propose → validate → apply` for the Tests case.
- Lint fix qualifies as a safe C3 candidate patch.
- Tests fix is escalated to a follow-up PR rather than smuggled in.

## Open points

- A follow-up branch (`work/<agent>/ci-tests-modules-rename`) should
  apply the per-symbol rename `modules.<X>.<Y>` → `apps.<X>.<Y>` across
  the 7 test files listed in
  `docs/governance/CODE_AUDIT_POST_PIVOT.md` §10.2, decide the
  architectural target for `tests/test_capture.py::run_agent` (re-bind
  to `apps.agent.service.run_agent` is the most likely answer), and
  re-run pytest under CI services.
- After the Tests fix, the `--cov-fail-under=30` gate may still
  compound. Coverage shortfall is a separate quality concern, not a
  bug.
- `STATUS.md` and `ROADMAP.md` should eventually mention "CI baseline
  partially restored" — left to a sync PR not in scope here.

## Next action

- Open a PR `work/claude/ci-repair-diagnostic → main` for this
  diagnostic + lint patch.
- After merge, open a follow-up branch
  `work/<agent>/ci-tests-modules-rename` for the Tests fix using the
  mapping table in `CODE_AUDIT_POST_PIVOT.md` §10.2.
