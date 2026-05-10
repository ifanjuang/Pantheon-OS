# Tests — request_classification

Documentation-level tests only.

---

## Test 1 — vague technical request

Input: `Combien d’UP ?`

Expected:

```text
primary_domain includes architecture_fr
question_type is technical_regulatory
context_dependency is high
recommended_mode is not answer_directly
```

---

## Test 2 — low-risk rewrite

Input: `Améliore ce mail.`

Expected:

```text
question_type is editorial
risk_level is low unless content indicates legal/contractual risk
recommended_mode may be answer_directly
```

---

## Test 3 — no final answer

Expected:

```text
skill produces classification only
no final user answer
no source retrieval
no tool execution
```
