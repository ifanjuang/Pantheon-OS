# EXTERNAL RUNTIME REVIEW TEMPLATE — Pantheon Next

> Standard template for classifying external runtimes, agent frameworks, MCP connectors, memory systems, browser-agent tools, benchmarks, dashboards and developer tools before adoption.

---

## 1. Doctrine

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

External options may assist Pantheon.

They must not silently become Pantheon core.

---

## 2. Review template

```yaml
external_option_review:
  name: null
  url: null
  reviewed_at: YYYY-MM-DD
  category:
    - runtime | mcp_connector | memory | benchmark | dashboard | developer_tool | skill_pack | retrieval | evaluation
  status:
    - allowed | blocked | watchlist | lab_only | candidate | rejected_for_core
  summary: null
  useful_for:
    - null
  risks:
    - null
  allowed_use:
    - null
  forbidden_use:
    - null
  required_approvals:
    - C0 | C1 | C2 | C3 | C4 | C5
  evidence:
    sources_read:
      - null
    limits:
      - null
  decision: null
  next_action: null
```

---

## 3. Required classification fields

Every review must state:

```text
what it is
what it is useful for
whether it touches runtime, memory, tools, external communication or secrets
whether it can remain lab-only
whether it is blocked for core
what approval level would be required for any experiment
```

---

## 4. Forbidden shortcuts

Do not classify an external tool as allowed only because it is popular.

Do not install before classification.

Do not give an external option authority over:

```text
approvals
memory promotion
skill promotion
workflow canonization
external send
file mutation
secret access
runtime routing
```

---

## 5. Status vocabulary

```text
watchlist        = interesting, no use yet
lab_only         = test only, non-sensitive sandbox
candidate        = may become useful after review
allowed          = allowed within a bounded policy
blocked          = must not be used
rejected_for_core = may be studied but must not become Pantheon core
```

---

## 6. Final rule

```text
Classify before testing.
Test before trusting.
Trust never replaces governance.
```
