# Examples — decision_arbitration

All examples are fictional and generic.

---

## Choose balanced variant with reserve

```yaml
decision_arbitration:
  arbitrated_by: ZEUS
  decision: select
  selected_variant: option_B
  rejected_variants:
    - option_A
    - option_C
  reason: "Option B best balances clarity and caution."
  required_modifications:
    - "Add THEMIS limitation."
    - "Keep assumptions visible."
  approval_impact: C1
```

---

## Ask user to choose

```yaml
decision_arbitration:
  arbitrated_by: ZEUS
  decision: ask_user
  reason: "Two variants are valid and depend on intended tone."
  options_to_present:
    - option_prudent
    - option_direct
```
