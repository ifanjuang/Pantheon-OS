# OpenWebUI Router Pipe — Spec (no activation)

> Specification for routing OpenWebUI user requests to a Hermes Agent Gateway under
> Pantheon Next governance, **without installing any Function, Pipe, Filter or Action**.

Date: 2026-05-11
Status: **draft spec only — not installed, not activated**

---

## 1. Doctrine boundary

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

This spec describes how an OpenWebUI **Pipe** could expose Hermes Agent as a
selectable model entry while keeping Pantheon Next as the only governance
authority. Nothing in this document installs, configures or enables any
OpenWebUI extension. No `docker-compose.yml` mutation, no `.env` mutation, no
Hermes skill activation.

See `docs/governance/OPENWEBUI_PLUGIN_POLICY.md` for the canonical plugin
typology and the security baseline that this spec must not weaken.

## 2. Vocabulary check (verified against upstream)

| Term | Canonical source | Verified excerpt |
|---|---|---|
| Pipe Function | `docs/governance/OPENWEBUI_PLUGIN_POLICY.md` §Pipe | "Pipe Functions can appear as selectable models." |
| Pipelines framework | `https://github.com/open-webui/pipelines/blob/main/README.md` | "Pipelines: UI-Agnostic OpenAI API Plugin Framework" — separate runtime, listens on port 9099 |
| Filter Function | `docs/governance/OPENWEBUI_PLUGIN_POLICY.md` §Filter | "Filter Functions can intercept messages." |
| Action Function | `docs/governance/OPENWEBUI_PLUGIN_POLICY.md` §Action | "Action Functions add buttons to messages." |
| Native function-calling Tool | OpenWebUI README (`open-webui/open-webui` main branch) | "Native Python Function Calling Tool: enhance your LLMs with built-in code editor support in the tools workspace." |

Upstream warning (verbatim from `open-webui/pipelines` README) that the
specification must respect:

```text
Pipelines are a plugin system with arbitrary code execution — don't fetch
random pipelines from sources you don't trust.
```

This warning is the reason `OPENWEBUI_PLUGIN_POLICY.md` requires every
Function / Pipe / Filter / Action / Tool to be reviewed before install.

## 3. Architectural placement (Documenté)

```text
User
 └─ OpenWebUI chat
     └─ OpenWebUI Pipe (Pantheon Router Pipe — spec only)
         ├─ classifies the request (single-role / workflow / Hermes delegation)
         ├─ fetches Pantheon Context Pack         (GET /runtime/context-pack)
         ├─ fetches Pantheon governance snapshot  (GET /domain/snapshot)
         └─ forwards execution to Hermes Gateway only when a Task Contract authorizes it
```

Pantheon must remain reachable only through **read-only** endpoints:

```text
GET /health
GET /runtime/context-pack
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
POST /domain/approval/classify   ← already shipped, classification only, no execution
```

