# Pantheon Doctor Report — 2026-05-10

Repository: `/home/user/Pantheon-OS`
Mode: C0 read-only
Operator: `operations/doctor.py`

> Companion to `operations/doctor.md`. Doctor observes and reports.
> Doctor does not repair, does not mutate sources, does not call the network.

## Summary

| Category | Status | Checks |
|---|---|---:|
| Root entry points | PASS | 1 |
| AI logs | PASS | 1 |
| Governance documents | WARN | 4 |
| Doctrine coherence | PASS | 3 |
| Runtime boundary | PASS | 1 |
| Canonical paths | WARN | 2 |
| Hygiene | PASS | 1 |

## Findings

| Check | Status | Evidence | Risk | Next action |
|---|---|---|---|---|
| `root_entry_points` | PASS | README.md, CLAUDE.md, CHANGELOG.md, VERSION present | low | — |
| `ai_logs_readme_present` | PASS | ai_logs/README.md found | low | — |
| `governance_docs_present` | PASS | 27 required governance docs present under docs/governance/ | low | — |
| `role_signal_docs_present` | PASS | ROLE_SIGNALS.md, ROLE_SIGNAL_PROFILES.md, ROUTING_FOUNDATION.md present | low | — |
| `doctrine_lines_present` | PASS | canonical OpenWebUI/Hermes/Pantheon Next triplet found in README, CLAUDE, STATUS | low | — |
| `architecture_doctrine_layers` | PASS | ARCHITECTURE.md mentions OpenWebUI, Hermes Agent and Pantheon | low | — |
| `hermes_not_in_agents_table` | PASS | no `\| HERMES \|` row found in AGENTS.md | low | — |
| `governance_index_coverage` | WARN | unreferenced in README.md: EXTERNAL_MEMORY_RUNTIME_REVIEWS_OPENCONCHO_HONCHO.md, EXTERNAL_RUNTIME_OPTION_REVIEWS_KANWAS_AKS_AGENTRQ_OPENCODE_SIX_HATS.md | low | add missing entries to docs/governance/README.md |
| `governance_dead_links` | WARN | unresolved: AI_LOG.md, EVALUATION.md, EXTERNAL_RUNTIME_REVIEW_TEMPLATE.md | medium | add the missing docs or fix the dead references |
| `forbidden_endpoints_absent` | PASS | no POST /agents/run, /runtime/execute or /memory/promote/auto handler in platform/api/ | low | — |
| `forbidden_paths_absent` | PASS | no domains/architecture, workflows/generic or memory/agency present | low | — |
| `legacy_paths_classified` | WARN | present but unclassified: skills/generic | medium | add a classification row in CODE_AUDIT_POST_PIVOT.md |
| `critical_todos_absent` | PASS | no TODO!/FIXME!/XXX! markers in docs, operations, platform/api or ai_logs | low | — |

## Required approvals before fix

| Finding | Approval |
|---|---|
| `governance_index_coverage` | C1 |
| `governance_dead_links` | C1 |
| `legacy_paths_classified` | C1 |

## Evidence Pack references

- files read: governance Markdown under `docs/governance/`, `README.md`, `CLAUDE.md`, `ai_logs/README.md`, `platform/api/**/*.py`
- commands run: none (no shell, no network, no mutation)
- assumptions: doctor checks reflect `operations/doctor.md` C0 scope
- limitations: live API endpoints, OpenWebUI runtime, Hermes runtime and Docker stack are not probed
