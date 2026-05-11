# Hermes Task Contract Bridge — Spec (no activation)

> Specification for sending Pantheon Task Contracts to Hermes Agent for
> execution while preserving Pantheon governance. No bridge is implemented or
> activated by this document.

Date: 2026-05-11
Status: **draft spec only**

---

## 1. Doctrine boundary

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

The Bridge is the contract surface between Pantheon Next (governance) and
Hermes Agent (execution). It is not a runtime, not a scheduler, not a workflow
engine, not a message bus. It is a specification for how a Task Contract
authored by Pantheon may be transmitted to Hermes, how the Evidence Pack must
flow back, and how Pantheon stays the authority.

References:

- `docs/governance/TASK_CONTRACTS.md` §§3, 4 (required fields, YAML shape)
- `docs/governance/TASK_CONTRACT_REVISIONS.md` (revision, resume policy)
- `docs/governance/HERMES_INTEGRATION.md` §§5, 6, 9, 10, 11
- `docs/governance/HERMES_EXECUTION_MODEL.md`
- `docs/governance/EVIDENCE_PACK.md`
- `docs/governance/APPROVALS.md`
- `docs/governance/ROLE_SIGNALS.md`
- `operations/openwebui_hermes_pantheon.md` §§7, 15, 16, 17

Upstream Hermes facts (verified verbatim from
`raw.githubusercontent.com/NousResearch/hermes-agent` README):

- `hermes`, `hermes model`, `hermes tools`, `hermes config set`,
  `hermes gateway`, `hermes setup`, `hermes claw migrate`, `hermes update`,
  `hermes doctor` are the CLI commands.
- Local install paths: `~/.hermes` (Linux/macOS), `%LOCALAPPDATA%\\hermes`
  (Windows).
- Docs: <https://hermes-agent.nousresearch.com/docs/> (canonical).
- Terminal backends listed in the README: local, Docker, SSH, Singularity,
  Modal, Daytona, Vercel Sandbox.

These values are quoted here so operators do not invent endpoints or commands
when later wiring Pantheon to Hermes.

## 2. Bridge inputs and outputs (Documenté)

### 2.1 Inputs (Pantheon → Hermes)

