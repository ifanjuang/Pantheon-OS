# EPISTEMIC CONTROL — Pantheon Next

> Doctrine for claim-level evidence, uncertainty handling and metacognitive control across Pantheon Roles, Hermes skills, Task Contracts and Evidence Packs.

---

## 1. Purpose

Pantheon Next must not only govern agents, skills and workflows.

It must govern the assertions they produce.

This document defines how Pantheon tracks factual claims, inferred claims, recommendations, uncertainty, confidence, source support, contradictions and approval impact.

Core rule:

```text
A confident sentence is not a validated claim.
```

---

## 2. Boundary

This document does not create:

```text
runtime
agent loop
message bus
truth oracle
model confidence engine
automatic verification engine
automatic memory promotion
```

It defines a governance contract.

Canonical boundary:

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

---

## 3. Why this exists

LLM failures are not only factual errors.

The dangerous failure mode is an unsupported or false claim expressed with inappropriate certainty.

In an agentic system, uncertainty must therefore control:

```text
when to answer
when to search
when to call a tool
when to consult another role
when to request user input
when to escalate approval
when to block finalization
```

Pantheon implements this as documentation and contract discipline, not as a new autonomous runtime layer.

---

## 4. Core principles

```text
Confidence is not evidence.
Evidence can support a claim without making it final.
A claim can be useful while remaining uncertain.
A role may lower certainty without new evidence.
A role may not increase certainty without new evidence.
A handoff must preserve uncertainty, limitations and risk flags.
A final answer must not be more certain than its weakest material claim.
```

Strong form:

```text
No certainty increase across summary, reformulation, handoff, AGORA consultation or final answer unless new evidence is attached.
```

---

## 5. Claim Register

The Claim Register is a structured list of material assertions produced during a task.

It belongs in the Evidence Pack when the task is consequential.

It does not replace existing Evidence Pack fields such as:

```text
files_read
sources_used
documents_used
assumptions
unsupported_claims
limitations
approval_required
next_safe_action
```

It refines them at claim level.

### 5.1 Claim schema

```yaml
claim_register:
  - claim_id: CL-YYYY-NNNN
    claim_text: ""
    claim_type: factual_observation | extraction_result | comparison_result | calculation | interpretation | risk_inference | recommendation | decision_candidate | memory_candidate | patch_candidate
    owner_role: ARGOS
    produced_by:
      skill: null
      workflow_step: null
      tool: null
    status: asserted | source_supported | tested | inferred_from_sources | conflicting | unsupported | blocked | validated | canonized
    evidence_refs: []
    source_tier: null
    reliability_level: null
    confidence:
      declared: low | medium | high
      basis: direct_source | repeated_extraction | calculation | inference | role_judgment | model_statement | unknown
    uncertainty:
      level: none | low | medium | high
      type:
        - missing_source
        - ambiguous_request
        - conflicting_sources
        - stale_source
        - incomplete_input
        - tool_failure
        - policy_conflict
        - domain_boundary_unclear
        - normative_uncertainty
      notes: []
    assumptions: []
    limitations: []
    contradictions: []
    approval_impact: C0 | C1 | C2 | C3 | C4 | C5
    memory_impact: none | candidate_only | promotion_review
    next_action: answer | verify | ask_user | consult_role | request_approval | block | stop
```

### 5.2 Claim status meanings

| Status | Meaning |
|---|---|
| `asserted` | Stated by a model, role or skill but not yet supported |
| `source_supported` | Supported by one or more identified sources |
| `tested` | Supported by command, test, check or reproducible operation |
| `inferred_from_sources` | Derived from sources but not directly stated by them |
| `conflicting` | Contradicted by another source, role, memory item or result |
| `unsupported` | Material claim lacking support |
| `blocked` | Cannot be used safely without missing evidence or approval |
| `validated` | Reviewed and accepted under the required approval path |
| `canonized` | Promoted into Pantheon source of truth, memory or active governance |

Rules:

```text
asserted is never enough for consequential output.
inferred_from_sources must expose its inference path.
conflicting claims must trigger ZEUS/THEMIS/APOLLO handling before finalization.
validated does not imply reusable memory.
canonized requires the relevant governance path.
```

---

## 6. Role Signal epistemic payload

Role Signals may carry claim references and uncertainty state.

This prevents uncertainty loss during handoff.

```yaml
role_signal:
  id: RS-YYYY-NNNN
  from_role: ARGOS
  to_role: THEMIS
  type: risk_warning
  content_summary: "A material claim may affect approval level."
  epistemic_payload:
    claim_refs: []
    weakest_claim_status: asserted | source_supported | tested | inferred_from_sources | conflicting | unsupported | blocked | validated | canonized
    uncertainty_level: none | low | medium | high
    uncertainty_reasons: []
    confidence_may_be_reduced_by_recipient: true
    confidence_may_be_increased_by_recipient: false
    evidence_required_to_increase_confidence: []
  requested_action: review | comment | continue | escalate | block | arbitrate
  risk_level: C0
```

Rules:

```text
IRIS may format the signal but must not improve claim status.
The receiving role may challenge or lower certainty.
The receiving role may increase certainty only by attaching new evidence.
Risk level must not be lowered through mediation.
Limitations must survive every handoff.
```

---

## 7. Skill epistemic contract

Every Pantheon-compatible skill should eventually declare what it is allowed to claim.

This belongs in the skill `manifest.yaml`.

