# ROLE SIGNAL PROFILES — Pantheon Next

> Canonical recipient profiles for structured role-to-role messages.
>
> IRIS should use local agent profiles when available, then this central profile registry, before asking a role to remind the expected message format.

---

## 1. Doctrine

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

Role Signal Profiles define the expected form of a message addressed to a Pantheon Role.

They do not implement:

```text
runtime message bus
agent loop
approval authority
memory promotion
workflow engine
tool execution
truth oracle
```

Canonical split:

```text
ROLE_SIGNALS.md = shared protocol.
ROLE_SIGNAL_PROFILES.md = central profile registry and invariants.
agents/{ROLE}/role_signal_profile.yaml = local usage profile for one role.
```

---

## 2. Purpose

A signal sent to THEMIS should not be shaped like a signal sent to ARGOS.

A signal sent to APOLLO should not omit final-readiness criteria.

A signal sent to ZEUS should clearly expose the decision point.

A signal sent through IRIS should not become more certain, less risky or less limited because it was reformatted.

`ROLE_SIGNAL_PROFILES.md` gives IRIS and future validators a stable reference before formatting an addressed signal.

Core rule:

```text
Use the local profile first when it exists.
Use the central profile when no local profile exists.
Ask for a format reminder only if the profile is insufficient.
Block if the reminder would require a substantive decision.
```

---

## 2b. Central schema and local profiles

The Role Signal schema remains centralized in:

```text
docs/governance/ROLE_SIGNALS.md
```

The epistemic rules remain centralized in:

```text
docs/governance/EPISTEMIC_CONTROL.md
```

The profile for a specific role may live in the agent folder:

```text
agents/{ROLE}/role_signal_profile.yaml
```

This document remains the central index and invariant policy for those local profiles.

Rules:

```text
A local role_signal_profile.yaml describes how the role uses Role Signals.
It must not redefine the Role Signal schema.
It must not redefine epistemic rules.
It must reference ROLE_SIGNALS.md and EPISTEMIC_CONTROL.md.
It may define emitted signal types, received signal types, required payloads, forbidden behaviors, escalation triggers and public summary rules.
It may be more specific than this document.
It must not be less restrictive than this document.
```

If a local profile conflicts with the central schema or governance doctrine, the central governance documents win.

---

## 2c. Why profiles may live in agent folders

Profiles are role-specific maintenance files.

Keeping them inside each agent folder is useful because the profile evolves with the agent responsibility:

```text
ARGOS evolves with source and evidence work.
THEMIS evolves with approval and veto policy.
APOLLO evolves with final readiness checks.
IRIS evolves with formatting and audience adaptation.
HEPHAESTUS evolves with skills, tests and rollback discipline.
```

The protocol should not be copied into each agent.

The profile should be local.

The distinction is:

```text
Protocol = one central schema.
Profile = one role-specific usage contract.
```

This avoids two bad outcomes:

```text
one huge central file that becomes painful to maintain;
many local copies of the schema that drift apart.
```

---

## 2d. Local profile lifecycle

A local profile is documentation and governance metadata, not executable runtime configuration.

Allowed states:

```text
missing
candidate
active
needs_review
deprecated
```

Recommended interpretation:

| State | Meaning |
|---|---|
| `missing` | No local profile exists; IRIS uses the central fallback profile |
| `candidate` | Local profile proposed but not yet accepted as reference |
| `active` | Local profile is the preferred reference for that role |
| `needs_review` | Local profile may be stale after governance changes |
| `deprecated` | Local profile kept for history, no longer preferred |

Rules:

```text
A missing local profile is acceptable.
A stale local profile must not override central governance.
A local profile change that weakens constraints requires review.
A local profile change that only adds specificity may be accepted as documentation.
```

---

## 2e. Local profile minimal shape

A local agent profile should use this shape when agent folders are materialized.

