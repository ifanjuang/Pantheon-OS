# Cross-Check

## Purpose

Detect contradictions and inconsistencies across multiple sources or agent outputs before synthesis hardens. Surface weak hypotheses and conflicting claims.

## Inputs

- `facts` (list) — set of factual extractions to compare
- `sources` (list) — provenance of each fact (used to weight conflicts)

## Outputs

- `contradictions` (list) — pairs of conflicting claims with evidence
- `weak_hypotheses` (list) — claims supported by only one source or low-confidence inference

## Required agents

- `@Prometheus` — adversarial reasoning, surfaces hidden contradictions

## Activation conditions

- Multiple agents have produced overlapping findings on the same subject
- Criticality ≥ C3 and the synthesis must be trustworthy
- Triggered by Zeus before Kairos when divergent signals are detected

## Rules

- A contradiction is only flagged with evidence from at least two sources
- Distinguish factual contradiction (incompatible claims) from interpretive divergence (same fact, different framing)
- Output preserves the original source attribution for each side
- Never silently resolve a contradiction — surface it for Apollo or Zeus to arbitrate

## Risks

- False positives on near-synonyms or paraphrases
- Missing contradictions hidden across modalities (numerical vs. textual)
- Excessive noise when comparing too many sources at once — cap at top-N most relevant
