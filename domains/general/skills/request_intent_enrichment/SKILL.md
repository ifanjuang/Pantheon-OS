# Skill — request_intent_enrichment

Status: candidate.

Domain: general.

Purpose: interpret the real intent of a user request before answer, retrieval or workflow selection.

---

## 1. Role

`request_intent_enrichment` transforms a short, vague or implicit request into a clear, bounded and answerable intent.

It is normally used by METIS after `request_classification`.

It does not answer the request.

---

## 2. Inputs

```text
user_request
request_classification
visible_conversation_context
known_project_context optional
```

---

## 3. Outputs

```yaml
request_intent_enrichment:
  original_request: null
  interpreted_intent: null
  likely_domain: null
  likely_topics: []
  implicit_needs: []
  known_context: []
  missing_context: []
  likely_answer_shape: []
  recommended_roles: []
  recommended_skills: []
  recommended_next_step: null
```

---

## 4. Allowed decisions

```text
answer_directly
answer_with_assumptions
ask_targeted_question
expand_context
route_to_workflow
```

---

## 5. Guardrails

This skill is an interpretation layer only.

It must not invent context, produce a final answer, bypass review, or turn every request into a workflow.

---

## 6. Example principle

```text
A question like “Combien d’UP ?” is not just asking for a number.
It likely asks for a regulated evacuation sizing method with assumptions, missing inputs and limits.
```

---

## 7. Final rule

```text
Understand the real request before structuring the answer.
```
