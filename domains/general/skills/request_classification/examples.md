# Examples — request_classification

All examples are fictional and generic.

---

## ERP question

Input:

```text
Combien d’UP il me faut ?
```

Output:

```yaml
request_classification:
  primary_domain: architecture_fr
  question_type: technical_regulatory
  topic_family:
    - erp_fire_safety
    - evacuation
  risk_level: medium
  context_dependency: high
  freshness_required: true
  evidence_required: true
  approval_hint: C1
  recommended_mode: answer_with_assumptions
```

---

## Simple rewrite

Input:

```text
Améliore ce mail.
```

Output:

```yaml
request_classification:
  primary_domain: general
  question_type: editorial
  risk_level: low
  context_dependency: low
  freshness_required: false
  evidence_required: false
  approval_hint: C1
  recommended_mode: answer_directly
```

---

## Sensitive contractual answer

Input:

```text
Réponds à l’avocat.
```

Output:

```yaml
request_classification:
  primary_domain: architecture_fr
  question_type: legal_contractual
  risk_level: high
  context_dependency: high
  freshness_required: false
  evidence_required: true
  approval_hint: C4
  recommended_mode: expand_context
```
