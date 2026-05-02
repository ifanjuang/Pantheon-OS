# Knowledge Selection — Updates

> Candidate evolution log. Proposed changes must remain candidates until reviewed under `SKILL_LIFECYCLE.md`.

---

## 2026-05-02 — Candidate creation

Status: `candidate`

Initial package created with:

```text
SKILL.md
manifest.yaml
examples.md
tests.md
UPDATES.md
```

Initial scope:

```text
Select Knowledge sources before retrieval.
Apply domain, privacy, project-scope, source-tier, reliability and freshness filters.
Prepare a visible selection report for the Evidence Pack.
Prevent OpenWebUI Knowledge from being treated as Pantheon Memory.
Prevent cross-project retrieval without trace and approval.
Prevent external RAG engines from being used without policy.
```

Method inspirations, kept non-runtime:

```text
AKS-style provenance metadata
Six-Hats-style review lenses
```

No external dependency added.

No runtime behavior added.

No Knowledge Registry mutation implemented.

---

## Candidate improvements to review later

### 1. Live OpenWebUI registry validation

Possible future improvement:

```text
Compare `knowledge/registry.example.yaml` with live OpenWebUI Knowledge Base names.
Produce a mismatch report.
Do not auto-create `knowledge/registry.yaml`.
```

Required approval:

```text
C2/C3 depending persistence
```

---

### 2. Hermes retrieval preflight mapping

Possible future improvement:

```text
Map selected_sources to a Hermes retrieval preflight payload.
Return rejected_sources as hard constraints.
Require Evidence Pack completion after retrieval.
```

Required approval:

```text
C3 if persisted as integration contract
```

---

### 3. Source freshness checker

Possible future improvement:

```text
Add documented checks for `regulatory_current` and `project_versioned` sources.
```

Restriction:

```text
No web/current lookup automation in Pantheon.
Hermes may perform checks only under Task Contract and Evidence Pack.
```

---

### 4. AKS comparison note

Possible future improvement:

```text
Compare AKS provenance fields with MEMORY_EVENT_SCHEMA.md and Evidence Pack fields.
Keep AKS as inspiration/test_read_only, not memory authority.
```

---

### 5. Six-Hats lightweight checklist

Possible future improvement:

```text
Convert the selection lenses into a short checklist usable by Hermes in high-risk source selection.
```

Restriction:

```text
Checklist must not expose raw chain-of-thought.
Checklist must produce only visible findings, warnings and decisions.
```

---

## Explicitly rejected evolutions

```text
auto-retrieval inside this skill
auto-ingestion into OpenWebUI
auto-creation of `knowledge/registry.yaml`
auto-promotion from Knowledge to Memory
external RAG engine call without policy
cross-project retrieval without explicit trace
graph memory creation
source selection by vector similarity alone
hidden tool calls
```
