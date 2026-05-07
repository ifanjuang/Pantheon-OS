# OPENWEBUI_PLUGIN_POLICY.md

## Purpose

This document defines how OpenWebUI plugins, Functions, Tools, Pipes, Filters and Actions may be used inside Pantheon Next.

OpenWebUI is a cockpit, not an execution runtime.

Core doctrine:

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

---

# Security baseline

OpenWebUI Functions execute Python code on the OpenWebUI server.

Therefore every Function, Tool, Pipe, Filter or Action must be treated as executable code.

Default policy:

```text
deny by default
allow by review
minimal permissions
no secrets by default
no filesystem by default
no shell by default
```

---

# Allowed OpenWebUI roles

OpenWebUI may:

- host chat sessions;
- expose Knowledge Collections;
- upload documents;
- display retrieved sources;
- display Evidence Packs;
- display approval requests;
- collect user approval or rejection;
- trigger approved Hermes actions;
- apply display filters;
- expose workspace models connected to Hermes.

---

# Forbidden OpenWebUI roles

OpenWebUI must not:

- become a workflow runtime;
- execute critical tools directly;
- mutate the repository directly;
- promote canonical memory;
- manage Pantheon approvals internally;
- run shell commands for C3+ actions;
- access secrets without explicit policy;
- bypass Hermes for governed execution;
- act as a provider router for Pantheon workflows.

---

# Function types

## Pipe

Pipe Functions can appear as selectable models.

Allowed use:

- route to Hermes;
- present specialized cockpit flows;
- wrap read-only retrieval;
- expose a non-critical UI integration.

Restricted use:

- multi-step agent execution;
- file mutation;
- external API write actions;
- shell execution.

A Pipe must not compete with Hermes Gateway as the main Pantheon execution endpoint.

---

## Filter

Filter Functions can intercept messages.

Allowed use:

- source display normalization;
- Evidence Pack formatting;
- light PII warning;
- citation formatting;
- prompt boundary reminders.

Restricted use:

- silent prompt mutation;
- hidden policy override;
- memory extraction;
- execution routing;
- modifying approval status.

Filters must be transparent when they affect governance-relevant content.

---

## Action

Action Functions add buttons to messages.

Allowed use:

- approve/reject candidate;
- request Evidence Pack;
- rerun through Hermes;
- export response;
- open source document;
- create approval request;
- send approved action back to Hermes.

Restricted use:

- execute shell;
- write repository;
- send external communication;
- delete data;
- mutate canonical memory.

Actions are appropriate for human-in-the-loop validation, not autonomous execution.

---

# Tools

OpenWebUI Tools may be used for low-risk read-only access.

Allowed examples:

- weather-like informational lookups;
- read-only internal search;
- source formatting;
- UI helper calls.

Pantheon-critical tools must be exposed through Hermes instead.

---

# Approval mapping

| Action type | Default level | Required handling |
|---|---|---|
| Display / formatting | C0 | Allowed if reviewed |
| Read-only retrieval | C0/C1 | Allowed with source display |
| Draft generation | C2 | Route through Hermes |
| Candidate approval UI | C3 | Human click + logged decision |
| Repo mutation | C3/C5 | Not directly in OpenWebUI |
| External communication | C4 | Draft only unless explicit approved connector |
| Secrets / destructive action | C5 | Prohibited by default |

---

# Plugin review checklist

Before enabling a plugin, verify:

```text
source repository
maintainer credibility
code scope
network access
filesystem access
secret access
shell/subprocess usage
external write actions
data retention
logging behavior
approval level
fallback behavior
```

Plugins from community repositories are `test-only` until reviewed.

---

# Recommended Pantheon OpenWebUI components

Initial allowed components should be limited to:

```text
Evidence Pack display Action
Approval request Action
Approve/Reject candidate Action
Hermes rerun Action
Source formatting Filter
Pantheon boundary reminder Filter
```

Everything else requires explicit review.

---

# Network policy

OpenWebUI plugins may call:

- Hermes Gateway;
- Pantheon read-only endpoints;
- approved internal services.

OpenWebUI plugins must not call:

- arbitrary external APIs;
- payment services;
- email senders;
- file deletion endpoints;
- GitHub write APIs;
- shell-execution APIs;
- memory promotion APIs.

Unless explicitly approved.

---

# Secrets policy

Plugins must not receive secrets by default.

If a plugin needs a secret:

- it must be documented;
- it must be scoped;
- it must be stored outside source code;
- it must not be shown to the model;
- it must not be logged;
- it must be reviewed as C5 if misuse is destructive.

---

# Logging policy

Governed OpenWebUI actions should log:

- action name;
- user/session reference;
- target message;
- approval result;
- timestamp;
- linked Evidence Pack;
- linked candidate or task.

Logs should not store raw secrets or private client data unless explicitly required and approved.

---

# Prohibited patterns

The following are forbidden:

- importing unreviewed plugin packs wholesale;
- global Functions with hidden behavior;
- plugin-based runtime orchestration;
- plugin-based memory promotion;
- plugin-based repo mutation;
- plugin-based external sending;
- plugin direct shell access;
- plugin bypassing Hermes approval checks.

---

# Decision principle

```text
OpenWebUI may trigger and display.
Hermes must execute.
Pantheon must govern.
```
