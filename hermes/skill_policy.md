# Hermes Skill Policy — Pantheon OS

> Reference policy for using Hermes skills inside Pantheon OS.

---

# 1. Principle

Hermes provides executable skills.

Pantheon provides governance, domain contracts and validation.

```text
Hermes skill = executable capability.
Pantheon skill = domain contract + governance layer.
```

Pantheon must not duplicate an existing Hermes capability when a controlled wrapper is enough.

---

# 2. Creation rule

Before creating a new Pantheon skill, the system must check:

```text
1. existing Pantheon skills;
2. existing Pantheon workflows;
3. Hermes built-in skills;
4. Hermes optional skills;
5. community skills as inspiration only;
6. near-duplicate names;
7. runtime and privacy risks.
```

A new skill can only be created as `candidate` first.

---

# 3. Decision classes

| Decision | Meaning |
|---|---|
| `use_existing` | Existing Pantheon skill or workflow is sufficient |
| `use_hermes_builtin` | Hermes built-in skill is sufficient under Pantheon policy |
| `wrap_hermes_skill` | Hermes executes; Pantheon defines contract, inputs, outputs and approvals |
| `create_candidate` | New Pantheon candidate skill is justified |
| `extend_existing` | Existing Pantheon skill should receive an update proposal |
| `reject_duplicate` | Request is already covered |
| `block_for_safety` | Request is too risky without sandbox, approval or policy |

---

# 4. Optional skills

Hermes optional skills are not enabled by default.

Pantheon rule:

```text
No Hermes optional skill may be installed, enabled or used in a real workflow without review.
```

Review must check:

- real utility;
- dependencies;
- API keys;
- filesystem access;
- network access;
- external actions;
- privacy exposure;
- sandbox requirement;
- rollback path.

---

# 5. Community skills

Community skills are inspiration sources, not trusted capabilities.

They must be classified as:

```text
integrate_now
integrate_later
interesting_not_priority
redundant
risky
reject
```

No community skill is installed directly into a Pantheon production environment.

---

# 6. External repository classification

Any repository used as inspiration must be evaluated only for what improves Pantheon.

For each retained idea, document:

- problem solved;
- Markdown file to modify;
- target section;
- architecture impact;
- code impact;
- risks;
- priority.

No external architecture is copied mechanically.

---

# 7. Skill factory policy

Automatic skill creation is not allowed.

A skill-factory mechanism may only produce a proposal.

Required flow:

```text
observed pattern
→ candidate proposal
→ name check
→ duplicate check
→ Hermes skill check
→ privacy check
→ review
→ human validation
→ file creation
```

Generated skills must not be written directly into active skill folders.

---

# 8. Meta-reasoning policy

Meta-reasoning skills such as analytical prisms, self-reflection and blind-spot reports are allowed as inspiration.

They must remain controlled:

- no hidden automatic self-improvement;
- no silent rewrite of active skills;
- explicit constraint report when analysis is partial;
- clear statement of what was not checked;
- no project memory promotion without review.

---

# 9. Manifest mapping

A Pantheon skill that uses Hermes must define a mapping:

```yaml
hermes_mapping:
  type: wrap_hermes_skill
  hermes_skill: official/category/name
  activation_required: true
  sandbox_required: true
  approval_required: true
```

If no Hermes skill is found:

```yaml
hermes_mapping:
  type: none_found
  checked: true
```

---

# 10. Risky skills

The following are risky by default:

- terminal;
- browser automation;
- web actions;
- MCP;
- file mutation;
- scheduler;
- gateways;
- credentials;
- external APIs;
- autonomous coding agents;
- automatic skill generation;
- automatic memory promotion.

Rule:

```text
sandbox + visible execution + approval required
```

---

# 11. Privacy

No real data from private conversations, real projects, clients, companies, addresses, construction sites or identifiable people may be injected into a Hermes skill without explicit validation.

Examples and tests must be fictional.

---

# 12. Updates

A positive result does not modify an active skill directly.

Required flow:

```text
useful result
→ UPDATES.md
→ review
→ optimization
→ validation
→ SKILL.md
```

XP may be granted only for real improvement, detected blockage, fixed blockage, simplification or new guardrail.

XP never triggers automatic level-up.

---

# 13. Final rule

Pantheon governs Hermes.

It does not replace it, duplicate it or delegate governance to it.