| Input | Source | Notes |
|---|---|---|
| Task Contract | `TASK_CONTRACTS.md` §§3, 4 | Required 16 fields validated by `schemas/task_contract.schema.yaml` (PR #141) |
| Context Pack | `GET /runtime/context-pack` | Static orientation pack, read-only |
| Domain snapshot | `GET /domain/snapshot` and `/domain/agents`, `/skills`, `/workflows`, `/memory`, `/knowledge`, `/legacy` | Read-only canonical view |
| Role Signal profiles | `GET /domain/role-signal-profiles` | Bloc 5 |
| Approval pre-classification | `POST /domain/approval/classify` | Already shipped, classification only |

### 2.2 Outputs (Hermes → Pantheon)

| Output | Target | Notes |
|---|---|---|
| Evidence Pack | `EVIDENCE_PACK.md` §3 minimum + §4 extended when relevant | Mandatory for consequential outputs |
| Task Contract revision request | `TASK_CONTRACT_REVISIONS.md` §6 + signal types in `ROLE_SIGNALS.md` §7 | `workflow_revision_signal`, `veto_signal`, `stop_gate_signal`, `risk_warning`, `source_gap_signal`, `skill_gap_signal` |
| Candidate artifacts | `HERMES_INTEGRATION.md` §10 | Candidate patches, candidate skills, candidate workflows, candidate memory events — never canonical by default |

## 3. Required bridge behaviour (Documenté)

| Concern | Required behaviour |
|---|---|
| Frame integrity | Hermes executes only the approved current Task Contract; no silent self-revision (`TASK_CONTRACT_REVISIONS.md` §10) |
| Approval discipline | C3 patches and C4 external actions require explicit user approval surfaced via OpenWebUI Actions; no silent escalation (`APPROVALS.md`) |
| Tool policy | Hermes uses only `allowed_tools` from the Task Contract; `forbidden_tools` block fallback (`TASK_CONTRACTS.md` §4) |
| Memory policy | No automatic memory promotion (`MEMORY_EVENT_SCHEMA.md` §9). Memory candidates only via Evidence Pack + C3 review |
| Run Graph visibility | Only public summaries surface to OpenWebUI Inline Run Stream; raw chain-of-thought forbidden (`RUN_GRAPH.md` §10b) |
| Boundary | Hermes never modifies governance Markdown, never canonizes a skill, never canonizes a workflow, never promotes memory autonomously |
| Forbidden surfaces | The bridge must not consume `/agents/run`, `/runtime/execute`, `/memory/promote/auto` (Doctor `forbidden_endpoints_absent`) |
| Legacy surfaces | The bridge must not consume `/agent/run`, `/orchestra/run`, `/orchestra/run-hitl`, `/orchestra/stream`, `/orchestra/runs/{run_id}/approve` (Doctor `legacy_runtime_surfaces_absent`, PR #146) |
| Hermes Dashboard | Never publicly exposed (`OPENWEBUI_INTEGRATION.md`, `operations/openwebui_hermes_pantheon.md` §"Boundary") |

## 4. Bridge shape (sketch, non implémenté)

The bridge is the YAML-over-HTTP envelope that wraps a Task Contract before
sending it to Hermes. The shape below sketches the on-the-wire form; it is
**not** implemented and **not** authorized for activation by this spec.

```yaml
task_contract_dispatch:
  pantheon_task_contract: <see schemas/task_contract.schema.yaml>
  context_pack_ref: GET /runtime/context-pack
  approval_pre_classification:
    action_kind: <see APPROVALS.md §3>
    decision: <not_required | required | forbidden_until_policy_exists>
  hermes_target:
    transport: spec_only
    notes: |
      Transport choice (local CLI, gateway HTTP, MCP, etc.) is À vérifier;
      see Hermes upstream docs https://hermes-agent.nousresearch.com/docs/.
  expected_response:
    evidence_pack_ref: <see EVIDENCE_PACK.md §3>
    candidate_artifacts: []
    role_signal_traceability_ref: <see EVIDENCE_PACK.md §6b>
```

`hermes_target.transport` is intentionally left `spec_only`. The decision
between a local-CLI bridge, an HTTP Gateway and an MCP target is **À
vérifier** in a live deployment; this spec must not pre-select one.

## 5. Signals that pause or revise the contract

Hermes may emit any of the following Role Signals (defined in
`ROLE_SIGNALS.md` §7) instead of silently mutating the contract:

```text
workflow_revision_signal   → ZEUS arbitration; TASK_CONTRACT_REVISIONS.md §5
veto_signal                → THEMIS blocks; cannot be overridden by AGORA
stop_gate_signal           → APOLLO blocks finalization
risk_warning               → THEMIS raises risk
source_gap_signal          → ARGOS reports missing source
skill_gap_signal           → HEPHAESTUS / HEPHAISTOS flags missing method
handoff_signal             → active role changes
clarification_request      → reroute via METIS or ATHENA
```

The bridge must surface these as structured records, not as free-form text.
Every signal that triggers a revision must produce a `task_contract_revision`
fragment per `TASK_CONTRACT_REVISIONS.md` §6.

## 6. Status legend per item

| Item | Status |
|---|---|
| Task Contract YAML shape | **Documenté** (`TASK_CONTRACTS.md` §4) + validated by `schemas/task_contract.schema.yaml` (PR #141) |
| Task Contract revision shape | **Documenté** (`TASK_CONTRACT_REVISIONS.md` §6) + validated by `schemas/task_contract_revision.schema.yaml` |
| Evidence Pack minimum shape | **Documenté** (`EVIDENCE_PACK.md` §3) + validated by `schemas/evidence_pack.schema.yaml` |
| Bridge envelope on the wire | **Non implémenté** (sketch above) |
| Bridge transport (CLI / HTTP / MCP) | **À vérifier** — depends on Hermes deployment choice |
| Hermes-side endpoint or command | **À vérifier** against `https://hermes-agent.nousresearch.com/docs/`; do not guess |
| Automated Pantheon → Hermes dispatch | **Candidate only** — requires C3+ approval, no auto-merge |
| Bridge consuming `/agents/run`, `/agent/run`, `/orchestra/*` | **Interdit pour core** (Doctor blocks) |
| Hermes Dashboard public exposure | **Interdit pour core** |
| Hermes auto-promotion of memory or canonization of skills/workflows | **Interdit pour core** |

## 7. Out of scope

- No bridge code is written.
- No HTTP route is added to `platform/api/`.
- No `docker-compose.yml`, `.env`, `modules.yaml`, `plugins.yaml` change.
- No Hermes installation, no `hermes setup`, no `hermes gateway`.
- No memory promotion. No skill activation. No workflow canonization.
- No scheduler. No agent loop. No message bus.

## 8. Verification references

- Repo: `TASK_CONTRACTS.md`, `TASK_CONTRACT_REVISIONS.md`, `HERMES_INTEGRATION.md`, `HERMES_EXECUTION_MODEL.md`, `HERMES_CAPABILITY_MAP.md`, `EVIDENCE_PACK.md`, `APPROVALS.md`, `ROLE_SIGNALS.md`.
- Operations: `operations/openwebui_hermes_pantheon.md` §§7, 15, 16, 17.
- Schemas: `schemas/task_contract.schema.yaml`, `schemas/task_contract_revision.schema.yaml`, `schemas/evidence_pack.schema.yaml` (PR #141).
- Doctor: `operations/doctor.py` `forbidden_endpoints_absent`, `legacy_runtime_surfaces_absent` (PR #146).
- Upstream: `NousResearch/hermes-agent` README — canonical CLI surface, install paths and docs URL.

## 9. Final rule

```text
Pantheon authors the contract.
Hermes executes the contract.
OpenWebUI displays the contract and its evidence.
A bridge spec is not a bridge.
```
