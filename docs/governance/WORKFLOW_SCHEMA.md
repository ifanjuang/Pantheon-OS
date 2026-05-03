# WORKFLOW SCHEMA — Pantheon Next

> Reference schema for workflow definitions.
> Workflows are governed definitions. Hermes executes them when a task contract authorizes execution.
>
> Adaptive/session workflow behavior is governed by `WORKFLOW_ADAPTATION.md`.

---

## 1. Principle

A workflow is a structured method, not a long prompt.

```text
Pantheon defines the workflow frame.
Pantheon may select, adapt, compose or generate a session workflow under governance.
Hermes executes bounded tasks.
OpenWebUI displays state, evidence and approvals.
```

A workflow must stay readable, testable and auditable.

Workflow templates are reusable governed patterns, not fixed rails.

Not every user request requires a workflow. Simple, low-risk requests may be handled through a single Pantheon Role and, when needed, a single bounded skill.

Reference:

```text
WORKFLOW_ADAPTATION.md
```

---

## 2. Single-role path

Some questions do not need workflow orchestration.

Use the single-role path when the task is:

```text
simple
low-risk
non-persistent
not externally sent
not memory-promoting
not file-mutating
not tool-complex
not dependent on multiple sources or branches
```

Examples:

```text
IRIS reformulates a short message.
ARGOS extracts one fact from a provided source.
ATHENA structures a simple plan.
THEMIS classifies an approval level.
APOLLO checks a short answer for unsupported claims.
```

A single-role path may still require an Evidence Pack if the output is consequential.

A single-role path must escalate to a workflow when:

```text
multiple roles are required
multiple sources must be reconciled
external communication is requested
approval level rises
memory could be affected
file mutation is requested
technical, contractual, financial or regulatory exposure appears
```

Minimal shape:

```yaml
single_role_task:
  id: client_message_tone_review
  role: IRIS
  purpose: "Rewrite a short draft without sending it."
  mode: suggest
  approval_level: C1
  evidence_required: false
  memory_impact: none
  forbidden_tools:
    - external_send
    - memory_write
```

---

## 3. Recommended directory structure

```text
domains/{domain}/workflows/{workflow_id}/
  workflow.yaml
  tasks.yaml
  examples.md
  tests.md
  UPDATES.md
```

`workflow.yaml` defines metadata and high-level structure.

`tasks.yaml` defines task-level steps.

`UPDATES.md` contains candidate improvements. It must not silently rewrite the active workflow.

---

## 4. Workflow fields

```yaml
id: quote_vs_cctp_review
name: Quote vs CCTP Review
domain: architecture_fr
status: candidate
version: 0.1.0
pattern: cascade
purpose: Compare a contractor quote against a CCTP and identify gaps, duplicates, risks and clarification points.
inputs:
  - cctp
  - quote
  - lot_scope
outputs:
  - diagnostic
  - inconsistency_table
  - missing_items
  - risk_notes
  - approval_required
agents:
  - ATHENA
  - ARGOS
  - HEPHAESTUS
  - THEMIS
  - APOLLO
skills:
  - project_context_resolution
  - source_check
  - quote_vs_cctp_consistency
approval_points:
  - external_communication
  - file_mutation
  - memory_promotion
memory_impact:
  - none_by_default
  - candidate_only_if_reusable_pattern_detected
evidence_required: true
fallback: keep_as_diagnostic_if_sources_are_incomplete
```

---

## 5. Task fields

```yaml
tasks:
  - id: resolve_project_context
    description: Determine whether project context is required and select the correct project context if needed.
    expected_output: project_context_result
    execution_mode: skill
    assigned_skill: project_context_resolution
    inputs:
      - user_request
      - visible_context
    dependencies: []
    tools_allowed:
      - read_reference_markdowns
      - read_project_memory_if_authorized
    tools_forbidden:
      - write_memory
      - write_notion
      - external_message
    memory_scope: session
    criticity: C0
    approval_required_if:
      - project_merge
      - alias_persistence
      - low_confidence
    success_criteria:
      - project_context_is_resolved_or_marked_not_required
      - uncertainty_is_visible
    failure_modes:
      - ambiguous_project
      - missing_registry
      - forbidden_knowledge_base
    output_schema: project_context_result
```

