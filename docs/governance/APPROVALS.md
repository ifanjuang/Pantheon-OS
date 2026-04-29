# APPROVALS — Pantheon OS

> Reference policy for action criticality and validation levels.

---

# 1. Purpose

`APPROVALS.md` defines the minimum validation level required before Pantheon, Hermes or OpenWebUI performs or proposes an action.

It prevents low-risk reads, reversible drafts, persistent mutations, external communications and critical operations from being treated the same way.

Core rule:

```text
The higher the persistence, exposure, responsibility or irreversibility, the higher the approval level.
```

---

# 2. Criticality levels

| Level | Name | Definition | Approval rule |
|---|---|---|---|
| C0 | Read / diagnostic | Read-only inspection, classification, diagnostics, source lookup | No explicit approval when within scope |
| C1 | Draft / suggestion | Draft text, recommendations, candidate outputs, non-persistent planning | No explicit approval unless sensitive |
| C2 | Low-risk reversible action | Reversible, local, low-risk action with limited scope | System trace required; approval if unclear |
| C3 | Persistent internal change | File mutation, branch patch, memory candidate, workflow candidate, skill candidate, local service configuration | Explicit validation or active instruction required |
| C4 | External / contractual / financial / responsibility action | External communication, client-facing message, contract, finance, responsibility exposure, sensitive redaction review | Explicit user approval required |
| C5 | Critical / irreversible / secrets / destructive | Secrets, deletion, destructive command, Docker socket, privileged volume, irreversible mutation, autonomy plugin | Explicit approval plus policy gate; often forbidden by default |

---

# 3. Action mapping

| Action | Default level | Notes |
|---|---:|---|
| `read` | C0 | Reading files, docs, metadata or public sources |
| `diagnostic` | C0 | Classification, audit, risk analysis without mutation |
| `draft` | C1 | Draft response, draft report, draft workflow, draft skill |
| `file_mutation` | C3 | Any persistent repository or filesystem change |
| `memory_promotion` | C3 | Candidate → project/system memory requires review |
| `external_communication` | C4 | Email, message, publication, client-facing output sent externally |
| `shell` | C3 / C5 | C3 for safe diagnostic commands; C5 for destructive, privileged or secret-related commands |
| `web_side_effect` | C4 | Any action that changes external state |
| `secret_or_volume_access` | C5 | Secrets, credentials, private volumes, Docker socket |
| `destructive` | C5 | Delete, overwrite, purge, force, irreversible mutation |
| `patch_candidate_generation` | C3 | Candidate patch only, no merge and no direct main write |
| `patch_application` | C3+ | Depends on touched files, runtime impact and rollback |
| `fallback_same_risk` | same | Same level as original action, trace required |
| `fallback_higher_risk` | escalated | New approval required before execution |

---

# 4. External tool action mapping

| Action | Default level | Notes |
|---|---:|---|
| `pdf_info_check` | C0 | Read PDF metadata/page count without mutation |
| `pdf_text_layer_check` | C0 | Detect selectable text or scan state |
| `pdf_metadata_check` | C0 / C1 | C1 if privacy interpretation is included |
| `pdf_ocr_prepare` | C2 / C3 | C2 for temporary copy; C3 for persistent project file |
| `pdf_sanitize_before_knowledge` | C3 | Persistent preparation before Knowledge ingestion |
| `pdf_redaction_review` | C3 / C4 | C4 if external/client-facing or responsibility-sensitive |
| `pdf_export_to_knowledge` | C3 | Requires Evidence Pack and Knowledge selection |
| `openwebui_plugin_install` | C3 | One-by-one installation only |
| `openwebui_batch_plugin_install` | C5 | Blocked by default |
| `hermes_plugin_install` | C3 | Sandbox first, allowlist required |
| `hermes_memory_plugin_install` | C4 | Touches memory behavior, review required |
| `hermes_autonomy_plugin_install` | C5 | Blocked by default unless explicit policy |
| `self_evolution_skill_candidate` | C3 | Candidate-only, no active mutation |
| `self_evolution_code` | C5 | Blocked until dedicated policy and sandbox |
| `external_service_install` | C3 | Docker/Portainer/local service install |
| `remote_mcp_server` | C5 | Blocked until audited |
| `secret_access` | C5 | Forbidden unless specific policy allows it |
| `docker_socket` | C5 | Forbidden unless specific policy allows it |

---

# 5. Tool mapping

