# Knowledge Selection

> Candidate Pantheon skill. Selects the correct Knowledge sources for a task before Hermes retrieval or execution.

---

# 1. Purpose

`knowledge_selection` prevents uncontrolled retrieval across OpenWebUI Knowledge Bases, project documents, generic templates and external sources.

It decides which Knowledge sources may be consulted for a Task Contract based on:

```text
domain
source tier
reliability level
privacy level
project scope
freshness policy
user intent
risk level
Evidence Pack requirements
```

This skill is a governance contract. It does not retrieve documents itself. Hermes or OpenWebUI retrieval mechanisms execute retrieval only after source selection is constrained.

---

# 2. Core rule

```text
Select allowed sources before retrieval.
Block risky or out-of-scope sources before content loading.
Return a source selection report for the Evidence Pack.
```

---

# 3. Responsibilities

This skill may:

- classify the user request by domain;
- read the Knowledge Registry;
- select candidate Knowledge Bases;
- reject Knowledge Bases outside the domain;
- reject Knowledge Bases outside the project scope;
- reject stale regulatory or project-versioned sources unless explicitly flagged;
- rank sources by source tier and reliability;
- ask for live source validation when registry entries are only examples;
- produce a source selection report;
- propose Knowledge Registry candidate updates;
- propose memory candidates only when the output is reusable and evidence-backed.

---

# 4. Non-responsibilities

This skill must not:

- retrieve documents directly;
- run vector search directly;
- ingest files into OpenWebUI;
- create or update `knowledge/registry.yaml` automatically;
- promote Knowledge into Memory;
- treat OpenWebUI Knowledge as Pantheon Memory;
- use project-scoped sources for another project without explicit trace;
- use private or sensitive sources in generic examples;
- call external RAG engines without tool policy;
- bypass THEMIS, APOLLO or approval requirements;
- expose raw chain-of-thought.

---

# 5. Inputs

Expected inputs:

```yaml
task_contract_id: string
user_intent: string
domain: general | architecture_fr | software | unknown
risk_level: C0 | C1 | C2 | C3 | C4 | C5
expected_output: string
project_scope: none | generic | project_id
privacy_context: public | internal | private | sensitive
freshness_need: static | current | regulatory_current | project_versioned
required_evidence: true
known_sources: []
forbidden_sources: []
```

Optional inputs:

```yaml
registry_ref: knowledge/registry.example.yaml | knowledge/registry.yaml
context_pack_ref: string
prior_evidence_pack_ref: string
memory_candidate_policy: candidate_only
```

---

# 6. Source filters

The selection must apply filters in this order:

```text
1. domain filter
2. privacy filter
3. project-scope filter
4. source-tier filter
5. reliability filter
6. freshness filter
7. forbidden-source filter
8. evidence requirement filter
```

A source rejected by an earlier filter cannot be restored by a later filter without explicit approval and trace.

---

# 7. Source tier policy

Source tiers follow `KNOWLEDGE_TAXONOMY.md` and `knowledge/registry.example.yaml`.

Default ranking:

```text
T0 = Pantheon source of truth
T1 = signed or official project documents
T2 = working project documents
T3 = generic official references
T4 = templates and examples
T5 = unverified external sources
```

Rules:

```text
T0 may define governance.
T1/T2 may support project-specific evidence only within matching project scope.
T3 must be checked for currency before regulatory, contractual or compliance use.
T4 is drafting aid only.
T5 is inspiration only and cannot support consequential claims alone.
```

---

# 8. Privacy and project-scope policy

Privacy filter:

```text
public   -> usable when relevant
internal -> usable for internal governance and non-client examples
private  -> usable only inside matching project scope and approval path
sensitive -> blocked unless explicitly authorized under C4/C5 policy
```

Project-scope filter:

```text
none      -> generic use allowed
generic   -> generic use allowed if no real private data
project_x -> only same project unless cross-project trace and anonymization are approved
```

Forbidden:

```text
private project data inside generic collection
cross-project reuse without trace
project-specific fact promoted to system memory without anonymization and review
```

---

# 9. Freshness policy

Freshness must be considered before retrieval.

Rules:

```text
static -> usable unless governance changed
periodic_6_months -> warning if stale
periodic_12_months -> warning if stale
regulatory_current -> must be checked before consequential use
project_versioned -> date, version and superseded state must be checked
```

If freshness cannot be verified:

```yaml
selection_status: conditional
warning: freshness_unverified
allowed_use: drafting_or_question_framing_only
```

---

# 10. AKS-inspired provenance fields

The source selection report should preserve provenance metadata when available.

Recommended fields:

```yaml
source_id: string
source_tier: T0 | T1 | T2 | T3 | T4 | T5
reliability_level: R0 | R1 | R2 | R3 | R4 | R5
privacy_level: public | internal | private | sensitive
project_scope: none | generic | project_id
last_checked: date | null
last_corroborated: date | null
confidence: low | medium | high | unknown
contributing_documents: []
traversal_path: []
limitations: []
```

These fields are metadata. They do not replace Evidence Pack source tracing.

---

# 11. Six-Hats-inspired selection lenses

The skill may use lightweight lenses to check whether the selected sources are defensible.

| Lens | Pantheon role | Question |
|---|---|---|
| White | ARGOS | What sources exist and what do they contain? |
| Black | THEMIS / HEPHAISTOS | Which sources are risky, stale, private or out of scope? |
| Yellow | ATHENA | Which source set is most useful for the task? |
| Green | PROMETHEUS | What alternative source path could reduce risk or improve coverage? |
| Red | IRIS / HECATE | Is user intent ambiguous or likely to be misread? |
| Blue | ZEUS / APOLLO | Is the final source set coherent, limited and evidence-ready? |

Rule:

```text
The lenses structure the review.
They do not override source-tier, privacy, freshness or approval rules.
```

---

# 12. Decisions

Possible decisions:

```text
select_sources
select_sources_with_warnings
request_registry_validation
request_user_scope_clarification
block_sources
fallback_to_governance_only
propose_registry_candidate_update
propose_memory_candidate
```

Decision meanings:

| Decision | Meaning |
|---|---|
| `select_sources` | Sources are allowed and sufficient for the task |
| `select_sources_with_warnings` | Sources may be used with explicit limitations |
| `request_registry_validation` | Live Knowledge names, scope or freshness must be checked |
| `request_user_scope_clarification` | Project or privacy scope is unclear |
| `block_sources` | Sources are not allowed under policy |
| `fallback_to_governance_only` | Use only Pantheon governance docs, no project/private retrieval |
| `propose_registry_candidate_update` | Registry improvement candidate only, no auto-write |
| `propose_memory_candidate` | Memory candidate only, never auto-promotion |

---

# 13. Output schema

Every run must produce a visible selection report.

```yaml
knowledge_selection_report:
  task_contract_id: string
  domain: string
  decision: select_sources | select_sources_with_warnings | request_registry_validation | request_user_scope_clarification | block_sources | fallback_to_governance_only
  selected_sources:
    - source_id: string
      openwebui_knowledge_base: string
      source_tier: string
      reliability_level: string
      privacy_level: string
      project_scope: string
      freshness_policy: string
      allowed_use: []
      limitations: []
  rejected_sources:
    - source_id: string
      reason: string
      policy_ref: string
  warnings: []
  required_checks: []
  evidence_pack_fields:
    - files_read
    - knowledge_bases_consulted
    - source_tiers_used
    - assumptions
    - unsupported_claims
    - limitations
  memory_impact: none | candidate_only
  approval_required: boolean
```

---

# 14. Evidence Pack requirements

The Evidence Pack must state:

```text
which Knowledge sources were selected
which Knowledge sources were rejected
why they were selected or rejected
which source tiers were used
whether any source was stale or unverified
whether any private/project-scoped source was involved
whether any claim relies only on low-tier sources
what assumptions remain
```

Rule:

```text
A selected source is not evidence until its content is actually consulted and cited or traced.
```

---

# 15. Approval policy

Approval is required when:

```text
private or sensitive source is selected
cross-project source reuse is proposed
stale regulatory source is used for consequential output
external RAG/retrieval engine is proposed
Knowledge Registry update is proposed
memory candidate promotion is proposed
source selection affects C3/C4/C5 output
```

Minimum approval:

```text
C0/C1: generic internal source selection
C2: non-sensitive live Knowledge validation
C3: persistent registry update or memory candidate review
C4: external contractual or project-specific consequential use
C5: secrets, sensitive data, destructive tools, shell or uncontrolled external runtime
```

---

# 16. Interaction with Hermes and OpenWebUI

OpenWebUI:

```text
exposes Knowledge Bases
shows selected sources and warnings
collects user clarification or approval
must not canonize Knowledge as Memory
```

Hermes:

```text
executes retrieval after selection
must respect selected_sources and rejected_sources
must include consulted sources in the Evidence Pack
must not query blocked sources silently
```

Pantheon:

```text
defines the selection policy
maintains Knowledge Registry examples/candidates
canonizes memory only after Evidence Pack and approval
```

---

# 17. Status

Current status: `candidate`.

This skill is not active until reviewed against:

```text
SKILL_LIFECYCLE.md
KNOWLEDGE_TAXONOMY.md
OPENWEBUI_INTEGRATION.md
OPENWEBUI_DOMAIN_MAPPING.md
EVIDENCE_PACK.md
APPROVALS.md
knowledge/registry.example.yaml
```
