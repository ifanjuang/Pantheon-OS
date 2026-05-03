# TASK CONTRACT REVISIONS — Pantheon Next

> Addendum to `TASK_CONTRACTS.md`.
>
> This document defines how single-role tasks, workflow revision signals, task contract revisions, resume policies and reset-to-baseline rules are represented before Hermes execution resumes.

---

## 1. Principle

A Task Contract is the execution frame.

A workflow may change during a session, but Hermes must not continue on an implicit or mutated frame.

Canonical rule:

```text
No execution change without a visible Task Contract frame.
No resumed execution without a resume policy.
No workflow revision without ZEUS arbitration and THEMIS/APOLLO checks where required.
```

This addendum complements:

```text
TASK_CONTRACTS.md
WORKFLOW_SCHEMA.md
WORKFLOW_ADAPTATION.md
EXECUTION_DISCIPLINE.md
APPROVALS.md
EVIDENCE_PACK.md
HERMES_INTEGRATION.md
```

---

## 2. Single-role task contract

Not every request requires a workflow.

A single-role task contract is allowed when one Pantheon Role can safely answer or act inside a bounded frame.

Use it when the request is:

```text
simple
low-risk
non-persistent
not externally sent
not memory-promoting
not file-mutating
not dependent on multiple branches
not dependent on source reconciliation
```

Examples:

```text
IRIS rewrites a short message without sending it.
ARGOS extracts one fact from a provided source.
ATHENA structures a simple plan.
THEMIS classifies an approval level.
APOLLO checks a short output for unsupported claims.
```

Minimal shape:

```yaml
single_role_task_contract:
  id: client_message_tone_review
  domain: general
  role: IRIS
  purpose: "Rewrite a short draft without sending it."
  mode: suggest
  approval_level: C1
  inputs:
    required:
      - draft_text
    optional:
      - tone
  outputs:
    required:
      - revised_text
      - limitations
  allowed_tools:
    - text_review
  forbidden_tools:
    - external_send
    - memory_write
    - file_write
  memory_impact: none
  evidence_required: false
  escalation_conditions:
    - external_send_requested
    - legal_or_contractual_claim_detected
    - project_private_context_required
    - multi_source_reconciliation_required
```

Rules:

```text
Single-role does not mean ungoverned.
Single-role may still need Evidence Pack if output is consequential.
Single-role must escalate when complexity, risk or persistence appears.
```

---

## 3. Escalation from single-role to workflow

A single-role task must escalate to a workflow when:

```text
more than one Pantheon Role becomes necessary
multiple sources must be reconciled
external communication is requested
approval level rises
memory could be affected
file mutation is requested
technical, contractual, financial or regulatory exposure appears
source conflict appears
user asks for execution rather than draft/suggestion
```

Escalation shape:

```yaml
single_role_escalation:
  from_task_contract: TC-2026-0001
  from_role: IRIS
  reason: "Draft became client-facing and contractually sensitive."
  triggered_by:
    - external_communication_possible
    - liability_risk_detected
  required_next_frame:
    type: workflow_task_contract
    roles:
      - THEMIS
      - APOLLO
      - IRIS
    approval_level: C4
    evidence_required: true
  execution_status: paused
```

Hermes must pause until the revised frame is approved when approval level increases.

---

## 4. Workflow revision signal

A workflow revision signal is a structured runtime signal that the current workflow or task contract no longer fits.

It may be emitted by Hermes or by a role-bound step.

It does not apply changes by itself.

```yaml
workflow_revision_signal:
  signal_id: WRS-2026-0001
  emitted_by: Hermes
  role_context: THEMIS
  severity: C4
  current_task_contract: TC-2026-0001
  current_step: iris_draft
  reason: "The output moved from internal draft to external contractual wording."
  detected_conditions:
    - external_use_possible
    - liability_language_detected
  recommendation: pause_for_zeus_arbitration
  execution_status: paused
  evidence_fragment:
    limitation: "External use requires C4 validation."
```

Allowed emitters:

```text
Hermes runtime
role-bound step
THEMIS precheck
APOLLO quality gate
CHRONOS dependency check
ARGOS source conflict check
```

Forbidden behavior:

```text
signals must not mutate workflows
signals must not change approvals
signals must not resume execution
signals must not canonize memory, skills or workflows
```

---

## 5. ZEUS arbitration for contract revision

After a workflow revision signal, ZEUS may arbitrate.

ZEUS may:

```text
continue unchanged
pause for user validation
add a step
remove a step
change dependencies
escalate single-role to workflow
reset to baseline
request more sources
request THEMIS review
request APOLLO review
reject the requested trajectory
```

ZEUS must not:

```text
lower approval without THEMIS clearance
bypass THEMIS veto
bypass APOLLO gate
activate skills
canonize workflows
promote memory
```

