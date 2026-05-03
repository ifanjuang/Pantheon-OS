# WORKFLOW ADAPTATION — Pantheon Next

> Doctrine for adaptive, dependency-based and role-consulted workflows.
>
> This document defines how Pantheon may select, adapt, compose or generate workflows in session while preserving governance.

---

## 1. Principle

Pantheon workflows are not fixed rails.

They are governed trajectories that may be:

```text
selected from an existing template
adapted from an existing template
composed from several patterns
generated in session from scratch
revised during execution
saved as a candidate for later review
reset to a baseline template
```

The repository contains templates, examples and validated patterns. It does not contain every possible workflow.

Canonical rule:

```text
Pantheon is the governance base.
Workflow templates are reusable examples.
Session workflows may be adapted or generated.
Hermes executes only the resulting Task Contract.
OpenWebUI exposes and validates.
```

---

## 2. Non-negotiable boundaries

Workflow adaptation must never bypass:

```text
APPROVALS.md
TASK_CONTRACTS.md
EVIDENCE_PACK.md
MEMORY.md
EXTERNAL_TOOLS_POLICY.md
HERMES_INTEGRATION.md
KNOWLEDGE_TAXONOMY.md
MODEL_ROUTING_POLICY.md
```

A workflow adaptation must not:

```text
lower approval requirements silently
remove THEMIS veto
remove APOLLO final evidence/quality gate
use an unclassified external tool
enable external communication without C4 approval
enable secrets, Docker socket or destructive shell access without C5
promote memory automatically
modify canonical Markdown without approval
activate a skill automatically
turn Pantheon into an autonomous runtime
```

---

## 3. Canonical vocabulary

| Term | Meaning |
|---|---|
| `workflow_template` | reusable governed pattern stored in the repo |
| `session_workflow` | workflow selected, adapted or generated for the current task/session |
| `workflow_override` | local/session change applied over a baseline template |
| `workflow_candidate` | durable proposal to add or update a workflow template |
| `workflow_revision_signal` | runtime signal that the current workflow no longer fits |
| `workflow_patch` | proposed change to the current session workflow |
| `task_contract_revision` | revised execution frame sent to Hermes |
| `resume_policy` | rule describing where and how execution resumes |
| `reset_to_baseline` | discard local/session override and return to original template |

---

## 4. Role distribution for workflow adaptation

Pantheon roles are abstract governance roles, not runtime workers.

Recommended role split:

| Role | Workflow adaptation responsibility |
|---|---|
| ZEUS | arbitrate, select, combine, suspend, reroute or request refactor |
| ATHENA | arrange the workflow, compose steps, structure the strategy |
| CHRONOS | order dependencies, define parallel groups, joins, waits and resume points |
| HEPHAISTOS | forge skills, strengthen methods, identify missing capabilities |
| PROMETHEUS | propose alternatives, variants and non-obvious paths |
| ARGOS | identify available inputs, sources, facts and missing material |
| THEMIS | classify risk, approvals, privacy, forbidden transitions and vetoes |
| APOLLO | validate proof, quality, unsupported claims and final coherence |
| HECATE | detect ambiguity, hidden risks and uncertainty |
| IRIS | shape human-facing communication after validation |
| HESTIA | identify project memory relevance without promoting memory |
| MNEMOSYNE | identify system-memory candidate relevance without promoting memory |

Canonical split:

```text
ATHENA agence les workflows.
HEPHAISTOS forge les skills.
CHRONOS règle les dépendances.
ZEUS arbitre les options.
THEMIS bloque.
APOLLO valide.
Hermes exécute.
```

---

## 5. Workflow design consultation

ZEUS may request a workflow design consultation before execution or after a revision signal.

A consultation may involve:

```text
ARGOS for source and input availability
ATHENA for workflow arrangement
CHRONOS for dependency graph and timing
HEPHAISTOS for missing skills or method robustness
PROMETHEUS for alternatives
THEMIS for approval and policy risk
APOLLO for evidence and final-quality feasibility
HECATE for ambiguity and unknowns
IRIS for output form and user-facing constraints
```

The consultation must produce visible structured outputs, not raw chain-of-thought.

---

## 6. Role need statement

Each consulted role may emit a `role_need_statement`.

```yaml
role_need_statement:
  role: ARGOS
  needs:
    - uploaded_documents
    - selected_knowledge_sources
  can_produce:
    - source_inventory
    - factual_findings
    - missing_sources
  cannot_produce:
    - final_contractual_position
  risks:
    - incomplete_source_set
  recommended_next_step: knowledge_selection
```

