# Examples — agent_forum_review

All examples are fictional and generic.

---

## Variant review

```yaml
agent_forum_review:
  purpose: "Compare three client response variants."
  participants:
    - THEMIS
    - APOLLO
    - IRIS
  max_rounds: 1
  opinions:
    - role: THEMIS
      preferred_variant: option_A
      reason: "Lowest responsibility risk."
    - role: APOLLO
      preferred_variant: option_B
      reason: "Best adherence to the initial request if limitations are added."
    - role: IRIS
      preferred_variant: option_B
      reason: "Clearest wording for the user."
  unresolved_disagreement: true
  recommended_next_step: decision_arbitration
```

---

## Workflow option review

```yaml
agent_forum_review:
  purpose: "Compare direct answer versus context expansion."
  participants:
    - METIS
    - HECATE
    - ARGOS
    - THEMIS
  opinions:
    - role: HECATE
      preferred_variant: ask_targeted_question
      reason: "Important missing context."
    - role: ARGOS
      preferred_variant: answer_with_assumptions
      reason: "Some useful context is already available."
  recommended_next_step: decision_arbitration
```
