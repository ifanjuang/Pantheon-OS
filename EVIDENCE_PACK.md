# EVIDENCE PACK — Pantheon OS

> Reference schema for proving what a result is based on.

---

# 1. Purpose

An Evidence Pack is the audit trail attached to any significant Pantheon or Hermes output.

It records what was read, used, assumed, produced and left unsupported.

Rule:

```text
A consequential output without evidence is a draft, not a validated result.
```

---

# 2. Minimal schema

| Field | Required | Purpose |
|---|---:|---|
| `files_read` | yes | Repository or local files inspected |
| `sources_used` | yes | External, regulatory, web or documentation sources used |
| `commands_run` | yes | Commands executed |
| `tools_used` | yes | Tools or integrations used |
| `knowledge_bases_consulted` | yes | OpenWebUI or other Knowledge Bases consulted |
| `documents_used` | yes | Project or system documents used |
| `assumptions` | yes | Explicit assumptions made |
| `unsupported_claims` | yes | Claims that still lack direct proof |
| `limitations` | yes | Missing data, scope limits, tool failures |
| `outputs` | yes | Files, patches, drafts, reports or candidates produced |
| `approval_required` | yes | Approval level or user validation needed |
| `next_safe_action` | yes | Recommended next action that does not exceed approval |

---

# 3. Generic shape

```yaml
evidence_pack:
  files_read: []
  sources_used: []
  commands_run: []
  tools_used: []
  knowledge_bases_consulted: []
  documents_used: []
  assumptions: []
  unsupported_claims: []
  limitations: []
  outputs: []
  approval_required: null
  next_safe_action: null
```

---

# 4. When it is mandatory

Evidence Pack is mandatory for:

- repository audit;
- quote / CCTP analysis;
- DPGF or quantity analysis;
- Markdown modification;
- code patch proposal;
- skill proposal;
- workflow proposal;
- memory candidate;
- client-facing communication;
- contractual or responsibility analysis;
- legacy audit;
- any output that may become canonical Pantheon truth.

---

# 5. Source discipline

Evidence must distinguish:

```text
file read
source used
document used
Knowledge Base consulted
assumption
unsupported claim
```

A model statement is not evidence.

A previous conversation is not canonical evidence unless it was already promoted to validated memory or is visible in the active session and disclosed as context.

---

# 6. Approval discipline

The Evidence Pack must state:

- whether approval is required;
- which criticality level applies;
- which action is safe next;
- which actions remain forbidden.

Example:

```yaml
approval_required:
  level: C3
  reason: "Markdown files were modified on a branch."
next_safe_action: "Run tests and review the diff before merge."
```

---

# 7. RAG discipline

When a result uses Knowledge Bases, the Evidence Pack must list:

- Knowledge Bases consulted;
- documents actually used;
- missing documents;
- source reliability level when available;
- whether cross-project data was used.

Rule:

```text
No cross-project document mixing without explicit trace or approval.
```

---

# 8. Limitations discipline

Limitations are not optional.

If no test was run, say:

```text
No tests were run.
```

If a source could not be checked, say:

```text
Source not verified.
```

If a conclusion is inferred, say:

```text
Inference, not directly proven by source.
```

---

# 9. Final rule

```text
Evidence Pack first. Canonization later.
```