Rules:

```text
Needs must be explicit.
Outputs must be bounded.
Risks must be visible.
Unsupported certainty is forbidden.
```

---

## 7. Workflow options

ATHENA may arrange workflow options.

PROMETHEUS may propose alternative paths.

HEPHAISTOS may identify skills or capabilities required to make an option executable and robust.

CHRONOS may define dependencies and concurrency.

THEMIS and APOLLO must check options before ZEUS arbitration.

Example:

```yaml
workflow_option:
  id: option_B_parallel_reinforced
  origin: adapted_from_template
  intent: "Multi-source review with evidence and policy gates."
  based_on:
    - quote_vs_cctp_review
    - knowledge_selection
  graph:
    parallel:
      - argos_document_search
      - argos_knowledge_check
      - themis_precheck
    optional_parallel:
      - argos_web_current_check
    join:
      - athena_consolidation
      - chronos_dependency_review
      - hephaistos_method_check
      - themis_final_check
      - apollo_evidence_gate
      - iris_draft
  approval:
    internal_analysis: C3
    client_facing_use: C4
  evidence_required: true
  memory_impact: candidate_only
  risks:
    - longer_execution
    - source_conflict_possible
  recommended_by: ATHENA
```

---

## 8. ZEUS arbitration

ZEUS may:

```text
select one workflow option
combine multiple options
request a simpler option
request a safer option
request a more parallel option
request a fallback option
suspend execution
ask the user for validation
reject all options and request new consultation
```

ZEUS must not:

```text
lower approvals without THEMIS clearance
bypass THEMIS veto
bypass APOLLO gate
authorize forbidden tools
canonize a generated session workflow automatically
```

Example:

```yaml
zeus_arbitration:
  decision: combine_options
  selected:
    primary: option_B_parallel_reinforced
    fallback: option_C_clarify_first
  reason: "The task involves multiple sources and possible external-facing output."
  modifications:
    - add_themis_precheck_before_parallel_group
    - make_web_check_required_only_if_current_regulation_is_needed
    - require_apollo_gate_before_iris
  approval:
    internal_analysis: C3
    external_use: C4
  execution:
    runtime: Hermes
    mode: dependency_graph
```

---

## 9. Dependency graph model

Pantheon workflows are dependency graphs, not necessarily linear chains.

Each role-bound step declares:

```text
required inputs
optional inputs
outputs
start conditions
pause conditions
approval impact
evidence obligations
allowed tools
forbidden tools
```

Hermes may execute all unblocked read-only or bounded steps in parallel.

Example:

```yaml
workflow_execution_plan:
  mode: dependency_graph
  steps:
    - id: argos_document_search
      role: ARGOS
      requires: []
      produces:
        - document_findings
      can_start_when:
        - uploaded_document_available
      evidence_required: true

    - id: argos_knowledge_check
      role: ARGOS
      requires:
        - knowledge_selection_report
      produces:
        - knowledge_findings
      evidence_required: true

    - id: themis_precheck
      role: THEMIS
      requires:
        - user_request_classified
      produces:
        - initial_approval_level
        - forbidden_actions

    - id: athena_consolidation
      role: ATHENA
      requires:
        - document_findings
        - knowledge_findings
      optional_requires:
        - web_findings
      join_policy: wait_required_then_include_optional_if_ready
      produces:
        - structured_analysis
        - contradictions
        - missing_sources

    - id: apollo_final_gate
      role: APOLLO
      requires:
        - structured_analysis
        - clearance_or_veto
        - evidence_pack_draft
      produces:
        - final_quality_status
```

---

## 10. Parallel execution policy

Parallel execution is allowed only when steps are:

```text
bounded
read-only or non-authoritative
not externally visible
not memory-promoting
not modifying the same file or state
not deciding approvals independently
joined and checked before final output
recorded in the Evidence Pack
```

Good parallel candidates:

```text
ARGOS document extraction
ARGOS Knowledge lookup after knowledge_selection
ARGOS web check when policy allows
HEPHAISTOS independent technical critique by branch
PROMETHEUS alternatives
HECATE ambiguity detection
CHRONOS dependency scan
THEMIS early precheck
```

Sequential or gated steps:

```text
ZEUS arbitration
THEMIS final veto
APOLLO final gate
memory promotion
external communication
file mutation
workflow canonization
skill promotion
C4/C5 actions
```

---

## 11. Workflow revision signal

Hermes or a role-bound step may emit a revision signal when the workflow no longer fits.

```yaml
workflow_revision_signal:
  emitted_by: Hermes
  role_context: THEMIS
  severity: C4
  reason: "The task moved from internal analysis to external contractual wording."
  current_step: iris_draft
  recommendation: pause_for_zeus_arbitration
  execution_status: paused
  evidence_fragment:
    limitation: "External use requires C4 validation."
```

Signals do not apply changes by themselves.

They trigger ZEUS arbitration.

---

## 12. Workflow patch and task contract revision

After arbitration, ZEUS may produce a `workflow_patch`.

```yaml
workflow_patch:
  requested_by: ZEUS
  reason: "Risk level changed during execution."
  change_type: add_review_step
  add_after: themis_precheck
  step:
    id: themis_external_wording_review
    role: THEMIS
    mission: "Review client-facing wording before draft release."
  approval_impact:
    from: C3
    to: C4
  evidence_required: true
```

A patch that changes execution must become a `task_contract_revision` before Hermes resumes.

```yaml
task_contract_revision:
  parent_task_contract: TC-2026-0001
  revision_id: REV-001
  status: approved_or_pending
  changes:
    - added_step: themis_external_wording_review
    - approval_level_changed: C3_to_C4
  resume_policy:
    mode: after_human_validation
    resume_from: themis_external_wording_review
```

---

## 13. Reset to baseline

A session workflow or override may be reset to a baseline template.

Reset means:

```text
discard local/session override
reload the baseline workflow template
keep the run log or adaptation report
keep evidence of why reset happened
never delete source evidence
```

Example:

```yaml
reset_to_baseline:
  base_template: domains/architecture_fr/workflows/quote_vs_cctp_review/workflow.yaml
  discarded_override: session_2026_05_03_variant_01
  reason: "Generated option was too broad for the current request."
  keep_log: true
```

---

## 14. Saving an adaptation

A session workflow may be saved only as a candidate.

```text
session_workflow
→ workflow_candidate
→ Evidence Pack
→ review
→ approval
→ possible template
```

It must not become canonical automatically.

Candidate minimum fields:

```yaml
workflow_candidate:
  id: candidate_quote_vs_cctp_reinforced
  origin: generated_in_session
  reason_for_candidate: "Reusable pattern observed."
  source_task_contract: TC-2026-0001
  source_evidence_pack: EP-2026-0001
  proposed_domain: architecture_fr
  status: candidate
  review_required: true
```

---

## 15. Langflow and LangGraph boundaries

Langflow may be used later for visual prototyping or session workflow editing.

LangGraph may be used later as an execution graph library inside Hermes.

Neither is source of truth.

```text
Pantheon workflow/session graph defines the method.
Langflow may visualize or prototype.
LangGraph may execute graph logic inside Hermes.
Hermes returns Evidence Pack.
Pantheon canonizes only after review.
```

Forbidden:

```text
Langflow as canonical workflow authority
LangGraph as central Pantheon orchestrator
hidden graph mutation
workflow execution without Task Contract
workflow canonization without review
```

---

## 16. Interaction with skills

HEPHAISTOS is the primary role for skill forging and method robustness.

HEPHAISTOS may identify:

```text
missing skill
weak skill
skill candidate improvement
need for tool policy review
need for tests
need for rollback
```

HEPHAISTOS must not activate or promote skills.

Skill changes follow `SKILL_LIFECYCLE.md` and `TASK_CONTRACTS.md`.

---

## 17. Evidence requirements

Every adaptation that affects output must be recorded.

Evidence Pack must include:

```text
initial workflow or reason no template was used
consulted roles
workflow options considered
selected option and reason
rejected options and reason
ZEUS arbitration result
THEMIS veto or clearance
APOLLO quality/evidence status
steps added, removed, skipped or revised
parallel groups and join policy
fallbacks and reset events
limitations and unsupported claims
approval required before external use
```

---

## 18. Final rule

```text
Pantheon workflows are adaptive governance graphs.
ATHENA arranges them.
HEPHAISTOS forges the skills that make them robust.
CHRONOS defines dependencies.
ZEUS arbitrates.
THEMIS blocks unsafe transitions.
APOLLO validates proof and quality.
Hermes executes the resulting Task Contract.
```