Pantheon must **never** be addressed as an OpenAI-compatible model backend by
OpenWebUI (`OPENWEBUI_INTEGRATION.md` §"OpenWebUI must point to Hermes
Gateway, not Pantheon API").

## 4. Pipe vs Pipelines framework — choice (À vérifier)

Two implementation paths exist upstream:

| Option | Where the code runs | Pros | Cons |
|---|---|---|---|
| Native OpenWebUI Pipe Function | OpenWebUI server process | Simpler install; built-in admin UI; sandboxing per OpenWebUI doctrine | Couples Pantheon routing concerns to OpenWebUI's process |
| `open-webui/pipelines` plugin framework | Separate Pipelines instance (default port `9099`) | Decouples routing; can be restarted independently; supports heavier workloads | Adds a second long-running service; "**arbitrary code execution**" warning applies as-is |

Pantheon Next has **not** decided between the two. **À vérifier** before any
deployment: which fits the OpenWebUI / Hermes Gateway topology best, and what
sandbox / network policies must be in place around the Pipelines instance.

Both options remain **non implémenté** today.

## 5. Required Pantheon governance bindings (Documenté)

Any Pipe — native or Pipelines — must, by design:

| Binding | Source of truth | Required behaviour |
|---|---|---|
| Approval classification | `POST /domain/approval/classify` | Pipe must call it before invoking Hermes for anything beyond C0 read-only |
| Task Contract framing | `TASK_CONTRACTS.md` | Pipe must materialize the request into a Task Contract and refuse to dispatch without one |
| Evidence Pack capture | `EVIDENCE_PACK.md` | Pipe must persist files_read / sources_used / approval_required / next_safe_action; raw chain-of-thought forbidden |
| Role Signal traceability | `ROLE_SIGNALS.md` §10b, `EVIDENCE_PACK.md` §6b | Pipe must surface only public summaries; never leak `raw_chain_of_thought`, `hidden_prompt`, `secret`, `api_key`, `private_key`, `tool_call` |
| Forbidden endpoints | Doctor `forbidden_endpoints_absent` | Pipe must not call `/agents/run`, `/runtime/execute`, `/memory/promote/auto` |
| Legacy surfaces | Doctor `legacy_runtime_surfaces_absent` (PR #146) | Pipe must not call `/agent/run`, `/orchestra/run`, `/orchestra/run-hitl`, `/orchestra/stream`, `/orchestra/runs/{run_id}/approve` |
| Model routing | `MODEL_ROUTING_POLICY.md` | Pipe must respect Pantheon model routing decisions; no silent C4/C5 fallback |
| Approval state | `APPROVALS.md` | C3+ approvals require explicit user validation surfaced as Actions, never silent execution |

## 6. Status legend per item

| Item | Status |
|---|---|
| Pipe spec exists | **Documenté** (this file) |
| Pipe native or Pipelines decision | **À vérifier** |
| Pipe code | **Non implémenté** |
| Pipe install in OpenWebUI | **Interdit pour core** until C3 review + approval |
| Pipe consuming `/agents/run`, `/runtime/execute`, `/memory/promote/auto` | **Interdit pour core** (Doctor `forbidden_endpoints_absent` blocks) |
| Pipe consuming `/agent/run` or `/orchestra/*` | **Interdit pour core** (Doctor `legacy_runtime_surfaces_absent`, PR #146) |
| Pipe wired to Hermes Gateway as OpenAI-compatible URL substitute | **Candidate only** — requires explicit C4 deployment review |

## 7. Out of scope

- No `Function`, `Pipe`, `Filter`, `Action` or `Tool` is installed by this spec.
- No change to `docker-compose.yml`, `.env`, `modules.yaml`, `plugins.yaml`.
- No change to any FastAPI route in `platform/api/`.
- No Hermes skill activation. No Hermes Dashboard exposure.
- No memory promotion. No scheduler.
- No OpenWebUI extension is fetched from any third-party source.

## 8. Verification references

- Repo: `docs/governance/OPENWEBUI_PLUGIN_POLICY.md`, `OPENWEBUI_INTEGRATION.md`, `MODEL_ROUTING_POLICY.md`, `TASK_CONTRACTS.md`, `EVIDENCE_PACK.md`, `ROLE_SIGNALS.md`.
- Operations: `operations/openwebui_hermes_pantheon.md` §§10-12 (cockpit, actions, Hermes operator).
- Doctor: `operations/doctor.py` checks `forbidden_endpoints_absent` and `legacy_runtime_surfaces_absent` (PR #146).
- Upstream (verified via `raw.githubusercontent.com`):
  - `open-webui/open-webui` README — built-in Functions, Pipelines framework reference.
  - `open-webui/pipelines` README — Pipelines framework, port 9099, arbitrary-code-execution warning.

## 9. Final rule

```text
A Pipe is governance-surface, not runtime. Pantheon classifies and approves.
Hermes executes only inside a Task Contract.
OpenWebUI displays the result.
A spec is not an installation.
```
