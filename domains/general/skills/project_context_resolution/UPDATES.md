# Project Context Resolution — Updates

> Candidate updates for the `project_context_resolution` skill.

---

# 1. Current status

```yaml
state: candidate
level: 0
validated_xp: 0
pending_xp: 0
```

This skill is not active yet.

---

# 2. Candidate improvements

No candidate improvements yet.

---

# 3. Review checklist before activation

Before activation, review must confirm:

- the skill does not force project context when it is not needed;
- typo-tolerant alias matching is bounded and traceable;
- partial clues such as municipality, street, client name or subject are handled;
- unresolved or ambiguous context blocks project-specific Knowledge use;
- Notion is read-only by default;
- every Notion write is displayed as an update candidate before approval;
- no private raw conversation history is exposed;
- no alias is persisted without validation;
- examples remain fictional and non-identifiable.

---

# 4. Future update candidates

Possible future improvements:

- connect to a `project_alias_registry.yaml` file;
- connect to `knowledge_registry.yaml`;
- define a Notion database field mapping template;
- add a project-context report template for OpenWebUI;
- add fuzzy matching thresholds for aliases and partial clues;
- add source-tier rules for conflicting project evidence.
