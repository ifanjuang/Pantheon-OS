# Agents — Pantheon Next

> Local maintenance folder for Pantheon Roles.

Pantheon agents are abstract cognitive and governance roles.

They are not runtime workers.

Hermes Agent executes.
Pantheon Roles govern, review, classify, arbitrate and validate.

---

## 1. Purpose

This folder may contain local documentation and metadata for each Pantheon Role.

Recommended structure:

```text
agents/{ROLE}/
  AGENT.md
  role_signal_profile.yaml
  examples.md
```

The local files describe role-specific usage.

They do not replace governance documents.

---

## 2. Canonical references

The following documents remain authoritative:

```text
docs/governance/AGENTS.md
docs/governance/ROLE_SIGNALS.md
docs/governance/ROLE_SIGNAL_PROFILES.md
docs/governance/EPISTEMIC_CONTROL.md
docs/governance/TASK_CONTRACTS.md
docs/governance/EVIDENCE_PACK.md
docs/governance/APPROVALS.md
```

Hierarchy:

```text
ROLE_SIGNALS.md = shared protocol
EPISTEMIC_CONTROL.md = claim, uncertainty and evidence rules
ROLE_SIGNAL_PROFILES.md = central profile registry and invariants
agents/{ROLE}/role_signal_profile.yaml = local role usage profile
```

If a local profile conflicts with governance documents, the governance documents win.

---

## 3. What belongs here

Allowed:

```text
local role profile
role-specific signal usage
role-specific required payloads
role-specific forbidden behaviors
role-specific escalation triggers
role-specific examples
public summary templates
```

Forbidden:

```text
runtime implementation
agent loop
message bus
tool execution authority
approval authority
memory promotion authority
skill activation authority
workflow canonization authority
hidden chain-of-thought
private client or project data
```

---

## 4. Local Role Signal Profile

Each role may eventually have:

```text
agents/{ROLE}/role_signal_profile.yaml
```

This file describes how the role uses Role Signals.

It must not redefine the Role Signal schema.

Minimum required references:

```yaml
canonical_schema: docs/governance/ROLE_SIGNALS.md
epistemic_reference: docs/governance/EPISTEMIC_CONTROL.md
profile_index: docs/governance/ROLE_SIGNAL_PROFILES.md
```

Core rule:

```text
The local profile may narrow authority.
The local profile may not expand authority.
```

---

## 5. Maintenance rule

When a role evolves:

1. update `docs/governance/AGENTS.md` if the responsibility changes;
2. update `docs/governance/ROLE_SIGNAL_PROFILES.md` if the central fallback or invariant changes;
3. update `agents/{ROLE}/role_signal_profile.yaml` if only the local usage profile changes;
4. add an `ai_logs/` entry for significant changes.

---

## 6. Current status

Local agent folders are optional.

A missing local profile means IRIS and future validators use the central fallback profile in:

```text
docs/governance/ROLE_SIGNAL_PROFILES.md
```

No local profile in this folder activates a runtime behavior.
