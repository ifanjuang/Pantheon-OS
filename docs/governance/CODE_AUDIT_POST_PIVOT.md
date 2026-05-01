# CODE AUDIT POST PIVOT — Pantheon Next

> Audit register for code and operational assets created before or during the Hermes-backed pivot.

---

## 1. Purpose

Pantheon Next has pivoted away from an autonomous agentic runtime.

The current target is:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

This document prevents two opposite mistakes:

1. deleting useful legacy code too early;
2. silently reactivating the old autonomous runtime path.

Legacy code must be classified before reuse, deletion or extension.

---

## 2. Audit rule

Before changing legacy code, classify it.

Allowed decisions:

```text
keep
reorient
archive
delete_later
to_verify
legacy
```

Definitions:

| Status | Meaning |
|---|---|
| keep | Component is aligned with Pantheon Next and may remain active |
| reorient | Component contains useful logic but must be reframed as governance, context, schema, contract or Hermes-side capability |
| archive | Component is kept for history only and must not be imported by active runtime |
| delete_later | Component appears obsolete but must be removed only after confirmation |
| to_verify | Component requires inspection before decision |
| legacy | Component belongs to the previous autonomous architecture and must not be extended without review |

---

## 3. Mandatory table

| Component | Path | Former role | Status | Proposed decision | Risk | Next action | Priority |
|---|---|---|---|---|---|---|---|
| FastAPI entrypoint | `platform/api/main.py` | API entrypoint | to_verify | Keep only if Domain API remains lightweight | May drift into runtime | Check routes against `ARCHITECTURE.md` | P0 |
| Domain Layer package | `platform/api/pantheon_domain/` | Domain API definitions | keep | Keep and align with context/policy endpoints | Low | Verify exposed routes | P0 |
| Runtime context package | `platform/api/pantheon_runtime/` | Static context pack endpoint | reorient | Rename conceptually as context export, not runtime | Name suggests Pantheon runtime | Avoid adding execution endpoints | P0 |
| Legacy dynamic registry | `platform/api/core/registry.py` | Runtime/module registry | to_verify | Reorient only if used for read-only domain metadata | May revive runtime pattern | Inspect imports and active use | P1 |
| Registries package | `platform/api/core/registries/` | Runtime registries | to_verify | Keep only as metadata registry if read-only | Agent/tool runtime drift | Audit dependencies | P1 |
| Approvals app | `platform/api/apps/approvals/` | Approval API | to_verify | Keep if aligned with C0-C5 policy | Could bypass docs if divergent | Compare with `APPROVALS.md` | P1 |
| Alembic migrations | `platform/api/alembic/` | Database migrations | to_verify | Keep only if used by active Domain API | Schema may encode old runtime | Audit migration chain | P1 |
| `modules.yaml` | `modules.yaml` | App/module enable registry | legacy | Do not extend until audited | May reactivate old modules | Classify each module | P1 |
| Docker Compose | `docker-compose.yml` | Previous stack | legacy | Keep until replaced by scoped compose docs | May deploy unwanted services | Create operations install doc before change | P1 |
| Installer UI | `scripts/install/ui/` | Installation interface | legacy | Archive or reorient after audit | Heavy UI before governance stabilized | Inspect before reuse | P2 |
| Legacy folder | `legacy/` | Archived components | archive | Keep non-imported | Accidental import | CI or doctor check later | P2 |
| Run Graph code | unknown | Runtime trace graph | to_verify | Keep only as future Evidence display if present | Can become runtime orchestration | Locate implementation | P2 |
| Memory promotion runtime | unknown | Automatic memory promotion | to_verify | Block unless candidate + C3 review | Memory pollution | Search before enabling | P1 |
| Skill promotion runtime | unknown | Automatic skill activation | to_verify | Block unless candidate review | Governance bypass | Search before enabling | P1 |
| LangGraph adapters | unknown | Graph orchestration | to_verify | Hermes-side only if kept | Recreates Pantheon runtime | Locate before use | P2/P3 |
| ARQ / Redis workers | unknown | Async runtime jobs | to_verify | Defer unless Domain API needs jobs | Runtime creep | Audit before deployment | P3 |
| Dashboard code | unknown | Admin UI | to_verify | Defer; OpenWebUI first | Heavy dashboard risk | Locate and classify | P3 |

---

## 4. Components to inspect first

Priority inspection list:

```text
platform/api/main.py
platform/api/pantheon_domain/
platform/api/pantheon_runtime/
platform/api/apps/
platform/api/core/registry.py
platform/api/core/registries/
modules.yaml
docker-compose.yml
.env.example
pyproject.toml
legacy/
scripts/install/ui/
```

---

## 5. Reclassification patterns

Old runtime concept → Pantheon Next-compatible form:

| Old concept | Correct reclassification |
|---|---|
| Agent loop Pantheon | Task Contracts + abstract agents + Hermes execution |
| DecisionPlan | Task Contract |
| ExecutionResult | Evidence Pack |
| Tool registry | External Tools Policy |
| Workflow engine | Workflow definitions executed by Hermes |
| Scheduler | External scheduler or Hermes-side capability under approval |
| Provider router | Runtime/provider concern handled outside Pantheon governance |
| Patch auto-apply | Patch candidate + Evidence Pack + approval |
| Memory consolidation job | Memory candidate + C3 promotion review |
| Plugin manager | Policy + sandbox + allowlist/blocklist |
| Dashboard runtime | Domain snapshot + OpenWebUI display |

---

## 6. Hard blockers

The following must not be reactivated inside Pantheon Next:

```text
Execution Engine
Agent Runtime
Tool Runtime
LLM Provider Router
Scheduler
LangGraph central orchestrator
memory auto-promotion
self-evolution auto-merge
plugin batch install
Docker socket access
secret access by default
public admin dashboard without auth/VPN
```

---

## 7. Evidence required for audit decisions

Every audit decision must identify:

- files read;
- imports checked;
- active routes checked;
- configuration files checked;
- commands run, if any;
- risk level;
- proposed decision;
- rollback or archive path.

Consequential decisions require an Evidence Pack.

Reference:

```text
docs/governance/EVIDENCE_PACK.md
```

---

## 8. Next action

Immediate next audit:

```text
repo_md_audit → code_audit_post_pivot
```

Expected output:

- list active endpoints;
- list legacy runtime components;
- list documentation/code contradictions;
- recommend keep/reorient/archive/delete_later/to_verify/legacy;
- update this table.
