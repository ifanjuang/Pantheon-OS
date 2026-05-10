# GOVERNANCE ENHANCEMENT BACKLOG — Pantheon Next

> Candidate backlog extracted from governance discussions.
>
> This document collects ideas that may improve Pantheon Next without turning it into a runtime.

---

## 1. Doctrine

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

This backlog is not an implementation plan.

All items remain candidates until reviewed, scoped and approved.

---

## 2. Role / Skill / Workflow boundary

Canonical distinction:

```text
Agent / Role = cognitive or governance function.
Skill = bounded reusable method.
Workflow = task procedure, often multi-role.
Tool = executable capability.
Runtime skill = executable Hermes capability.
```

Rules:

```text
Agents do not execute tools.
Agents do not mutate files.
Agents do not promote memory.
Skills do not become agents by default.
Workflows belong to tasks, not to agents.
Hermes executes under Task Contracts.
```

Candidate update:

```text
Add a Role vs Skill Decision Rule to AGENTS.md.
Add a Role / Skill / Workflow / Tool taxonomy to MODULES.md or WORKFLOW_SCHEMA.md.
```

---

## 3. Agent responsibility refinements

Candidate refinements:

| Role | Candidate refinement |
|---|---|
| ZEUS | Arbitrates changes of course and unresolved disagreement. |
| ATHENA | Frames strategy and arranges method. |
| ARGOS | Observes facts and sources only. |
| HECATE | Detects ambiguity, hidden risk and insufficient certainty. |
| THEMIS | Owns approvals, vetoes and safety/risk gates. |
| APOLLO | Owns final coherence, evidence quality and stop gate readiness. |
| HERA | Becomes Deliverable Steward and Trajectory Supervisor. |
| CHRONOS | Owns dependencies, freshness, checkpoints and sequence. |
| HEPHAESTUS | Owns method robustness, skill security, tests and rollback thinking. |
| DEMETER | Owns quantities, resources, costs and tabular/economic reviews. |
| POSEIDON | Owns site, water, soil, networks and physical constraints. |
| IRIS | Owns wording, tone and communication drafts only. |
| PROMETHEUS | Owns variants, contradictions and adversarial option search. |
| METIS | Owns tactical simplification and smallest safe path. |
| MNEMOSYNE | Owns system memory candidate review. |
| HESTIA | Owns project memory candidate review. |
| DAEDALUS | Owns system structure, diagrams, boundaries and design patterns. |

Candidate cleanup:

```text
Remove or rename HERMES as an abstract Pantheon Role to avoid collision with Hermes Agent runtime.
Reconcile HEPHAESTUS / HEPHAISTOS spelling.
Prefer refining existing roles before adding new roles.
```

Potential future role:

```text
GAIA may be considered later for carbon, reuse, biodiversity, lifecycle and climate resilience.
Do not add GAIA until those responsibilities become clearly transversal and cannot be handled by POSEIDON, DEMETER, HEPHAESTUS and CHRONOS.
```

---

## 4. Ad hoc Role Consultation

A Pantheon Role may request a bounded consultation from another role outside a formal workflow when the task remains simple, low-risk and non-persistent.

Rules:

```text
The consulted role returns a structured signal or recommendation only.
The consulted role does not execute.
The consulted role does not approve unless it is already the approval owner.
The consulted role does not promote memory.
The consulted role does not activate skills.
The consulted role does not canonize workflows.
```

Escalate to a workflow if:

```text
more than 2 or 3 roles are needed
sources must be compared
risk is C3/C4/C5
output is external-facing or contractual
Evidence Pack is required
memory or files are impacted
Hermes must execute tools
```

Candidate schema:

```yaml
role_consultation:
  from_role: IRIS
  to_role: THEMIS
  reason: possible_contractual_commitment
  question: "Can this wording create unintended responsibility?"
  expected_output:
    - risk_level
    - forbidden_wording
    - safer_wording_guidance
```

---

## 5. Role Procedures

A role may have an internal procedure when its intervention must be repeatable.

A Role Procedure is not a Workflow.

Examples:

```text
THEMIS approval_veto_procedure
APOLLO final_gate_procedure
ARGOS source_inventory_procedure
HERA trajectory_review_procedure
CHRONOS freshness_dependency_procedure
```

A role procedure defines:

```text
trigger
inputs
checks
outputs
signals
escalation conditions
forbidden actions
```

Forbidden:

```text
role procedure executing tools
role procedure mutating files
role procedure promoting memory
role procedure bypassing Task Contracts or approvals
```

---

## 6. Workflow complexity ladder

Workflow complexity should depend on the request, not only on the domain.

Candidate ladder:

| Level | Meaning | Typical use |
|---|---|---|
| W0 | No workflow | simple answer or rewrite |
| W1 | Single-role path | one cognitive function is enough |
| W2 | Light workflow | 2–4 roles, moderate risk |
| W3 | Standard workflow | multiple sources, normal professional review |
| W4 | Complex workflow | contradictions, responsibility, several gates |
| W5 | Critical gated workflow | C4/C5, external action, mutation, memory, high risk |

Rule:

```text
No workflow by default.
One role if sufficient.
Light workflow when useful.
Complex workflow only when necessary.
Critical workflow only when risk imposes it.
```

Candidate output:

```yaml
workflow_complexity_decision:
  level: W2
  reason:
    - client_facing_draft
    - responsibility_risk_low
  selected_roles:
    - IRIS
    - THEMIS
    - APOLLO
  evidence_required: light
  escalation_conditions:
    - external_send_requested
    - contractual_position_detected
```

---

## 7. Request Brief and Request Routing

Before substantial work, Pantheon should create a compact request brief.

Candidate schema:

```yaml
request_brief:
  domain: general | architecture_fr | software | mixed
  intent: null
  deliverable_type: response | report | dossier | audit | article | cctp | documentation
  expected_depth: short | standard | complete | expert
  risk_level: C0 | C1 | C2 | C3 | C4 | C5
  source_need: none | light | required | critical
  ambiguity_level: low | medium | high
  memory_impact: none | candidate | possible_promotion
  external_use: false
  recommended_mode: direct | stepwise | extended_refinement
```

Candidate document:

```text
REQUEST_ROUTING.md or section in WORKFLOW_SCHEMA.md
```

---

## 8. HERA as Deliverable Steward

HERA should supervise trajectory and progress satisfaction.

HERA asks:

```text
Does the work still answer the original request?
Are milestones sufficiently reached?
Is the level of detail adequate?
Should the task continue, pause, change method or escalate to ZEUS?
```

HERA does not:

```text
validate final truth
approve risky actions
replace APOLLO
replace THEMIS
run tools
```

Canonical split:

```text
HERA keeps the trajectory.
APOLLO decides final readiness.
ZEUS arbitrates change of course.
THEMIS blocks unsafe action.
```

---

## 9. Milestone Gates and Stop Gates

A request may contain several milestones.

Candidate statuses:

```text
not_started
in_progress
satisfactory
insufficient
blocked
needs_user_input
requires_cap_change
```

Candidate gate:

```yaml
milestone_gate:
  id: source_inventory
  goal: "Sources are identified or missing sources are explicit."
  owner_role: HERA
  status: satisfactory | insufficient | blocked
  next_action:
    if_satisfactory: continue
    if_insufficient: ask_ARGOS_to_complete
    if_blocked: ask_user_or_ZEUS
```

Stop gate:

```yaml
stop_gate:
  owner_role: APOLLO
  can_stop_if:
    - required_milestones_satisfactory
    - no_themis_veto
    - no_unresolved_major_contradiction
    - final_output_matches_initial_intent
  must_continue_if:
    - missing_required_section
    - unresolved_contradiction
    - duplicated_content
    - unsupported_claim
    - drift_from_user_intent
```

---

## 10. Deliverable Operating Model

A complete deliverable is not a single answer.

A report, dossier, audit, CCTP, long article, documentation package or strategic note should be governed by a Deliverable Contract.

Candidate sequence:

```text
Request Brief
→ Deliverable Contract
→ Production Plan
→ Task Cards
→ Section Gates
→ Global Gate
→ Stop Gate
→ Output Package
```

Candidate Deliverable Contract:

```yaml
deliverable_contract:
  id: DC-YYYY-NNNN
  type: report | dossier | article | cctp | audit | documentation
  owner_role: HERA
  final_gate_owner: APOLLO
  arbitration_owner: ZEUS
  required_sections: []
  milestones: []
  definition_of_done: []
  stop_gate_required: true
```

Candidate production modes:

| Mode | Meaning |
|---|---|
| `direct` | simple response |
| `stepwise` | medium deliverable with plan and review |
| `extended_refinement` | long deliverable with iterations and checkpoints |

Rule:

```text
No premature final answer for complete deliverables.
```

---

## 11. Extended Refinement / Night Run

A user may ask for a long improvement session.

This must be bounded and executed by Hermes under Task Contract, not by Pantheon core.

Candidate schema:

```yaml
extended_refinement_run:
  mode: night_run
  objective: null
  max_duration: user_defined
  max_revision_loops: 6
  checkpoint_interval: each_milestone
  stop_conditions:
    - user_stop
    - definition_of_done_reached
    - max_duration_reached
    - repeated_no_improvement
    - missing_required_input
    - approval_required
  forbidden_actions:
    - external_send
    - memory_promotion
    - file_mutation_without_approval
    - destructive_tool
    - bypass_themis
```

OpenWebUI may expose:

```text
progress view
checkpoint review
stop control
final package preview
```

---

## 12. Deliverable Asset Layer

Complete deliverables may include assets when they clarify, prove, compare or synthesize.

Asset types:

```text
diagram
table
chart
D3.js visualization
image reference
map
annex
bibliography
Evidence map
risk matrix
Gantt / timeline
```

Candidate Asset Plan:

```yaml
asset_plan:
  required_assets:
    - type: diagram
      purpose: explain_workflow
      owner_role: DAEDALUS
    - type: table
      purpose: compare_options
      owner_role: DEMETER
    - type: chart
      purpose: visualize_distribution
      owner_role: DEMETER
  forbidden_assets:
    - unsourced_google_image
    - decorative_chart_without_data
```

