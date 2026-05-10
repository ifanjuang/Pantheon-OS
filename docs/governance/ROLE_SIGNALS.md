# ROLE SIGNALS — Pantheon Next

> Canonical schema for structured communication between Pantheon Roles.
>
> Roles may consult other roles. They do not chat freely, execute tools, mutate files or bypass governance.

---

## 1. Doctrine

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

Pantheon Roles are cognitive and governance roles.

They may communicate through structured signals.

They must not form a hidden autonomous agent network.

---

## 2. Purpose

`ROLE_SIGNALS.md` defines how a role may ask, inform, request review, transfer a bounded result or escalate to another role.

It supports:

```text
ad hoc role consultation
workflow dependency handoff
AGORA bounded consultation
Run Graph visibility
Evidence Pack traceability
Task Contract revision signals
```

It does not implement:

```text
runtime message bus
scheduler
agent loop
tool execution
memory promotion
approval bypass
```

---

## 3. Ownership model

No single role owns all transmission.

Responsibilities:

| Responsibility | Owner |
|---|---|
| Decide whether consultation is needed | METIS / ATHENA |
| Organize role order and graph | ATHENA |
| Define dependencies, waits and joins | CHRONOS |
| Transfer factual findings | ARGOS |
| Escalate uncertainty | HECATE |
| Escalate risk or veto | THEMIS |
| Request final readiness review | APOLLO |
| Arbitrate disagreement or change of course | ZEUS |
| Format role-to-role signals and user-facing wording | IRIS |
| Execute runtime transport under Task Contract | Hermes Agent |
| Display state and validation to user | OpenWebUI |
| Govern schema, evidence and limits | Pantheon Next |

Canonical split:

```text
ATHENA organizes the route.
CHRONOS manages dependency timing.
ZEUS arbitrates.
THEMIS blocks unsafe signals.
APOLLO validates final readiness.
IRIS formats addressed signals.
Hermes transports/executes runtime work under Task Contract.
Pantheon governs the signal schema and limits.
```

---

## 4. IRIS signal mediation

IRIS may be invoked to transform an intent, finding, warning, question or handoff into a structured message adapted to the addressed role.

IRIS is a formatter and clarity mediator.

IRIS is not:

```text
message bus
runtime dispatcher
approval authority
memory authority
workflow engine
AGORA replacement
Hermes replacement
```

IRIS may:

```text
shape a signal for the addressed role
choose the correct signal type
reduce ambiguity in the message
remove irrelevant detail
preserve limitations and risk flags
request a safer signal format
prepare a public Run Graph summary
prepare a user-facing summary after validation
```

IRIS must not:

```text
change the factual content of ARGOS findings
lower THEMIS risk level
weaken an APOLLO stop gate
hide HECATE uncertainty
choose ZEUS arbitration result
execute Hermes tools
send external messages
promote memory
activate skills
```

Canonical rule:

```text
IRIS formats the signal.
The sender owns the substance.
The addressed role owns its response.
THEMIS owns risk.
APOLLO owns final readiness.
ZEUS owns arbitration.
```

---

## 5. Addressed signal profiles

A signal should be shaped according to the addressed role.

| Addressed role | Signal should emphasize | Avoid |
|---|---|---|
| ZEUS | decision needed, options, conflict, arbitration request | excessive detail without decision point |
| METIS | request intent, ambiguity, implicit needs, routing uncertainty | premature solution |
| ATHENA | method, structure, dependencies, route proposal | raw unstructured findings |
| ARGOS | source need, factual question, extraction target | opinion-heavy wording |
| HECATE | uncertainty, hidden risk, unknowns, ambiguity | false certainty |
| THEMIS | risk, approval level, forbidden action, liability exposure | softened warnings |
| APOLLO | completeness, coherence, unsupported claims, final readiness | partial data without limits |
| HERA | trajectory, milestone status, satisfaction gap, continue/pause signal | isolated facts without progress meaning |
| CHRONOS | sequence, dependency, wait, join, freshness, deadline | unordered requests |
| HEPHAESTUS | method robustness, skill gap, tests, rollback, technical weakness | vague improvement request |
| DEMETER | quantities, costs, resources, tables, units, economic assumptions | unquantified claims |
| POSEIDON | site, water, networks, soil, environment, physical constraints | abstract strategy without site constraints |
| PROMETHEUS | alternatives, contradictions, edge cases, adversarial review | single-option framing |
| IRIS | tone, wording, audience, communication constraints | unresolved risk without THEMIS signal |
| HESTIA | project-memory relevance, project facts, context scope | system-level generalization |
| MNEMOSYNE | reusable system rule, pattern, memory candidate evidence | local project detail as universal rule |
| DAEDALUS | structure, diagram, system boundary, architecture pattern | vague conceptual drift |