```yaml
epistemic_contract:
  output_claim_types:
    - factual_observation
    - extraction_result
    - comparison_result
    - risk_inference
    - recommendation
  minimum_evidence:
    factual_observation: source_ref_required
    extraction_result: document_ref_required
    comparison_result: two_source_refs_required
    calculation: formula_or_input_ref_required
    risk_inference: source_or_claim_ref_required
    recommendation: assumptions_and_limits_required
  forbidden_claims:
    - final_contractual_validation
    - final_legal_conclusion
    - final_memory_promotion
    - active_skill_approval
    - workflow_canonization
  uncertainty_required_when:
    - missing_primary_source
    - conflicting_sources
    - stale_reference
    - incomplete_input
    - tool_failure
    - cross_project_context
    - policy_boundary_unclear
  escalation_triggers:
    - unsupported_claim_with_C3_or_above_impact
    - contradiction_between_T0_and_lower_source
    - client_facing_output
    - memory_candidate
    - skill_gap_detected
```

Rules:

```text
A skill cannot become an authority by producing confident wording.
A skill may propose, extract, compare, calculate, flag or recommend only within its epistemic contract.
A skill that exceeds its contract must be treated as producing unsupported claims.
```

---

## 8. Task Contract epistemic requirements

Task Contracts should be able to require claim-level evidence.

```yaml
epistemic_requirements:
  claim_register_required: true
  minimum_claim_status_for_final: source_supported
  allow_inferred_claims: true
  unsupported_claim_policy: list_and_limit | block_final | ask_user | request_sources
  contradiction_policy: zeus_arbitration_required
  uncertainty_policy:
    expose_uncertainty: true
    require_uncertainty_type: true
    require_next_action_for_high_uncertainty: true
  final_answer_policy:
    no_certainty_increase_without_evidence: true
    display_material_limitations: true
```

Rules:

```text
For C0-C1 simple answers, claim-level tracking may remain lightweight.
For consequential C2-C5 work, material claims must be traceable.
For C4-C5 output, unsupported material claims block finalization.
```

---

## 9. Workflow gates

Workflow adaptation should use four epistemic gates when needed.

| Gate | Primary role | Purpose |
|---|---|---|
| Source Gate | ARGOS | Identify sources, missing sources, source tiers and source conflicts |
| Uncertainty Gate | HECATE | Identify ambiguity, unknowns and failure modes |
| Risk Gate | THEMIS | Convert uncertainty and action impact into approval level or veto |
| Final Claim Gate | APOLLO | Verify that final wording does not overstate weak claims |

Default activation:

| Risk | Gates |
|---|---|
| C0-C1 simple | Source Gate if source-dependent |
| C1 with assumptions | Source Gate + Final Claim Gate |
| C2-C3 | Source Gate + Uncertainty Gate + Risk Gate |
| C4-C5 | All gates + explicit human validation |

Rules:

```text
The gates are governance checks, not runtime workers.
They may be represented as role steps in a workflow or as review responsibilities in an Evidence Pack.
```

---

## 10. Role responsibilities

| Role | Epistemic responsibility |
|---|---|
| METIS | Frames request intent, ambiguity, context need and answer strategy |
| ARGOS | Owns source inventory, fact extraction and source-supported claims |
| HECATE | Owns ambiguity, uncertainty, hidden risks and failure modes |
| PROMETHEUS | Searches contradictions, edge cases and alternative interpretations |
| HEPHAESTUS | Checks method robustness, skill gaps, tests and rollback needs |
| THEMIS | Converts risk and uncertainty into approval, veto or safer path |
| APOLLO | Blocks final answers that overstate evidence or hide limitations |
| IRIS | Reformulates without increasing certainty or hiding limitations |
| ZEUS | Arbitrates conflicting options without bypassing evidence or approval |
| HESTIA | Reviews project-memory relevance without promoting memory |
| MNEMOSYNE | Reviews system-memory relevance without promoting memory |

---

## 11. OpenWebUI display

OpenWebUI should display a concise summary, not the full internal machinery.

Recommended user-facing fields:

```text
result
key evidence
unsupported material claims
assumptions
limitations
contradictions
approval required
blocked actions
next safe action
```

OpenWebUI must not treat the Claim Register as canonical memory.

---

## 12. Memory relationship

A claim may become a memory candidate.

It does not become memory by being listed in the Claim Register.

Promotion remains:

```text
claim
→ memory candidate
→ Evidence Pack
→ THEMIS/APOLLO review
→ C3+ approval
→ project or system memory
```

Rules:

```text
Validated claim is not automatically memory.
Memory candidate is not canonical memory.
Canonized memory requires the memory promotion path.
```

---

## 13. Forbidden drift

Do not implement:

```text
metacognition agent as runtime authority
automatic truth scoring
automatic claim canonization
automatic confidence upgrade
hidden role debate to resolve truth
OpenWebUI memory canonization
Hermes self-approval
skill self-activation
workflow self-canonization
```

---

## 14. Implementation sequence

Recommended sequence:

```text
1. Add Claim Register to Evidence Pack doctrine.
2. Add epistemic_requirements to Task Contracts.
3. Add epistemic_payload to Role Signals.
4. Add epistemic_contract to Skill Lifecycle manifests.
5. Add Source/Uncertainty/Risk/Final Claim gates to workflow examples.
6. Add OpenWebUI display expectations for unsupported claims and limitations.
```

Do not start with code.

Start with documentation contracts and examples.

---

## 15. Final rule

```text
Pantheon does not trust confidence.
Pantheon traces claims.
Hermes executes under contract.
OpenWebUI displays evidence and limits.
Canonization happens only after proof and approval.
```
