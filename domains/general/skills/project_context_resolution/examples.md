# Project Context Resolution — Examples

> Fictional examples only. No real project, client, address or private discussion data.

---

# 1. No project context required

## Input

```text
Explain the general difference between a technical review and a contractual validation.
```

## Result

```yaml
project_context:
  status: not_required
  confidence: 0.95
  recommended_action: proceed_without_project_context
  evidence:
    - source: current_request
      summary: "The request is generic and does not depend on project documents."
```

---

# 2. Clear project alias

## Input

```text
For Hill House, compare the contractor quote with the specification.
```

## Result

```yaml
project_context:
  status: resolved
  selected_project_id: PRJ-001
  selected_project_label: Hill House
  matched_aliases:
    - Hill House
  matched_clues:
    - project_alias
  confidence: 0.92
  evidence:
    - source: project_alias_registry
      summary: "Alias matches PRJ-001."
  allowed_knowledge_bases:
    - KB_PROJECT_PRJ_001
  recommended_action: proceed
```

---

# 3. Typo and partial clue

## Input

```text
Check the planning issue for the Belvil street renovation file.
```

## Result

```yaml
project_context:
  status: ambiguous
  candidate_projects:
    - project_id: PRJ-021
      label: Belleville Street House
      confidence: 0.72
    - project_id: PRJ-033
      label: Belleville Courtyard Works
      confidence: 0.66
  matched_clues:
    - municipality_typo
    - street_name
    - project_subject
  recommended_action: ask_user
```

---

# 4. User clarification

## Prompt

```text
Which project are you referring to?
1. PRJ-021 — Belleville Street House
2. PRJ-033 — Belleville Courtyard Works
3. Another project
```

---

# 5. Notion read-only lookup

## Input

```text
I only remember that it was the small extension project near the station.
```

## Result

```yaml
project_context:
  status: unresolved
  confidence: 0.41
  recommended_action: read_notion
  reason: "No local alias was sufficient. Notion may contain a structured project registry."
```

No write is allowed at this stage.

---

# 6. Notion update candidate

## Proposed visible update

```yaml
notion_update_candidate:
  target_database: "Projects"
  target_page: "PRJ-044"
  proposed_changes:
    - field: "Aliases"
      before: "Station Extension"
      after: "Station Extension, Small extension near the station"
      reason: "The user repeatedly refers to PRJ-044 with this alternate phrase."
  requires_user_approval: true
```

The update is not applied until the user approves it.
