# Extract Facts

## Purpose

Extract structured factual information from raw document content: named entities, numerical values, commitments, decisions, and documentary anomalies. Feeds downstream agents with cleaned and indexed data.

## Inputs

- `content` (text) — raw text of the document(s) to process
- `sources` (list) — optional list of source identifiers/URLs for citation

## Outputs

- `facts` (list) — structured extractions (entities, values, commitments)
- `citations` (list) — source references attached to each fact

## Required agents

- `@Argos` — performs the extraction

## Activation conditions

- A document needs to be ingested for downstream analysis
- The pipeline requires structured data rather than free-form text
- Triggered by Hermes router when input includes a document attachment

## Rules

- Extract, don't interpret — causes and solutions belong elsewhere
- Tag certainty per fact: Explicit / Implicit / Inferred
- Never fill a gap with an invented value — leave `[MISSING]`
- Always cite the source location (section/page) for each extraction

## Risks

- Hallucination of entities not present in the source
- Loss of context when extracting in isolation
- Source corruption or unreadable input — must be flagged, not silently dropped
