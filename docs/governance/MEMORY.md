# MEMORY — Pantheon OS

> Source of truth for Pantheon OS memory governance.
> Memory is validated knowledge, not raw storage.

---

# 1. Core principle

Memory is not passive storage.

It is a controlled knowledge system.

Information becomes memory only when it is:

- useful;
- traceable;
- checked;
- validated;
- assigned to the correct level.

Rule:

```text
Validation matters more than accumulation.
```

---

# 2. Memory levels

Pantheon uses four strict memory levels:

```text
SESSION → CANDIDATES → PROJECT or SYSTEM
```

| Level | Status | Role | Authority |
|---|---|---|---|
| Session | temporary | working context for the current interaction | not reliable beyond the session |
| Candidates | persisted but not validated | proposed facts, patterns, rules, skills or workflows | not canonical |
| Project | validated project context | project-specific facts, constraints, decisions and risks | canonical for that project only |
| System | validated reusable memory | reusable rules, methods, patterns and standards | canonical across Pantheon |

Terminology rule:

```text
Use system memory, not agency memory.
```

---

# 3. Session memory

Nature:

```text
temporary
not canonical
not automatically persisted
```

May contain:

- current request context;
- working assumptions;
- temporary reasoning state;
- user-provided active-session data;
- intermediate extracted facts.

Agents:

- ZEUS;
- ATHENA;
- ARGOS.

Rule:

```text
Session memory disappears unless explicitly converted into a candidate.
```

---

# 4. Candidate memory

Nature:

```text
persisted
not validated
not canonical
```

May contain:

- potential project facts;
- repeated patterns;
- proposed reusable rules;
- skill candidates;
- workflow candidates;
- project context candidates;
- system memory candidates.

Agents:

- ARGOS collects;
- HESTIA reviews project relevance;
- MNEMOSYNE reviews system relevance;
- THEMIS validates legitimacy;
- APOLLO validates quality.

Rule:

```text
Candidate memory is not reliable until promoted.
```

---

# 5. Project memory

Nature:

```text
validated
project-specific
not reusable by default
```

May contain:

- validated project facts;
- decisions;
- constraints;
- risks;
- stakeholders;
- project-specific preferences;
- project-specific unresolved issues.

Agent:

```text
HESTIA
```

Rule:

```text
Project memory must not be generalized into system memory without a separate promotion review.
```

---

# 6. System memory

Nature:

```text
validated
reusable
cross-project
high-risk if wrong
```

May contain:

- reusable methods;
- governance rules;
- validated patterns;
- naming conventions;
- recurring professional checks;
- durable operating principles.

Agent:

```text
MNEMOSYNE
```

Rule:

```text
System memory requires explicit validation and evidence.
```

---

# 7. Promotion cycle

Standard cycle:

```text
SESSION
→ CANDIDATES
→ Evidence Pack
→ THEMIS validation
→ APOLLO quality check
→ PROJECT or SYSTEM
```

Memory promotion is at least:

```text
C3
```

Reference:

```text
APPROVALS.md
EVIDENCE_PACK.md
TASK_CONTRACTS.md
```

---

# 8. Promotion requirements

A candidate can be promoted only if all conditions are met:

- source is identifiable;
- evidence is available;
- scope is clear;
- target memory level is justified;
- usefulness is real;
- contradiction check is complete;
- privacy risk is reviewed;
- cross-project contamination risk is reviewed;
- stale or obsolete source risk is reviewed.

Mandatory output:

```text
Evidence Pack
```

---

# 9. Rejection rules

A candidate must be rejected or kept pending if it is:

- unverifiable;
- unsupported;
- redundant;
- obsolete;
- contradictory;
- too vague;
- too project-specific for system memory;
- privacy-sensitive without need;
- based on a stale or unknown source;
- already contradicted by source-of-truth Markdown.

Allowed decisions:

```text
promote_to_project
promote_to_system
keep_candidate
reject
archive
needs_more_evidence
```

---

# 10. Knowledge versus memory

Reference:

```text
KNOWLEDGE_TAXONOMY.md
```

Distinction:

| Element | Knowledge | Memory |
|---|---|---|
| Uploaded document | yes | no |
| OpenWebUI collection | yes | no |
| CCTP / quote / PDF | yes | no |
| Validated project fact | maybe source | project memory |
| Validated reusable rule | maybe source | system memory |
| Pantheon policy | can be mirrored | canonical in Markdown |

Rule:

```text
Documents are knowledge.
Validated reusable facts become memory candidates.
Pantheon alone canonizes memory.
```

---

# 11. Interaction with skills

Skills may:

- read relevant memory;
- produce memory candidates;
- flag contradictions;
- request promotion review.

Skills must not:

- modify validated memory directly;
- promote candidates directly;
- treat Knowledge documents as memory;
- write project/system memory without review.

---

# 12. Interaction with workflows

Workflows may:

- create memory candidates;
- call `memory_promotion_review`;
- require THEMIS/APOLLO validation;
- attach Evidence Packs;
- mark information as `needs_more_evidence`.

Workflows must not:

- bypass C3 approval;
- promote memory silently;
- mix projects without explicit trace.

---

# 13. Interaction with Hermes

Hermes may:

- read context exports;
- propose memory candidates;
- include memory impact in task outputs;
- produce Evidence Packs.

Hermes must not:

- mutate validated project memory;
- mutate validated system memory;
- promote memory;
- treat its local state as Pantheon truth;
- read undocumented internal state unless policy explicitly allows it.

Reference:

```text
HERMES_INTEGRATION.md
```

---

# 14. Evidence Pack requirements

Every memory candidate intended for promotion must include:

```text
files_read
sources_used
commands_run
tools_used
knowledge_bases_consulted
documents_used
assumptions
unsupported_claims
limitations
outputs
approval_required
next_safe_action
```

If evidence is incomplete:

```text
Do not promote.
```

---

# 15. Example

Repeated observation:

```text
Quote reviews often miss VMC scope coordination.
```

Candidate:

```text
Check VMC scope in quote_vs_cctp_review.
```

Evidence:

```text
Multiple reviewed CCTP/quote comparisons with missing VMC scope.
```

Validation:

```text
THEMIS confirms responsibility relevance.
APOLLO confirms reusable quality.
```

Promotion:

```text
SYSTEM memory if reusable.
PROJECT memory if tied to one project.
```

---

# 16. Summary

```text
session    = temporary working context
candidates = unvalidated proposals
project    = validated project-specific memory
system     = validated reusable memory
knowledge  = source documents, not memory
```

Final rule:

```text
No evidence, no promotion.
No validation, no memory.
```
