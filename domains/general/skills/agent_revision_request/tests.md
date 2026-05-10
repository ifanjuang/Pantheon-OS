# Tests — agent_revision_request

Documentation-level tests only.

---

## Test 1 — bounded request

Expected:

```text
revision request names requesting role, target role, target output and requested change
```

---

## Test 2 — no free loop

Expected:

```text
request does not create open-ended discussion
request does not trigger repeated retries without ZEUS or APOLLO review
```

---

## Test 3 — no hidden rewrite

Expected:

```text
original output and revision request remain traceable
```