```yaml
agent: ARGOS
profile_type: role_signal_profile
profile_status: candidate
canonical_schema: docs/governance/ROLE_SIGNALS.md
epistemic_reference: docs/governance/EPISTEMIC_CONTROL.md
profile_index: docs/governance/ROLE_SIGNAL_PROFILES.md

role_scope:
  primary_function: "Source and fact observation."
  does_not_do:
    - final_approval
    - memory_promotion
    - tool_execution

emits:
  - information_transmission
  - source_gap_signal
  - risk_warning

receives:
  - clarification_request
  - handoff_signal
  - role_consultation

required_payloads:
  - evidence_refs
  - epistemic_payload
  - assumptions
  - limitations

must_preserve:
  - risk_level
  - limitations
  - weakest_claim_status
  - uncertainty_level
  - veto_status
  - stop_gate_status

can_lower_certainty: true
can_increase_certainty: false
certainty_increase_requires:
  - new_source
  - new_test
  - new_evidence_ref

forbidden:
  - execute_tool
  - approve_external_action
  - promote_memory
  - activate_skill
  - canonize_workflow
  - mutate_file
  - send_external_message
  - increase_claim_certainty_without_evidence
  - remove_unsupported_claims

escalation_conditions:
  - conflicting_sources
  - missing_primary_source
  - C3_or_above_impact

public_summary:
  allowed: true
  must_avoid:
    - raw_private_reasoning
    - hidden_prompt
    - secret
    - private_project_data
    - unsupported_conclusion
```

---

## 2f. Local profile fields

| Field | Required | Purpose |
|---|---:|---|
| `agent` | yes | Pantheon Role name |
| `profile_type` | yes | Must be `role_signal_profile` |
| `profile_status` | yes | `candidate`, `active`, `needs_review`, `deprecated` |
| `canonical_schema` | yes | Points to `docs/governance/ROLE_SIGNALS.md` |
| `epistemic_reference` | yes | Points to `docs/governance/EPISTEMIC_CONTROL.md` |
| `profile_index` | yes | Points to this document |
| `role_scope` | yes | What the role does and explicitly does not do |
| `emits` | yes | Signal types this role may emit |
| `receives` | yes | Signal types this role may receive |
| `required_payloads` | yes | Payloads required for useful review |
| `must_preserve` | yes | Values that cannot be lost during mediation |
| `can_lower_certainty` | yes | Whether the role can downgrade claim confidence/status |
| `can_increase_certainty` | yes | Whether the role may upgrade certainty at all |
| `certainty_increase_requires` | yes | Evidence required before any upgrade |
| `forbidden` | yes | Behaviors the local profile cannot authorize |
| `escalation_conditions` | yes | Conditions that require another role, approval or stop gate |
| `public_summary` | yes | Rules for Run Graph / Inline Run Stream display |

---

## 2g. Profile resolution order

When IRIS or a future validator needs to format a signal, profile resolution should follow this order:

```text
1. If agents/{ROLE}/role_signal_profile.yaml exists and is active, use it.
2. If the local profile exists but is candidate or needs_review, use it as advisory only.
3. If no usable local profile exists, use the canonical fallback profile in this document.
4. If the profile is insufficient, ask for a format reminder.
5. If the format reminder requires judgment, risk classification, approval or arbitration, block formatting and route to the competent role.
```

A local profile may narrow what a role accepts.

A local profile may not expand authority beyond central governance.

---

## 2h. Valid local refinements

A local profile may add:

```text
more precise required fields;
role-specific forbidden fields;
role-specific escalation triggers;
role-specific public summary templates;
role-specific handoff expectations;
role-specific evidence requirements;
role-specific examples.
```

A local profile must not add:

```text
new execution powers;
authority to approve actions;
authority to promote memory;
authority to activate skills;
authority to canonize workflows;
authority to bypass THEMIS;
authority to bypass APOLLO;
authority to increase certainty without evidence;
authority to expose raw private reasoning.
```

---

## 2i. Local profile examples

### ARGOS local profile intent

ARGOS should be strict on facts, sources and missing evidence.

A local ARGOS profile should usually require:

```text
evidence_refs
source_boundary
missing_sources
claim_refs
epistemic_payload
limitations
```

ARGOS may lower certainty when sources are weak or missing.

ARGOS may increase certainty only when a new source, document, command or evidence reference is attached.

### THEMIS local profile intent

THEMIS should be strict on approval, forbidden transitions and responsibility exposure.

A local THEMIS profile should usually require:

```text
action_at_risk
approval_level
forbidden_action
safer_path
epistemic_payload
approval_impact
```

THEMIS may veto.

THEMIS must not soften risk for readability.

### IRIS local profile intent

IRIS should be strict on wording, audience and preservation of substance.

A local IRIS profile should usually require:

```text
audience
intent
tone
constraints
forbidden_wording_if_known
risk_level
epistemic_payload
```

IRIS may improve clarity.

IRIS must not improve truth.

### APOLLO local profile intent

APOLLO should be strict on final readiness.

A local APOLLO profile should usually require:

