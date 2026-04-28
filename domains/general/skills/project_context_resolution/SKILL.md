# Project Context Resolution

> Candidate Pantheon skill. Resolves which project, topic and source context a user request belongs to before a workflow uses project-specific data.

---

# 1. Purpose

`project_context_resolution` prevents Pantheon from answering with the wrong project context.

It identifies the likely project behind a request, including alternate names, shorthand labels, old names, client-side names and internal references.

It may use session context, previous messages, project memory, Knowledge metadata and approved Notion lookups to resolve ambiguity.

---

# 2. Core rule

```text
Resolve the project context before using project-specific knowledge, memory or workflow actions.
```

If the context is ambiguous, the skill must ask for confirmation instead of guessing silently.

---

# 3. Responsibilities

This skill may:

- detect whether the request is project-specific or system-wide;
- identify candidate projects;
- match project aliases;
- review recent conversation context;
- review session memory;
- query project memory when available;
- inspect Knowledge Registry metadata;
- request a read-only Notion lookup if policy allows;
- produce a confidence score;
- ask the user when confidence is insufficient;
- propose a project alias update candidate;
- propose a Notion update candidate;
- show the exact fields it wants to update before any write.

---

# 4. Non-responsibilities

This skill must not:

- write to Notion without explicit user approval;
- create or update Pantheon memory directly;
- merge two projects without validation;
- expose private raw conversation history;
- use a project Knowledge Base if the project identity is unresolved;
- silently persist inferred aliases;
- treat Notion as more authoritative than signed project documents or Pantheon validated memory.

---

# 5. Resolution order

```text
1. Current user request
2. Current chat title and recent visible messages
3. Session memory
4. Project alias registry
5. Pantheon project memory
6. OpenWebUI Knowledge Registry
7. Notion read-only lookup if allowed
8. User clarification if uncertainty remains
```

---

# 6. Confidence policy

```yaml
high_confidence:
  threshold: 0.85
  action: proceed_with_trace

medium_confidence:
  threshold: 0.60
  action: consult_memory_or_notion_read_only

low_confidence:
  threshold: below_0.60
  action: ask_user
```

Even with high confidence, user validation is required if the request leads to a durable update, Notion write, memory promotion, contract-sensitive action or cross-project comparison.

---

# 7. Output contract

The skill returns:

```yaml
project_context:
  status: resolved | ambiguous | unresolved
  selected_project_id: null
  selected_project_label: null
  matched_aliases: []
  candidate_projects: []
  confidence: 0.0
  evidence:
    - source: current_request | conversation | memory | knowledge_registry | notion
      summary: ""
  missing_information: []
  allowed_knowledge_bases: []
  forbidden_knowledge_bases: []
  recommended_action: proceed | ask_user | read_notion | propose_update
```

---

# 8. Notion policy

Notion may be used as a structured project registry if connected and authorized.

Allowed first phase:

```text
read-only lookup
```

Forbidden without explicit approval:

```text
create page
update page
rename project
add alias
change status
change client data
change contract data
```

Before any write, Pantheon must display:

```yaml
notion_update_candidate:
  target_database: ""
  target_page: ""
  proposed_changes:
    - field: ""
      before: ""
      after: ""
      reason: ""
  requires_user_approval: true
```

---

# 9. Alias handling

Aliases are candidates until validated.

Examples of aliases:

- internal project code;
- client-side project name;
- building name;
- municipality shorthand;
- old name;
- folder name;
- Notion page title.

Alias promotion requires evidence and approval.

---

# 10. Status

Current status: `candidate`.

This skill is not active until reviewed with Knowledge Registry, memory policy and Notion connector policy.
