# Examples — request_intent_enrichment

All examples are fictional and generic.

---

## ERP UP request

Input:

```text
Combien d’UP il me faut ?
```

Output:

```yaml
request_intent_enrichment:
  interpreted_intent: "Estimate required ERP evacuation units of passage."
  likely_domain: architecture_fr
  likely_topics:
    - ERP
    - fire_safety
    - evacuation
  implicit_needs:
    - type_erp
    - occupancy
    - level
    - number_of_exits
    - exit_widths
    - main_or_accessory_exit
  likely_answer_shape:
    - assumptions
    - provisional_sizing
    - minimum_widths
    - limitations
    - documents_to_verify
  recommended_next_step: context_scope_expansion
```

---

## CCTP article request

Input:

```text
Fais-moi un article CCTP pour une cloison acoustique.
```

Output:

```yaml
request_intent_enrichment:
  interpreted_intent: "Draft a market-ready CCTP article with assumptions and limits."
  implicit_needs:
    - support
    - location
    - acoustic_performance
    - fire_rating
    - height
    - interfaces
    - applicable_standards
  recommended_next_step: answer_with_assumptions
```
