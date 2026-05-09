# Examples — brief_adherence_review

All examples are fictional and generic.

---

## Method note

Input:

```text
Initial request: Draft a methodology note for structural works in a condominium.
Draft: A broad technical note that implies final structural validation.
```

Output:

```yaml
brief_adherence_review:
  missing_points:
    - limits_of_mission
    - required_structural_study
    - required_investigations
  scope_drift:
    - draft_implies_final_structural_validation
  recommended_revision:
    - add_limits_on_architect_scope
    - state_that_structural_study_is_mandatory
  final_status: revise
```

---

## Simple email

Input:

```text
Initial request: make the email more human.
Draft: short clear email with same meaning.
```

Output:

```yaml
brief_adherence_review:
  missing_points: []
  scope_drift: []
  final_status: pass
```
