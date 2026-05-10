# OpenWebUI Inline Run Stream — Pantheon Next

> Optional V1 display specification for temporary plain-text progress updates in OpenWebUI.
>
> This is not an implementation guide for a runtime. It is an operating boundary for a future display aid.

---

## 1. Purpose

The Inline Run Stream displays short progress messages while Hermes executes a governed task.

It is meant to answer, in simple user-facing language:

```text
What is happening now?
What is missing?
Who is waiting for what?
What warning or veto occurred?
What changed in the workflow?
What is the next safe step?
```

Canonical rule:

```text
OpenWebUI displays.
Hermes Agent executes.
Pantheon Next governs.
```

The Inline Run Stream must not become an execution layer.

---

## 2. V1 decision

V1 is intentionally minimal.

```text
inline text only
plain language
non-technical by default
no emoji
no colors
no D3 panel
no graph panel
no live dashboard
optional
disabled by default
```

Default format:

```text
ROLE : short message.
```

Example:

```text
METIS : Je clarifie l’intention de la demande.
ATHENA : Je prépare la méthode d’analyse.
ARGOS : Je vérifie les documents disponibles.
THEMIS : Il manque une pièce utile. La conclusion devra rester prudente.
APOLLO : Je vérifie que la synthèse reste claire et limitée aux preuves disponibles.
ZEUS : Je poursuis avec les informations disponibles.
```

---

## 3. Activation policy

Default configuration:

```yaml
inline_run_stream:
  enabled: false
  mode: disabled
  tone: public
  detail_level: clear
  emojis: false
  colors: false
  panel: false
  show_raw_events: false
  show_chain_of_thought: false
  show_technical_terms: false
  show_full_document_content: false
  max_messages_per_run: 60
  max_message_length: 180
```

Allowed modes:

| Mode | Meaning | Status |
|---|---|---|
| `disabled` | No inline progress display | default |
| `status_only` | Temporary OpenWebUI status updates only | first candidate |
| `message_delta` | Temporary visible text chunks in the assistant message | review before use |
| `replace_final` | Replace temporary text with final answer | review before use |
| `debug` | Technical raw event inspection | blocked by default |

Production activation requires review under:

```text
docs/governance/APPROVALS.md
docs/governance/EXTERNAL_TOOLS_POLICY.md
docs/governance/OPENWEBUI_INTEGRATION.md
docs/governance/RUN_GRAPH.md
```

---

## 4. OpenWebUI implementation boundary

OpenWebUI may support this through one of the following future mechanisms:

```text
native OpenWebUI Tool or Function emitting status events
minimal Pipe used only as display/routing adapter
Action that requests a Run Graph summary
assistant message streaming with temporary status text
```

Rules:

```text
A Pipe must not orchestrate the workflow.
A Function must not read broad filesystem paths.
A Tool must not execute Hermes work directly unless explicitly scoped.
OpenWebUI must not become approval authority.
OpenWebUI must not become memory authority.
```

If a native OpenWebUI Function or Pipe is used, it must be treated as external executable code and reviewed before activation.

Forbidden in the OpenWebUI component:

```text
subprocess
Docker socket
secret access
broad filesystem read
filesystem write
repository mutation
memory promotion
skill activation
workflow activation
external message send
raw database connection disclosure
```

---

## 5. Hermes boundary

Hermes remains the execution runtime.

Hermes may provide:

```text
progress indicators
tool status
bounded execution outputs
Evidence Pack fragments
workflow revision signals
missing-source signals
```

Hermes must not:

```text
canonize memory
promote skills
approve its own actions
bypass Pantheon policies
push to main
access secrets by default
```

Inline Run Stream only displays a public-facing summary of observed execution state.

---

## 6. Pantheon boundary

Pantheon may structure observed events into:

```text
Run Graph
request frame state
AGORA consultation state
role state
source state
tool state
warning state
veto state
approval state
workflow revision state
Evidence Pack delta
```

Pantheon must not use this feature to:

```text
execute a workflow
run agents
call tools
schedule work
hide runtime execution
replace Hermes
replace OpenWebUI
```

---

## 7. Allowed public messages

Allowed messages are short state summaries.

Examples:

```text
METIS : Je clarifie l’intention de la demande.
ATHENA : Je prépare la méthode d’analyse.
ARGOS : Je vérifie les documents disponibles.
ARGOS : Le devis et le CCTP sont pris en compte.
DEMETER : J’attends les quantités extraites du devis.
ARGOS : Les quantités exploitables sont transmises à DEMETER.
THEMIS : Attention, la conclusion devra rester prudente car une pièce manque.
THEMIS : Je bloque cette action car elle nécessite une validation préalable.
CHRONOS : La branche quantitative est suspendue. L’analyse technique continue.
APOLLO : Je vérifie que la synthèse reste claire et limitée aux preuves disponibles.
ZEUS : Le workflow est ajusté. Je poursuis avec les informations disponibles.
```

---

## 8. Forbidden messages

Forbidden:

```text
raw chain-of-thought
hidden reasoning
system prompts
internal prompts
raw Hermes logs
raw event dumps
secrets
API keys
credentials
full private document extracts
unnecessary client/project identifiers
sensitive file paths
unsupported certainty
technical jargon in default mode
```

Bad examples:

```text
ATHENA : workflow.node.started quote_vs_cctp_review initialized.
ARGOS : parsing source chunk 37 with hidden context.
THEMIS : C3 gate activated by internal policy resolver.
APOLLO : I reasoned through all possible risks and decided...
```

Good examples:

```text
ATHENA : Je prépare la méthode d’analyse.
ARGOS : Je vérifie les documents disponibles.
THEMIS : Une validation sera nécessaire avant toute modification.
APOLLO : Je vérifie que la réponse reste cohérente avec les pièces disponibles.
```

---

## 9. Temporary display warning

Inline messages may be visually temporary.

They may be:

```text
shown while running
hidden after completion
collapsed in the UI
replaced by the final answer
kept only in a status history
```

But temporary display is not secure deletion.

Rule:

```text
Never put sensitive content in temporary messages.
```

---

## 10. Final answer behavior

The final answer should remain clean.

It may include:

```text
result
limits
sources summary
Evidence Pack summary when required
approval required
next safe action
```

It should not include the full Inline Run Stream unless the user asks for a recap.

If the stream is summarized in the final output, keep it short:

```text
Workflow summary: documents checked, one missing source found, analysis continued with a stated limitation.
```

---

## 11. Safety checklist before implementation

Before implementing this feature, verify:

- OpenWebUI version and event behavior;
- whether native Function, Tool, Action or Pipe is the smallest safe path;
- no broad filesystem access;
- no Docker socket;
- no secret access;
- no repository mutation;
- no memory promotion;
- no skill activation;
- no workflow activation;
- no raw chain-of-thought display;
- no private data in messages;
- rollback path exists;
- feature can be disabled.

---

## 12. Rollback

Rollback must be simple:

```text
disable feature flag
remove OpenWebUI Function/Pipe/Action if used
stop emitting inline events
keep final answer behavior unchanged
keep Evidence Pack behavior unchanged
```

---

## 13. Final rule

```text
Inline Run Stream shows progress.
It does not prove, approve, decide, remember or execute.
```
