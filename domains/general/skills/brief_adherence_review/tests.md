# Tests — brief_adherence_review

Documentation-level tests only.

---

## Test 1 — detect scope drift

Input: draft promises validation beyond the initial mission.

Expected:

```text
scope_drift is not empty
final_status is revise or block
```

---

## Test 2 — detect missing required points

Input: long deliverable omits a key point from the initial request.

Expected:

```text
missing_points includes omitted point
recommended_revision is explicit
```

---

## Test 3 — no rewrite without trace

Expected:

```text
skill recommends revision
skill does not silently rewrite final answer
```
