# RUN GRAPH — Pantheon Next

> Read-only observation schema for governed task progress, workflow adaptation, request orchestration and user-facing run summaries.
>
> Run Graph is not a runtime. It does not execute, decide, approve, promote memory, activate skills or mutate workflows.

---

## 1. Purpose

`RUN_GRAPH.md` defines how Pantheon may describe the visible state of a request while Hermes executes bounded work under a Task Contract.

It supports two future display layers:

```text
Inline Run Stream V1 = short temporary text updates in OpenWebUI
Run Graph Snapshot = structured state for later graph/panel visualization
```

Core rule:

```text
OpenWebUI displays.
Hermes Agent executes.
Pantheon Next governs.
```

The Run Graph exists to make execution understandable, auditable and bounded without exposing raw chain-of-thought.

---

## 2. Non-runtime boundary

Run Graph must not become:

```text
workflow runtime
agent runtime
tool runtime
scheduler
approval engine
memory engine
OpenWebUI backend model
Hermes replacement
```

Run Graph may only:

```text
record observed state
summarize progress
show missing inputs
show sources and tools used at a high level
show warnings, vetoes and approvals
show METIS request framing summaries
show AGORA consultation summaries
show workflow revision signals
support Evidence Pack summaries
```

Forbidden:

```text
execute_task
run_agent
call_tool
activate_skill
promote_memory
canonize_workflow
approve_action
show_raw_chain_of_thought
show_raw_prompts
show_secrets
show_full_private_document_content
```

---

## 3. V1 scope — Inline Run Stream

V1 is intentionally simple.

```text
plain text
inline in OpenWebUI
temporary visual display
no emoji
no colors
no D3
no panel
no graph rendering
non-technical public wording by default
disabled by default
```

Default format:

```text
ROLE : short message.
```

Examples:

```text
METIS : Je clarifie l’intention de la demande.
ATHENA : Je prépare la méthode d’analyse.
ARGOS : Je vérifie les documents disponibles.
THEMIS : Attention, la conclusion devra rester prudente.
APOLLO : Je vérifie que la synthèse reste claire et limitée aux preuves disponibles.
ZEUS : Je poursuis avec les informations disponibles.
```

The stream is display-only. It is not evidence, approval, memory or workflow execution.

---

## 4. Display modes

Allowed modes:

| Mode | Meaning | Status |
|---|---|---|
| `disabled` | No inline stream, no run panel | default |
| `inline_v1` | Temporary plain text updates in OpenWebUI | first candidate |
| `snapshot` | Final or refreshed structured run graph summary | later |
| `panel_d3` | Interactive graph panel | blocked until explicit review |
| `live_panel` | D3/SSE/WebSocket live panel | blocked until explicit review |

Default:

```yaml
run_graph:
  enabled: false
  mode: disabled
```

V1 target:

```yaml
run_graph:
  enabled: true
  mode: inline_v1
  show_technical_terms: false
  show_raw_events: false
  show_chain_of_thought: false
```

---

## 5. Event categories

Run Graph may receive or derive structured observations.

These are observations, not runtime commands.

```text
run.started
run.completed
run.failed
request.frame_created
request.context_expansion_needed
workflow.selected
workflow.node.started
workflow.node.completed
workflow.node.blocked
role.started
role.waiting
role.completed
agora.started
agora.completed
information.requested
information.transmitted
source.consulted
source.missing
tool.started
tool.completed
tool.failed
evidence.updated
warning.raised
veto.raised
approval.required
workflow.revision_signal
workflow.patch_candidate
workflow.patch_accepted
workflow.patch_rejected
```

V1 may display only a public-facing subset.

---

## 6. Node types

Run Graph may later represent these node types:

| Node type | Meaning |
|---|---|
| `role` | Pantheon abstract role such as METIS, ATHENA, ARGOS, THEMIS |
| `consultation` | AGORA bounded consultation summary |
| `workflow_step` | Bounded step in a workflow/session workflow |
| `skill` | Pantheon skill contract or Hermes skill mapping |
| `tool` | Concrete executable capability used by Hermes |
| `document` | File or project document used as source |
| `knowledge_base` | OpenWebUI Knowledge collection or declared Knowledge source |
| `website` | External web page or website consulted |
| `data_object` | Intermediate result such as extracted items or risk notes |
| `governance` | Approval, veto, warning or Evidence Pack state |

V1 does not render these nodes visually. It may summarize them in plain text only.

---

## 7. Role states

Allowed role states:

```text
idle
working
waiting
blocked
warning
veto
completed
approved
needs_user_input
```

V1 wording must be simple:

