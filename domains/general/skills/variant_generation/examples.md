# Examples — variant_generation

All examples are fictional and generic.

---

## Client answer variants

```yaml
variant_set:
  requested_by: ATHENA
  generated_by: PROMETHEUS
  count: 3
  purpose: "Compare possible client response tones."
  variants:
    - id: option_A
      title: "Very cautious"
      strengths:
        - "Lowest responsibility exposure."
      weaknesses:
        - "May feel distant."
    - id: option_B
      title: "Balanced"
      strengths:
        - "Clear and human."
      weaknesses:
        - "Needs a visible limitation."
    - id: option_C
      title: "Firm"
      strengths:
        - "Strong boundary."
      weaknesses:
        - "Less conciliatory."
```

---

## Technical strategy variants

```yaml
variant_set:
  count: 3
  purpose: "Compare response strategies for incomplete technical data."
  variants:
    - id: answer_with_assumptions
    - id: ask_targeted_question
    - id: provide_method_only
```