```text
completeness_status
contradictions
unsupported_claims
evidence_status
limitations_to_display
stop_gate_decision
weakest_claim_status
```

APOLLO may block finalization when the answer overstates weak evidence.

---

## 3. IRIS formatting hierarchy

IRIS should apply this hierarchy:

```text
1. Use the local agent profile when available and active.
2. If no active local profile exists, use the canonical Role Signal Profile in this document.
3. If the known profile is insufficient, send a format_reminder_request.
4. If the response only returns structure, format the signal.
5. If the response requires judgment, risk classification, approval or arbitration, stop and route to the competent role.
```

This prevents IRIS from inventing the recipient's needs while also preventing a free-form role debate.

IRIS must not use a local profile to bypass the central schema, lower risk, hide limitations or increase claim certainty without evidence.

---

## 4. Format reminder request

IRIS may ask the addressed role to remind the expected format.

A format reminder is about structure only.

It is not a decision.

```yaml
format_reminder_request:
  id: FRR-YYYY-NNNN
  from_role: IRIS
  to_role: THEMIS
  purpose: "Remind the expected structure for a risk review signal."
  context_summary: "A draft may imply validation of a contractor quote."
  expected_output:
    - required_fields
    - forbidden_fields
    - escalation_conditions
  constraints:
    no_decision: true
    no_approval: true
    no_execution: true
    no_memory_promotion: true
    no_tool_call: true
    no_external_send: true
    no_certainty_increase_without_evidence: true
```

Allowed response:

```yaml
format_reminder_response:
  id: FRR-YYYY-NNNN-RESPONSE
  from_role: THEMIS
  to_role: IRIS
  required_fields:
    - action_at_risk
    - approval_level
    - forbidden_transition
    - safer_alternative
  forbidden_fields:
    - final_approval_claim
    - softened_risk
    - missing_limitation
    - certainty_upgrade
  escalation_conditions:
    - C3_or_above
    - external_use
    - contractual_or_financial_impact
  no_decision: true
```

Forbidden response:

```yaml
format_reminder_response:
  decision: "Approved"
  risk_level: "C1"
  final_wording: "Send this to the client."
```

---

## 5. Format blocked

If a format reminder would require the addressed role to decide, IRIS must stop and route the task.

```yaml
format_blocked:
  from_role: IRIS
  reason: "The requested format requires substantive risk classification."
  blocked_action: format_signal
  next_role: THEMIS
  next_action: "THEMIS must classify risk directly."
  escalation_required: true
```

Examples of blocked cases:

```text
THEMIS must classify risk.
APOLLO must decide stop gate readiness.
ZEUS must arbitrate options.
ARGOS must verify a source.
DEMETER must calculate or review quantities.
MNEMOSYNE must evaluate memory candidate scope.
A local profile would require changing claim status.
A local profile would require lowering risk.
```

---

## 6. Canonical recipient profiles

The profiles below are fallback canonical profiles.

When local agent profiles exist, they may refine these structures but must preserve the same invariants.

### 6.1 ZEUS — arbitration profile

Use when a decision, route change or conflict must be arbitrated.

```yaml
ZEUS:
  default_profile: arbitration
  required_fields:
    - decision_needed
    - available_options
    - tradeoffs
    - blocked_paths
    - recommended_route
    - approval_impacts
  forbidden_fields:
    - raw_debate
    - hidden_vote
    - unresolved_veto
    - unsupported_recommendation
    - certainty_upgrade_without_evidence
  escalation_conditions:
    - conflicting_role_outputs
    - workflow_revision_signal
    - C3_or_above_route_change
```

### 6.2 METIS — request framing profile

Use when intent, implicit need or initial route is unclear.

```yaml
METIS:
  default_profile: request_framing
  required_fields:
    - original_request
    - interpreted_intent
    - implicit_needs
    - ambiguity_points
    - smallest_safe_path
  forbidden_fields:
    - premature_solution
    - unbounded_workflow
    - unsupported_assumption
  escalation_conditions:
    - multi_domain_request
    - ambiguous_external_use
    - user_intent_conflict
```

### 6.3 ATHENA — method and route profile

Use when a task needs structure, method, sequencing or workflow design.

```yaml
ATHENA:
  default_profile: method_route
  required_fields:
    - task_intent
    - available_inputs
    - proposed_method
    - role_sequence
    - workflow_complexity_level
    - dependencies
  forbidden_fields:
    - raw_findings_without_structure
    - route_without_risk_check
  escalation_conditions:
    - W3_or_above
    - missing_required_input
    - deliverable_contract_needed
```