Arbitration shape:

```yaml
zeus_arbitration:
  arbitration_id: ZA-2026-0001
  source_signal: WRS-2026-0001
  decision: revise_task_contract
  reason: "External-facing output requires a safer frame."
  selected_change:
    type: add_step
    step_id: themis_external_wording_review
  approval_impact:
    from: C1
    to: C4
  required_checks:
    - THEMIS
    - APOLLO
  execution_status: pending_task_contract_revision
```

---

## 6. Task contract revision

A task contract revision is the visible revised execution frame sent to Hermes after arbitration.

A revision is required when a change affects:

```text
approval level
allowed tools
forbidden tools
inputs
outputs
memory impact
evidence requirements
workflow steps
dependencies
external visibility
file mutation
skill use
fallback policy
```

Minimal shape:

```yaml
task_contract_revision:
  parent_task_contract: TC-2026-0001
  revision_id: REV-001
  status: pending_approval
  reason: "Risk level changed during execution."
  source_signal: WRS-2026-0001
  arbitration: ZA-2026-0001
  changes:
    approval_level:
      from: C1
      to: C4
    added_steps:
      - id: themis_external_wording_review
        role: THEMIS
        purpose: "Review client-facing wording before release."
    evidence_required:
      from: false
      to: true
    forbidden_tools_added:
      - external_send_without_approval
  resume_policy:
    mode: after_human_validation
    resume_from: themis_external_wording_review
    preserve_outputs:
      - iris_draft_v1
    require_new_evidence_pack_fragment: true
```

Status values:

```text
pending_approval
approved
rejected
superseded
reset_to_baseline
```

---

## 7. Resume policy

A resume policy defines how Hermes may continue after a pause, revision or approval.

Required fields:

```yaml
resume_policy:
  mode: after_human_validation
  resume_from: themis_external_wording_review
  preserve_outputs:
    - argos_findings
    - iris_draft_v1
  discard_outputs:
    - unsafe_client_draft
  replay_required: false
  require_new_evidence_pack_fragment: true
  stop_if:
    - approval_denied
    - source_conflict_unresolved
    - forbidden_tool_required
```

Allowed modes:

| Mode | Use |
|---|---|
| `continue_current_step` | No material change; continue with same contract |
| `resume_from_step` | Restart from a named step after revision |
| `after_human_validation` | Wait for approval before resuming |
| `replay_from_checkpoint` | Rerun from a prior known-safe point |
| `reset_to_baseline` | Discard session override and return to template |
| `stop_and_report` | Stop execution and return diagnostic only |

Rules:

```text
No resume without explicit resume point.
No resume after C4/C5 escalation without required approval.
No resume if required source conflict remains unresolved.
No resume that silently discards evidence.
```

---

## 8. Reset to baseline

Reset to baseline discards a session workflow override and returns to a known workflow template or single-role frame.

It is allowed when:

```text
generated session workflow became too broad
workflow complexity exceeds task need
risk increases without value
user asks to return to standard behavior
ZEUS rejects the generated option
THEMIS blocks the adapted path
APOLLO rejects evidence feasibility
```

Shape:

```yaml
reset_to_baseline:
  parent_task_contract: TC-2026-0001
  discarded_override: session_workflow_variant_01
  baseline:
    type: workflow_template
    ref: domains/architecture_fr/workflows/quote_vs_cctp_review/workflow.yaml
  reason: "Generated option exceeded current task scope."
  preserve_evidence: true
  preserve_outputs:
    - source_inventory
  discard_outputs:
    - overbroad_workflow_plan
  next_status: pending_baseline_task_contract
```

Rules:

```text
Reset does not erase evidence.
Reset does not canonize the discarded path.
Reset does not delete user-provided sources.
Reset may still require a new Task Contract if execution continues.
```

---

## 9. Evidence requirements

Every revision must add an Evidence Pack fragment.

Minimum fields:

```text
previous_task_contract
source_signal
arbitration_result
changes_requested
approval_impact
steps_added_or_removed
dependencies_changed
outputs_preserved
outputs_discarded
resume_policy
limitations
next_safe_action
```

If the task returns to single-role or baseline, the Evidence Pack must state why.

---

## 10. Hermes boundary

Hermes may:

```text
emit revision signals
pause when contract no longer fits
execute a revised task contract after approval
return partial outputs and evidence fragments
```

Hermes must not:

```text
revise its own contract silently
resume after approval escalation without approval
promote a session workflow to canonical workflow
promote memory
activate skills
send external communications
```

---

## 11. Final rule

```text
The Task Contract is the execution frame.
A revision changes the frame.
A resume policy controls continuation.
Hermes executes only the approved current frame.
Pantheon remains the authority.
```
