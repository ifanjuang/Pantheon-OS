# ROADMAP — Pantheon OS

> Feuille de route consolidée pour faire évoluer Pantheon OS en système d’exécution multi-agent modulaire, gouverné, inspectable et portable.

Thèse produit : Pantheon OS n’est pas un chatbot. C’est un environnement d’exécution contrôlé où agents spécialisés, workflows explicites, skills réutilisables, tools gouvernés, mémoire auditable et politiques de risque coopèrent comme une équipe experte structurée.

---

# 1. Vision

Pantheon OS cible les environnements professionnels à forte densité documentaire, réglementaire, décisionnelle et opérationnelle : architecture, chantier, conduite de projet, conformité, juridique, audit, conseil, IT et recherche.

Le système doit rester :

- modulaire ;
- explicable ;
- inspectable ;
- gouverné ;
- portable entre domaines ;
- piloté par documentation.

Le runtime reste générique. La valeur métier vit dans les domain overlays.

---

# 2. Preservation Rules

Toute évolution doit préserver ces règles.

## 2.1 Core domain-agnostic

Le core fournit contrats, exécution, routing, state, registries, policies, evaluation, observability, memory abstractions et document services. Il ne porte pas de logique métier.

## 2.2 Filesystem-driven modularity

Ajouter un agent, skill, tool ou workflow doit rester une opération de dossier + manifest + contrat valide.

## 2.3 Séparation agent / skill / tool / workflow

- un agent raisonne ;
- une skill applique une capacité réutilisable ;
- un tool exécute une action technique ou externe ;
- un workflow structure l’exécution.

## 2.4 Workflows explicites

L’exécution reste structurée, visible, traçable et testable. Pas de chaîne implicite de prompts.

## 2.5 Gouvernance explicite

Criticité, réversibilité, draft-first, veto, escalation, approval et decision debt restent des objets runtime.

## 2.6 Mémoire multi-couches et sélective

La mémoire doit distinguer session, project, agency, functional, raw history, candidate facts, active facts, summaries, cards et traces.

Elle ne doit jamais devenir un dump de contexte.

## 2.7 Outputs structurés

Les runs sérieux exposent contexte, findings, analysis, certainty, impacts, options, validation required et memory target.

## 2.8 Domain overlays hors core

Les domaines architecture, legal, software, consulting et futurs overlays restent hors du runtime kernel.

---

# 3. Target Architecture

```text
platform/
  api/              FastAPI apps
  ui/               OpenWebUI integration + admin console
  data/             persistence and runtime state
  infra/            Docker, deployment, scripts

core/
  contracts/        base types and interfaces
  registry/         registries
  decision/         control plane
  execution/        data plane
  state/            session and run state
  policies/         policy engine and action gate
  evaluation/       scorecards and tests
  learning/         controlled improvement loop
  observability/    traces, logs, runs
  memory/           memory abstractions and routing
  documents/        ingestion, indexing, retrieval, citation
  packaging/        context and artifact bundles
  llm/              provider abstraction, budget, routing

modules/
  agents/
  skills/
  tools/
  workflows/
  prompts/
  templates/

domains/
  architecture/
  legal/
  software/
  consulting/
```

---

# 4. Domain Overlay Model

Chaque overlay métier fournit sa valeur sans modifier le core.

Un overlay peut contenir : prompts, skills, workflows, policies, trusted sources, templates, evaluation cases, agents spécifiques si besoin.

Activation par configuration : domaine actif, overlays enabled, priorités, politiques injectées.

---

# 5. Agent Pantheon

## 5.1 Control agents

- ZEUS : orchestration, arbitrage, coordination finale ;
- ATHENA : planning, classification, décomposition ;
- METIS : délibération structurée, hypothèses, conflits ;
- PROMETHEUS : contradiction, critique, anti-consensus ;
- THEMIS : procédure, règles, policy, veto ;
- HERA : supervision post-run ;
- APOLLO : validation finale et confidence scoring ;
- HECATE : incertitude et missing information.

## 5.2 Research and analysis agents

- HERMES : precheck, routing, source strategy ;
- DEMETER : ingestion et normalisation ;
- ARGOS : extraction de faits, citations, entités, relations ;
- ARTEMIS : filtrage de pertinence.

