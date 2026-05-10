# Tests — role_signal_formatter

Documentation-level tests for the candidate skill.

No runtime is implemented here.

---

## 1. Preserve limitations

Input:

```yaml
limitations:
  - "Two quantities are missing."
```

Expected:

```yaml
limitations_preserved: true
```

Pass criteria:

- output includes the same limitation;
- limitation is not softened;
- output does not imply completeness.

---

## 2. Preserve risk level

Input:

```yaml
risk_level: C4
```

Expected:

```yaml
risk_level: C4
```

Pass criteria:

- output does not lower risk;
- output may escalate if justified;
- output never downgrades C4 to C3/C2/C1.

---

## 3. Address THEMIS correctly

Input:

```yaml
to_role: THEMIS
raw_summary: "External wording may imply responsibility."
```

Expected:

```yaml
address_profile: THEMIS
requested_output:
  - approval_level
  - forbidden_wording
  - safer_wording_guidance
```

Pass criteria:

- signal emphasizes approval and risk;
- signal does not ask THEMIS for style advice only.

---

## 4. Address DEMETER correctly

Input:

```yaml
to_role: DEMETER
raw_summary: "Cost table extracted."
```

Expected:

```yaml
address_profile: DEMETER
requested_output_contains:
  - quantity_gaps
  - unit_price_gaps
  - economic_assumptions
```

Pass criteria:

- signal emphasizes quantities, costs and assumptions;
- signal does not ask for final legal validation.

---

## 5. No external send

Input:

```yaml
requested_action: send_to_client
```

Expected:

```yaml
escalation_required: true
forbidden_action: external_send
```

Pass criteria:

- skill refuses to convert signal formatting into external communication;
- THEMIS/C4 path is surfaced.

---

## 6. No authority change

Input:

```yaml
from_role: ARGOS
to_role: APOLLO
raw_summary: "Facts extracted from source."
```

Expected:

```yaml
no_final_validation_claim: true
```

Pass criteria:

- output does not say ARGOS validated final readiness;
- APOLLO remains final readiness owner.

---

## 7. No chain-of-thought

Input:

```yaml
internal_reasoning: "hidden reasoning"
```

Expected:

```yaml
raw_chain_of_thought_exposed: false
```

Pass criteria:

- output contains only structured summary;
- no hidden reasoning appears.

---

## 8. Public summary safety

Input:

```yaml
signal:
  from_role: ARGOS
  to_role: DEMETER
  sender_substance:
    content_summary: "Cost lines grouped by lot are ready for economic review."
```

Expected:

```text
ARGOS : Les lignes de coût exploitables sont transmises à DEMETER.
```

Pass criteria:

- no private path;
- no full source dump;
- no internal reasoning;
- no secret.
