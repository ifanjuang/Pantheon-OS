# SECURITY AUDIT — Pantheon Next (public repo)

> Read-only diagnostic audit of the public `ifanjuang/Pantheon-OS` repository.
> Documentation only. No code change, no credential rotation, no
> infrastructure mutation performed by this audit.

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

Status: **Documented / not runtime**. Approval level: **C0 (read /
diagnostic)** for the audit itself; remediation actions reference
their own approval levels.

Audit date: 2026-05-03.
Auditor: Claude Code on branch `work/claude/security-audit-public-repo`.
Base commit at audit time: `9001ccf` (post merge of PR #93 lint fix).

---

## 1. Scope and method

### 1.1 In scope

- full git history of the default branch and every reachable ref;
- working-tree configuration files: `.env.example`,
  `docker-compose.yml`, `.gitignore`, `.github/workflows/ci.yml`,
  `modules.yaml`, `config/*.yaml`, `.claude/settings.json`;
- Python source under `platform/`;
- Frontend under `platform/ui/`;
- Operations under `operations/`, `scripts/`;
- Migrations under `alembic/`;
- presence / absence of standard public-OSS governance files
  (`LICENSE`, `SECURITY.md`, `CODEOWNERS`).

### 1.2 Out of scope

- third-party dependency CVE deep dive (delegated to GitHub
  Dependabot once enabled — see §6);
- runtime penetration testing of any deployed instance;
- review of private deployments (NAS, Portainer, OpenWebUI live
  config) — those are not in this repository;
- rotation of any allegedly leaked credential;
- modification of GitHub repository settings (rulesets, secret
  scanning, branch protection) — those are explicit user actions
  recommended in §6.

### 1.3 Method

| Step | Tool | Result |
|---|---|---|
| Full-history secret scan | `gitleaks 8.21.2 --redact` over 245 commits | **0 leaks** |
| Tracked-file pattern scan | `grep` for hardcoded API keys, bearer tokens, passwords | **0 hits in code** |
| Internal URL / NAS path scan | `grep` for private IPs, NAS volume paths, internal hostnames | placeholders only (`192.168.x.x` shown as example URLs) |
| Personal data scan | `grep` for SIRET, SIREN, IBAN, French phone, RCS, real emails | **0 hits** |
| Filename-based history scan | `git log --all --diff-filter=A` for `*.env`, `*.pem`, `*.key`, `id_rsa`, `secret*`, `password*`, `credential*`, `token*` | **0 sensitive filenames ever committed** |
| `.env` ever committed | `git log --all -- '*.env'` (excluding `.example`) | **never** |
| Production guard in code | review of `platform/api/core/settings.py` | **present** — rejects weak `JWT_SECRET_KEY` / `ADMIN_PASSWORD` and `< 32` char keys when `DEBUG=false` |

The audit was conducted with redacted reporting: gitleaks ran with
`--redact` so any matched value would be masked; no real secret value
appears in this report.

---

## 2. Summary

```text
History scan:           CLEAN (0 leaks across 245 commits)
Working-tree code scan: CLEAN (no hardcoded secrets)
Personal data scan:     CLEAN (no real names, emails, IDs, IBAN, SIRET, RCS)
Real client/project:    CLEAN (no real engagement data)
Author privacy:         CLEAN (commits via GitHub noreply email)
Production guard:       PRESENT (settings.py rejects weak prod secrets)
```

No critical (C5) or high-risk (C4-only) leak found in the source or
its history.

The findings below are **defensive hygiene** items that strengthen a
public-repo posture but do not indicate any active compromise.

---

## 3. Findings

Severity legend — operational risk that this finding adds to the
public-repo posture:

| Sev | Meaning |
|---|---|
| INFO | informational, no action required |
| LOW | minor hygiene improvement |
| MEDIUM | meaningful exposure if misconfigured downstream |
| HIGH | meaningful exposure if reused as-is in production |
| CRITICAL | active compromise / immediate action |

| # | Sev | Title | Location | Approval to remediate |
|---|---|---|---|---|
| 1 | HIGH | Secret reuse in legacy compose: `JWT_SECRET_KEY` is consumed as `OPENAI_API_KEY` and `WEBUI_SECRET_KEY` for OpenWebUI | `docker-compose.yml:80–84` | C3 (file change in legacy MVP wiring) |
| 2 | MEDIUM | Postgres exposed on host without `127.0.0.1:` bind | `docker-compose.yml:38` | C3 |
| 3 | MEDIUM | Ollama exposed on host without auth | `docker-compose.yml:100` | C3 |
| 4 | MEDIUM | OpenWebUI exposed on host without reverse proxy | `docker-compose.yml:88` | C3 |
| 5 | MEDIUM | Adminer (DB UI) reachable on `:8080` (dev profile only) | `docker-compose.yml:115` | C3 |
| 6 | LOW | `adminer` Docker image unpinned (`image: adminer`) | `docker-compose.yml:113` | C3 |
| 7 | LOW | `OPENAI_API_KEY=sk-...` placeholder uses recognizable prefix bots scrape for | `.env.example:22` | C3 |
| 8 | LOW | `DEBUG=true` is the default; production guard mitigates but env discipline matters | `.env.example:31`, `platform/api/core/settings.py:40` | C3 (deployment doc clarification) |
| 9 | MEDIUM | No `LICENSE` file at repo root | repo root | C3 (governance addition) |
| 10 | MEDIUM | No `SECURITY.md` policy at repo root or `.github/` | repo root / `.github/` | C3 |
| 11 | MEDIUM | No `CODEOWNERS` file | `.github/CODEOWNERS` | C3 |
| 12 | HIGH | No branch protection / ruleset on `main` (verified separately earlier in session) | GitHub repo settings | C4 (external/admin action) |
| 13 | UNKNOWN | GitHub secret scanning enabled? | GitHub repo settings | C4 |
| 14 | UNKNOWN | Dependabot alerts / security updates enabled? | GitHub repo settings | C4 |
| 15 | INFO | Forks may carry historical state — moot here since gitleaks history scan is clean | — | — |

### 3.1 Detail — Finding #1 (HIGH): secret reuse in `docker-compose.yml`

`docker-compose.yml` injects the same env value `${JWT_SECRET_KEY}`
into three different roles for the OpenWebUI service:

```yaml
openwebui:
  environment:
    OPENAI_API_KEY: ${JWT_SECRET_KEY}        # role 1: API key for /v1 backend
    WEBUI_SECRET_KEY: ${JWT_SECRET_KEY}      # role 2: OpenWebUI session/cookie secret
```

The same value also signs application JWTs (role 3: `JWT_SECRET_KEY`).

Why it matters: a single leak of `JWT_SECRET_KEY` compromises three
trust domains at once. JWT signing, OpenWebUI session integrity, and
the model-backend authorization header all collapse to one token.

This is legacy MVP wiring (already classified `legacy` in
`docs/governance/CODE_AUDIT_POST_PIVOT.md` §3 row "Docker Compose",
and the compose file itself states it is not the final target). The
target architecture (`OpenWebUI → Hermes Agent Gateway → Pantheon`)
does not have this anti-pattern.

Recommendation (no fix applied here):

- introduce three distinct env vars: `JWT_SECRET_KEY`,
  `WEBUI_SECRET_KEY`, `HERMES_API_KEY`;
- rotate any production deployment that reused the values;
- add the new vars to `.env.example` with the existing `changeme`
  placeholder pattern.

### 3.2 Detail — Findings #2 to #5 (MEDIUM): exposed ports

The compose file binds without a localhost restriction:

```text
db        → 5432:5432   (Postgres + pgvector, full DB access)
api       → 8000:8000   (FastAPI Pantheon Domain API + legacy MVP)
openwebui → 3000:8080   (chat / Knowledge UI)
ollama    → 11434:11434 (LLM API, no auth by default)
adminer   → 8080:8080   (DB admin UI, dev profile only)
```

If the Docker host is internet-reachable, these are public. On a LAN
or NAS-only deployment the risk is limited but still meaningful
because Ollama in particular has no authentication and would expose
an open LLM proxy.

Recommendation (no fix applied here):

- bind to `127.0.0.1:` for dev profiles, or place behind an auth-
  enforcing reverse proxy (Caddy, nginx + basic auth, Traefik with
  middleware) for any non-loopback exposure;
- never expose `adminer` outside loopback;
- never expose `ollama` outside loopback unless a sidecar adds auth
  and rate limiting.

The wiring is already classified `legacy` in
`CODE_AUDIT_POST_PIVOT.md`. The right rewrite is the post-pivot
target compose split (Pantheon Domain API / Hermes Gateway /
OpenWebUI bridge / separate DBs).

### 3.3 Detail — Finding #6 (LOW): unpinned image

```yaml
adminer:
  image: adminer
```

No tag means `:latest`, which is unsafe for reproducibility and
supply-chain hygiene. Recommendation: pin to a specific digest or
semver (`adminer:4.8.1` or `adminer@sha256:...`).

### 3.4 Detail — Finding #7 (LOW): recognizable placeholder prefix

```text
.env.example:22   # OPENAI_API_KEY=sk-...
```

`sk-` is the OpenAI key prefix that bots scrape repos for. The
placeholder is harmless on its own but increases the chance someone
copies the file, fills it with a real `sk-…` value, and accidentally
commits it. Recommendation:

```text
# OPENAI_API_KEY=sk-REPLACE_WITH_YOUR_KEY_DO_NOT_COMMIT
```

### 3.5 Detail — Findings #9 to #11: missing public-OSS governance files

| File | Purpose | Why it matters on a public repo |
|---|---|---|
| `LICENSE` | declares reuse rights | without one, default copyright applies — anyone can read but cannot legally reuse |
| `SECURITY.md` | declares vulnerability disclosure path | gives a defined channel for responsible disclosure; expected by GitHub / Google's OSS scorecard |
| `.github/CODEOWNERS` | auto-request reviews on critical paths | makes review routing explicit; complements branch protection |

These are governance gaps, not active risks.

### 3.6 Detail — Finding #12 (HIGH): no branch protection on `main`

Verified earlier in session: the GitHub UI shows "Classic branch
protections have not been configured". A direct push (or a force
push, or a deletion) of `main` is currently not blocked at the
platform level.

