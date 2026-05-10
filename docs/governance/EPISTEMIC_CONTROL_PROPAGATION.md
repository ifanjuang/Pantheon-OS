# EPISTEMIC CONTROL PROPAGATION — Pantheon Next

> Adoption map for applying `EPISTEMIC_CONTROL.md` across Evidence Packs, Task Contracts, Role Signals, Skill Lifecycle and Workflow Adaptation.

---

## 1. Purpose

`EPISTEMIC_CONTROL.md` defines the doctrine.

This document defines where that doctrine is applied across the existing operational governance documents.

It is documentation-only.

It does not create:

```text
runtime
agent loop
tool execution
OpenWebUI action
Hermes binding
memory promotion
skill activation
workflow activation
```

Canonical boundary:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

---

## 2. Adoption map

| Target document | Adoption point | Required effect |
|---|---|---|
| `EVIDENCE_PACK.md` | Claim Register and epistemic summary | Consequential outputs track material claims, uncertainty and unsupported assertions |
| `TASK_CONTRACTS.md` | `epistemic_requirements` block | Task Contracts can require claim-level evidence and contradiction policy |
| `ROLE_SIGNALS.md` | `epistemic_payload` block | Role handoffs preserve claim refs, uncertainty and certainty-change constraints |
| `ROLE_SIGNAL_PROFILES.md` | IRIS formatting hierarchy | IRIS cannot increase certainty or hide limitations while formatting signals |
| `SKILL_LIFECYCLE.md` | `epistemic_contract` manifest block | Skills declare allowed claim types, minimum evidence and forbidden claims |
| `WORKFLOW_ADAPTATION.md` | Source / Uncertainty / Risk / Final Claim gates | Workflow adaptation uses uncertainty as a routing, verification and blocking signal |
| `STATUS.md` | Current global status | Mark claim-level epistemic control as documented, with runtime enforcement not implemented |
| `ROADMAP.md` | P1 governance task | Track operational propagation before any runtime implementation |

---

## 3. Evidence Pack adoption

Status: started.

`EVIDENCE_PACK.md` should treat Claim Register as the place where material assertions are tracked.

Minimum effects:

```text
claim_register added to minimum or extended evidence where consequential
epistemic_summary added to extended evidence where relevant
role signal traceability can reference epistemic_payloads
limitations discipline covers unsupported claims and unjustified certainty increase
```

Evidence Pack rule:

```text
Evidence Pack first. Claim discipline inside the Evidence Pack. Canonization later.
```

---

## 4. Task Contract adoption

Status: pending.

Task Contracts should include an optional `epistemic_requirements` block.

Reference shape:

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
C0-C1 simple tasks may use lightweight claim tracking.
C2-C5 consequential tasks must trace material claims.
C4-C5 outputs must block unsupported material claims unless the user explicitly accepts a draft with limits.
```

---

## 5. Role Signal adoption

Status: pending.

Role Signals should include optional `epistemic_payload` when claim state, uncertainty or approval impact matters.

Reference shape:

```yaml
epistemic_payload:
  claim_refs: []
  weakest_claim_status: asserted | source_supported | tested | inferred_from_sources | conflicting | unsupported | blocked | validated | canonized
  uncertainty_level: none | low | medium | high
  uncertainty_reasons: []
  confidence_may_be_reduced_by_recipient: true
  confidence_may_be_increased_by_recipient: false
  evidence_required_to_increase_confidence: []
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

## 6. Role Signal Profile adoption

Status: pending.

`ROLE_SIGNAL_PROFILES.md` should make the IRIS formatting hierarchy epistemic-safe.

Required rule:

```text
IRIS may improve clarity, structure and audience fit.
IRIS must not increase certainty, remove limitations, soften a veto, lower risk or hide unsupported claims.
```

If formatting would require substantive judgment, the existing `format_blocked` path remains correct.

---

## 7. Skill Lifecycle adoption

Status: started.

`SKILL_LIFECYCLE.md` should require each Pantheon-compatible skill to declare the types of claims it is allowed to produce.

Minimum manifest block:

```yaml
epistemic_contract:
  output_claim_types: []
  minimum_evidence: {}
  forbidden_claims: []
  uncertainty_required_when: []
  escalation_triggers: []
```

Skill rule:

```text
A skill becomes trustworthy through evidence discipline, not confident output.
```

---

## 8. Workflow Adaptation adoption

Status: pending.

`WORKFLOW_ADAPTATION.md` should recognize four epistemic gates:

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

---

## 9. STATUS adoption

Status: pending.

`STATUS.md` should record:

```text
EPISTEMIC_CONTROL.md = documented
Claim Register = documented, runtime enforcement not implemented
Task Contract epistemic_requirements = planned or partially documented
Role Signal epistemic_payload = planned or partially documented
Skill epistemic_contract = partially documented
Workflow epistemic gates = documented target
```

This avoids overstating implementation.

---

## 10. ROADMAP adoption

Status: pending.

`ROADMAP.md` should add a P1 task:

```text
Propagate claim-level epistemic control across Evidence Packs, Task Contracts, Role Signals, Skill Lifecycle and Workflow Adaptation before any runtime implementation.
```

A later P2/P3 task may cover structured-output validation or Hermes-side enforcement, but only after the documentation contracts are stable.

---

## 11. Final rule

```text
Doctrine first.
Schema references second.
Examples third.
Runtime enforcement later, only if needed.
```
