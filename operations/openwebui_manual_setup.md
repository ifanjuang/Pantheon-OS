# OpenWebUI Manual Setup Checklist — Pantheon Next

> Manual operator checklist for configuring OpenWebUI as a cockpit for Pantheon Next.

This document does not automate OpenWebUI configuration.

It explains how to mirror Pantheon canonical domains into OpenWebUI-facing assets while preserving the authority split:

```text
Pantheon defines domains.
OpenWebUI exposes domain-facing assets.
Hermes applies the selected domain through Task Contracts.
```

---

## 1. Scope

Use this checklist to configure OpenWebUI manually for:

- Ollama connections;
- Knowledge Bases;
- Workspace Models / presets;
- operator Skills;
- safe usage boundaries.

Do not use this checklist to:

- make OpenWebUI the source of truth;
- create Pantheon memory directly;
- activate Pantheon skills;
- bypass Hermes;
- bypass approvals;
- install unreviewed plugins;
- mutate Pantheon governance Markdown.

---

## 2. Source documents

Read these Pantheon governance documents before configuring OpenWebUI:

```text
docs/governance/OPENWEBUI_INTEGRATION.md
docs/governance/OPENWEBUI_DOMAIN_MAPPING.md
docs/governance/MODEL_ROUTING_POLICY.md
docs/governance/KNOWLEDGE_TAXONOMY.md
docs/governance/MEMORY.md
docs/governance/APPROVALS.md
docs/governance/EVIDENCE_PACK.md
```

Reference examples:

```text
config/openwebui_domain_mapping.example.yaml
config/model_routing.example.yaml
```

---

## 3. Authority rules

| Item | Authority |
|---|---|
| Canonical domain | Pantheon `domains/*` |
| Knowledge source status | Pantheon Knowledge policy |
| Agent role | Pantheon `AGENTS.md` |
| Skill activation | Pantheon `SKILL_LIFECYCLE.md` |
| Model fallback | Pantheon `MODEL_ROUTING_POLICY.md` |
| Runtime execution | Hermes |
| UI exposure | OpenWebUI |

OpenWebUI settings are operational configuration, not canonical governance.

---

## 4. Ollama connections

### 4.1 Single Ollama instance

Valid minimal setup:

```text
Ollama URL: http://ollama:11434
Prefix ID: empty
```

Use this if OpenWebUI has only one Ollama instance.

All Workspace Models may use models from this one instance.

### 4.2 Multi Ollama instance

If several Ollama instances are available, use prefixes.

Example:

```text
nas/     → http://ollama-nas:11434
gpu/     → http://ollama-gpu:11434
remote/  → http://ollama-remote:11434
```

Rules:

- use prefixes when model names overlap;
- keep private project data local by default;
- do not route C4/C5 work to remote models without explicit policy;
- record fallback if a preferred model is unavailable.

---

## 5. Knowledge Bases

OpenWebUI Knowledge Bases are document sources.

They are not Pantheon memory.

Create Knowledge Bases manually from the mapping policy.

### 5.1 General governance Knowledge Bases

Recommended:

```text
pantheon_governance
pantheon_approvals
pantheon_task_contracts
pantheon_evidence_pack
pantheon_memory_policy
```

Minimum first setup:

```text
pantheon_governance
```

Suggested content:

```text
README.md
docs/governance/ARCHITECTURE.md
docs/governance/AGENTS.md
docs/governance/MODULES.md
docs/governance/APPROVALS.md
docs/governance/TASK_CONTRACTS.md
docs/governance/EVIDENCE_PACK.md
docs/governance/MEMORY.md
docs/governance/OPENWEBUI_INTEGRATION.md
docs/governance/OPENWEBUI_DOMAIN_MAPPING.md
docs/governance/MODEL_ROUTING_POLICY.md
```

### 5.2 Architecture FR Knowledge Bases

Recommended:

```text
architecture_fr_cctp_models
architecture_fr_dpgf_models
architecture_fr_contract_clauses
architecture_fr_notices
architecture_fr_sdis_erp
architecture_fr_plu_reference
architecture_fr_site_reports
```

Rules:

- separate agency references from project-private documents;
- do not mix projects silently;
- mark obsolete templates;
- do not treat project facts as system memory.

### 5.3 Software Knowledge Bases

Recommended:

```text
software_repo_docs
code_audit_post_pivot
api_contract_docs
```

Suggested content:

```text
docs/governance/CODE_AUDIT_POST_PIVOT.md
docs/governance/PRE_REFACTOR_ARCHITECTURE_FINDINGS.md
docs/governance/WORKFLOW_SCHEMA.md
docs/governance/SKILL_LIFECYCLE.md
docs/governance/MEMORY_EVENT_SCHEMA.md
```

