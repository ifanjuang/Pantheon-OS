# KNOWLEDGE TAXONOMY — Pantheon OS

> Reference taxonomy for OpenWebUI Knowledge, document reliability and separation from Pantheon memory.

---

# 1. Purpose

`KNOWLEDGE_TAXONOMY.md` defines how documents, references, templates and Knowledge Bases are organized.

It prevents three common errors:

- treating uploaded documents as validated memory;
- mixing project documents across unrelated projects;
- using draft or obsolete sources as if they were canonical.

Core rule:

```text
Documents are knowledge.
Validated reusable facts become memory candidates.
Pantheon alone canonizes memory.
```

---

# 2. Layers

| Layer | Name | Role | Canonical? |
|---:|---|---|---|
| 1 | Stable references | Official, regulatory, normative or long-lived references | No, unless promoted or cited in Pantheon docs |
| 2 | Models / frameworks / methods | Internal templates, methods, checklists, reusable models | No, unless stored in Pantheon templates or memory |
| 3 | Project documents / active knowledge | CCTP, quotes, contracts, PLU extracts, reports, correspondence | No, project evidence only |
| Memory | Validated memory | Project/system facts validated through Pantheon policy | Yes after validation |

---

# 3. Initial OpenWebUI Knowledge collections

Initial planned collections:

```text
pantheon_governance
architecture_fr_cctp_models
architecture_fr_dpgf_models
architecture_fr_contract_clauses
architecture_fr_notices
architecture_fr_sdis_erp
software_repo_docs
hermes_reference
openwebui_reference
```

Future project collections should follow:

```text
project_{project_id}_{safe_label}
```

Example:

```text
project_2026_001_sample_house
```

No real project name should be used in repository examples.

---

# 4. Reliability levels

| Level | Meaning | Example |
|---:|---|---|
| R0 | Draft / unknown source | unverified note, rough draft |
| R1 | Useful example, not validated | external example, community pattern |
| R2 | Validated internal model | reviewed office template or checklist |
| R3 | Official or normative reference | regulation, standard, official notice |
| R4 | Validated Pantheon rule | approved method, governance decision |
| R5 | Pantheon source of truth | reference Markdown, active policy, validated memory |

Rule:

```text
Higher reliability sources override lower reliability sources when they conflict.
```

---

# 5. Source tiers

| Tier | Source type | Use |
|---:|---|---|
| T0 | Pantheon source-of-truth Markdown / validated memory | Canonical governance and memory |
| T1 | Signed or official project documents | Project-specific evidence |
| T2 | Working project documents | Useful but must be checked for version/status |
| T3 | Generic official references | Regulatory or professional reference |
| T4 | Templates and examples | Drafting aid only |
| T5 | External unverified sources | Inspiration only |

---

# 6. Project separation

Default rule:

```text
Do not mix two project Knowledge collections unless the user explicitly asks for comparison or reuse analysis.
```

Allowed cross-project use:

- anonymized method extraction;
- explicit comparison;
- reusable pattern candidate;
- system memory candidate after review.

Forbidden cross-project use:

- using one client/project fact to answer another project;
- merging aliases without validation;
- importing sensitive documents into a generic collection;
- treating old project context as current fact.

---

# 7. Status metadata

Documents should eventually carry a status:

```text
draft
active
superseded
archived
do_not_use
```

A superseded or archived document may be cited only if the answer explicitly states its status.

---

# 8. Freshness metadata

Regulatory or external references should eventually carry:

```yaml
freshness:
  last_checked: null
  check_required_after: null
  source_url: null
```

If a time-sensitive source is stale, Pantheon should say so.

---

# 9. Knowledge versus memory

| Element | Knowledge | Memory |
|---|---|---|
| Uploaded PDF | yes | no |
| Project contract | yes | no, unless summarized into validated project memory |
| CCTP | yes | no |
| Reusable method | yes | candidate, then system memory if validated |
| Client decision | source document first | project memory only after validation |
| Pantheon policy | can be mirrored in Knowledge | canonical in Markdown |

---

# 10. Evidence Pack requirement

Whenever Knowledge is used, the Evidence Pack must list:

- Knowledge collections consulted;
- documents used;
- source tier or reliability level when known;
- missing documents;
- whether cross-project data was used;
- limitations.

---

# 11. Final rule

```text
OpenWebUI stores and retrieves knowledge.
Hermes may query it under task contract.
Pantheon decides what becomes memory.
```