## 5.3 Memory agents

- HESTIA : mémoire projet ;
- MNEMOSYNE : mémoire agence ;
- HADES : retrieval profond et archives.

## 5.4 Output agents

- KAIROS : synthèse ;
- DAEDALUS : documents et dossiers ;
- IRIS : communication ;
- HEPHAESTUS : diagrammes et artefacts techniques ;
- APHRODITE : polish, jamais validation.

## 5.5 System agents

- ARES : fallback contrôlé ;
- POSEIDON : load et flow control.

---

# 6. Governance Model

## 6.1 Criticity C1-C5

Criticité contrôle profondeur, agents, validations, veto, traceability.

## 6.2 Reversibility

Actions : internal note, memory write, external communication, critical / irreversible action.

## 6.3 Draft-first

Toute action sérieuse suit génération, validation, exécution.

## 6.4 Decision debt

États D0-D3 : resolved, provisional, conditional, blocked / critical.

Chaque debt conserve justification, lift condition, deadline éventuelle, phase de revue.

## 6.5 Veto chain

Un veto inclut verdict, justification, severity, lift_condition.

Chaîne cible :

```text
execute_agents
→ veto_check
→ veto_themis
→ veto_zeus
→ zeus_judge
```

---

# 7. Memory Roadmap

## 7.1 Memory layers

Pantheon doit formaliser : session memory, project memory, agency/global memory, functional memory, raw history, candidate facts, active facts, summaries, compact cards, traces.

## 7.2 Memory routing

Après chaque run : temporary context → session memory ; validated project decision → HESTIA ; reusable pattern → MNEMOSYNE proposal ; contradiction → decision debt ou escalation ; noise → ignored.

## 7.3 Auditable context injection

Le système doit exposer le contexte injecté avant ou après exécution : facts, cards, summaries, chunks, documents, decisions, exclusions importantes.

## 7.4 Candidate fact lifecycle

```text
raw source
→ extraction / reflection
→ candidate fact
→ validation / scoring
→ active fact
→ consolidation
→ context injection
```

## 7.5 Consolidation and dry-run

La consolidation doit être prudente et inspectable. Opérations sensibles avec dry-run obligatoire : promotion, rétractation, supersession, fusion, condensation, card replacement.

## 7.6 Cards and summaries

Les cards sont des vues compactes, pas des sources de vérité. Les summaries sont des couches dérivées rattachées à des fenêtres, sources ou scopes vérifiables.

## 7.7 External inspiration decision

Les idées de `hermes-local-memory` sont retenues pour la doctrine mémoire : raw history protégée, facts candidats, cards compactes, contexte inspectable, dry-run, consolidation explicite.

`mage0535/hermes-memory-installer` est ajouté en veille ciblée. À retenir : installation mémoire locale rapide, architecture mémoire en tiers, injection mémoire, auto-mount de skills et archivage local. À ne pas reprendre tel quel : SQLite FTS5 comme source de vérité principale, installation intrusive non auditée, promotion mémoire non validée, court-circuit des modèles mémoire Pantheon. Décision : utile comme référence d’expérience d’installation mémoire locale, à intégrer plus tard dans la doctrine Installer UI + Memory, après stabilisation Approval Gate, PolicyGate et modèle mémoire multi-couches.

À ne pas reprendre : remplacement de PostgreSQL/pgvector par SQLite, suppression du runtime FastAPI, suppression des workers ou copie mécanique de l’architecture externe.

---

# 8. Documentation Strategy

Le système doit minimiser le contexte de démarrage.

Auto-loaded nucleus : `AGENTS.md`, `ARCHITECTURE.md`, éventuellement un fichier opérationnel léger.

Non auto-loaded par défaut : archives, learnings détaillés, runs, sessions, anciens historiques.

---

# 9. Implementation Phases

## Phase A — MVP Foundation

Objectif : boucle contrôlée end-to-end.

Tâches : FastAPI skeleton, PostgreSQL + pgvector, JWT/RBAC, manifests, base contracts, SessionState, RunState, workflow minimal, agent minimal, tool behind policy gate, route OpenWebUI, SSE, ingestion document simple, retrieval cité, run logging.

Succès : API boot, manifests validés, workflow E2E, streaming, ingestion + citation.

