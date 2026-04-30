# OPENWEBUI INTEGRATION — Pantheon Next

> Governance reference for the OpenWebUI layer in the Pantheon Next architecture.

---

## 1. Role

OpenWebUI is the user cockpit.

It exposes:

- chat;
- Knowledge Bases;
- conversations;
- results;
- approval requests;
- Evidence Pack summaries;
- user-facing actions.

OpenWebUI does not govern Pantheon Next.

OpenWebUI does not execute Hermes tasks.

OpenWebUI does not canonize memory.

---

## 2. Canonical operating rule

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

OpenWebUI must remain a presentation, interaction and validation surface.

It must not become the business authority, the canonical memory layer, the runtime engine or the source of truth.

---

## 3. Connection model

OpenWebUI should connect to Hermes Agent Gateway through an OpenAI-compatible endpoint.

Target example:

```text
OPENAI_API_BASE_URL = http://hermes_agent_gateway:8642/v1
OPENAI_API_KEY = API_SERVER_KEY / HERMES_API_SERVER_KEY
```

Pantheon API is not the OpenAI-compatible backend.

Pantheon API exposes governance, context and domain endpoints such as:

```text
/runtime/context-pack
/domain/snapshot
/domain/approval/policy
/domain/approval/classify
/domain/task-contracts
/domain/evidence-schema
```

OpenWebUI must not point to Pantheon API unless a dedicated and explicitly documented `/v1` model gateway is created later.

This is not the current target.

---

## 4. Knowledge is not memory

OpenWebUI Knowledge is a document retrieval surface.

Pantheon Memory is validated canonical memory.

Rule:

```text
OpenWebUI Knowledge ≠ Pantheon Memory.
```

A document uploaded to an OpenWebUI Knowledge Base may be used as a source.

It becomes Pantheon memory only if the information is:

1. extracted;
2. recorded as a memory candidate;
3. supported by an Evidence Pack;
4. reviewed;
5. approved at C3 minimum;
6. promoted to `memory/project` or `memory/system`.

OpenWebUI conversation history is not Pantheon memory.

---

## 5. Approval surface

OpenWebUI may display approval requests created by Pantheon or returned by Hermes under Pantheon policy.

Possible actions:

- approve;
- reject;
- request clarification;
- ask for another Evidence Pack;
- ask for rerun with stricter constraints;
- request THEMIS/APOLLO review.

OpenWebUI does not define the approval level.

Approval levels are defined in:

```text
docs/governance/APPROVALS.md
```

---

## 6. Evidence display

OpenWebUI may display a user-facing Evidence Pack summary.

Minimum display fields:

- task id;
- task contract id;
- criticality;
- sources used;
- files read;
- tools used;
- assumptions;
- limitations;
- unsupported claims;
- approval required;
- next safe action.

The canonical Evidence Pack format is defined in:

```text
docs/governance/EVIDENCE_PACK.md
```

---

## 7. OpenWebUI plugins and extensions

OpenWebUI plugins are external tools.

They are not Pantheon skills.

They are not Pantheon governance.

They must be classified before use in:

```text
docs/governance/EXTERNAL_TOOLS_POLICY.md
```

Default rule:

```text
blocked until reviewed
```

Forbidden by default:

- batch install from GitHub;
- plugins with hidden memory write;
- plugins with shell access;
- plugins that send external messages without approval;
- plugins that bypass Evidence Packs;
- plugins that turn OpenWebUI into the runtime authority.

---

## 8. Recommended first capabilities

OpenWebUI capabilities may be reviewed later under external tools policy.

Potential candidates:

- Markdown quality display;
- Evidence Pack viewer;
- approval request display;
- Knowledge source selector;
- export to Word / PDF / Excel;
- lightweight mind map or infographic rendering.

Each must be reviewed individually.

No batch installation.

---

## 9. SearXNG and search

SearXNG may be used as a local search capability only if classified in `EXTERNAL_TOOLS_POLICY.md`.

Rules:

- local or LAN exposure only unless explicitly approved;
- no direct memory write;
- no automatic source trust;
- results must be cited or recorded in an Evidence Pack when consequential;
- external search must not bypass domain source policy.

---

## 10. Non-goals

OpenWebUI must not implement:

- Pantheon governance;
- canonical memory promotion;
- autonomous runtime orchestration;
- uncontrolled plugin installation;
- secret access;
- direct repository mutation;
- skill activation;
- workflow activation;
- external communication without approval.

---

## 11. Status

Current status: documented target.

To verify:

- actual OpenWebUI endpoint configuration;
- Hermes Gateway availability;
- whether OpenWebUI Actions are installed;
- whether approval display is implemented;
- whether Evidence Pack summaries are displayed;
- whether Knowledge source metadata is preserved.
