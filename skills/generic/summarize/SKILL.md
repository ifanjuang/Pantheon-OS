# Summarize

## Purpose

Contextual synthesis of validated material. Selects what matters, hierarchizes by decisional impact, and produces a structured summary tailored to the request criticality.

## Inputs

- `facts` (list) — validated facts from upstream agents
- `context` (dict) — current run context (criticality, audience, request type)

## Outputs

- `summary` (text) — formatted synthesis adapted to criticality (C1/C2 short, C3 decision, C4/C5 strategic)
- `key_points` (list) — top decision-relevant items, ordered by impact

## Required agents

- `@Kairos` — performs the synthesis

## Activation conditions

- A pipeline has produced multiple agent outputs that need consolidation
- Always activated as the last step before delivery (after Apollo validation)
- Skipped only when the answer is a pure data dump

## Rules

- Synthesis must not contradict any veto issued by Themis
- Last line is always an action, not a conclusion
- Format strictly follows the criticality template (no fluff)
- If agents disagree, the synthesis names the divergence and the chosen side

## Risks

- Loss of nuance when compressing too aggressively
- Premature closure on weakly-supported claims
- Style drift when the audience is not specified — Iris adapts the tone afterward