## Phase B — Controlled Orchestration

Objectif : séparer décision et exécution.

Tâches : DecisionContext, DecisionAction, DecisionPlan, DecisionEngine, control/data split, DAG workflow, criticity, HITL checkpoints, veto nodes, conflict resolution.

Succès : plan avant exécution, criticity modifie le runtime, pause/resume, veto visibles.

## Phase C — Context, Memory, and Efficiency

Objectif : réduire contexte inutile et préserver continuité.

Tâches : formaliser memory layers, externaliser raw outputs, retrieve relevant state, checkpoints, smart_read, smart_diff, smart_grep, cache, analytics, recovery after compaction/crash, post-run consolidation, candidate scoring, lean-memory checks, context preview.

Succès : moins de raw context injecté, continuité robuste, reads moins coûteux, métriques visibles, candidate promotion sélective, hot memory compacte.

## Phase D — Policy, Security, Approval, and Governance

Objectif : rendre les actions risquées gouvernables, auditables et stoppables.

Tâches :

- PolicyEngine ;
- ActionGate ;
- modèle `ApprovalRequest` ;
- statuts `pending / approved / rejected / expired / escalated / cancelled` ;
- assignee personne / équipe ;
- decision note ;
- approval API ;
- pause/resume workflow ;
- expiration automatique ;
- escalation ;
- audit log ;
- secret isolation ;
- lineage source → tool → agent → output ;
- veto severity ;
- explicit decision debt.

Succès : aucune action risquée ne s’exécute silencieusement, chaque approval est traçable, un workflow peut être suspendu puis repris, une action expirée ne s’exécute pas.

## Phase E — Evaluation and Deliberation

Objectif : mesurer la qualité et réduire la fausse confiance.

Tâches : EvaluationRunner, scorecards, workflow comparison, metrics, Hera scoring, Metis artifacts, Prometheus checks, Apollo enrichment.

Succès : workflows benchmarkables, weak claims rejetables, supervision explicite.

## Phase F — Structured Skills and Workflow Packs

Objectif : transformer les patterns répétés en blocs versionnés.

Tâches : SkillRegistry, manifests, versions, states draft/candidate/active/archived, diff, rollback, promotion, workflow CRUD, console visibility.

Succès : skills testées en isolation, workflows promus/rollback, versions actives connues.

## Phase G — Document Intelligence and Knowledge Layer

Objectif : couche documentaire forte, citée, multimodale.

Tâches : PDF/DOCX/MD/TXT, metadata, hybrid retrieval, citations fiables, synthesis cache, markdown indexing, images/plans/photos plus tard.

Succès : citations page/section, retrieval hybride robuste, synthèses réutilisables.

## Phase H — Architecture Overlay

Objectif : valeur architecture / chantier sans polluer le core.

Sous-modules : decisions, planning, chantier, finance, communications, webhooks, Vitruve.

Succès : overlay activable sans toucher core, skills métier visibles, flux chantier/planning/décision cohérents.

## Phase I — Observability and Console

Objectif : rendre Pantheon inspectable et contrôlable.

Tâches : prompt traces, decision traces, tool traces, scores, feedback, blocked actions, approvals view, workflow UI, run state, metrics, toggles, logs, replay, browser action traces.

Succès : opérateurs comprennent pourquoi un run a produit un résultat, avec quel contexte, quelles approvals et quelles preuves d’action.

## Phase J — Governed Browser Tool

Objectif : ajouter une capacité navigateur gouvernée pour consultation, extraction, test et interaction web contrôlée.

Tâches :

- tool browser minimal ;
- sandbox ou remote browser ;
- screenshot before/after ;
- action trace ;
- policy gate ;
- approval gate pour effets de bord ;
- HTTP direct fallback ;
- domain browser skills ;
- tests de non-régression sur sites simples ;
- blocage login / paiement / publication sans approval.

Succès : extraction web reproductible, actions traçables, aucun effet de bord sans validation, preuves visuelles disponibles dans la console.

## Phase K — Controlled Learning

Objectif : améliorer sans mutation silencieuse.

Tâches : FeedbackEvent, LearningEngine, GapAnalyzer, candidate workflow generation, human approval, pattern promotion to MNEMOSYNE, proposals for wiki/templates/skills.

