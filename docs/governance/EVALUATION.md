# EVALUATION — Pantheon Next

> Governance doctrine for evaluating skills, workflows, outputs, external tools and runtime candidates.
>
> Evaluation measures. Evaluation does not govern by itself.

---

## 1. Doctrine

```text
OpenWebUI exposes.
Hermes Agent executes.
Pantheon Next governs.
```

Evaluation artifacts may inform decisions.

They must not become:

```text
approval authority
memory promotion authority
skill promotion authority
workflow canonization authority
runtime execution authority
```

---

## 2. Purpose

`EVALUATION.md` defines how Pantheon may later assess:

```text
skill candidates
workflow candidates
Hermes execution quality
retrieval quality
source adherence
structured-output reliability
external tool usefulness
browser-agent benchmarks
long deliverable quality
```

This document is intentionally governance-first.

No evaluation runtime is implemented here.

---

## 3. Allowed evaluation uses

Allowed:

```text
compare candidate skills
compare workflow variants
measure source adherence
measure output consistency
measure failure modes
measure regression risk
prepare Evidence Pack inputs
support APOLLO final-readiness review
support THEMIS risk review
support HEPHAESTUS skill robustness review
```

Forbidden:

```text
automatic skill promotion
automatic workflow canonization
automatic memory promotion
automatic merge
automatic external send
automatic approval
runtime routing authority inside Pantheon
```

---

## 4. Candidate evaluation tools

Candidate families may include:

```text
Promptfoo-style evaluation suites
structured-output validators
schema conformance checks
retrieval precision checks
source citation checks
regression fixtures
browser-agent benchmarks
Doctor reports
human review scorecards
```

External tools remain blocked until classified under:

```text
EXTERNAL_TOOLS_POLICY.md
EXTERNAL_RUNTIME_OPTIONS.md
EXTERNAL_AI_OPTION_REVIEWS.md
EXTERNAL_ECOSYSTEM_REVIEWS.md
```

---

## 5. Scorecard model

Candidate scorecard:

```yaml
evaluation_scorecard:
  id: EVAL-YYYY-NNNN
  target_type: skill | workflow | output | external_tool | runtime_candidate | deliverable
  target_ref: null
  evaluator_role: APOLLO | THEMIS | HEPHAESTUS | ARGOS | DEMETER | DAEDALUS
  method: manual | fixture | schema_validation | benchmark | regression
  source_set: []
  metrics:
    - name: source_adherence
      value: null
      status: pass | warn | fail | not_applicable
    - name: evidence_quality
      value: null
      status: pass | warn | fail | not_applicable
    - name: policy_alignment
      value: null
      status: pass | warn | fail | not_applicable
  limitations: []
  decision: inform_only | candidate_pass | candidate_warn | candidate_fail | blocked
```

A passing scorecard is not promotion.

Promotion still requires the appropriate approval and Evidence Pack.

---

## 6. Role split

```text
ARGOS verifies sources and factual extraction.
HEPHAESTUS evaluates method robustness and skill behavior.
THEMIS evaluates policy, approval and risk.
APOLLO evaluates completeness, coherence and final readiness.
ZEUS arbitrates conflicting evaluation outcomes.
```

---

## 7. Final rule

```text
Evaluate before trusting.
Measure without granting authority.
Use evaluation as evidence, not as approval.
```
