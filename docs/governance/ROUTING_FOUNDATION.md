# ROUTING FOUNDATION — Pantheon Next

> Canonical routing foundation for role / skill / workflow boundaries, request briefs, workflow complexity and light consultation.
>
> This document promotes the stable subset of `GOVERNANCE_ENHANCEMENT_BACKLOG.md` into an operational governance reference.

---

## 1. Doctrine

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

Routing foundation exists to decide the smallest safe way to answer, draft, analyze, review or execute a request.

It must not become:

```text
runtime
scheduler
agent loop
tool runtime
workflow engine
memory promotion engine
automatic prompt router
```

---

## 2. Core taxonomy

Canonical distinction:

```text
Pantheon Role = cognitive or governance responsibility.
Pantheon Skill = bounded reusable method or capability contract.
Workflow = task procedure, often multi-role.
Tool = executable capability.
Hermes skill = executable runtime capability.
Task Contract = bounded execution frame sent to Hermes.
```

Rules:

```text
Roles reason, classify, review, arbitrate and validate.
Skills carry bounded methods.
Workflows organize task procedure.
Tools execute concrete operations.
Hermes executes under Task Contract.
Pantheon governs the method and validation.
OpenWebUI displays and gathers user validation.
```

---

## 3. Role vs Skill Decision Rule

Use a Role when the need is:

```text
judgment
classification
arbitration
approval
veto
uncertainty detection
brief adherence
trajectory supervision
final readiness
```

Use a Skill when the need is:

```text
repeatable method
bounded transformation
structured check
extract / compare / score / format operation
reusable domain procedure
runtime-mappable capability
```

Use a Workflow when the need is:

```text
several roles
ordered steps
parallel checks
source comparison
approval gates
Evidence Pack
section-by-section or lot-by-lot production
persistent or external impact
```

Do not create a new Role for a narrow task that can be represented as a Skill.

Do not create a Skill for a broad governance responsibility that belongs to a Role.

Do not create a Workflow when a single-role path is enough.

---

## 4. Hermes naming boundary

Hermes Agent is the execution runtime.

Hermes Agent is not a Pantheon Role.

If a document uses `HERMES` as an agent-like entry, interpret it as:

```text
Hermes Agent runtime interface
```

not as:

```text
Pantheon cognitive role
```

Future cleanup should remove or rename any abstract `HERMES` role to avoid collision.

---

## 5. Request Brief

Before substantial work, Pantheon should produce or infer a compact Request Brief.

A Request Brief is required when a request is:

```text
ambiguous
multi-domain
source-dependent
risk-sensitive
external-facing
long-form
likely to require workflow
likely to affect memory or files
```

A Request Brief may be implicit for simple requests.

Candidate schema:

```yaml
request_brief:
  original_request: null
  interpreted_intent: null
  domain: general | architecture_fr | software | mixed
  deliverable_type: response | report | dossier | audit | article | cctp | documentation | code_change
  expected_depth: short | standard | complete | expert
  target_reader: null
  risk_level: C0 | C1 | C2 | C3 | C4 | C5
  source_need: none | light | required | critical
  ambiguity_level: low | medium | high
  memory_impact: none | candidate | possible_promotion
  file_impact: none | candidate_patch | persistent_change
  external_use: false
  recommended_mode: direct | single_role | light_workflow | standard_workflow | complex_workflow | critical_workflow
```

Reference roles:

```text
METIS frames the request.
HECATE exposes ambiguity.
ATHENA arranges the method.
THEMIS classifies risk.
APOLLO checks final adherence.
```

---

## 6. Workflow complexity ladder

Workflow complexity depends on the request, not only on the domain.

