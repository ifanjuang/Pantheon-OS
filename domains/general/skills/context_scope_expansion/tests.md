# Tests — context_scope_expansion

Documentation-level tests only.

---

## Test 1 — no search everywhere

Input: vague request with medium risk.

Expected:

```text
source plan is bounded
web is required only with purpose
knowledge_selection is recommended when Knowledge sources are needed
```

---

## Test 2 — blocking missing input

Input: regulated sizing question without occupancy or plan.

Expected:

```text
missing_context.blocking includes occupancy or equivalent
response_mode is answer_with_assumptions or ask_targeted_question
```

---

## Test 3 — no direct retrieval

Expected:

```text
skill proposes source families only
no documents are read
no web search is executed
```
