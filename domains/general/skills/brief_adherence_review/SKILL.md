# Skill — brief_adherence_review

Status: candidate.

Domain: general.

Purpose: verify that an answer or deliverable remains aligned with the initial request, expected audience, scope, tone, assumptions, limits and evidence.

---

## 1. Role

`brief_adherence_review` is normally used by APOLLO after drafting or before final output.

It checks whether the response still answers the original request instead of drifting into adjacent topics.

It does not rewrite by itself unless paired with IRIS or another drafting role.

---

## 2. Inputs

```text
initial_user_request
interpreted_intent
expected_deliverable
draft_output
known_context
constraints
risk_flags
```

---

## 3. Outputs

```yaml
brief_adherence_review:
  initial_request: null
  expected_deliverable: null
  required_points: []
  missing_points: []
  scope_drift: []
  coherence_issues: []
  unsupported_claims: []
  recommended_revision: []
  final_status: pass | revise | block
```

---

## 4. Checks

```text
answers the real request
keeps expected format
keeps expected audience
stays inside scope
keeps assumptions visible
keeps limits visible
avoids unsupported certainty
keeps sections coherent
avoids contradictory statements
```

---

## 5. Guardrails

This skill is a review layer only.

It must not approve high-risk outputs alone, ignore THEMIS warnings, or hide missing sources.

---

## 6. Final rule

```text
A polished answer is not acceptable if it no longer answers the original request.
```
