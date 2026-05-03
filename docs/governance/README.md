# Governance docs — Pantheon Next

Source of truth for project doctrine, architecture, status and policies.

These files were originally split between the repository root and governance discussions. They are consolidated under `docs/governance/` to keep the root readable and to make the Markdown governance layer explicit.

The active operating model is:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

The runtime must not treat these documents as decorative notes. They drive development decisions.

---

## Inventory

| File | Role |
|---|---|
| `STATUS.md` | Current project state and implementation status |
| `ROADMAP.md` | Active priorities and phased trajectory |
| `ARCHITECTURE.md` | Technical anatomy after the Hermes-backed pivot |
| `MODULES.md` | Module and domain definition contract |
| `AGENTS.md` | Abstract agent roster and responsibilities |
| `MEMORY.md` | Canonical memory governance |
| `APPROVALS.md` | Approval criticality policy C0-C5 |
| `TASK_CONTRACTS.md` | Hermes/Pantheon task execution contracts |
| `EVIDENCE_PACK.md` | Audit contract for consequential outputs |
| `HERMES_INTEGRATION.md` | Pantheon ↔ Hermes boundary and context export rules |
| `OPENWEBUI_INTEGRATION.md` | OpenWebUI cockpit, Knowledge and validation boundary |
| `OPENWEBUI_DOMAIN_MAPPING.md` | Mapping policy between Pantheon canonical domains and OpenWebUI Knowledge Bases, Workspace Models and operator Skills |
| `MODEL_ROUTING_POLICY.md` | Model selection policy for OpenWebUI presets, Ollama instances, Hermes execution and Pantheon abstract agents |
| `EXTERNAL_TOOLS_POLICY.md` | Governance for external integrations |
| `EXTERNAL_RUNTIME_OPTIONS.md` | Classification of optional runtimes, workflow labs, context engines and graph/workspace tools |
| `EXTERNAL_AI_OPTION_REVIEWS.md` | Focused reviews for AnimoCerebro and Caliber/ai-setup external AI options |
| `KNOWLEDGE_TAXONOMY.md` | Knowledge vs Memory classification |
| `CODE_AUDIT_POST_PIVOT.md` | Legacy/runtime code classification register |
| `PRE_REFACTOR_ARCHITECTURE_FINDINGS.md` | Read-only audit synthesis of existing code assets to preserve or reclassify before refactor |
| `WORKFLOW_SCHEMA.md` | Canonical workflow/task definition schema |
| `WORKFLOW_ADAPTATION.md` | Adaptive workflow doctrine: session workflows, dependency graphs, role consultation, ZEUS arbitration and reset/candidate rules |
| `SKILL_LIFECYCLE.md` | Skill lifecycle, XP, status and Hermes mapping policy |
| `MEMORY_EVENT_SCHEMA.md` | Memory event and candidate schema before promotion |
| `EXTERNAL_WATCHLIST.md` | External repo / tool watchlist |
| `VERSIONS.md` | Tracking versions of runtimes and models |

---

## Root entry points

The following files stay at the repository root:

- `README.md` — product entry point for Pantheon Next.
- `CLAUDE.md` — Claude-specific repository guidance aligned with Pantheon Next.
- `CHANGELOG.md` — release/change history.
- `VERSION` — current version marker.

The AI coordination journal lives in `ai_logs/`.

Reference:

```text
ai_logs/README.md
```

---

## Governance rules

1. Read `ai_logs/README.md` and recent log entries before intervention.
2. Read `docs/governance/STATUS.md` before structural changes.
3. Read the relevant governance document before modifying code.
4. Do not push directly to `main`.
5. Use a dedicated branch.
6. Add an `ai_logs/YYYY-MM-DD-slug.md` entry after significant intervention.
7. Do not write real private project/client data into the repository.
8. If code contradicts Markdown, Markdown is the source of truth.
9. If code is technically better than Markdown, update Markdown first before generalizing the code path.

---

## Forbidden drift

Pantheon Next must not silently recreate:

- autonomous Pantheon runtime;
- Execution Engine;
- Agent Runtime;
- Tool Runtime;
- LLM Provider Router;
- scheduler;
- LangGraph central orchestrator;
- memory auto-promotion;
- self-evolution auto-merge;
- uncontrolled plugin installation.

Hermes Agent executes. Pantheon Next governs. OpenWebUI exposes.
