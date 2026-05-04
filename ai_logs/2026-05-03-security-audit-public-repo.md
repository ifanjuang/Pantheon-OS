# AI LOG ENTRY — 2026-05-03

Branch: `work/claude/security-audit-public-repo`

A: Claude Code

## Objective

Read-only diagnostic security audit of the public repository
`ifanjuang/Pantheon-OS`. Documentation only. No code change, no
credential rotation, no infrastructure mutation. Approval level: C0
(read / diagnostic).

## Operating context

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

The audit was prompted by a user concern about safety on a public
repo. The deliverable is a single reference document under
`docs/governance/SECURITY_AUDIT.md` plus this AI log.

## Coordination check

- `git fetch --all --prune` done before work.
- ChatGPT branches in flight at audit time:
  `work/chatgpt/execution-discipline-ai-options`,
  `work/chatgpt/strengthen-doctor-checklist`,
  `work/chatgpt/sync-architecture-fr-status-roadmap` (merged during
  the session as PR #104),
  `work/chatgpt/task-contract-revision-doctrine`. None touch the
  audit scope.
- PR #93 (CI lint repair) merged during this audit; branch was
  rebased on the new `main` (`9001ccf`) and inherits the green Lint
  baseline.
- No collision with any other in-flight work.

## Scope

In scope:

- full git history (all reachable refs);
- working-tree config: `.env.example`, `docker-compose.yml`,
  `.gitignore`, `.github/workflows/ci.yml`, `modules.yaml`,
  `config/*.yaml`, `.claude/settings.json`;
- Python under `platform/`;
- Frontend under `platform/ui/`;
- Operations / scripts / migrations;
- Presence of standard public-OSS files (`LICENSE`, `SECURITY.md`,
  `CODEOWNERS`).

Out of scope (explicit):

- third-party dependency CVEs (delegated to Dependabot);
- runtime pen-testing of any deployed instance;
- private deployments (NAS / Portainer / OpenWebUI live config);
- credential rotation;
- modifications to GitHub repo settings (rulesets, secret scanning).

## Method

| Step | Tool / command | Result |
|---|---|---|
| Full-history secret scan | `gitleaks 8.21.2 detect --redact` | 0 leaks across 245 commits |
| Tracked-file pattern scan | `grep` for hardcoded API keys, bearer tokens, passwords | 0 hits in code |
| Internal URL / NAS path scan | `grep` for private IPs, NAS volume paths, internal hostnames | placeholders only |
| Personal data scan | `grep` for SIRET, SIREN, IBAN, French phone, RCS, real emails | 0 hits |
| Filename-based history scan | `git log --all --diff-filter=A` for `*.env`, `*.pem`, `*.key`, `id_*`, `secret*`, `password*`, `credential*`, `token*` | 0 sensitive filenames ever committed |
| `.env` ever committed | `git log --all -- '*.env'` excluding `.example` | never |
| Production guard | review of `platform/api/core/settings.py:76–92` | present, rejects weak `JWT_SECRET_KEY` / `ADMIN_PASSWORD` and `< 32` char keys when `DEBUG=false` |

The audit ran with `--redact` so no secret value appears in any
artifact, including this log.

## Summary

```text
History scan:           CLEAN (0 leaks across 245 commits)
Working-tree code scan: CLEAN (no hardcoded secrets)
Personal data scan:     CLEAN (no real names, emails, IDs, IBAN, SIRET, RCS)
Real client/project:    CLEAN (no real engagement data)
Author privacy:         CLEAN (commits via GitHub noreply email)
Production guard:       PRESENT (settings.py rejects weak prod secrets)
```

No critical / high-confidence leak found. The 15 findings are
**defensive hygiene** items (2 HIGH, 7 MEDIUM, 3 LOW, 2 UNKNOWN, 1 INFO).
The 7 MEDIUM rows split into 4 compose-port bindings and 3 missing
OSS-governance files (`LICENSE`, `SECURITY.md`, `CODEOWNERS`).

## Findings

The 15 findings are listed in `docs/governance/SECURITY_AUDIT.md` §3
with severity, location and remediation approval level. Highlights:

1. **HIGH** — `docker-compose.yml:80–84`: `JWT_SECRET_KEY` reused as
   `OPENAI_API_KEY` and `WEBUI_SECRET_KEY` for OpenWebUI. One leak
   compromises three trust domains. Already classified `legacy` in
   `CODE_AUDIT_POST_PIVOT.md`. Recommended split into distinct env
   vars; no fix applied.
2. **MEDIUM** — `docker-compose.yml`: Postgres / Ollama / OpenWebUI
   / Adminer ports bound without `127.0.0.1:` prefix. Ollama in
   particular has no auth by default and would be an open LLM proxy
   if the host is internet-reachable.
3. **MEDIUM** — No `LICENSE`, no `SECURITY.md`, no `CODEOWNERS`.
4. **HIGH** — No branch protection / ruleset on `main` (verified
   earlier in session via the GitHub UI banner). Soft control by AI
   convention is not a hard control.
5. **UNKNOWN** — GitHub Secret scanning + Push protection +
   Dependabot status: not exposed via the MCP tools available to
   this session. User-action items.

## Already-good defenses preserved

- `.gitignore` excludes `.env`, `*.pem`, `*.key`, `secrets/`.
- Production guard in `platform/api/core/settings.py:76–92`.
- Test secrets in `.github/workflows/ci.yml` clearly labelled
  `test-…`.
- Internal URLs are env-driven (`settings.TELEGRAM_TOKEN`,
  `settings.WA_PHONE_ID`).
- Privacy doctrine in `CLAUDE.md`,
  `domains/architecture_fr/rules.md`, `knowledge_policy.md`,
  `output_formats.md`, `templates/README.md`, `hermes/context/*`
  forbids real client/project data.
- AI-agent branch convention + AI logs give per-intervention audit.

## Recommendations (proposed, not applied)

Listed in `docs/governance/SECURITY_AUDIT.md` §5:

- C3 (separate PRs): add `LICENSE`, `SECURITY.md`,
  `.github/CODEOWNERS`; harden `.env.example` placeholder; split
  compose secrets and bind dev ports to loopback; pin `adminer`
  image.
- C4 (admin actions, external to this PR): configure rulesets on
  `main` and `work/**`/`claude/**`/`feature/**`; enable Secret
  scanning + Push protection + Dependabot alerts + security
  updates.
- C3 governance: cross-link the audit from
  `CODE_AUDIT_POST_PIVOT.md`; add a `gitleaks` requirement in
  `EXTERNAL_TOOLS_POLICY.md` or `EVIDENCE_PACK.md` for PRs that
  touch `.env*`, `docker-compose*.yml`, `.github/workflows/*.yml` or
  `platform/api/core/settings.py`.

## Changes

| File | Status | Summary |
|---|---|---|
| `docs/governance/SECURITY_AUDIT.md` | new | Reference audit document. Sections: scope and method, summary, 14 findings, defenses preserved, recommendations, verification checklist, reproducibility commands, final rule. Severity legend: INFO / LOW / MEDIUM / HIGH / CRITICAL |
| `ai_logs/2026-05-03-security-audit-public-repo.md` | new | This log |

No other file is modified. No fix is applied. No code, no
endpoint, no script, no automation, no credential touched.

## Files Touched

- `docs/governance/SECURITY_AUDIT.md`
- `ai_logs/2026-05-03-security-audit-public-repo.md`

## Critical files impacted

- none — this PR adds a new governance doc and an AI log entry.

## Tests

- `gitleaks 8.21.2 detect --redact` on full history: 0 leaks /
  245 commits scanned in 1.45s.
- `grep`-based pattern scans: 0 hits.
- Other tests not run. Documentation only.

## Validation

- Read `ai_logs/README.md`.
- Read `docs/governance/STATUS.md` (no modification).
- Read existing classifications in
  `docs/governance/CODE_AUDIT_POST_PIVOT.md` to align this audit's
  severity statements with the existing legacy posture.
- `.gitignore` fully read; covers `.env`, `*.pem`, `*.key`,
  `secrets/`.
- `docker-compose.yml` fully read.
- `.env.example` fully read.
- `.github/workflows/ci.yml` already reviewed earlier in session.
- `platform/api/core/settings.py` fully read.
- `platform/api/apps/admin/setup_engine.py` and
  `platform/api/apps/webhooks/telegram.py` reviewed for token
  handling.
- `platform/ui/` scanned for client-side leaks: clean.
- `config/*.yaml` scanned: clean.
- `.claude/settings.json` reviewed: only Bash allowlist for
  docker/git, no secrets.
- `legacy/` content listed (`INSTALL.md`, `README.md`, `apps/`,
  `benchmarks/`); not opened — out of audit scope (already
  classified `archive` in `CODE_AUDIT_POST_PIVOT.md`).
- No real client / project / address / chantier / personal /
  budget data introduced into the report.
- Redacted output mode used everywhere a value could leak.
- No code, no endpoint, no script, no automation, no credential
  rotation.
- No autonomous runtime path reactivated.

## Doctrine alignment

- C0 (read / diagnostic) for the audit itself.
- Each finding's remediation references its own approval level
  (mostly C3 for repo-side fixes, C4 for GitHub-side admin
  actions).
- Pantheon Next governs; remediation does not happen here.
- Privacy by default respected throughout the report.
- Cross-references to `APPROVALS.md`, `EVIDENCE_PACK.md`,
  `CODE_AUDIT_POST_PIVOT.md` and `EXTERNAL_TOOLS_POLICY.md`
  preserved.

## Open points

- **Branch protection (Finding #12)**: requires a GitHub admin
  action by the repo owner. Cannot be fixed by this PR.
- **GitHub-side security toggles (Findings #13, #14)**: not
  introspectable through the MCP tools available in this session;
  must be verified in the GitHub UI under Settings → Code security.
- **`LICENSE` choice (Finding #9)**: needs a deliberate choice by
  the project author (e.g. Apache-2.0 + CC-BY-4.0, or AGPL-3.0)
  before a PR can land it.
- **`SECURITY.md` channel (Finding #10)**: needs a disclosure
  channel decision (private email vs GitHub security advisory).
- **Compose split (Finding #1, #2-#5)**: legacy MVP wiring already
  classified `legacy`. The right rewrite is the post-pivot target
  compose split (Pantheon Domain API / Hermes Gateway / OpenWebUI
  bridge / separate DBs). Not in this PR's scope.

## Next action

- Open PR `work/claude/security-audit-public-repo → main` for
  review and merge of the audit document.
- After merge, schedule three follow-up PRs (one each, scope-tight):
  - `work/<agent>/add-license-and-security-md`,
  - `work/<agent>/harden-env-example-and-compose-loopback`,
  - `work/<agent>/codeowners-and-gitleaks-policy`.
- Schedule one user-action ticket for §5.2 (rulesets + Secret
  scanning + Dependabot).
