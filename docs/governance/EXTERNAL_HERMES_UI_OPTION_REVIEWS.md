# EXTERNAL HERMES UI OPTION REVIEWS — Pantheon Next

> Focused classification addendum for Hermes-facing web UIs, dashboards, workspaces, memory providers, search plugins, skill packs, self-evolution tools and ecosystem catalogues.
>
> These tools may assist Hermes operations. None of them becomes Pantheon authority.

---

## 1. Principle

Canonical split:

```text
OpenWebUI expose.
Hermes Agent exécute.
Pantheon Next gouverne.
```

Hermes UIs are technical consoles.

Hermes skills and plugins are executable capabilities only after review.

They may help observe or operate Hermes, but they must not replace:

```text
OpenWebUI as user cockpit
Pantheon governance docs as source of truth
Task Contracts as execution frame
Evidence Packs as proof contract
Approvals as authority gates
Pantheon Memory as canonical memory
```

---

## 2. Summary table

| Tool | Repository / source | Type | Status | Allowed use | Main risk |
|---|---|---|---|---|---|
| Hermes Dashboard | official Hermes feature | native Hermes technical dashboard | `local_admin_only` | local config/session/log inspection | secrets exposure, cron/scheduler drift |
| Hermes WebUI | `nesquena/hermes-webui` | browser/mobile Hermes UI | `hermes_ui_lab_candidate` | local/Tailscale Hermes UI | repo write, tool execution, OpenWebUI confusion |
| Hermes Workspace | `outsourc-e/hermes-workspace` | advanced Hermes workspace/control plane | `lab_ui_candidate` | technical workspace in lab | swarm/autonomy, terminal/write access |
| Hermes HUD UI | `joeynyc/hermes-hudui` | Hermes monitor/HUD | `monitor_only_lab` | local monitoring | Hermes memory confusion, cron/editing |
| Hermes Agent Self-Evolution | `NousResearch/hermes-agent-self-evolution` | automatic optimization/self-evolution | `blocked_for_core` | offline research only | automatic skill/prompt/code mutation |
| Hermes Ecosystem / Atlas | `ksimback/hermes-ecosystem` | ecosystem catalogue/watchlist | `reference_catalog_only` | external discovery and classification | auto-import, false authority |
| Mnemosyne | `AxDSan/mnemosyne` | local Hermes memory provider | `watch_test_only` / `rejected_for_core_memory` | sandbox local memory research | parallel memory authority |
| Hermes Optimization Guide | `OnlyTerp/hermes-optimization-guide` | setup/operations guide | `reference_only` | installation ideas to review manually | unreviewed Telegram/LightRAG/background services |
| ComfyUI Skills OpenClaw | `HuangYuChuh/ComfyUI_Skills_OpenClaw` | ComfyUI workflow skill bridge | `creative_skill_lab_candidate` | sandbox image-generation workflows | uncontrolled model/workflow execution |
| drawio-skill | `Agents365-ai/drawio-skill` | diagram generation skill | `diagram_skill_candidate` | local diagram export candidate | generated diagrams becoming source of truth |
| SkillClaw | `AMAP-ML/SkillClaw` | collective skill evolution | `blocked_for_core` | research only | self-evolving skills / continual learning |
| Web Search Plus | `robbyczgw-cla/web-search-plus-plugin` / OpenClaw skill `web-search-plus` | web search plugin / skill | `search_plugin_candidate` | sandbox search with allowlist | paid APIs, web leakage, search authority drift |

---

## 3. Hermes Dashboard

Classification:

```text
local_admin_only
```

Allowed:

```text
local technical inspection
Hermes config review
session/log inspection
skill inspection
```

Forbidden:

```text
public exposure
unauthenticated LAN exposure
cron/scheduler authority
Pantheon memory authority
OpenWebUI replacement
```

Approval:

```text
local read-only lab: C3
LAN exposure: C4
secrets / cron / broad write access: C5
```

---

## 4. Hermes WebUI

Classification:

```text
hermes_ui_lab_candidate
```

Repository:

```text
https://github.com/nesquena/hermes-webui
```

Allowed:

```text
local browser access to Hermes
mobile access through Tailscale/VPN
Hermes chat testing
Hermes session inspection
workspace browsing in read-only mode first
```

Forbidden:

```text
replace OpenWebUI
replace Pantheon governance
become workflow authority
become memory authority
public internet exposure
direct repo write by default
autonomous cron or scheduler authority
```

Approval:

```text
local read-only lab: C3
LAN/Tailscale with password: C4
public exposure, repo write or cron: C5
```

---

## 5. Hermes Workspace

Classification:

```text
lab_ui_candidate
```

Repository:

```text
https://github.com/outsourc-e/hermes-workspace
```

Allowed:

```text
Hermes technical workspace
local lab dashboard
session inspection
skill inspection
controlled terminal in lab only
```

Forbidden:

```text
replace OpenWebUI
replace Pantheon governance
autonomous swarm mode
workflow authority
memory authority
public exposure
write access to Pantheon repo by default
```

Approval:

```text
local read-only lab: C3
LAN exposed: C4
swarm, write access, terminal ops: C5
```

---

## 6. Hermes HUD UI

Classification:

```text
monitor_only_lab
```

Repository:

```text
https://github.com/joeynyc/hermes-hudui
```

Allowed:

```text
local Hermes monitoring
session inspection
skill inspection
cost/model capability visibility
```

Forbidden:

```text
Pantheon cockpit
Pantheon memory authority
workflow authority
public exposure
editing Hermes memory as Pantheon truth
cron activation without approval
```

Approval:

```text
local monitoring: C3
LAN exposed: C4
memory edit or cron: C5
```

---

## 7. Hermes Agent Self-Evolution

Classification:

```text
blocked_for_core
research_only
```

Repository:

```text
https://github.com/NousResearch/hermes-agent-self-evolution
```

Allowed:

```text
offline research
fictive skill optimization tests
Promptfoo / DSPy evaluation inspiration
candidate generation only
```

Forbidden:

```text
automatic skill promotion
automatic prompt replacement
automatic code mutation
direct PR without human review
use on real client/project data
continuous improvement loop
Pantheon memory promotion
```

Approval:

```text
read docs: C0
sandbox fictive evaluation: C3
repo write or real skill mutation: C5
```

---

## 8. Hermes Ecosystem / Atlas

Classification:

```text
reference_catalog_only
```

Repository:

```text
https://github.com/ksimback/hermes-ecosystem
```

Allowed:

```text
identify Hermes-related projects
feed external option reviews
monitor new skills and UI projects
compare community classifications
```

Forbidden:

```text
Pantheon runtime
Hermes replacement
OpenWebUI replacement
model routing authority
workflow authority
memory authority
security authority
deploy Atlas RAG against private project data
import repos without Pantheon review
```

Approval:

```text
read catalog: C0
add classification entry: C1/C3
import or test repo from catalog: C3
connect private data or external API keys: C4/C5
```

---

## 9. Mnemosyne

Classification:

```text
watch_test_only
rejected_for_core_memory
```

Repository:

```text
https://github.com/AxDSan/mnemosyne
```

Relevant properties:

```text
local-first Hermes memory provider
SQLite-backed
sqlite-vec and FTS5 search
no external databases
no API keys
no network calls
sub-millisecond/local positioning
```

Potential value:

```text
local Hermes memory backend research
SQLite memory provider design reference
fast local retrieval pattern
privacy-first memory implementation reference
```

Pantheon decision:

```text
Do not use as Pantheon Memory.
Do not let Hermes memory become canonical Pantheon memory.
Study only in sandbox if needed.
```

Allowed:

```text
read documentation
sandbox test with fictive data
compare with Pantheon Memory candidate flow
study SQLite/FTS/vector design
```

Forbidden:

```text
replace Pantheon Memory
promote Hermes memories automatically
connect real client/project data without approval
write canonical memory
bypass Evidence Pack validation
```

Approval:

```text
read docs: C0
sandbox fictive local test: C3
private project data or memory migration: C4/C5
```

---

## 10. Hermes Optimization Guide

Classification:

```text
reference_only
operations_inspiration
```

Repository:

```text
https://github.com/OnlyTerp/hermes-optimization-guide
```

Potential value:

```text
Hermes setup patterns
migration notes
LightRAG setup references
Telegram gateway references
skill creation notes
```

Risk:

```text
background services
Telegram gateway
external API keys
LightRAG ingestion
scheduled delivery
unreviewed operational shortcuts
```

Allowed:

```text
read and extract operations ideas
compare with operations/hermes_lab.md when created
use as checklist inspiration only
```

Forbidden:

```text
copy-paste installation without review
activate Telegram gateway without C4/C5
run LightRAG ingestion on private data without policy
create background services from the guide without approval
```

Approval:

```text
read guide: C0
adapt documentation: C1/C3
run local service based on guide: C3/C4
Telegram / external gateway / private data ingestion: C4/C5
```