Candidate Asset Contract:

```yaml
asset_contract:
  id: ASSET-001
  type: d3_chart
  purpose: null
  data_source: []
  owner_role: DEMETER
  implementation_layer: Hermes
  display_layer: OpenWebUI
  fallback:
    - markdown_table
    - static_svg
  evidence_required: true
```

Rules:

```text
No chart without data source.
No web image as reusable asset unless rights are verified.
No D3.js without fallback.
No external script loading without review.
No asset without purpose.
```

---

## 13. Context Expansion and Research Scope

Pantheon may broaden context only through governed scopes.

Candidate scopes:

```yaml
research_scope:
  narrow:
    sources:
      - uploaded_files
      - selected_project_knowledge
  expanded:
    sources:
      - uploaded_files
      - project_memory
      - selected_openwebui_knowledge
      - official_sources
  broad:
    sources:
      - official_sources
      - web_references
      - image_references
      - academic_or_technical_sources
    requires:
      - source_tier_report
      - freshness_check
      - evidence_pack
```

Rules:

```text
Knowledge is not Memory.
OpenWebUI Knowledge is source material.
Context expansion must be disclosed if consequential.
Sources must be tiered and freshness-checked where relevant.
```

---

## 14. D3.js, charts and visual assets

Candidate skills:

```text
asset_plan_builder
diagram_brief_builder
table_builder
chart_spec_builder
d3_chart_builder
reference_image_search
image_rights_check
visual_evidence_pack
context_expansion
knowledge_broadening
asset_quality_check
```

D3 chart contract:

```yaml
chart_spec:
  chart_type: bar | line | stacked_bar | timeline | sankey | network | gantt
  purpose: null
  data_source: null
  data_status: verified | partial | estimated | unknown
  required_fallback:
    - markdown_table
    - static_svg
  evidence_required: true
```

Forbidden:

```text
invented data
hidden assumptions
external JS without allowlist
interactive chart without static fallback
visual authority without source trace
```

---

## 15. Skill lifecycle improvements

Candidate additions to SKILL_LIFECYCLE.md:

```text
Use when / Do not use when required for every skill.
Benchmark pack required before activation.
Skill loading policy: index first, body only if selected.
Skill filtering / deduplication before activation.
Legacy skills blocked by default.
Candidate skills allowed only with review.
```

Candidate benchmark directory:

```text
domains/{domain}/skills/{skill}/benchmarks/
  cases.yaml
  expected_outputs.yaml
  forbidden_outputs.yaml
```

---

## 16. Evaluation and guardrails

Candidate docs:

```text
EVALUATION.md
GUARDRAIL_REGISTRY.md
```

Candidate tests:

```text
approval classification
Evidence Pack completeness
unsupported claim detection
memory promotion prevention
skill activation prevention
workflow complexity selection
external repository classification
client-facing risk detection
```

Guardrail examples:

```text
no_source_no_claim
no_external_send_without_C4
no_memory_promotion_without_evidence
no_skill_activation_without_review
no_cross_project_knowledge_without_trace
no_docker_socket_by_default
```

Evaluation tools may measure but must not govern.

---

## 17. Run Graph, Handoff and Scorecards

Candidate concepts:

```text
Run Graph
Inline Run Stream
Handoff Protocol
Hermes Result Scorecard
Contradiction Ledger
Freshness Gate
Revision Log
Maturity Score
```

Candidate Hermes Result Scorecard:

```yaml
hermes_result_scorecard:
  source_quality: high | medium | low
  evidence_quality: high | medium | low
  scope_adherence: pass | warning | fail
  approval_alignment: pass | warning | fail
  unsupported_claims: 0
  memory_impact: none | candidate | promotion_requested
  recommended_status: accept_as_draft | request_rerun | block | require_human_review
```

---

## 18. ADRs and durable decisions

Candidate ADRs:

```text
ADR-0001-openwebui-hermes-pantheon-boundary.md
ADR-0002-agents-are-roles-not-workers.md
ADR-0003-knowledge-is-not-memory.md
ADR-0004-no-pantheon-runtime.md
ADR-0005-workflow-complexity-ladder.md
```

Use ADRs for doctrine decisions, not for every minor change.

---

## 19. Branch and PR discipline

Rules extracted from current cleanup:

```text
Do not merge old divergent branches raw.
Create clean branches from current main.
Extract useful files or ideas selectively.
Avoid broad ROADMAP.md rewrites when an addendum is safer.
Log every substantial intervention in ai_logs.
Delete old branches only after content is merged, extracted or explicitly rejected.
```

---

## 20. Candidate next PRs

Suggested PR sequence:

```text
1. agents-routing-foundation
2. workflow-complexity-ladder
3. deliverable-operating-model
4. asset-layer-and-context-expansion
5. skill-lifecycle-benchmarks
6. external-ecosystem-review
7. run-graph-handoff-scorecard
8. evaluation-guardrails
```

Each PR should stay small enough to review.

---

## 21. Final rule

```text
Improve the governance layer.
Do not expand the runtime layer.
```
