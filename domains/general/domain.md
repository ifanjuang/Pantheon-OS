# General Domain — Pantheon OS

> Reference domain for invariant Pantheon capabilities.

---

# 1. Purpose

The `general` domain contains reusable system capabilities that are not tied to a specific business domain.

It defines how Pantheon selects, adapts, audits, creates and improves skills and workflows.

---

# 2. Scope

The `general` domain may contain capabilities for:

- request triage;
- workflow preflight;
- adaptive orchestration;
- skill design;
- workflow design;
- name checking;
- Hermes skill checking;
- memory candidate review;
- skill health review;
- agent status reporting;
- workflow trace reporting;
- source and repository evaluation;
- non-intrusive feedback collection.

---

# 3. Rules

General-domain capabilities must remain:

- domain-neutral;
- reusable;
- privacy-safe;
- traceable;
- reversible;
- compatible with Hermes-backed execution;
- aligned with Pantheon governance.

They must not contain real project names, real client names, private conversation data, addresses, companies, construction sites or identifiable examples.

---

# 4. Structure

```text
domains/general/
  domain.md
  skills/
  workflows/
  templates/
```

---

# 5. First priority

The first general-domain capability is:

```text
adaptive_orchestration
```

It decides whether a workflow should be used as-is, adapted, simplified, extended, switched, paused, or replaced by a candidate workflow proposal.
