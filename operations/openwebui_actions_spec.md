# OpenWebUI Actions — Spec (no activation)

> Specification for OpenWebUI Action buttons used inside Pantheon Next.
> Read-only spec. No Action is created, installed or enabled by this document.

Date: 2026-05-11
Status: **draft spec only**

---

## 1. Doctrine boundary

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

OpenWebUI Actions are user-facing buttons attached to messages. They are
human-in-the-loop surfaces, not autonomous executors. This spec lists the
Pantheon-aligned Action set documented in
`docs/governance/OPENWEBUI_PLUGIN_POLICY.md` §"Recommended Pantheon OpenWebUI
components" and gives each one a verifiable status.

Upstream definition (verified against `OPENWEBUI_PLUGIN_POLICY.md` §Action):

> "Action Functions add buttons to messages. Actions are appropriate for
> human-in-the-loop validation, not autonomous execution."

## 2. Recommended Pantheon Action set

Source: `OPENWEBUI_PLUGIN_POLICY.md` §"Recommended Pantheon OpenWebUI
components" (lines 197 onward).

| Action label | Pantheon role | Purpose | Status |
|---|---|---|---|
| Evidence Pack display | APOLLO / IRIS | Renders the Evidence Pack returned by a Hermes run | **Documenté** spec only |
| Approval request | THEMIS | Surfaces a `POST /domain/approval/classify` decision for human validation | **Documenté** spec only |
| Approve candidate | ZEUS / user | Marks a Hermes candidate (patch, skill, workflow, memory candidate) approved | **Non implémenté** |
| Reject candidate | ZEUS / user | Marks a Hermes candidate rejected with reason | **Non implémenté** |
| Hermes rerun | user | Re-emits the same Task Contract to Hermes with the same constraints | **Candidate only** |
| Source formatting | IRIS | Renders sources cited in the Evidence Pack as a public summary | **Documenté** spec only |
| Pantheon boundary reminder | THEMIS | Inserts a doctrine-aligned notice when a request risks crossing the boundary | **Documenté** spec only |

Per `OPENWEBUI_PLUGIN_POLICY.md` §"Approval mapping", Actions that mutate
governance artefacts (skill canonization, workflow canonization, memory
promotion) require **C3+ approval** and are forbidden until the required
Pantheon flow exists.

## 3. Required bindings (Documenté)

| Concern | Source of truth | Required behaviour |
|---|---|---|
| C0-C5 levels | `APPROVALS.md` | Every Action must declare its approval level; the cockpit must show it |
| Evidence Pack | `EVIDENCE_PACK.md` | `Evidence Pack display` Action shows minimum fields; no raw chain-of-thought |
| Role Signal display | `ROLE_SIGNALS.md` §10b + `RUN_GRAPH.md` | Actions surface only public summaries (e.g., `ARGOS : sources prises en compte`) |
| Forbidden surfaces | Doctor `forbidden_endpoints_absent` and `legacy_runtime_surfaces_absent` | No Action may POST to `/agents/run`, `/runtime/execute`, `/memory/promote/auto`, `/agent/run`, `/orchestra/*` |
| Authentication | `OPENWEBUI_INTEGRATION.md` §"Boundary rules" | Actions are visible only to authenticated users with the right group; Hermes Dashboard exposure remains forbidden |

## 4. Forbidden Action behaviour

Documented in `OPENWEBUI_PLUGIN_POLICY.md` §"Forbidden OpenWebUI roles" and
restated here for clarity:

```text
No Action may:
  - canonize memory automatically
  - canonize skills automatically
  - canonize workflows automatically
  - mutate any governance Markdown
  - call a Hermes execution endpoint without an approved Task Contract
  - call any legacy POST surface (/agents/run, /runtime/execute,
    /memory/promote/auto, /agent/run, /orchestra/*)
  - send messages externally without C4 approval
  - access secrets or the Docker socket
```

Actions are **interdites pour core** when they include any of the above
behaviours; they may exist as **candidate only** with explicit C3+ review.

## 5. Action lifecycle

Per `OPENWEBUI_PLUGIN_POLICY.md` §"Plugin review checklist", every Action
follows this lifecycle, with no shortcut:

```text
proposal
→ doctrine review (THEMIS)
→ security review (HEPHAESTUS / HEPHAISTOS)
→ Evidence Pack template defined
→ approval level mapped (APPROVALS.md)
→ candidate code reviewed
→ install in dev OpenWebUI
→ user acceptance review
→ promotion to recommended Pantheon component
```

No step is skipped. The candidate code is **not** installed by this spec.

## 6. Status legend per item

| Item | Status |
|---|---|
| Action set definition | **Documenté** (this file + `OPENWEBUI_PLUGIN_POLICY.md`) |
| Action approval mapping | **Documenté** |
| Action code | **Non implémenté** |
| Action install in OpenWebUI | **Interdit pour core** until C3 review |
| Action triggering Hermes execution without Task Contract | **Interdit pour core** |
| Hermes rerun Action with bounded Task Contract | **Candidate only** |
| Action calling `/agents/run`, `/agent/run`, `/orchestra/*` | **Interdit pour core** (Doctor checks block) |

## 7. Out of scope

- No Action Function is installed, registered or enabled.
- No `docker-compose.yml`, `.env`, `modules.yaml`, `plugins.yaml` change.
- No FastAPI route added or modified.
- No Hermes skill activation.
- No memory promotion, no scheduler, no agent loop.

## 8. Verification references

- `docs/governance/OPENWEBUI_PLUGIN_POLICY.md` §§"Function types", "Approval mapping", "Plugin review checklist", "Recommended Pantheon OpenWebUI components".
- `docs/governance/OPENWEBUI_INTEGRATION.md` §§"Role", "Boundary rules".
- `docs/governance/APPROVALS.md` C0-C5 mapping.
- `docs/governance/EVIDENCE_PACK.md` §3 (minimum), §6b (role signal traceability).
- `docs/governance/RUN_GRAPH.md` §10b (Role Signal visibility).
- `operations/openwebui_hermes_pantheon.md` §11 "OpenWebUI actions".
- Upstream: `open-webui/open-webui` README (verified via raw GitHub) — built-in Functions / Actions vocabulary.

## 9. Final rule

```text
Actions are buttons. Buttons surface decisions.
Decisions belong to Pantheon roles, not to Action code.
A spec is not an installation.
```