### 6.4 ARGOS — source and fact profile

Use when a role needs facts, sources, extraction or source-gap detection.

```yaml
ARGOS:
  default_profile: source_fact_request
  required_fields:
    - source_needed
    - factual_question
    - expected_extraction
    - source_boundary
    - missing_material_to_report
    - epistemic_payload
  forbidden_fields:
    - opinion_request
    - final_conclusion_request
    - unsupported_inference
  escalation_conditions:
    - source_conflict
    - current_source_required
    - missing_primary_source
```

### 6.5 HECATE — uncertainty profile

Use when hidden ambiguity, uncertainty or blind spots may alter the answer.

```yaml
HECATE:
  default_profile: uncertainty_review
  required_fields:
    - claim_or_route_under_review
    - uncertainty_points
    - hidden_risks
    - assumptions
    - possible_failure_modes
    - weakest_claim_status
  forbidden_fields:
    - false_certainty
    - hidden_assumption
    - minimized_unknown
  escalation_conditions:
    - unresolved_material_ambiguity
    - unknown_source_boundary
    - high_cost_if_wrong
```

### 6.6 THEMIS — risk and approval profile

Use when risk, approval, veto, external action or responsibility must be assessed.

```yaml
THEMIS:
  default_profile: risk_review
  required_fields:
    - action_at_risk
    - approval_level
    - forbidden_action
    - liability_or_policy_exposure
    - safer_path
    - escalation_required
    - epistemic_payload
  forbidden_fields:
    - final_approval_claim
    - softened_risk
    - missing_limitation
    - approval_by_majority
    - certainty_upgrade_without_evidence
  escalation_conditions:
    - C3_or_above
    - external_send
    - file_mutation
    - memory_promotion
    - runtime_activation
    - legal_financial_or_contractual_impact
```

### 6.7 APOLLO — final readiness profile

Use when coherence, completeness, evidence quality or finalization is at stake.

```yaml
APOLLO:
  default_profile: final_readiness
  required_fields:
    - completeness_status
    - contradictions
    - unsupported_claims
    - evidence_status
    - limitations_to_display
    - stop_gate_decision
    - weakest_claim_status
  forbidden_fields:
    - finalization_without_limits
    - ignored_themis_veto
    - hidden_uncertainty
    - certainty_upgrade_without_evidence
  escalation_conditions:
    - missing_required_section
    - unresolved_contradiction
    - unsupported_claim
    - themis_veto_present
```

### 6.8 HERA — trajectory profile

Use for progress satisfaction, milestone state and whether to continue, pause or change route.

```yaml
HERA:
  default_profile: trajectory_review
  required_fields:
    - original_intent
    - current_milestone
    - milestone_status
    - satisfaction_gap
    - continue_pause_or_reroute_signal
  forbidden_fields:
    - isolated_fact_without_progress_meaning
    - final_truth_validation
  escalation_conditions:
    - repeated_no_improvement
    - milestone_blocked
    - drift_from_request
```

### 6.9 CHRONOS — dependency and time profile

Use for sequencing, waits, joins, freshness and timing.

```yaml
CHRONOS:
  default_profile: dependency_review
  required_fields:
    - steps_involved
    - dependencies
    - blockers
    - wait_conditions
    - join_policy
    - freshness_or_deadline_constraints
  forbidden_fields:
    - unordered_request
    - dependency_hidden_as_assumption
  escalation_conditions:
    - blocked_dependency
    - outdated_source
    - parallel_step_conflict
```

### 6.10 HEPHAESTUS — robustness and skill profile

Use for technical robustness, skill gaps, tests, rollback and method hardening.

```yaml
HEPHAESTUS:
  default_profile: method_robustness
  required_fields:
    - method_under_review
    - weakness_or_gap
    - required_skill_or_test
    - rollback_need
    - activation_risk
    - epistemic_contract_impact
  forbidden_fields:
    - vague_improvement_request
    - activation_without_review
    - missing_rollback
  escalation_conditions:
    - skill_activation_requested
    - external_tool_needed
    - tests_missing_for_consequential_use
```

### 6.11 DEMETER — quantities and resources profile

Use for costs, quantities, resources, units, tabular review and economic assumptions.

```yaml
DEMETER:
  default_profile: quantity_resource_review
  required_fields:
    - quantity_or_cost_object
    - units
    - assumptions
    - missing_quantities
    - economic_or_resource_question
    - source_or_estimate_status
  forbidden_fields:
    - unquantified_claim
    - final_price_certainty_without_source
  escalation_conditions:
    - missing_units
    - conflicting_quantities
    - estimate_presented_as_verified
```

