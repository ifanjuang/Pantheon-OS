# Examples — role_signal_formatter

All examples are fictional and generic.

The skill formats structured role-to-role messages. It does not execute, approve or arbitrate.

---

## 1. ARGOS to DEMETER

Input:

```yaml
role_signal_input:
  from_role: ARGOS
  to_role: DEMETER
  intended_signal_type: information_transmission
  raw_summary: "Cost lines grouped by lot are ready."
  payload_ref: extracted_cost_table.v1
  confidence: partial
  limitations:
    - "Two unit prices are missing."
  requested_action: review
  risk_level: C1
```

Output:

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
    limitations:
      - "Two unit prices are missing."
  mediated_message:
    question_or_request: "Review the extracted cost table and identify quantity gaps, unit gaps and economic assumptions."
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

---

## 2. IRIS to THEMIS

Input:

```yaml
role_signal_input:
  from_role: IRIS
  to_role: THEMIS
  intended_signal_type: risk_warning
  raw_summary: "Draft wording may imply contractor quote validation."
  payload_ref: client_message_draft.v1
  confidence: medium
  limitations:
    - "Mission scope not fully confirmed."
  requested_action: review
  risk_level: C3
```

Output:

```yaml
addressed_role_signal:
  mediator_role: IRIS
  from_role: IRIS
  to_role: THEMIS
  signal_type: risk_warning
  address_profile: THEMIS
  sender_substance:
    content_summary: "Draft wording may imply validation of a contractor quote."
    payload_ref: client_message_draft.v1
    confidence: medium
    limitations:
      - "Mission scope not fully confirmed."
  mediated_message:
    question_or_request: "Classify whether this wording creates responsibility exposure and whether C4 approval is required before external use."
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

---

## 3. HECATE to ZEUS

Input:

```yaml
role_signal_input:
  from_role: HECATE
  to_role: ZEUS
  intended_signal_type: workflow_revision_signal
  raw_summary: "The task moved from a simple rewrite to a contractual position."
  payload_ref: request_frame.v2
  confidence: high
  limitations: []
  requested_action: arbitrate
  risk_level: C4
```

Output:

```yaml
addressed_role_signal:
  mediator_role: IRIS
  from_role: HECATE
  to_role: ZEUS
  signal_type: workflow_revision_signal
  address_profile: ZEUS
  sender_substance:
    content_summary: "The task moved from a simple rewrite to a contractual position."
    payload_ref: request_frame.v2
    confidence: high
    limitations: []
  mediated_message:
    question_or_request: "Arbitrate whether the route should escalate from W1 to W4 with THEMIS review before drafting."
    requested_output:
      - route_decision
      - required_roles
      - approval_path
  constraints:
    preserve_risk_level: true
    preserve_limitations: true
    no_external_send: true
  status: open
```

---

## 4. APOLLO to ZEUS

Input:

```yaml
role_signal_input:
  from_role: APOLLO
  to_role: ZEUS
  intended_signal_type: stop_gate_signal
  raw_summary: "The report is coherent but two source limitations remain."
  payload_ref: final_review.v1
  confidence: high
  limitations:
    - "One source is outdated."
    - "One section relies on assumption."
  requested_action: finalize_with_limits
  risk_level: C2
```

Output:

```yaml
addressed_role_signal:
  mediator_role: IRIS
  from_role: APOLLO
  to_role: ZEUS
  signal_type: stop_gate_signal
  address_profile: ZEUS
  sender_substance:
    content_summary: "The report is coherent but two source limitations remain."
    payload_ref: final_review.v1
    confidence: high
    limitations:
      - "One source is outdated."
      - "One section relies on assumption."
  mediated_message:
    question_or_request: "Decide whether to finalize with visible limits or request revision before final output."
    requested_output:
      - final_route
      - limits_to_display
  constraints:
    preserve_risk_level: true
    preserve_limitations: true
    no_external_send: true
  status: open
```

---

## 5. Public Run Graph summary

Input:

```yaml
addressed_role_signal:
  from_role: ARGOS
  to_role: DEMETER
  signal_type: information_transmission
  sender_substance:
    content_summary: "Cost lines grouped by lot are ready for economic review."
```

Output:

```text
ARGOS : Les lignes de coût exploitables sont transmises à DEMETER.
```

Forbidden output:

```text
ARGOS : raw extraction details, internal path, hidden reasoning or full private data.
```
