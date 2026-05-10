# Skill — request_classification

Status: candidate.

Domain: general.

Purpose: classify a user request before answer, retrieval, workflow selection or execution.

---

## 1. Role

`request_classification` determines what kind of request is being made and what level of caution, context and evidence is required.

It is normally used by METIS before ATHENA arranges a method.

It does not answer the request.

---

## 2. Inputs

```text
user_request
visible_conversation_context
known_project_hint optional
known_domain_hint optional
```

---

## 3. Outputs

```yaml
request_classification:
  primary_domain: null
  secondary_domains: []
  question_type: null
  topic_family: []
  risk_level: low | medium | high | unknown
  context_dependency: low | medium | high
  freshness_required: false
  evidence_required: false
  approval_hint: C0 | C1 | C2 | C3 | C4 | C5 | unknown
  recommended_mode: answer_directly | answer_with_assumptions | ask_targeted_question | expand_context | route_to_workflow
```

---

## 4. Classification families

Allowed broad categories:

```text
technical
regulatory
legal_contractual
financial
organizational
editorial
client_relation
project_memory
system_memory
urbanism
erp_fire_safety
accessibility
market_documents
software
infra
image_visual_communication
```

---

## 5. Guardrails

This skill is a preflight classifier only.

It must not produce a final answer, select sources on its own, mutate memory, or replace THEMIS/APOLLO review.

---

## 6. Final rule

```text
Classify before searching.
Classify before over-answering.
Classify before escalating.
```
