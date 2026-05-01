# Governance docs

Source of truth for project doctrine, architecture, status and policies.

These files were originally at the repository root and have been moved here
to keep the root readable. The runtime references them by filename via
`platform/api/pantheon_runtime/router.py` (truth_files) and a few skill
manifests under `domains/general/skills/`.

## Inventory

| File | Role |
|---|---|
| `AGENTS.md` | Abstract agent roster and responsibilities |
| `APPROVALS.md` | Approval criticality policy (C1/C2/C3) |
| `ARCHITECTURE.md` | Technical anatomy post-pivot |
| `EVIDENCE_PACK.md` | Audit contract for consequential outputs |
| `EXTERNAL_TOOLS_POLICY.md` | Governance for external integrations |
| `EXTERNAL_WATCHLIST.md` | External repo / tool watchlist |
| `HERMES_INTEGRATION.md` | Pantheon ↔ Hermes ↔ OpenWebUI boundary |
| `KNOWLEDGE_TAXONOMY.md` | Knowledge vs Memory classification |
| `MEMORY.md` | Memory governance (validated lessons) |
| `MODULES.md` | Module definition contract |
| `ROADMAP.md` | Active priorities and Memory roadmap |
| `STATUS.md` | Project state — components delivery status |
| `TASK_CONTRACTS.md` | Hermes/Pantheon task execution contracts |
| `VERSIONS.md` | Tracking versions of runtimes and models |

Stays at the repository root (entry points / SemVer):

- `README.md`
- `CLAUDE.md`
- `CHANGELOG.md`
- `VERSION`

The AI coordination journal lives in `ai_logs/` (one file per session, plus `ai_logs/README.md` for the rules).