### 6.12 POSEIDON — site and physical constraints profile

Use for site, water, networks, soil, climate, environment and physical constraints.

```yaml
POSEIDON:
  default_profile: physical_constraint_review
  required_fields:
    - site_or_environment_object
    - physical_constraint
    - source_or_observation
    - impact_on_method
    - unresolved_site_unknowns
  forbidden_fields:
    - abstract_strategy_without_site_constraint
    - hidden_environmental_assumption
  escalation_conditions:
    - water_or_network_conflict
    - unknown_soil_or_site_condition
    - environmental_or_regulatory_constraint
```

### 6.13 PROMETHEUS — variants and contradiction profile

Use for alternatives, edge cases, adversarial review and contradiction search.

```yaml
PROMETHEUS:
  default_profile: alternatives_contradictions
  required_fields:
    - primary_option
    - alternative_options
    - contradiction_to_test
    - edge_cases
    - failure_modes
  forbidden_fields:
    - single_option_framing
    - novelty_without_usefulness
  escalation_conditions:
    - several_valid_options
    - high_cost_wrong_route
    - contradiction_between_sources
```

### 6.14 IRIS — wording and communication profile

Use for tone, audience, wording and communication constraints.

```yaml
IRIS:
  default_profile: communication_formatting
  required_fields:
    - audience
    - intent
    - tone
    - constraints
    - forbidden_wording_if_known
    - epistemic_payload
  forbidden_fields:
    - unresolved_risk_without_themis_signal
    - external_send_claim
    - certainty_upgrade
    - hidden_limitation
  escalation_conditions:
    - client_facing_risk
    - legal_or_contractual_wording
    - approval_required_before_send
```

### 6.15 HESTIA — project memory profile

Use for project-specific context and project memory relevance.

```yaml
HESTIA:
  default_profile: project_memory_relevance
  required_fields:
    - project_scope
    - candidate_project_fact
    - source
    - confidence
    - why_project_specific
    - evidence_pack_ref
  forbidden_fields:
    - system_generalization
    - unsupported_project_fact
  escalation_conditions:
    - project_memory_candidate
    - cross_project_contamination_risk
```

### 6.16 MNEMOSYNE — system memory profile

Use for reusable system patterns, doctrine and system memory candidates.

```yaml
MNEMOSYNE:
  default_profile: system_memory_candidate
  required_fields:
    - reusable_rule_or_pattern
    - source_evidence
    - scope
    - confidence
    - conflict_check
    - evidence_pack_ref
  forbidden_fields:
    - local_project_detail_as_universal_rule
    - memory_promotion_claim
  escalation_conditions:
    - system_memory_candidate
    - conflict_with_existing_memory
    - missing_evidence_pack
```

### 6.17 DAEDALUS — structure and diagram profile

Use for systems, schemas, boundaries, diagrams and architecture patterns.

```yaml
DAEDALUS:
  default_profile: structural_design
  required_fields:
    - system_or_schema_object
    - boundary
    - components
    - relationships
    - diagram_or_structure_need
  forbidden_fields:
    - vague_conceptual_drift
    - hidden_runtime_boundary_change
  escalation_conditions:
    - architecture_boundary_risk
    - diagram_needed_for_clarity
    - runtime_boundary_ambiguity
```

---

## 7. Public summaries

Profiles may support public Run Graph summaries, but public summaries must never include private reasoning or sensitive data.

Allowed:

```text
IRIS : Je reformule le signal pour THEMIS avec les limites et le niveau de risque visibles.
```

Forbidden:

```text
IRIS : raw private reasoning, hidden prompts, full file paths, secrets, client data or unsupported conclusions.
```

Local profiles may define public summary templates, but they must preserve the same privacy and evidence limits.

---

## 8. Final rule

```text
Profiles define expected structure.
Local profiles may live in agents/{ROLE}/role_signal_profile.yaml.
Local profiles describe usage; they do not redefine the protocol.
Local profiles may narrow authority; they may not expand it.
Format reminders repair missing structure.
Format reminders do not decide.
IRIS formats.
IRIS improves clarity, not truth.
The source role owns substance.
The addressed role owns response.
THEMIS owns risk.
APOLLO owns readiness.
ZEUS owns arbitration.
Hermes executes only under Task Contract.
```
