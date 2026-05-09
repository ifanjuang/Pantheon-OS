# Skill — context_scope_expansion

Status: candidate.

Domain: general.

Purpose: decide whether a response needs more context, where that context should come from, and whether the user should be asked for a missing input.

---

## 1. Role

`context_scope_expansion` is used after request classification and intent enrichment.

It chooses the smallest useful context expansion.

It does not retrieve sources by itself.

It routes source selection to `knowledge_selection` when needed.

---

## 2. Inputs

```text
request_classification
request_intent_enrichment
visible_context
known_project_context optional
memory_policy
knowledge_policy
```

---

## 3. Outputs

```yaml
context_scope_expansion:
  context_needed: true
  known_context: []
  missing_context:
    blocking: []
    useful_but_not_blocking: []
  sources_to_check:
    session_context: true
    uploaded_documents: false
    project_memory: false
    system_memory: false
    openwebui_knowledge: []
    web:
      required: false
      purpose: []
  recommended_agents: []
  response_mode: answer_with_assumptions
```

---

## 4. Guardrails

This skill proposes a context plan only.

It must not search everywhere by default, retrieve documents directly, read memory without policy, or invent missing context.

---

## 5. Final rule

```text
Expand context only when it materially improves correctness, safety or usefulness.
```