---

## 6. Addressed signal envelope

When IRIS mediates a signal, use this envelope.

```yaml
addressed_role_signal:
  id: RS-YYYY-NNNN
  mediator_role: IRIS
  from_role: ARGOS
  to_role: THEMIS
  signal_type: risk_warning
  address_profile: THEMIS
  sender_substance:
    content_summary: "A contractor quote is being discussed for possible client-facing use."
    payload_ref: quote_review.summary
    confidence: partial
    limitations:
      - "The architect mission scope is not fully available."
  mediated_message:
    question_or_request: "Classify whether this wording could create responsibility or require C4 approval."
    requested_output:
      - approval_level
      - forbidden_wording
      - safer_wording_guidance
  constraints:
    preserve_risk_level: true
    preserve_limitations: true
    no_external_send: true
  status: open
```

The mediated message may clarify form.

It must not distort substance.

---

## 7. Signal types

Allowed signal types:

```text
role_need_statement
information_transmission
clarification_request
role_consultation
risk_warning
veto_signal
brief_adherence_signal
workflow_revision_signal
handoff_signal
stop_gate_signal
memory_candidate_signal
skill_gap_signal
asset_need_signal
source_gap_signal
```

Forbidden signal types:

```text
execute_tool
approve_external_action
promote_memory
activate_skill
canonize_workflow
send_external_message
mutate_file
access_secret
raw_chain_of_thought
```

---

## 8. Base schema

Every role signal should follow this shape when structured output is needed.

```yaml
role_signal:
  id: RS-YYYY-NNNN
  from_role: ARGOS
  to_role: DEMETER
  type: information_transmission
  purpose: "Transmit extracted quantities for economic review."
  content_summary: "Quantities extracted from the available DPGF."
  payload_ref: source_inventory.quantities
  confidence: partial
  assumptions: []
  limitations:
    - "The plumbing lot was not included in the provided schedule."
  risk_level: C1
  evidence_refs:
    - EP-2026-0001.source_inventory
  requested_action: review | comment | continue | escalate | block | arbitrate
  deadline_or_dependency: null
  status: open | answered | superseded | blocked | closed
```

Rules:

```text
content_summary must be short.
payload_ref should point to a bounded output, not raw private reasoning.
limitations must be explicit when confidence is partial.
risk_level must not be lowered by the sender.
```

---

## 9. Ad hoc Role Consultation

A role may consult another role without a formal workflow when the task is simple and low-risk.

```yaml
role_consultation:
  id: RC-YYYY-NNNN
  from_role: IRIS
  to_role: THEMIS
  reason: possible_contractual_commitment
  question: "Can this wording create unintended responsibility?"
  context_summary: "Draft client message about contractor quote review."
  expected_output:
    - risk_level
    - forbidden_wording
    - safer_wording_guidance
  max_rounds: 1
  risk_level: C1
  status: open
```

Allowed:

```text
bounded question
bounded answer
one clarification round by default
public summary if relevant
Evidence Pack reference if consequential
```

Forbidden:

```text
open-ended debate
raw chain-of-thought
tool execution
file mutation
approval bypass
memory promotion
skill activation
workflow canonization
```

Escalate to a workflow if:

```text
more than 2 or 3 roles are needed
sources must be compared
risk is C3/C4/C5
external-facing output is involved
Evidence Pack is required
memory or files are impacted
Hermes must execute tools
```

---

## 10. Information transmission

Use information transmission when one role has produced a bounded output needed by another role.

Example:

```yaml
role_signal:
  from_role: ARGOS
  to_role: DEMETER
  type: information_transmission
  content_summary: "Cost lines grouped by lot are ready for economic review."
  payload_ref: extracted_cost_table.v1
  confidence: medium
  limitations:
    - "Unit prices are missing for two lines."
  requested_action: review
```

