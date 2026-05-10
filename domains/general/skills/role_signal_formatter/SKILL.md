# Skill — role_signal_formatter

Status: candidate.

Domain: general.

Purpose: format a structured role signal according to the addressed Pantheon Role, preserving substance, limitations and risk while improving clarity and routing precision.

---

## 1. Role in Pantheon

`role_signal_formatter` supports IRIS signal mediation.

It helps transform role-to-role messages into governed `Role Signals` or `Addressed Role Signals`.

It does not create a message bus.

It does not execute, approve, arbitrate, promote memory, activate skills or send external messages.

Core rule:

```text
Format the signal. Do not alter authority.
```

---

## 2. Use when

Use this skill when:

```text
a role must consult another role
a role finding must be transmitted to another role
AGORA needs structured role inputs
Run Graph needs a public summary of a signal
THEMIS/APOLLO/ZEUS needs a concise addressed request
workflow handoff needs a clean payload
risk, limitation or confidence must be preserved in transmission
```

Examples:

```text
ARGOS → DEMETER: transmit quantities for review
IRIS → THEMIS: ask if wording creates liability
HECATE → ZEUS: escalate route ambiguity
APOLLO → ZEUS: emit stop gate decision
THEMIS → ATHENA: block unsafe workflow transition
ATHENA → ARGOS: request source inventory
```

---

## 3. Do not use when

Do not use this skill for:

```text
free-form debate
raw chain-of-thought exchange
external communication
memory promotion
skill activation
workflow canonization
tool execution
runtime message transport
approval decision itself
```

If the message changes risk, authority, persistence or execution, escalate to THEMIS / ZEUS / Task Contract rather than only formatting it.

---

## 4. Formatting hierarchy

IRIS must use a profile-first approach.

```text
1. Use the known Role Signal Profile.
2. If the known profile is insufficient, send a format_reminder_request.
3. If the reminder response only returns structure, format the signal.
4. If the response requires judgment, risk classification, approval or arbitration, stop and route to the competent role.
```

Reference:

```text
docs/governance/ROLE_SIGNAL_PROFILES.md
```

The format reminder exists to recover structure, not to obtain a decision.

---

## 5. Inputs

Expected input:

```yaml
role_signal_input:
  from_role: ARGOS
  to_role: DEMETER
  intended_signal_type: information_transmission
  raw_summary: "Cost lines grouped by lot are ready."
  payload_ref: extracted_cost_table.v1
  confidence: partial
  limitations: []
  requested_action: review
  risk_level: C1
```

Optional format reminder input:

```yaml
format_reminder_request:
  from_role: IRIS
  to_role: THEMIS
  purpose: "Remind the expected structure for a risk review signal."
  constraints:
    no_decision: true
    no_approval: true
    no_execution: true
```

---

## 6. Outputs

Expected output:

```yaml
addressed_role_signal:
  mediator_role: IRIS
  from_role: ARGOS
  to_role: DEMETER
  signal_type: information_transmission
  address_profile: DEMETER
  sender_substance:
    content_summary: "Cost lines grouped by lot are ready for economic review."
    payload_ref: extracted_cost_table.v1
    confidence: partial
    limitations: []
  mediated_message:
    question_or_request: "Review the extracted cost table and identify missing quantities, unit gaps or economic assumptions."
    requested_output:
      - quantity_gaps
      - unit_price_gaps
      - economic_assumptions
  constraints:
    preserve_risk_level: true
    preserve_limitations: true
    no_external_send: true
  status: open
```

Blocked output when structure requires substance:

```yaml
format_blocked:
  from_role: IRIS
  reason: "The requested format requires substantive risk classification."
  blocked_action: format_signal
  next_role: THEMIS
  next_action: "THEMIS must classify risk directly."
  escalation_required: true
```

---

## 7. Address profiles

The skill must adapt the signal to the receiving role.

Examples:

```text
To THEMIS: emphasize risk, approval level, forbidden action.
To APOLLO: emphasize completeness, coherence, unsupported claims.
To ZEUS: emphasize decision point, options, conflict, arbitration request.
To ARGOS: emphasize source need and factual extraction target.
To DEMETER: emphasize quantities, units, costs, assumptions.
To CHRONOS: emphasize dependencies, waits, freshness, sequence.
To HERA: emphasize trajectory, milestone status, satisfaction gap.
To PROMETHEUS: emphasize alternatives, contradictions and edge cases.
To IRIS: emphasize audience, tone, wording and communication constraints.
```

Full profiles live in `ROLE_SIGNAL_PROFILES.md`.

---

## 8. Guardrails

The skill must preserve:

```text
sender role
addressed role
risk level
confidence
limitations
payload reference
approval requirement
forbidden actions
```

The skill must not:

```text
rewrite partial evidence as certain
soften a THEMIS warning
turn a recommendation into approval
turn a role signal into external wording
omit limitations
add unsupported facts
hide uncertainty
change requested authority
```

A format reminder response must not be accepted if it contains:

```text
final approval
risk downgrade
external send instruction
memory promotion
skill activation
workflow canonization
substantive decision
```

---

## 9. Evidence relationship

For consequential outputs, Evidence Pack may record:

```text
original signal
mediated signal
format reminder request
format reminder response
addressed role
risk level
limitations preserved
response received
```

Signal formatting is not proof.

---

## 10. Approval relationship

Formatting a signal is normally C0/C1.

Escalate if the mediated signal would:

```text
request file mutation
request memory promotion
request external communication
trigger C3/C4/C5 decision
activate a runtime skill
authorize tool execution
```

---

## 11. Final rule

```text
Use the recipient profile first.
Ask for a format reminder only as fallback.
Block if the reminder becomes a decision.
IRIS may mediate form.
The source role owns substance.
The addressed role owns response.
THEMIS owns risk.
APOLLO owns readiness.
ZEUS owns arbitration.
Hermes owns runtime execution only under Task Contract.
```