The Pantheon Next AI-agent doctrine relies on convention
(`work/<agent>/...` branches + AI logs), which is a strong soft
control but not a hard one. Adding a Ruleset that requires PRs and
blocks force-push / deletion on `main` closes that gap.

This is an admin / external action (C4). Concrete proposal sits in
the earlier branch-protection discussion of this session; can be
re-issued as a self-contained ruleset JSON if requested.

### 3.7 Detail — Findings #13 and #14 (UNKNOWN): GitHub side checks

The MCP tools available to this session do not expose the Code
security configuration of the repo (secret scanning, push
protection, Dependabot alerts, Dependabot security updates,
Dependabot version updates, code scanning).

Recommendation: verify in GitHub UI under Settings → Code security
and ensure the following are at least "enabled":

- Secret scanning;
- Secret scanning push protection;
- Dependabot alerts;
- Dependabot security updates;
- Code scanning (CodeQL) — optional but useful for the FastAPI
  legacy code under `platform/api/`.

These are all platform-level toggles; no commit needed.

---

## 4. Already-good defenses worth keeping

Listed for completeness — these reduce blast radius and should be
preserved:

| Defense | Location |
|---|---|
| `.gitignore` excludes `.env`, `*.pem`, `*.key`, `secrets/` | `.gitignore:140–214` |
| Production guard rejects weak `JWT_SECRET_KEY`/`ADMIN_PASSWORD` and < 32-char keys when `DEBUG=false` | `platform/api/core/settings.py:76–92` |
| Test secrets in CI are clearly labeled and do not reference `secrets.*` | `.github/workflows/ci.yml:66–80` |
| Author identity in commits uses GitHub noreply email | git log `ifanjuang <…@users.noreply.github.com>` |
| Internal URLs are env-driven, not hardcoded (`settings.TELEGRAM_TOKEN`, `settings.WA_PHONE_ID`) | `platform/api/apps/admin/setup_engine.py`, `platform/api/apps/webhooks/telegram.py` |
| Privacy doctrine forbids real client/project data in repo content | `CLAUDE.md`, `domains/architecture_fr/rules.md`, `knowledge_policy.md`, `output_formats.md`, `templates/README.md`, `hermes/context/*` |
| Skill / workflow lifecycle keeps everything `candidate` until reviewed | `SKILL_LIFECYCLE.md`, `WORKFLOW_SCHEMA.md`, `WORKFLOW_ADAPTATION.md` |
| `EXTERNAL_TOOLS_POLICY.md` and review docs make `blocked` the default for unclassified external tools | `docs/governance/` |
| AI-agent branch convention (`work/<agent>/...` + AI log) yields per-intervention audit | `ai_logs/README.md` |