| Tool category | Default level | Policy |
|---|---:|---|
| read file | C0 | Allowed within scope |
| search files | C0 | Allowed within scope |
| web search / extract | C0 / C1 | Allowed for lookup; cite sources when used |
| write file | C3 | Requires explicit task scope |
| patch | C3 | Requires branch and review path |
| terminal | C3 / C5 | Depends on command; destructive or privileged commands are C5 |
| process control | C3 | Start/stop local processes only when scoped |
| delegate task | C1 / C2 | Must preserve authority model |
| cron / scheduled job | C3 / C4 | Requires explicit approval and rollback |
| MCP | C3 / C5 | Depends on server capabilities |
| browser automation | C4 / C5 | External effects require approval |
| vision analyze | C1 / C3 | C3 when private or contractual docs are involved |
| image generation | Out of core | Not a Pantheon governance primitive |
| Docker socket | C5 | Forbidden unless a specific policy allows it |
| secrets access | C5 | Forbidden unless a specific policy allows it |

---

# 6. Mandatory escalation

Always escalate when the action involves:

- external visibility;
- legal, contractual, financial or responsibility exposure;
- secrets or credentials;
- Docker socket or privileged host volumes;
- deletion, overwrite or force operations;
- memory promotion;
- active skill promotion;
- workflow activation;
- unresolved uncertainty;
- cross-project data mixing;
- private project data;
- plugin installation;
- external tool installation;
- fallback with higher risk;
- remediation that mutates repository, runtime configuration, memory, workflow, skill or policy.

---

# 7. Fallback / retry / alternative execution policy

A fallback cannot bypass approval.

If an action fails, is blocked, or is postponed, an alternative path must be evaluated as a new action when it changes:

- tool;
- data exposure;
- persistence;
- network access;
- memory impact;
- shell access;
- approval level;
- external side effect.

Allowed without new approval:

- same tool;
- same scope;
- same data exposure;
- same or lower risk;
- retry already allowed by task contract;
- Evidence Pack records the retry.

Requires approval:

- new tool;
- higher risk;
- external service;
- persistent output;
- Knowledge ingestion;
- plugin install;
- memory impact;
- workflow/skill/policy modification.

Forbidden fallback by default:

- unallowlisted tool;
- destructive action;
- secret access;
- Docker socket;
- external send;
- memory write;
- batch plugin installation;
- remote MCP server not audited.

Rule:

```text
A blocked path cannot be replaced by an unreviewed path.
```

---

# 8. Remediation Candidate Lane

When an issue, failure or blocker is detected, Pantheon may open a parallel remediation candidate lane.

This lane may:

- diagnose the issue;
- identify the affected component;
- propose a fix;
- prepare a patch candidate;
- propose tests;
- propose rollback;
- produce an Evidence Pack.

It must not:

- apply the fix automatically;
- bypass approval;
- mutate validated memory;
- activate skills;
- change workflows;
- alter policies;
- modify runtime configuration;
- access secrets;
- use Docker socket.

Approval mapping:

| Remediation action | Default level |
|---|---:|
| detect problem | C0 |
| propose correction | C1 |
| generate patch candidate | C3 |
| apply patch | C3+ |
| patch active skill/workflow/policy | C3/C4 |
| patch secrets/Docker/destructive path | C5 |

Rule:

```text
Detect → document → propose → validate → apply.
```

Not:

```text
Detect → fix automatically.
```

---

# 9. Relationship with Hermes

Hermes may execute operational work only inside the approved action level.

Hermes must not:

- upgrade its own approval level;
- bypass Pantheon policy;
- treat local skill execution as approval;
- write project/system memory directly;
- push to `main`;
- send external communications without explicit approval;
- use fallback to bypass a blocked tool;
- apply remediation patches without approval.

---

# 10. Relationship with OpenWebUI

OpenWebUI is the cockpit and approval surface.

It may display:

- requested action;
- approval level;
- expected outputs;
- evidence pack;
- risks;
- fallback proposal;
- remediation proposal;
- approve / reject options.

It must not become the final authority for Pantheon canonical truth.

---

# 11. Relationship with external tools

External tools are capabilities, not authorities.

They may be used only when:

- classified in `EXTERNAL_TOOLS_POLICY.md`;
- allowed by task contract;
- compatible with C-level approval;
- Evidence Pack requirements are satisfied;
- rollback exists.

Unknown external tools are C5 / blocked by default.

---

# 12. Final rule

```text
No persistent, external, critical, fallback, remediation or irreversible action without a visible approval path.
```
