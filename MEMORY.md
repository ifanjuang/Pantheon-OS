# MEMORY.md — Pantheon Next Runtime Memory

This file defines the hot operational memory for Pantheon Next.

It is not a knowledge base.
It is not a project archive.
It is not a roadmap.
It is not a place for long documents.

It contains compact, high-signal memory that may be injected into assistant and session runs.

Stable knowledge must be routed to the appropriate layer:
- session memory → short-lived execution context
- project memory → dossier / affair / workflow-specific continuity
- agency memory → reusable methods, patterns, lessons, standards

---

# 1. Product Identity

§
PROJECT_NAME: Pantheon Next

§
PRODUCT_THESIS: Pantheon Next turns AI from a chat interface into a structured working team for complex professional work.

§
CORE_POSITIONING: Pantheon Next is a modular multi-agent execution system for high-expertise environments such as architecture, project management, legal, compliance, audit, consulting, and IT.

§
NOT_A_CHATBOT: Pantheon Next is not a chatbot wrapper, not a prompt-chaining framework, not a low-code automation layer, and not a generic assistant shell.

§
INTERFACE_RULE: OpenWebUI is the interface layer only. Pantheon Next owns orchestration, state, policies, memory, evaluation, and execution.

---

# 2. Core Runtime Identity

§
MODULARITY_FIRST: Agents, skills, tools, workflows, prompts, templates, policies, and memory adapters must remain modular and replaceable.

§
CORE_DOMAIN_AGNOSTIC: The core runtime stays domain-agnostic. Domain-specific behavior lives in overlays and modules, not in the core.

§
RUNTIME_OVER_PROMPTS: Prompts describe behavior, but runtime controls execution. Workflows define what happens. Policies define what is allowed. Evaluators define what is good enough.

§
CONTROL_DATA_SPLIT: Pantheon Next separates the control plane from the data plane. Control decides. Data executes.

§
NO_DIRECT_TOOL_CALLS: Agents never bypass runtime governance. Risky tool calls pass through PolicyEngine and ActionGate.

§
DRAFT_FIRST: High-impact outputs should be drafted, validated, and only then executed or delivered.

§
HUMAN_CONTROL: High-risk actions require explicit approval before execution.

---

# 3. Repository Model

§
REPO_STRUCTURE: Pantheon Next uses core/, modules/, domains/, platform/, config/, and tests/.

§
CORE_SCOPE: core/ contains contracts, registries, decision, execution, state, policies, evaluation, learning, observability, memory, documents, and llm abstractions.

§
MODULES_SCOPE: modules/ contains reusable agents, skills, tools, workflows, prompts, and templates.

§
DOMAINS_SCOPE: domains/ contains domain overlays such as architecture, legal, software, or future specialized layers.

§
PLATFORM_SCOPE: platform/ contains FastAPI services, UI integration, persistence, runtime storage, and infrastructure.

§
MANIFEST_RULE: Runtime blocks are discovered through manifests. Invalid manifests must fail at startup.

§
OVERLAY_RULE: Domain-specific behavior belongs in domains/{domain}/, not in the generic core.

---

# 4. Memory Model

§
MEMORY_SCOPES: Pantheon memory has three main scopes: session, project, and agency.

§
SESSION_MEMORY: Session memory is short-lived runtime continuity for the current run or thread.

§
PROJECT_MEMORY: Project memory stores validated project decisions, constraints, assumptions, clarifications, and continuity specific to one affair.

§
AGENCY_MEMORY: Agency memory stores reusable patterns, methods, templates, lessons, and standards that survive across projects.

§
FUNCTIONAL_MEMORY: Functional memory tracks temporary task state and intermediate execution context during active runs.

§
SOURCE_OF_TRUTH: Structured storage is the source of truth. Markdown memory is a runtime layer, not the primary database of record.

---

# 5. Memory Routing Rules

§
MEMORY_SELECTIVITY: Not everything should be stored.

§
NOISE_RULE: Noise should be ignored.

§
TASK_STATE_RULE: Temporary task state belongs in functional or session memory.

§
PROJECT_DECISION_RULE: Validated project decisions belong in project memory.

§
PATTERN_RULE: Reusable cross-project patterns may be proposed to agency memory.

§
POST_RUN_ROUTING: After a run, outputs must be routed selectively rather than dumped wholesale into memory.

§
ROUTING_PRIORITY: Session continuity comes first, project continuity second, agency promotion last.

---

# 6. Memory Hygiene Rules

§
MEMORY_MUST_STAY_COMPACT: Runtime memory must remain lean enough to be injected without wasting context budget.

§
NO_VERBOSE_ACCUMULATION: Long prose, detailed archives, and raw session residue do not belong in hot memory.

§
PROMOTION_REQUIRES_SCORING: Candidate long-lived memory should be scored before promotion.

§
PROMOTION_CRITERIA: Promotion criteria include novelty, durability, specificity, and reduction value.

§
STALE_MEMORY_REMOVAL: Temporary progress notes, TODO residue, and expired session outcomes should be removed from hot memory.

§
CONDENSE_TO_POINTERS: If detailed knowledge already exists elsewhere, hot memory should keep only a compact pointer.

§
STRUCTURAL_PROPOSALS: Recurrent patterns may justify proposals for wiki pages, templates, or skills, but such promotion must remain explicit and governed.

§
MEMORY_HYGIENE_LOOP: Pantheon should eventually support post-run consolidation and periodic lean-memory checks.

---

# 7. Runtime Governance Reminders

§
CRITICITY_RULE: Runs use C1–C5 criticity levels that affect activation depth, validation, and escalation.

§
REVERSIBILITY_RULE: Every meaningful action must be interpreted through reversibility.

§
VETO_RULE: Structured vetoes must include verdict, justification, severity, and lift condition.

§
TRACEABILITY_RULE: Important outputs must remain traceable to sources, tools, and agents.

§
APPROVAL_RULE: High-risk actions must stop for approval instead of continuing silently.

---

# 8. Active Stable Priorities

§
CURRENT_PRIORITY: Build and maintain a controlled execution system before adding more adaptive complexity.

§
CONTROLLED_LOOP_FIRST: The durable priority is a reliable controlled loop: precheck → planning → execution → validation → synthesis.

§
DO_NOT_OVERBUILD: Do not prioritize graph memory, advanced learning, or heavy orchestration before the controlled execution loop is reliable.

§
MEMORY_DISCIPLINE: Preserve selective memory, bounded context, and explicit promotion rules as the system evolves.

§
OVERLAY_DISCIPLINE: Keep the runtime generic and push métier-specific behavior into domain overlays.

---

# 9. Active Memory Notes

§
HOT_DIRECTION: Pantheon should remain manifest-first, modular, and overlay-driven.

§
HOT_MEMORY_WARNING: MEMORY.md must stay smaller and more operational than ARCHITECTURE.md or ROADMAP.md.

§
MEMORY_EVOLUTION: Future memory operations may include post-run consolidation, memory trimming, and controlled pattern promotion.

§
KNOWLEDGE_SEPARATION: Runtime memory is not the same thing as knowledge storage, wiki pages, indexed markdown, or long-form documentation.

---

# 10. Final Rule

§
GOOD_MEMORY: Good runtime memory is compact, stable, selective, and useful across runs.

§
BAD_MEMORY: If memory becomes a dump of architecture notes, roadmap sequencing, or stale execution residue, it stops functioning as runtime memory.