---

## 5. Recommendations (proposed, not applied)

### 5.1 Repo file additions (C3, separate PRs)

1. Add `LICENSE` (project author chooses the license — typical
   options for a governance-heavy project: Apache-2.0 for code +
   CC-BY-4.0 for docs, or AGPL-3.0 if explicitly intended).
2. Add `SECURITY.md` declaring disclosure channel (private email
   or GitHub security advisory) and supported branches.
3. Add `.github/CODEOWNERS` mapping critical paths to the user's
   GitHub handle to auto-request review.
4. Update `.env.example`: stronger placeholder for the OpenAI key
   line.
5. Update `docker-compose.yml`: split secret roles (`JWT_SECRET_KEY`
   ≠ `WEBUI_SECRET_KEY` ≠ `HERMES_API_KEY`); bind ports to
   `127.0.0.1:` for dev profile; pin `adminer` image; add a comment
   reminding "legacy MVP only".

### 5.2 GitHub admin actions (C4, external)

6. Configure a Ruleset on `main`:
   - require pull request before merging;
   - block force pushes;
   - block deletions;
   - require linear history;
   - approvals: 0 (solo + AI agents) — the PR gate itself enforces
     review;
   - status checks: require `Lint`, `Tests`, `Security audit` once
     the test rename PR turns Tests green.