---

## 6. Retrieval mode guidance

When attaching Knowledge to an OpenWebUI Workspace Model:

```text
Focused Retrieval = default for large collections.
Full Context = only for short governance documents or small reference docs.
```

Avoid Full Context for large project folders.

If native function calling is enabled and Knowledge is not used correctly, add explicit model instructions to search/read Knowledge before answering.

---

## 7. Workspace Models / presets

Workspace Models are user-facing presets.

They may mirror Pantheon abstract agents, but they do not define them.

### 7.1 General presets

Recommended:

```text
ATHENA Planner
ARGOS Extractor
THEMIS Risk Check
APOLLO Validator
ZEUS Arbitration
IRIS Communication
```

### 7.2 Architecture FR presets

Recommended:

```text
ATHENA Architecture Planner
ARGOS Document Extractor
THEMIS Contract Risk Check
HEPHAESTUS Technical Review
APOLLO Architecture Validator
IRIS Client Communication
```

### 7.3 Software presets

Recommended:

```text
ATHENA Software Planner
ARGOS Repo Inspector
HEPHAESTUS Code Reviewer
THEMIS Change Gate
APOLLO Merge Validator
```

---

## 8. Workspace Model setup template

For each preset, configure:

```text
Name
Base model
System prompt
Attached Knowledge Bases
Attached operator Skills
Tools disabled by default unless policy allows them
Visibility / access control
```

Recommended system prompt skeleton:

```text
You are operating as the OpenWebUI preset for <PANTHEON_AGENT_ROLE>.
Pantheon domains, rules, approvals, memory and skills remain canonical in the Pantheon repository.
Do not promote memory.
Do not claim an action was executed unless Hermes or an approved tool actually executed it.
For consequential outputs, identify required Evidence Pack fields and approval level.
If the request exceeds this preset boundary, ask for Hermes/Pantheon task contract handoff.
```

---

## 9. Operator Skills

OpenWebUI Skills are plain Markdown operator aids.

They are not Pantheon active skills.

Recommended operator Skills:

```text
source_check_playbook
approval_classification_playbook
evidence_pack_summary_playbook
cctp_review_prompt
dpgf_review_prompt
quote_vs_cctp_review_prompt
notice_architecturale_prompt
client_message_safety_prompt
repo_md_audit_prompt
legacy_classification_prompt
api_contract_check_prompt
context_export_review_prompt
```

Rules:

- keep Skills short;
- include domain and risk boundary;
- do not include private client/project data;
- do not instruct tools to mutate files unless an approval path exists;
- mark deprecated Skills inactive rather than deleting them immediately.

---

## 10. Tools and Actions

Default rule:

```text
Tools off unless explicitly allowed by policy.
```

Do not enable by default:

```text
filesystem write
shell
secret access
plugin install
external send
public web publish
memory write
```

OpenWebUI Actions may later support:

```text
view Evidence Pack
approve/reject C3/C4/C5 action
request rerun
request clarification
handoff to Hermes
```

Until then, Actions must remain manual or read-only.

---

## 11. Access control

Recommended initial access:

```text
pantheon_governance       → internal only
architecture_fr_*         → internal only or project-scoped
software_repo_docs        → internal only
project-private KBs       → restricted to project operators
client/project documents  → never public
```

---

## 12. Minimum viable manual setup

Start with only this:

```text
1. One Ollama connection.
2. One Knowledge Base: pantheon_governance.
3. Three Workspace Models:
   - ATHENA Planner
   - ARGOS Extractor
   - APOLLO Validator
4. One operator Skill:
   - evidence_pack_summary_playbook
```

Do not start by creating every agent preset.

---

## 13. Verification checklist

After setup, verify:

```text
OpenWebUI can see the intended Ollama models.
pantheon_governance Knowledge Base contains current governance docs.
Workspace Models do not claim canonical authority.
Workspace Models do not promote memory.
Skills are marked as operator aids.
Private documents are not mixed with general Knowledge.
Remote models are not used for private data unless policy allows it.
```

---

## 14. Evidence Pack trace

If an output uses OpenWebUI-mapped assets and becomes consequential, record:

```text
pantheon_domain
openwebui_knowledge_bases_used
openwebui_workspace_model_used
openwebui_operator_skills_used
source_status
project_scope
privacy_level
model_used
fallback_used
unsupported_claims
approval_required
```

---

## 15. Final rule

```text
OpenWebUI is a cockpit.
Pantheon is the canonical governance layer.
Hermes is the execution runtime.
```
