# Hermes Context Pack — Verification spec (no activation)

> Read-only verification checklist for the Pantheon `GET /runtime/context-pack`
> endpoint consumed by Hermes Agent. No runtime is started. No Hermes skill is
> installed. No mutation.

Date: 2026-05-11
Status: **verification spec only**

---

## 1. Doctrine boundary

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

Hermes Agent consumes the Pantheon Context Pack as a static orientation pack.
The Context Pack is read-only; it carries no execution authority. This spec
provides a verification procedure that can be run by an operator without
installing Hermes, without enabling any Hermes skill, and without starting any
container.

References:

- `docs/governance/HERMES_INTEGRATION.md` §7 (Runtime Context Pack)
- `docs/governance/HERMES_EXECUTION_MODEL.md`
- `docs/governance/HERMES_CAPABILITY_MAP.md`
- `platform/api/pantheon_context/router.py` (canonical implementation)

Upstream (verified via `raw.githubusercontent.com/NousResearch/hermes-agent`):

> "Hermes Agent ☤ — The self-improving AI agent built by Nous Research."
> Docs: <https://hermes-agent.nousresearch.com/docs/>
> CLI surface: `hermes`, `hermes model`, `hermes tools`, `hermes config set`,
> `hermes gateway`, `hermes setup`, `hermes claw migrate`, `hermes update`,
> `hermes doctor`. Install paths: `~/.hermes` on Linux/macOS,
> `%LOCALAPPDATA%\\hermes` on Windows.

These canonical values come from the upstream README and are cited here so
operators do not invent variables, paths or commands.

## 2. Canonical Pantheon endpoint

Per `HERMES_INTEGRATION.md` §7 (verbatim):

```http
GET /runtime/context-pack
```

The endpoint is implemented in `platform/api/pantheon_context/router.py` and
returns a JSON document with `project`, `mode`, `status`, `doctrine`,
`route_boundary`, `truth_files`, `active_rules`, `domain_packages`,
`memory_levels`, `limitations`.

The endpoint must remain **read-only**. The Doctor check
`forbidden_endpoints_absent` blocks `POST /runtime/execute` and the spec
relies on that boundary.

## 3. Verification procedure (operator, no install)

The procedure is purely static. It uses only `curl` against a running Pantheon
API instance the operator already controls. No Hermes binary is invoked. No
Hermes skill is installed.

### 3.1 Reachability

```bash
curl -sS -o /dev/null -w "%{http_code}\\n" http://localhost:8000/health
```

Expected: `200`.

### 3.2 Context Pack shape

```bash
curl -sS http://localhost:8000/runtime/context-pack
```

The response must contain at minimum:

```json
{
  "project": "Pantheon Next",
  "mode": "hermes_backed_domain_layer",
  "route_boundary": "read_only_context_export_not_execution_runtime",
  "truth_files": ["README.md", "ai_logs/README.md", "docs/governance/STATUS.md", "..."],
  "domain_packages": ["domains/general", "domains/architecture_fr"]
}
```

Verified test coverage: `tests/test_api_smoke.py::test_context_pack_endpoint`.

### 3.3 Boundary checks

For each of these endpoints, the verification must observe **HTTP 200** with a
JSON body that contains the canonical schema declared by the Bloc 5 work
(`platform/api/pantheon_domain/router.py`):

```text
GET /domain/snapshot
GET /domain/agents
GET /domain/skills
GET /domain/workflows
GET /domain/memory
GET /domain/knowledge
GET /domain/legacy
GET /domain/role-signals
GET /domain/role-signal-profiles
GET /domain/routing-foundation
GET /domain/governance-index
```

Verified test coverage: `tests/test_governance_api.py` (PR #142).

### 3.4 Forbidden surfaces

The Pantheon API must continue to reject `POST` requests to:

```text
/agents/run
/runtime/execute
/memory/promote/auto
```

Verified static check: Doctor `forbidden_endpoints_absent`.

Additionally, the audit recorded in `CODE_AUDIT_POST_PIVOT.md` §3 documents
that the legacy surfaces `/agent/run` and `/orchestra/*` remain present by
design during the transition and are flagged `WARN` by Doctor
`legacy_runtime_surfaces_absent` (PR #146). Hermes must not call them.

### 3.5 Hermes Doctor recommendation

The upstream README cites `hermes doctor` as the Hermes-side diagnostic
command. If Hermes is installed locally, an operator may run `hermes doctor`
to inspect Hermes' view of the Context Pack URL. This document does **not**
authorize running `hermes` from Pantheon — it cites the command for parity
with the upstream documentation.

## 4. What this verification does NOT do

- It does **not** install Hermes.
- It does **not** call `hermes` or any Hermes-side command.
- It does **not** start any container or service.
- It does **not** write to disk anywhere except an optional operator-side log.
- It does **not** mutate `docker-compose.yml`, `.env`, `modules.yaml`,
  `plugins.yaml` or any Pantheon governance file.
- It does **not** activate, register or canonize any Hermes skill.
- It does **not** open or expose the Hermes Dashboard.

## 5. Status legend per item

| Item | Status |
|---|---|
| `GET /runtime/context-pack` | **Documenté** + implemented (`platform/api/pantheon_context/router.py`) |
| Verification procedure (this file) | **Documenté** |
| Hermes-side consumption of the Context Pack | **À vérifier** in a live Hermes install, outside this PR |
| `~/.hermes/skills/pantheon-os/` deployment | **Candidate only** — local skill template under `hermes/templates/pantheon-os/` |
| Hermes Dashboard public exposure | **Interdit pour core** |
| `hermes` CLI invocation from Pantheon code | **Interdit pour core** |
| Hermes Function-Calling fine-tune integration | **Non implémenté** — referenced as upstream repo `NousResearch/Hermes-Function-Calling` for context |

## 6. Out of scope

- No new Pantheon endpoint.
- No change to the existing endpoint payload.
- No Hermes skill installation.
- No new doctrine. The doctrine is the one in `HERMES_INTEGRATION.md` and
  `HERMES_EXECUTION_MODEL.md`.

## 7. Verification references

- Repo: `HERMES_INTEGRATION.md` §§3, 6, 7, 8, 9, 10, 11, 12 — boundary, context exports, task flow.
- Repo: `HERMES_EXECUTION_MODEL.md`, `HERMES_CAPABILITY_MAP.md`.
- Repo: `platform/api/pantheon_context/router.py`.
- Repo: `tests/test_api_smoke.py::test_context_pack_endpoint`.
- Repo: `tests/test_governance_api.py` (Bloc 5).
- Doctor: `operations/doctor.py` `forbidden_endpoints_absent` + `legacy_runtime_surfaces_absent` (PR #146).
- Upstream: `NousResearch/hermes-agent` README — CLI commands, install paths, docs URL.
- Upstream: `NousResearch/Hermes-Function-Calling` README — fine-tune function-calling context (not core).

## 8. Final rule

```text
The Context Pack orients Hermes. It does not execute.
Pantheon stays read-only on this surface.
A verification procedure is not an installation.
```