| State | Public wording example |
|---|---|
| `working` | `ARGOS : Je vérifie les documents disponibles.` |
| `waiting` | `DEMETER : J’attends les quantités extraites du devis.` |
| `blocked` | `ATHENA : Je ne peux pas poursuivre cette partie sans le plan.` |
| `warning` | `THEMIS : Attention, la conclusion devra rester prudente.` |
| `veto` | `THEMIS : Je bloque cette action car elle nécessite une validation préalable.` |
| `completed` | `APOLLO : La vérification est terminée.` |

---

## 8. Source metadata

When sources are shown, V1 must use short public summaries only.

Allowed:

```text
ARGOS : Le devis et le CCTP sont pris en compte.
ARGOS : Le DPGF n’est pas fourni.
ARGOS : Une référence officielle a été consultée.
```

Forbidden by default:

```text
full private file path
secret or token
raw database connection string
full private document content
unredacted personal data
large quoted passages
```

Structured source metadata may include:

```yaml
source:
  id: null
  type: document | knowledge_base | database | website | governance_doc
  label: null
  status: consulted | missing | rejected | not_used
  used_by: []
  evidence_required: true
  public_label: null
  sensitive: false
```

---

## 9. Evidence relationship

Run Graph may support Evidence Packs, but does not replace them.

Rule:

```text
Inline Run Stream is not evidence.
Run Graph is not evidence by itself.
Evidence Pack remains the audit contract.
```

Run Graph may feed Evidence Pack fields such as:

```text
steps_executed
sources_consulted
tools_used
missing_sources
workflow_adaptations
warnings
vetoes
approvals_required
limitations
```

Consequential outputs still require `EVIDENCE_PACK.md`.

---

## 10. Workflow revision visibility

Run Graph may display workflow changes in plain language.

Example:

```text
ZEUS : Le workflow est ajusté. La partie quantitative sera traitée comme partielle.
CHRONOS : La branche quantitative est suspendue. L’analyse technique continue.
```

Rules:

- revision signal does not apply the change;
- workflow patch does not become canonical;
- durable workflow updates remain candidates;
- THEMIS and APOLLO gates remain mandatory when risk requires them.

---

## 10b. Role Signal visibility

Role Signals defined in `ROLE_SIGNALS.md` and shaped via `ROLE_SIGNAL_PROFILES.md` may be surfaced in the Run Graph only as public summaries.

Allowed surface forms:

```text
short ROLE : message in the Inline Run Stream
public summary line in a snapshot node
addressed_role_signal summary attributed to IRIS as mediator
role_consultation summary attributed to the asking role and the answering role
handoff_signal summary attributed to ATHENA or the active role
workflow_revision_signal summary attributed to the emitter
veto_signal summary attributed to THEMIS
stop_gate_signal summary attributed to APOLLO
format_reminder_request and format_reminder_response summaries attributed to IRIS
format_blocked summary attributed to IRIS
```

Forbidden surface forms:

```text
raw chain-of-thought
raw internal prompts
raw mediated message bodies that contain private substance
secrets, tokens, credentials or connection strings
full private document content
unredacted personal data
private file paths
sensitive client data
source dumps from a Knowledge Base
internal Hermes tool transcripts
```

Display constraints:

```text
Role Signals are observations, not runtime commands.
Run Graph never executes a role signal.
Run Graph never edits a role signal payload.
Run Graph never approves, vetoes or arbitrates from a role signal.
Run Graph may show that a signal exists, by whom, to whom and at what risk level.
Authoritative content lives in the Evidence Pack, not in the Run Graph.
```

Reference flow:

```text
ROLE_SIGNALS.md          schema and types
ROLE_SIGNAL_PROFILES.md  expected addressed-role structure
EVIDENCE_PACK.md         persistent traceability
TASK_CONTRACT_REVISIONS.md  revision impact
```

---

## 11. Temporary display and persistence warning

Inline Run Stream messages may be visually temporary in OpenWebUI.

They may be hidden, collapsed, replaced or not shown in the final answer.

However:

```text
Do not treat temporary display as secure deletion.
```

OpenWebUI, browser, server or logs may retain traces depending on implementation.

Therefore V1 messages must never include:

```text
secrets
private raw document extracts
sensitive full file paths
confidential client details
raw chain-of-thought
internal prompts
```

---

## 12. Output levels

Inline Run Stream should support three wording levels later:

| Level | Meaning | Default |
|---|---|---|
| `public` | Simple, non-technical, general-reader wording | yes |
| `professional` | Slightly more precise but still readable | optional |
| `technical` | Event/tool/source details for debugging | blocked by default |

V1 default:

```yaml
inline_run_stream:
  tone: public
  detail_level: clear
  show_technical_terms: false
```

---

## 13. Final rule

```text
Show progress, not private reasoning.
Show state, not chain-of-thought.
Show limitations, not false certainty.
Show governance, not hidden automation.
```

Run Graph is a visibility layer.

It is not a runtime.
