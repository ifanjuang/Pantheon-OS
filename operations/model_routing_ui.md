# Model Routing UI — Operations Spec

> Candidate specification for a future local/admin UI that helps define compute nodes, Ollama models and Pantheon role-to-model routing.
>
> This is not an implementation.

---

## 1. Purpose

The Model Routing UI is a future operator interface for managing two local policy registries:

```text
config/compute_nodes.local.yaml
config/model_routing.local.yaml
```

It exists to help the operator define which local or LAN model-serving machines may be used by Hermes for Pantheon roles.

It must not become a runtime, router, scheduler or autonomous configuration manager.

Canonical split:

```text
Pantheon defines model policy.
Hermes applies model routing during execution.
Ollama serves models.
OpenWebUI exposes user-facing presets.
```

---

## 2. Scope

Allowed scope:

```text
list configured compute nodes
run read-only health checks against Ollama /api/tags
list available local models
create candidate compute node entries
create candidate model registry entries
assign model ids to Pantheon roles
set fallback policies
validate C0-C5 fallback constraints
export YAML
show drift between example and local configs
produce a Doctor-compatible report
```

Forbidden scope:

```text
execute Pantheon tasks
execute Hermes tasks
call models for user work
install models automatically
pull Ollama models automatically
scan LAN automatically
store secrets
show secrets
mutate OpenWebUI configuration
mutate Hermes configuration silently
mutate Pantheon governance docs
activate skills
canonize workflows
promote memory
```

---

## 3. UI sections

### 3.1 Compute Nodes

Fields:

```text
id
label
provider
base_url
health_url
locality
local_only
data_policy
tags
allowed_criticality
enabled
notes
```

Required behavior:

```text
base_url is displayed without credentials
healthcheck uses GET /api/tags only
healthcheck result is read-only
remote nodes default to public_data_only
C4-C5 use requires explicit policy
```

### 3.2 Model Registry

Fields:

```text
model_id
provider
compute_node_id
model
type
context_length
embedding_dim
capabilities
notes
```

Supported model types:

```text
chat
embedding
reranker
vision
specialized
```

Initial Pantheon use should only rely on:

```text
chat
embedding
```

### 3.3 Role Routing

Fields:

```text
role
openwebui_preset_name
model_id
fallback_model_ids
required_capabilities
if_unavailable
max_criticality_without_manual_review
```

Rules:

```text
ARGOS / IRIS / CHRONOS may use safer fallback for C0-C2.
ATHENA may degrade to draft/candidate for C3.
THEMIS / APOLLO / ZEUS must not silently fallback for C4-C5.
HEPHAESTUS should prefer technical/coding-capable models for repo/code tasks.
```

### 3.4 Validation

The UI may validate:

```text
referenced compute_node_id exists
referenced model_id exists
model type is compatible with role
fallback ids exist
C4-C5 fallback is blocked or manual-review only
remote/public-data-only node is not used for private_data_allowed routing
required capabilities are present
local files are not marked for commit
```

It must not validate model quality.

---

## 4. Persistence

The UI may write only local candidate files:

```text
config/compute_nodes.local.yaml
config/model_routing.local.yaml
```

These files should normally be ignored by Git if they contain real LAN IPs, machine names or operator-specific infrastructure.

Sanitized examples belong in:

```text
config/compute_nodes.example.yaml
config/model_routing.example.yaml
```

---

## 5. Approval levels

| Action | Approval |
|---|---:|
| View model routing policy | C0 |
| Run health check against configured local node | C1 |
| Create/edit local candidate routing config | C3 |
| Expose UI on LAN | C4 |
| Store provider secrets | C5 |
| Auto-discover LAN model servers | C5 |
| Pull/install models automatically | C5 |
| Mutate OpenWebUI/Hermes config directly | C4/C5 |
| Allow C4-C5 silent fallback | blocked |

---

## 6. Evidence Pack requirements

If model routing affects a consequential output, the Evidence Pack must record:

```text
requested_agent
preferred_model
actual_model
model_id
compute_node_id
instance_id
fallback_used
fallback_reason
criticality
output_limitations
manual_review_required
```

If a fallback was blocked, the output should report:

```text
model_unavailable
fallback_blocked
manual_review_required
next_safe_action
```

---

## 7. Relationship with OpenWebUI

OpenWebUI may expose role presets, but it is not the policy source.

OpenWebUI presets can mirror names from `config/model_routing.local.yaml`:

```text
ATHENA Planner
ARGOS Extractor
THEMIS Risk Check
APOLLO Validator
IRIS Communication
HEPHAESTUS Technical Review
ZEUS Arbitration
```

If OpenWebUI presets diverge from Pantheon policy, Pantheon policy wins.

---

## 8. Relationship with Hermes

Hermes may consume the routing policy later.

Allowed future flow:

```text
Pantheon policy / local routing YAML
→ Hermes reads candidate routing config
→ Hermes selects model endpoint during Task Contract execution
→ Evidence Pack records actual model and compute node
```

Forbidden:

```text
Hermes silently rewrites routing policy
Hermes silently bypasses C4-C5 fallback rules
Hermes installs models on nodes without approval
Hermes probes the network without approval
```

---

## 9. Relationship with Pantheon API

A future read-only endpoint may expose sanitized policy state:

```text
GET /domain/model-routing
GET /domain/compute-nodes
```

Write endpoints are forbidden until an approval flow exists:

```text
POST /domain/model-routing
PATCH /domain/model-routing
POST /domain/compute-nodes
PATCH /domain/compute-nodes
POST /models/install
```

---

## 10. Minimum viable UI

A minimal implementation would include:

```text
one local admin page
YAML import/export
node list
model list
role mapping table
read-only healthcheck button
validation report
no task execution
no direct OpenWebUI mutation
no direct Hermes mutation
```

Preferred first implementation mode:

```text
local-only
admin-only
candidate YAML export
manual review before use
```

---

## 11. Final rule

```text
The UI helps define policy.
It does not route, execute, approve, remember or canonize.
```
