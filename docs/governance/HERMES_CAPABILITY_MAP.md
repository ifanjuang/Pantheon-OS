# HERMES_CAPABILITY_MAP.md

## Purpose

This document maps Pantheon Next capabilities to the correct operational layer.

It exists to prevent legacy code from being reactivated as an autonomous Pantheon runtime.

Core doctrine:

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

Any capability must be classified before implementation, refactor, migration or deletion.

---

# Classification rules

## Hermes capability

A capability belongs to Hermes when it executes work.

Examples:

- parse a PDF;
- run OCR;
- call a tool;
- inspect a repository;
- prepare a patch candidate;
- generate an Evidence Pack;
- extract memory candidates;
- run a bounded workflow.

Hermes capabilities must be:

- bounded;
- auditable;
- interruptible;
- allowed by policy;
- compatible with approval levels.

---

## OpenWebUI capability

A capability belongs to OpenWebUI when it exposes, displays or validates work.

Examples:

- chat interface;
- Knowledge Base upload;
- model/workspace selection;
- Evidence Pack display;
- approval buttons;
- action buttons;
- filters for display or moderation.

OpenWebUI must not execute critical workflows directly.

---

## Pantheon capability

A capability belongs to Pantheon when it defines governance or truth.

Examples:

- doctrine;
- canonical memory;
- approval policy;
- task contracts;
- abstract workflows;
- Evidence Pack format;
- external tool policy;
- domain taxonomy.

Pantheon must not execute tools directly.

---

## Legacy capability

A capability belongs to legacy when it reintroduces an autonomous Pantheon runtime or conflicts with the current architecture.

Examples:

- Pantheon execution engine;
- Pantheon agent runtime;
- Pantheon tool runtime;
- Pantheon LLM provider router;
- autonomous memory promotion;
- scheduler or event bus inside Pantheon;
- OpenAI-compatible agent backend competing with Hermes Gateway.

Legacy code may be preserved as reference, but must not be reactivated without governance review.

---

# Capability map

| Existing / candidate area | Target layer | Target form | Status | Rule |
|---|---|---|---|---|
| PDF parsing | Hermes | skill/tool | candidate | Execution capability. |
| OCR extraction | Hermes | tool | candidate | Must return evidence metadata and confidence. |
| Table extraction | Hermes | tool | candidate | Useful for DPGF, CCTP and reports. |
| Document ingestion | Hermes | skill | candidate | OpenWebUI uploads; Hermes parses. |
| Knowledge retrieval | Hermes + OpenWebUI | skill / KB | candidate | Retrieval is not canonical memory. |
| Evidence Pack generation | Hermes | skill | priority | Format is defined by Pantheon. |
| Memory candidate extraction | Hermes | skill | priority | Candidate only, never canonical direct write. |
| Canonical memory promotion | Pantheon + human approval | governance process | active doctrine | Requires evidence and approval. |
| Approval classification | Pantheon | policy/API | active doctrine | THEMIS classification before sensitive work. |
| Approval display | OpenWebUI | Action/UI | candidate | User-facing validation only. |
| Repo read-only audit | Hermes | skill | priority | C0/C1 unless it creates patches. |
| Repo patch candidate | Hermes | skill | candidate | Must use branch + diff + Evidence Pack. |
| Repo merge | Human/GitHub | approval action | restricted | Not automatic. |
| External communication draft | Hermes | skill | candidate | External sending requires C4 approval. |
| External communication sending | Human / approved connector | action | restricted | Never automatic by default. |
| Meeting summary | Hermes | skill | candidate | Generates candidates and actions, not canon. |
| OpenWebUI plugins | OpenWebUI | tools/functions/actions | restricted | Must follow plugin policy. |
| Pantheon OpenAI-compatible backend | Legacy | archive/reference | reject as runtime | Hermes Gateway already owns this boundary. |
| Pantheon dynamic module runtime | Legacy / to audit | archive or reorient | risky | May recreate autonomous runtime. |
| Pantheon scheduler/event engine | Legacy | archive/reference | reject as runtime | Scheduling belongs outside Pantheon core. |
| Pantheon LLM provider routing | Legacy | archive/reference | reject | Provider selection belongs to Hermes/OpenWebUI. |
| Auto memory extraction to canonical | Legacy | reject | prohibited | Violates memory governance. |
| LangGraph orchestration | Hermes only | internal runtime option | restricted | No Pantheon LangGraph server. |
| PageIndex / structural retrieval | Hermes/OpenWebUI lab | retrieval adapter | test-only | Knowledge retrieval, not memory. |
| OpenDataLoader PDF | Hermes | parser skill/tool | candidate | Good fit for document ingestion. |
| Mem0 | Hermes | operational memory | test-only | May produce candidates only. |
| Notion mirror | Optional external UI | mirror | optional | Never canonical source of truth. |
| Postgres memory index | Pantheon API / indexer | index | candidate | Index only, not sole canonical store. |

---

# Priority Hermes skills

The first Hermes-compatible skills should be:

```text
pdf_ingest_opendataloader
knowledge_retrieve
evidence_pack_builder
memory_candidate_extract
repo_doctor_readonly
repo_patch_candidate
approval_request
meeting_summary
```

Each skill must define:

- purpose;
- inputs;
- outputs;
- allowed tools;
- forbidden actions;
- approval level;
- Evidence Pack requirements;
- memory policy.

---

# Migration rule

Do not move code into `legacy/` only because Hermes does not currently execute it.

First classify it as:

```text
Hermes capability
OpenWebUI capability
Pantheon governance
Legacy runtime
Reference pattern
```

Only move to legacy when the component clearly reintroduces runtime drift or has no valid target layer.

---

# Decision principle

```text
If it executes, Hermes owns it.
If it displays or validates, OpenWebUI owns it.
If it defines truth, Pantheon owns it.
If it competes with Hermes as runtime, legacy owns it.
```
