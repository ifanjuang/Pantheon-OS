# Examples — context_scope_expansion

All examples are fictional and generic.

---

## ERP context expansion

Input:

```yaml
request_intent_enrichment:
  interpreted_intent: "Estimate ERP units of passage."
```

Output:

```yaml
context_scope_expansion:
  context_needed: true
  known_context: []
  missing_context:
    blocking:
      - occupancy
      - number_of_exits
      - available_widths
    useful_but_not_blocking:
      - level
      - public_waiting_area
  sources_to_check:
    session_context: true
    uploaded_documents: true
    project_memory: true
    system_memory: true
    openwebui_knowledge:
      - architecture_fr_erp_fire_safety
    web:
      required: true
      purpose:
        - current_regulatory_reference_check
  response_mode: answer_with_assumptions
```

---

## Simple editorial request

Input:

```text
Améliore ce mail.
```

Output:

```yaml
context_scope_expansion:
  context_needed: false
  response_mode: answer_directly
```
