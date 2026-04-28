# Project Context Resolution — Tests

> Documentation-level tests. These tests define expected behavior before implementation.

---

# 1. General request must not force project context

## Given

A user asks a general question that does not require project-specific data.

## Expected

```yaml
project_context:
  status: not_required
  recommended_action: proceed_without_project_context
```

---

# 2. Clear project alias resolves directly

## Given

The request contains a validated project alias.

## Expected

```yaml
project_context:
  status: resolved
  confidence_min: 0.85
  allowed_knowledge_bases_required: true
```

---

# 3. Typo-tolerant matching proposes candidates

## Given

The user gives an approximate project name with typos.

## Expected

```yaml
project_context:
  status: resolved | ambiguous
  matched_clues_required: true
  evidence_required: true
```

If confidence is below threshold, the system asks the user.

---

# 4. Partial clue matching

## Given

The user remembers only a municipality, street, client name or project subject.

## Expected

The system must search aliases and metadata before asking the user.

```yaml
expected_sources:
  - project_alias_registry
  - project_memory
  - knowledge_registry
  - notion_read_only_lookup_if_allowed
```

---

# 5. Ambiguous project requires user clarification

## Given

Two or more projects match with similar confidence.

## Expected

```yaml
project_context:
  status: ambiguous
  recommended_action: ask_user
```

The user question must be short and list candidate projects.

---

# 6. Unresolved project blocks project Knowledge use

## Given

Project identity is unresolved.

## Expected

```yaml
forbidden:
  - use_project_knowledge_base
  - use_project_memory
```

---

# 7. Notion is read-only by default

## Given

The system needs Notion to resolve context.

## Expected

```yaml
allowed:
  - read_notion
forbidden_without_approval:
  - write_notion
  - update_alias
  - change_project_status
```

---

# 8. Notion update must be shown before approval

## Given

The system proposes to add an alias or update a project field in Notion.

## Expected

```yaml
notion_update_candidate_required: true
user_approval_required: true
auto_write: false
```