Succès : feedback négatif produit des améliorations candidates, pas des mutations automatiques.

## Phase L — Software / Code Branch

Objectif : spécialisation software isolée.

Tâches : minimal_code_context, change_impact_analysis, architecture_map, review workflows, debug workflows, repo onboarding, pre-merge checks.

## Phase M — Durable Execution and Portability

Objectif : longs runs, reprise et migration.

Tâches : checkpoints, retries, replay runner, memory export/import, workflow bundles, server migration, durable orchestration si justifiée.

---

# 10. External Inspiration Map

## À intégrer maintenant

- agentsmd/agents.md : modèle de fichier agent-facing.
- Hermes Skills system : skills documentées, catégorisées, activables.
- mnfst/manifest : manifests déclaratifs.
- nadimtuhin/claude-token-optimizer : contexte de démarrage minimal.
- hermes-local-memory : doctrine mémoire auditable, context preview, candidate facts, cards compactes, dry-runs.
- suryamr2002/langgraph-approval-hub : modèle Approval Gate, statuts d’approbation, audit log, pending queue, expiration, escalation.
- browser-use/browser-harness : screenshots before/after, browser action traces, domain browser skills, HTTP direct fallback.

## À intégrer plus tard

- mksglu/context-mode : externalisation de contexte.
- ooples/token-optimizer-mcp : smart reads et cache.
- JuliusBrussee/cavekit : spec-first execution.
- nexus9888/hermes-memory-skills : consolidation mémoire et hygiene.
- mage0535/hermes-memory-installer : expérience d’installation mémoire locale, injection mémoire, auto skill mounting et archivage ; à étudier après stabilisation du modèle mémoire Pantheon.
- remote browser sandboxing si le besoin d’automatisation web devient réel.

## Intéressant mais non prioritaire

- Honcho import patterns.
- SQLite local-first memory, uniquement comme référence de simplicité locale.
- Browser domain skills publics, à adapter uniquement après stabilisation du Browser Tool.

## À rejeter pour Pantheon OS

- remplacement de PostgreSQL/pgvector par SQLite ;
- suppression de FastAPI comme runtime ;
- worker mémoire opaque ;
- promotion automatique massive de mémoire importée ;
- copie mécanique d’une architecture externe ;
- dépendance directe à un dashboard Vercel/Supabase pour les approvals ;
- agent libre sur le Chrome personnel par défaut ;
- auto-modification de helpers pendant un run ;
- actions web sans Approval Gate.

---

# 11. Repo Governance

Branches recommandées :

- `main` : stable ;
- `develop` : intégration ;
- `experiment/*` : explorations ;
- `overlay/*` : overlays métier.

Règles :

- toute migration schema est versionnée ;
- toute brique critique a des tests ;
- toute exploration V3 reste isolée ;
- les Markdown de référence pilotent le code ;
- si le code est techniquement meilleur que la documentation, proposer d’abord une mise à jour documentaire.

---

# 12. Immediate Priorities

1. Auditer le code contre `README.md`, `ARCHITECTURE.md`, `MODULES.md`, `AGENTS.md`, `ROADMAP.md`, `STATUS.md`.
2. Vérifier l’état réel de la mémoire : raw history, candidate facts, active facts, cards, summaries, traces.
3. Finaliser ou cadrer le module `decisions`.
4. Compléter la refonte mémoire : scopes, candidate facts, active facts, context preview, dry-run consolidation.
5. Ajouter ou vérifier Approval Gate / HITL pour actions sensibles.
6. Compléter tests mémoire, approvals, orchestration et workflows C1-C5.
7. Renforcer observability et console : approvals, contexte injecté, traces d’action.
8. Préparer webhooks.
9. Préparer retrieval multimodal.
10. Reporter le Browser Tool après PolicyEngine, Approval Gate et Observability.
11. Instrumenter pour DSPy plus tard.

---

# 13. Final Target

Pantheon OS doit devenir un environnement d’exécution où agents restent remplaçables, workflows versionnés, skills réutilisables, tools gouvernés, mémoire structurée, approvals traçables, évaluation active, validation humaine présente quand le risque l’exige, overlays porteurs de valeur métier et core mince, portable, générique.
