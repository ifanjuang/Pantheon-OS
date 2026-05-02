# MODEL ROUTING POLICY — Pantheon Next

> Governance policy for model selection across OpenWebUI, Ollama instances, Hermes and Pantheon abstract agents.

---

## 1. Principle

Pantheon Next must not become a model router.

```text
OpenWebUI exposes configured models and presets.
Hermes resolves and executes model calls.
Pantheon Next defines the policy, allowed mappings and fallback rules.
```

This policy governs which model families or instances may be used for each abstract agent role.

It does not implement execution.

---

## 2. Supported operating modes

Pantheon must support both deployment situations:

```text
single_ollama_instance
multi_ollama_instance
```

### 2.1 Single Ollama instance mode

OpenWebUI has only one Ollama connection.

Example:

```text
Ollama URL: http://ollama:11434
Prefix ID: empty
```

Agent presets can still exist in OpenWebUI Workspace Models, but all base models come from the same Ollama instance.

Example:

```text
ATHENA Planner       → qwen3:14b
ARGOS Extractor      → llama3.1:8b
THEMIS Risk Check    → qwen3:14b
APOLLO Validator     → deepseek-r1:14b
IRIS Communication   → mistral:7b
```

If a preferred model is missing, Hermes must apply the configured fallback rule.

### 2.2 Multi Ollama instance mode

OpenWebUI has several Ollama connections.

Example:

```text
nas/     → http://ollama-nas:11434
gpu/     → http://ollama-gpu:11434
remote/  → http://ollama-remote:11434
```

`Prefix ID` should be used when the same model names exist on multiple instances or when the operator wants explicit instance routing.

Example:

```text
ATHENA Planner       → gpu/qwen3:14b
ARGOS Extractor      → nas/llama3.1:8b
APOLLO Validator     → gpu/deepseek-r1:14b
IRIS Communication   → nas/mistral:7b
```

---

## 3. Separation of authority

| Layer | Role |
|---|---|
| OpenWebUI | exposes available models, connections and Workspace Model presets |
| Hermes | executes model calls and applies fallback at runtime |
| Pantheon Next | defines allowed model policy, fallback rules and risk constraints |

Pantheon must not:

```text
call Ollama directly as a runtime router
select models opaquely without trace
fallback silently on high-risk outputs
store secrets for model providers without policy
mutate OpenWebUI settings directly
```

---

## 4. Abstract agent model classes

| Agent | Typical model needs |
|---|---|
| ATHENA | planning, structured reasoning, task decomposition |
| ARGOS | extraction, source discipline, low hallucination |
| THEMIS | cautious reasoning, policy, approval/risk classification |
| APOLLO | validation, contradiction detection, final quality gate |
| IRIS | tone control, concise communication, drafting |
| HESTIA | project context continuity, memory candidate discipline |
| MNEMOSYNE | reusable pattern extraction, system memory candidate discipline |
| HEPHAESTUS | technical feasibility, implementation and architecture critique |
| PROMETHEUS | adversarial challenge and weak-assumption detection |
| ZEUS | arbitration, routing, final workflow decision |

---

## 5. Model capability labels

Allowed capability labels:

```text
reasoning
planning
extraction
structured_output
validation
contradiction_check
policy_review
source_discipline
style_control
summarization
coding
long_context
low_latency
local_only
private_data_allowed
public_data_only
```

Capability labels are governance hints. They do not prove model quality.

---

## 6. Fallback behavior

Allowed fallback strategies:

| Strategy | Meaning |
|---|---|
| `use_fallback_with_warning` | use fallback and record the substitution |
| `stop_and_request_manual_review` | stop if preferred/allowed model unavailable |
| `degrade_to_draft_only` | produce draft only, no final validation |
| `degrade_to_diagnostic_only` | produce diagnostic only, no action recommendation |
| `block` | do not run |

Default fallback rule:

```text
C0-C2 may use fallback with warning.
C3 may use fallback only if evidence remains sufficient.
C4-C5 must stop or request manual review unless policy explicitly allows fallback.
```

---

## 7. Criticality constraints

| Criticality | Model routing rule |
|---|---|
| C0 | any allowed model sufficient for diagnostic/read-only work |
| C1 | fallback allowed with warning |
| C2 | fallback allowed if action remains reversible |
| C3 | fallback must be recorded and may reduce output to candidate/draft |
| C4 | fallback normally stops and asks for manual review |
| C5 | fallback blocked unless explicitly approved |

---

## 8. OpenWebUI Workspace Model presets

OpenWebUI may expose role presets such as:

```text
ATHENA Planner
ARGOS Extractor
THEMIS Risk Check
APOLLO Validator
IRIS Communication
```

These presets are user-facing conveniences, not Pantheon canonical authority.

The Pantheon policy remains in:

```text
docs/governance/MODEL_ROUTING_POLICY.md
config/model_routing.example.yaml
```

If OpenWebUI presets differ from Pantheon policy, Pantheon policy wins.

---

## 9. Required trace in Evidence Pack

When model routing affects a consequential output, record:

```text
requested_agent
preferred_model
actual_model
instance_id
fallback_used
fallback_reason
criticality
output_limitations
manual_review_required
```

Reference:

```text
EVIDENCE_PACK.md
TASK_CONTRACTS.md
APPROVALS.md
```

---

## 10. Single instance policy

If OpenWebUI has only one Ollama instance, this is valid.

Rules:

- preferred models may all use the same instance;
- unavailable models must trigger configured fallback behavior;
- a missing validator model must not silently produce final C4/C5 validation;
- instance prefix may be empty;
- OpenWebUI Workspace Models may still be used as role presets.

---

## 11. Multi instance policy

If several Ollama instances are configured:

- use explicit prefixes when possible;
- distinguish local/NAS/GPU/remote capacity;
- avoid routing private project data to remote models unless policy allows it;
- record the selected instance in Evidence Packs for consequential outputs;
- do not rely on automatic balancing for C4/C5 outputs unless explicitly reviewed.

---

## 12. Security and privacy

Private project data should use:

```text
local_only
private_data_allowed
```

Remote/cloud models require explicit policy.

Sensitive data, secrets, credentials and private client data must not be sent to models unless the relevant policy and approval path allow it.

---

## 13. Future API surface

A future read-only endpoint may expose this policy:

```text
GET /domain/model-routing
```

It must be read-only at first.

Forbidden until C3 approval flow exists:

```text
POST /domain/model-routing
PATCH /domain/model-routing
POST /models/install
POST /providers/update
```

---

## 14. Final rule

```text
Pantheon defines model policy.
OpenWebUI exposes presets.
Hermes executes with trace.
```