7. Configure a Ruleset on `work/**`, `claude/**`, `feature/**`:
   - block deletions (preserve AI audit trail);
   - allow force push (agents may rebase their own work);
   - no required PR.
8. Enable Secret scanning + Push protection + Dependabot alerts +
   Dependabot security updates in Settings → Code security.

### 5.3 Doctrine additions (C3, governance)

9. Add an entry to `docs/governance/CODE_AUDIT_POST_PIVOT.md`
   linking back to this audit (already classified `legacy` for the
   compose file; this audit confirms that classification with
   concrete severity).
10. Add a short policy in `docs/governance/EXTERNAL_TOOLS_POLICY.md`
    or `EVIDENCE_PACK.md` requiring a per-PR `gitleaks` check before
    any merge that touches `.env*`, `docker-compose*.yml`,
    `.github/workflows/*.yml` or `platform/api/core/settings.py`.

---

## 6. Verification checklist for the user

Once §5.2 is acted upon, the following commands should produce the
documented evidence:

```text
# Branch protection in place
gh api repos/ifanjuang/Pantheon-OS/rulesets

# Secret scanning enabled
GitHub UI → Settings → Code security → Secret scanning: ON
GitHub UI → Settings → Code security → Push protection:  ON

# Dependabot enabled
GitHub UI → Settings → Code security → Dependabot alerts: ON
GitHub UI → Settings → Code security → Dependabot security updates: ON

# CODEOWNERS effective
open a draft PR touching docs/governance/ and verify auto-request
of @ifanjuang appears
```

No automated remediation is suggested for the GitHub-side items —
they are platform actions and must be performed by the repo owner.

---

## 7. Reproducibility

The audit can be re-run by anyone with read access:

```bash
# Install gitleaks (pinned version)
curl -fsSL https://github.com/gitleaks/gitleaks/releases/download/v8.21.2/gitleaks_8.21.2_linux_x64.tar.gz \
  | tar -xz -C /tmp gitleaks

# Run history scan with redacted output
/tmp/gitleaks detect --source . --no-banner --no-color \
  --report-format json --report-path /tmp/gitleaks-report.json --redact

# Working-tree pattern scans (see commit message for full set)
grep -rEn '(api[_-]?key|secret|token|password|bearer)\s*[=:]\s*["\047][a-zA-Z0-9_\-]{15,}["\047]' \
  --include='*.py' --include='*.yml' --include='*.yaml' --include='*.json' \
  platform/ scripts/ config/

# History filename scan
git log --all --diff-filter=A --name-only --pretty=format: \
  | grep -iE '(secret|password|credential|token|\.pem|\.key|\.p12|\.pfx|id_(rsa|dsa|ecdsa|ed25519))$'
```

---

## 8. Final rule

```text
A public repo is read by everyone forever.
A clean history today does not eliminate the cost of one bad commit tomorrow.
Branch protection, secret scanning and explicit doctrine reduce that cost.
The fixes here are governance and hygiene, not panic.
```