| Level | Name | Meaning | Typical use |
|---|---|---|---|
| W0 | Direct | No workflow | simple answer, simple rewrite, low-risk factual response |
| W1 | Single-role | One role or one bounded skill | short draft, one approval classification, one source extraction |
| W2 | Light workflow | Few roles, light review | client-facing draft, modest ambiguity, low/moderate risk |
| W3 | Standard workflow | Multiple sources or normal professional review | repo audit, quote review, structured report |
| W4 | Complex workflow | Several gates, contradictions, long deliverable | full dossier, CCTP, contractual analysis, multi-section report |
| W5 | Critical gated workflow | High-risk or persistent/external action | C4/C5, file mutation, memory promotion, external send, runtime activation |

Selection rule:

```text
Start at the smallest safe level.
Escalate only when ambiguity, risk, source dependency, persistence or external impact requires it.
Never use workflow complexity to hide missing evidence.
```

Candidate output:

```yaml
workflow_complexity_decision:
  level: W2
  reason:
    - client_facing_draft
    - liability_wording_risk
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

## 7. Ad hoc Role Consultation

A Pantheon Role may request a bounded consultation from another role outside a formal workflow when the task remains:

```text
simple
low-risk
non-persistent
not externally sent
not memory-promoting
not file-mutating
```

The consulted role returns a signal or recommendation only.

It does not execute.

It does not approve unless it is already the approval owner under `APPROVALS.md`.

It does not promote memory, activate skills or canonize workflows.

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

Escalate to workflow when:

```text
more than 2 or 3 roles are needed
sources must be compared
risk is C3/C4/C5
output is external-facing or contractual
Evidence Pack is required
memory or files are impacted
Hermes must execute tools
```

---

## 8. Role Procedures

A Role Procedure is a repeatable internal checklist for a role.

A Role Procedure is not a Workflow.

Examples:

```text
THEMIS approval_veto_procedure
APOLLO final_gate_procedure
ARGOS source_inventory_procedure
HERA trajectory_review_procedure
CHRONOS freshness_dependency_procedure
```

A Role Procedure may define:

```text
trigger
inputs
checks
outputs
signals
escalation conditions
forbidden actions
```

A Role Procedure must not:

```text
execute tools
mutate files
promote memory
activate skills
bypass Task Contracts
bypass approvals
```

---

## 9. HERA trajectory responsibility

HERA is the trajectory and satisfaction supervisor for substantial requests and complete deliverables.

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
replace THEMIS
replace APOLLO
run tools
```

Canonical split:

```text
HERA keeps the trajectory.
APOLLO decides final readiness.
ZEUS arbitrates changes of course.
THEMIS blocks unsafe action.
```

---

## 10. APOLLO Stop Gate

APOLLO owns final readiness.

A substantial answer or deliverable should not be finalized if:

```text
required sections are missing
major contradictions remain unresolved
scope drift remains visible
unsupported claims are present
required evidence is missing
THEMIS has raised a blocking concern
```

Candidate stop gate:

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

For complete deliverables, the stop gate should reference the deliverable's Definition of Done.

---

## 11. Deliverable routing

A complete deliverable is not a single answer.

Examples:

```text
rapport complet
dossier complet
article long
CCTP complet
audit complet
documentation package
mémoire technique
```

A complete deliverable should route to:

```text
Request Brief
→ Deliverable Contract
→ Production Plan
→ milestones
→ section gates
→ global gate
→ stop gate
→ output package
```

Do not use a long single response when the user asked for a complete governed deliverable.

If the user requests a long improvement session, route to Extended Refinement / Night Run only under a bounded Task Contract and never as Pantheon runtime.

---

## 12. Skill trigger documentation

Every candidate or active skill should document:

```text
Use when
Do not use when
Inputs
Outputs
Forbidden actions
Escalation conditions
Evidence relationship
Approval relationship
Memory relationship
Hermes mapping
```

This rule is especially important for skills that can interrupt the user, broaden context, use external sources, trigger visual assets or influence external-facing outputs.

---

## 13. Final rule

```text
Direct answer when safe.
Single role when enough.
Light workflow when useful.
Complex workflow when necessary.
Critical gated workflow when risk requires it.
Hermes executes only under Task Contract.
Pantheon governs the route, evidence and validation.
```