---

## 11. ComfyUI Skills OpenClaw

Classification:

```text
creative_skill_lab_candidate
```

Repository:

```text
https://github.com/HuangYuChuh/ComfyUI_Skills_OpenClaw
```

Potential value:

```text
turn ComfyUI API workflows into callable agent skills
support OpenClaw, Codex and Claude Code style skill directories
multi-server ComfyUI management
workflow schema mapping
local visual generation lab
```

Allowed:

```text
sandbox creative/image workflow tests
fictive examples only
local ComfyUI server only at first
review workflow schema before exposure
```

Forbidden:

```text
automatic creative workflow execution from Pantheon
public ComfyUI exposure
private/client image processing without approval
auto-install custom nodes or models
workflow output treated as source of truth
```

Approval:

```text
read docs: C0
local sandbox with fictive images: C3
private data/images or external ComfyUI: C4/C5
```

---

## 12. drawio-skill

Classification:

```text
diagram_skill_candidate
```

Repository:

```text
https://github.com/Agents365-ai/drawio-skill
```

Potential value:

```text
generate draw.io diagrams from text
export PNG / SVG / PDF
support agent-skill format across Hermes/OpenClaw/Codex/Claude Code
produce repository diagrams or governance visuals
```

Pantheon fit:

```text
Strong candidate for diagram generation after README diagram process is stabilized.
Useful for draft diagrams, not source of truth.
```

Allowed:

```text
sandbox generation of fictional diagrams
candidate visuals for README/assets
export local diagrams for review
```

Forbidden:

```text
replace governance Markdown
publish diagrams without human validation
generate diagrams from private client/project data without approval
overwrite validated Lucid exports without review
```

Approval:

```text
read docs: C0
sandbox diagram generation: C3
README asset replacement: C3
private/project data diagrams: C4
```

---

## 13. SkillClaw

Classification:

```text
blocked_for_core
research_only
```

Repository:

```text
https://github.com/AMAP-ML/SkillClaw
```

Relevant positioning:

```text
collective skill evolution
agentic evolver
continual learning / self-evolving skill topics
```

Allowed:

```text
read paper/repo
compare with Pantheon skill lifecycle
extract evaluation vocabulary if useful
```

Forbidden:

```text
automatic skill evolution
automatic skill promotion
continuous learning loop
mutation of Pantheon skills
mutation of Hermes skills
private data skill training
```

Approval:

```text
read docs: C0
sandbox fictive research: C3
repo/skill mutation: C5
```

---

## 14. Web Search Plus

Classification:

```text
search_plugin_candidate
sandbox_only_until_policy
```

Repository / source:

```text
https://github.com/robbyczgw-cla/web-search-plus-plugin
https://openclaw.army/skills/robbyczgw-cla/web-search-plus
```

Note:

```text
The originally supplied `robbyczgw-cla/hermes-web-search-plus` path should be treated as an alias/to-verify reference. The reviewed upstream target is `web-search-plus-plugin` / OpenClaw skill `web-search-plus`.
```

Potential value:

```text
multi-provider web search
intelligent provider routing
SearXNG-compatible self-hosted option
local caching
provider diagnostics
```

Risks:

```text
external API keys
paid providers
web leakage of private context
search results treated as evidence without quality tiering
auto-routing across providers without policy
```

Allowed:

```text
read documentation
sandbox search on public queries
evaluate routing/diagnostic fields
map provider outputs to Evidence Pack fields
```

Forbidden:

```text
send private project/client context to web providers without approval
enable all providers without allowlist
treat search output as canonical source
store provider secrets in repo
use search mode on sensitive data
```

Approval:

```text
read docs: C0
sandbox public query: C2/C3
external API keys: C4
private data / broad research mode: C4/C5
```

---

## 15. Common Docker / Portainer rule

Do not install these by default in the production lab stack.

Recommended stack order:

```text
1. OpenWebUI + postgres_openwebui + searxng
2. Pantheon API + postgres_pantheon
3. Hermes Agent + official dashboard
4. Optional single Hermes UI lab candidate
5. Optional individual skill/plugin sandbox after classification
```

Forbidden by default:

```text
Docker socket
public dashboard
secret mounts
repo write access
cron activation
auto-install skills
auto-evolution
external provider keys
private data ingestion
```

---

## 16. Final rule

```text
Hermes tools may assist execution.
They do not govern.
They do not approve.
They do not canonize memory.
They do not replace OpenWebUI.
They do not replace Pantheon Markdown.
```
