# Skill — decision_arbitration

Status: candidate.

Domain: general.

Purpose: support ZEUS when several options, variants or role opinions conflict and a bounded decision is needed.

---

## 1. Role

`decision_arbitration` helps ZEUS select, combine, reject or pause options.

It is used after variant generation or AGORA review when the best path is not obvious.

It does not bypass THEMIS, APOLLO or human approval.

---

## 2. Inputs

```text
initial_request
interpreted_intent
variants
forum_review optional
risk_flags
evidence_state
approval_constraints
```

---

## 3. Outputs

```yaml
decision_arbitration:
  arbitrated_by: ZEUS
  decision: select | combine | reject_all | ask_user | pause
  selected_variant: option_B
  reason: "Best balance between usefulness and safety."
  required_modifications:
    - "Add THEMIS limitation."
    - "Keep assumptions visible."
  approval_impact: C1
```

---

## 4. Arbitration criteria

Priority order:

```text
1. safety, responsibility and compliance
2. adherence to the initial request
3. evidence and available sources
4. operational usefulness
5. clarity for the user
6. simplicity
7. style or elegance
```

---

## 5. Allowed decisions

```text
select one option
combine options
reject all options
request safer option
request clearer option
ask the user to choose
pause for missing information
```

---

## 6. Guardrails

ZEUS may decide the path, but cannot erase safety, evidence or approval constraints.

---

## 7. Final rule

```text
Choose the safest useful path, not the most fluent-looking one.
```
