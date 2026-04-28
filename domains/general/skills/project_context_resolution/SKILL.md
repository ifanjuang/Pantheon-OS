# Project Context Resolution

> Candidate Pantheon skill. Resolves whether a user request needs project context and, if so, which project, topic and source context it belongs to.

---

# 1. Purpose

`project_context_resolution` prevents Pantheon from answering with the wrong project context.

It identifies the likely project behind a request, including alternate names, shorthand labels, old names, client-side names, internal references, municipalities, streets, client names, building names, topics and partial user memories.

It must also detect when no project context is required.

Not every question needs project resolution. If the request is general, procedural, conceptual or answerable with high confidence without project-specific data, the skill must not force a project lookup.

---

# 2. Core rule

```text
Resolve project context only when project-specific memory, knowledge, documents or workflow actions are needed.
```

If the project context is needed and ambiguous, the skill must ask for confirmation instead of guessing silently.

If no project context is needed, it must return `status: not_required` and let the workflow continue.

---

# 3. Responsibilities

This skill may:

- detect whether the request is project-specific, system-wide or context-free;
- identify candidate projects;
- match project aliases;
- tolerate typos, approximate names and incomplete references;
- use partial clues such as municipality, street, client name, building type, subject, document type or past discussion topic;
- review recent visible conversation context;
- review session memory;
- query project memory when available;
- inspect Knowledge Registry metadata;
- request a read-only Notion lookup if policy allows;
- produce a confidence score;
- ask the user which project is meant when confidence is insufficient;
- propose a project alias update candidate;
- propose a Notion update candidate;
- show the exact fields it wants to update before any write.

---

# 4. Non-responsibilities

This skill must not:

- force project resolution when the answer does not need it;
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
2. Need-for-context check
3. Current chat title and recent visible messages
4. Session memory
5. Project alias registry
6. Pantheon project memory
7. OpenWebUI Knowledge Registry
8. Notion read-only lookup if allowed
9. User clarification if uncertainty remains
```

---

# 6. Need-for-context check

Before searching for a project, the skill must decide whether project context is required.

Project context is not required when the request is:

- general advice;
- conceptual architecture;
- system design;
- generic regulatory explanation;
- generic wording improvement;
- generic social media rewriting;
- answerable with already visible context;
- explicitly not tied to a project.

Project context is required when the request depends on:

- a project document;
- a project contract;
- a quote, CCTP, DPGF, PLU, notice or report;
- project memory;
- client-specific facts;
- project timeline;
- project responsibilities;
- a Notion project record;
- a project Knowledge Base.

---

# 7. Confidence policy

```yaml
not_required:
  action: proceed_without_project_context

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

# 8. Output contract

The skill returns:

```yaml
project_context:
  status: not_required | resolved | ambiguous | unresolved
  selected_project_id: null
  selected_project_label: null
  matched_aliases: []
  matched_clues: []
  candidate_projects: []
  confidence: 0.0
  evidence:
    - source: current_request | conversation | session_memory | project_memory | knowledge_registry | notion
      summary: ""
  missing_information: []
  allowed_knowledge_bases: []
  forbidden_knowledge_bases: []
  recommended_action: proceed_without_project_context | proceed | ask_user | read_notion | propose_update
```

---

# 9. User clarification

When uncertainty remains, the skill asks a short targeted question.

Preferred format:

```text
Which project are you referring to?
1. Candidate project A
2. Candidate project B
3. Another project
```

If the user only remembers a partial clue, the system may ask for:

- municipality;
- street;
- client name;
- building type;
- project subject;
- approximate year;
- document type;
- internal folder name.

---

# 10. Notion policy

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

# 11. Alias handling

Aliases are candidates until validated.

Examples of aliases and clues:

- internal project code;
- client-side project name;
- building name;
- municipality shorthand;
- street name;
- client or stakeholder name;
- old project name;
- folder name;
- Notion page title;
- main project subject.

Alias promotion requires evidence and approval.

---

# 12. Status

Current status: `candidate`.

This skill is not active until reviewed with Knowledge Registry, memory policy and Notion connector policy.