---

## 6. Dependency graph fields

For adaptive or dependency-aware workflows, task definitions may also include:

```yaml
tasks:
  - id: argos_document_search
    role: ARGOS
    requires: []
    optional_requires: []
    produces:
      - document_findings
    can_start_when:
      - uploaded_document_available
    pause_conditions:
      - source_unreadable
      - missing_required_document
    join_policy: null
    evidence_required: true
```

Allowed dependency fields:

| Field | Purpose |
|---|---|
| `requires` | Mandatory upstream outputs or conditions |
| `optional_requires` | Inputs to include if ready, without blocking unless ZEUS/ATHENA marks them required |
| `produces` | Declared outputs made available to later tasks |
| `can_start_when` | Start condition separate from strict dependency |
| `pause_conditions` | Conditions that pause execution and may emit a revision signal |
| `join_policy` | How parallel branches are consolidated |

Rules:

```text
Hermes may execute all unblocked bounded steps in parallel.
ATHENA arranges workflow steps.
CHRONOS defines dependencies, joins and waits.
ZEUS arbitrates changes.
THEMIS blocks unsafe transitions.
APOLLO validates final evidence and quality.
```

---

## 7. Workflow patterns

Allowed initial patterns:

| Pattern | Use |
|---|---|
| `solo` | one bounded task or one role/skill; no workflow graph required |
| `cascade` | sequential steps with dependencies |
| `parallel` | independent branches merged at review |
| `arena` | competing or contradictory analyses before synthesis |
| `dependency_graph` | steps start when required inputs are available |

Later patterns:

| Pattern | Status | Note |
|---|---|---|
| `crew` | P2/P3 | only if stable multi-role teams are needed |
| `flow` | P2/P3 | only if event-driven execution becomes necessary |
| `conditional` | P2 | useful, but must stay readable |

Forbidden as Pantheon core:

```text
LangGraph central orchestrator
hidden agent loop
scheduler-owned workflow execution
automatic workflow mutation
automatic workflow activation
automatic workflow canonization
```

---

## 8. Criticality

Workflow tasks use C0-C5.

```text
C0 = read / diagnostic
C1 = draft / suggestion
C2 = reversible low-risk action
C3 = persistent internal change
C4 = external / contractual / financial / responsibility action
C5 = critical / irreversible / secrets / destructive
```

A legacy schema that starts at C1 must be corrected before activation.

---

## 9. Validation rules

A workflow is invalid if:

- two tasks share the same id;
- a dependency references an unknown task;
- a task has no expected output;
- a task has an execution mode but no matching assignment;
- C3+ tasks have no approval path;
- consequential outputs have no Evidence Pack requirement;
- memory impact is undefined;
- external tools are not allowlisted;
- adaptive changes bypass `WORKFLOW_ADAPTATION.md`;
- dependency graph steps have undeclared outputs or unresolved required inputs.

A single-role task is invalid if:

- it is used to hide a multi-role workflow requirement;
- it includes external action without approval;
- it mutates files or memory without Task Contract and approval;
- it bypasses THEMIS or APOLLO when risk requires them.

---

## 10. Adaptive orchestration

`adaptive_orchestration` may propose workflow changes only as candidate updates unless the change is:

```text
low-risk
reversible
inside current run
not persistent
not externally visible
not a memory promotion
not a skill level-up
```

It may also decide that no workflow is needed and that a single-role path is sufficient.

Durable workflow changes require review.

Reference:

```text
WORKFLOW_ADAPTATION.md
```

---

## 11. Evidence

Every consequential workflow must record:

```text
files_read
sources_used
knowledge_bases_consulted
tools_used
commands_run
steps_executed
parallel_groups_executed
join_policies_used
workflow_adaptations
fallbacks_used
failed_attempts
unsupported_claims
limitations
approval_required
next_safe_action
```

Single-role consequential outputs must still record the evidence needed for their approval level.

Reference:

```text
EVIDENCE_PACK.md
WORKFLOW_ADAPTATION.md
```

---

## 12. Final rule

```text
Simple requests may use a single role.
Workflows define method when orchestration is needed.
Workflow adaptation defines governed session changes.
Task contracts frame execution.
Hermes executes.
Pantheon validates and canonizes.
```
