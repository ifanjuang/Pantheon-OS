# Tests — request_intent_enrichment

Documentation-level tests only.

---

## Test 1 — infer implicit intent

Input: `Combien d’UP ?`

Expected:

```text
interpreted_intent mentions units of passage / evacuation sizing
implicit_needs include occupancy, exits and widths
recommended_next_step is not final answer without context
```

---

## Test 2 — no invented context

Input: `Combien d’UP ?`

Expected:

```text
known_context remains empty if not provided
missing_context is explicit
no project facts are invented
```

---

## Test 3 — no final answer

Expected:

```text
skill enriches intent only
no final calculation
no regulatory conclusion
```
