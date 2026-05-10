# Skill — workflow_live_narrator

Status: candidate.

Domain: general.

Purpose: transform structured Run Graph, request orchestration and workflow events into short, public-facing progress messages for optional OpenWebUI inline display.

---

## 1. Role

`workflow_live_narrator` is a display and narration skill.

It converts observed execution state into clear, temporary, user-visible messages.

It does not reason privately, execute tasks, approve actions, activate workflows, promote memory or validate final outputs.

Core rule:

```text
Show progress, not private reasoning.
```

---

## 2. Inputs

Expected inputs:

```text
run_id
task_contract_id
latest_run_event
current_role
current_request_frame
current_agora_state
current_workflow_state
source_state
tool_state
approval_state
workflow_revision_state
evidence_delta
visibility_policy
```

The skill may also receive a bounded list of recent public events to avoid repetitive messages.

---

## 3. Outputs

Primary output:

```text
ROLE : short public-facing message.
```

Output fields for structured use:

```yaml
inline_message:
  role: ATHENA
  message: "Je prépare la méthode d’analyse."
  tone: public
  visible: true
  temporary: true
  technical: false
  evidence: false
  approval: false
```

---

## 4. Default wording mode

Default wording is:

```text
plain
short
non-technical
public-facing
without emoji
without color
without raw event names
```

Good examples:

```text
METIS : Je clarifie l’intention de la demande.
ATHENA : Je prépare la méthode d’analyse.
ARGOS : Je vérifie les documents disponibles.
ARGOS : Le devis et le CCTP sont pris en compte.
DEMETER : J’attends les quantités extraites du devis.
THEMIS : Attention, la conclusion devra rester prudente car une pièce manque.
APOLLO : Je vérifie que la synthèse reste claire et limitée aux preuves disponibles.
ZEUS : Je poursuis avec les informations disponibles.
```

Bad examples:

```text
ATHENA : workflow.node.started.
ARGOS : document_read tool call initiated on internal path.
THEMIS : C3 policy gate activated by internal resolver.
APOLLO : My reasoning says this is coherent.
```

---

## 5. Allowed event transformations

Allowed input events:

```text
run.started
run.completed
run.failed
request.frame_created
request.context_expansion_needed
workflow.selected
workflow.node.started
workflow.node.completed
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
warning.raised
veto.raised
approval.required
workflow.revision_signal
workflow.patch_candidate
```

The skill must convert these into simple messages.

Examples:

| Event | Output |
|---|---|
| `request.frame_created` | `METIS : Je clarifie l’intention de la demande.` |
| `workflow.selected` | `ATHENA : Je prépare la méthode d’analyse.` |
| `source.missing` | `ARGOS : Une pièce utile manque. Je la signale dans les limites.` |
| `role.waiting` | `DEMETER : J’attends les quantités extraites du devis.` |
| `information.transmitted` | `ARGOS : Les quantités exploitables sont transmises à DEMETER.` |
| `warning.raised` | `THEMIS : Attention, cette conclusion devra rester prudente.` |
| `veto.raised` | `THEMIS : Je bloque cette action car elle nécessite une validation préalable.` |
| `workflow.revision_signal` | `ZEUS : Le workflow est ajusté. Je poursuis avec les informations disponibles.` |

---

## 6. Forbidden output

The skill must never output:

```text
raw chain-of-thought
hidden reasoning
internal prompts
system prompts
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

---

## 7. Evidence relationship

Inline narration is not evidence.

The skill may mention that evidence is being assembled, but it must not replace the Evidence Pack.

Allowed:

```text
APOLLO : Je vérifie que les limites et les sources restent visibles.
```

Forbidden:

```text
APOLLO : Cette analyse est validée définitivement.
```

Reference:

```text
docs/governance/EVIDENCE_PACK.md
```

---

## 8. Approval relationship

The skill may display that approval is needed.

Allowed:

```text
THEMIS : Une validation sera nécessaire avant toute modification.
```

Forbidden:

```text
THEMIS : J’approuve cette modification.
```

Approval authority remains governed by `APPROVALS.md`.

---

## 9. Memory relationship

The skill must not create or promote memory.

It may display that a reusable point could become a candidate later only if this is already represented by the governed event stream.

Forbidden:

```text
MNEMOSYNE : Je mémorise cette règle.
```

Allowed:

```text
MNEMOSYNE : Ce point pourra être proposé comme mémoire candidate si une validation est demandée.
```

---

## 10. Implementation posture

This skill is a Pantheon candidate skill.

It is not a Hermes executable skill by default.

It may later be mapped to:

```text
OpenWebUI Function or Tool for display
OpenWebUI Pipe for display-only routing
Hermes-side template processor
Pantheon API read-only formatter
```

Any implementation must remain optional and disabled by default.

---

## 11. Final rule

```text
Narrate visible state.
Never narrate private reasoning.
Never execute.
Never approve.
Never canonize.
```
