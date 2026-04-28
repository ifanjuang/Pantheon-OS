# Hybrid Research

## Purpose

Perform research that combines multiple knowledge sources: local document corpus (RAG), vector store (pgvector), long-term archives, and optional web search. Returns ranked, deduplicated, sourced results.

## Inputs

- `query` (text) — research question or keywords
- `context` (dict) — current run context (project, criticality, domain)

## Outputs

- `results` (list) — ranked findings with relevance scores
- `sources` (list) — citation list (document refs, URLs, archive entries)

## Required agents

- `@Hermes` — qualifies the research request and chooses sources
- `@Hades` — long-term archive retrieval (C4/C5 only)
- `@Argos` — extracts facts from retrieved documents

## Activation conditions

- A request requires evidence beyond the immediate context
- Triggered by Hermes router when criticality ≥ C2 and the answer needs sourcing
- Can be invoked as a sub-step of larger workflows (deep_research, dossier_build)

## Rules

- Always combine at least two sources before returning (never single-source)
- Web search restricted to trusted sources defined by the active domain
- Deduplicate by content hash, not by URL
- Tag each result with its provenance (rag / vector / archive / web)

## Risks

- Outdated cached results — set TTL per source
- Web noise overwhelming RAG signal — apply Artemis filter if volume > threshold
- Archive access on inappropriate criticality — guarded by Hades's C4/C5 trigger
