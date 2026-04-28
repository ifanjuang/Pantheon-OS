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
| C3 | Persistent internal change | File mutation, branch patch, memory candidate, workflow candidate, skill candidate | Explicit validation or active instruction required |
| C4 | External / contractual / financial / responsibility action | External communication, client-facing message, contract, finance, responsibility exposure | Explicit user approval required |
| C5 | Critical / irreversible / secrets / destructive | Secrets, deletion, destructive command, Docker socket, privileged volume, irreversible mutation | Explicit approval plus policy gate; often forbidden by default |

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

---

# 4. Tool mapping

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

# 5. Mandatory escalation

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
- private project data.

---

# 6. Relationship with Hermes

Hermes may execute operational work only inside the approved action level.

Hermes must not:

- upgrade its own approval level;
- bypass Pantheon policy;
- treat local skill execution as approval;
- write project/system memory directly;
- push to `main`;
- send external communications without explicit approval.

---

# 7. Relationship with OpenWebUI

OpenWebUI is the cockpit and approval surface.

It may display:

- requested action;
- approval level;
- expected outputs;
- evidence pack;
- risks;
- approve / reject options.

It must not become the final authority for Pantheon canonical truth.

---

# 8. Final rule

```text
No persistent, external, critical or irreversible action without a visible approval path.
```