Information transmission does not mean the receiving role must accept the information as true.

The receiving role may respond with:

```text
accepted_for_review
needs_more_source
blocked_by_limitation
risk_escalation
```

---

## 11. Risk and veto signals

THEMIS may emit a risk warning or veto signal.

```yaml
role_signal:
  from_role: THEMIS
  to_role: ZEUS
  type: veto_signal
  purpose: "Block external-facing wording before approval."
  content_summary: "The draft creates a contractual commitment without C4 approval."
  risk_level: C4
  requested_action: block
  escalation:
    required_approval: C4
    next_safe_action: "Keep as internal draft or request explicit user validation."
```

Rules:

```text
A veto signal cannot be overridden by AGORA majority.
ZEUS may reroute but cannot bypass the veto.
APOLLO cannot finalize against a THEMIS veto.
```

---

## 12. Stop Gate signal

APOLLO may emit a stop gate signal.

```yaml
role_signal:
  from_role: APOLLO
  to_role: ZEUS
  type: stop_gate_signal
  purpose: "Decide whether the answer can be finalized."
  content_summary: "The output is coherent but source limitations must be visible."
  decision: ready_with_limits
  unresolved_items:
    - missing_quantity_schedule
  requested_action: finalize_with_limits
```

Allowed decisions:

```text
ready
ready_with_limits
needs_revision
needs_user_input
blocked
```

---

## 13. Workflow revision signal

Workflow revision signals are used when the current route no longer fits.

```yaml
role_signal:
  from_role: HECATE
  to_role: ZEUS
  type: workflow_revision_signal
  purpose: "Escalate ambiguity that changes the task route."
  content_summary: "The request moved from a simple rewrite to a contractual position."
  recommended_change: escalate_to_W4
  risk_level: C4
  requested_action: arbitrate
```

Signals do not apply the change by themselves.

ZEUS arbitrates.

THEMIS checks risk.

ATHENA restructures the method if approved.

---

## 14. Handoff signal

Use a handoff signal when the active role changes.

```yaml
handoff_signal:
  from_role: ATHENA
  to_role: ARGOS
  task_context: "Source inventory before report drafting."
  required_inputs:
    - uploaded_files
    - selected_knowledge_sources
  expected_output:
    - source_inventory
    - missing_sources
    - usable_facts
  blockers:
    - no_files_available
```

Handoff is not delegation of authority.

The receiving role performs only its defined responsibility.

---

## 15. AGORA relationship

AGORA is a bounded consultation mode composed of role signals.

AGORA may collect:

```text
variant_signal
risk_signal
source_gap_signal
brief_adherence_signal
method_signal
```

AGORA must output:

```text
structured summary
variant comparison
risk table
recommendation for ZEUS
```

AGORA must not output:

```text
raw chain-of-thought
unbounded debate
majority vote overriding THEMIS or APOLLO
```

---

## 16. Run Graph relationship

Role Signals may be displayed in Run Graph or Inline Run Stream only as public summaries.

Allowed public message:

```text
ARGOS : Les sources exploitables sont transmises à DEMETER.
```

Forbidden public message:

```text
ARGOS : raw internal reasoning, hidden prompt, private file path, secret or raw source dump.
```

Reference:

```text
RUN_GRAPH.md
```

---

## 17. Evidence Pack relationship

Consequential role signals should be referenced in the Evidence Pack.

Evidence Pack may record:

```text
role_signals
addressed_role_signals
role_consultations
handoffs
risk_warnings
vetoes
stop_gate_decisions
workflow_revision_signals
```

Signal content is not proof by itself.

The signal must point to evidence when it supports a factual or consequential claim.

---

## 18. Persistence

Role Signals are session artifacts by default.

They become persistent only if:

```text
included in an Evidence Pack
included in a Task Contract revision
included in a workflow candidate
included in a memory candidate
included in a PR or governance document
```

Persistence must not imply canonization.

---

## 19. Final rule

```text
Roles may consult other roles.
They communicate through structured signals.
IRIS may format addressed signals.
Signals are bounded, traceable and non-executing.
ATHENA organizes.
CHRONOS sequences.
ZEUS arbitrates.
THEMIS blocks.
APOLLO validates readiness.
Hermes executes runtime transport under Task Contract.
Pantheon governs the schema.
```
