# Pantheon OS — Modules

## Overview

Pantheon OS est construit à partir de blocs runtime modulaires.

Le système distingue :

- core runtime logic ;
- reusable runtime modules ;
- domain overlays ;
- platform and infrastructure.

Un module n’est pas seulement un dossier. Un module est une unité runtime avec une identité, un contrat, un manifest, un cycle de vie, des dépendances explicites et une activation contrôlée.

---

# 1. Module Philosophy

## 1.1 Modular by default

Tout ce qui peut varier, évoluer ou être remplacé doit rester hors du core : agents, skills, tools, workflows, prompts, templates.

Le core fournit exécution, gouvernance, contrats, états et registries. Les modules fournissent le comportement.

## 1.2 Filesystem as source of truth

Un module doit être découvrable depuis le filesystem. Ajouter un module doit principalement signifier ajouter un dossier, un manifest et une implémentation conforme au contrat.

## 1.3 Core and modules separation

Le core ne doit pas absorber de logique métier. Les modules ne doivent pas réimplémenter la gouvernance core.

Limite :

- le core définit comment l’exécution fonctionne ;
- les modules définissent ce qui est exécuté.

## 1.4 Explicit modules

Chaque module déclare ce qu’il est, ce qu’il dépend, ce qu’il produit, quand il doit être utilisé et quand il ne doit pas l’être.

---

# 2. Main Module Families

## 2.1 Agents

Les agents sont des unités de raisonnement. Ils interprètent, structurent, produisent des sorties, appellent skills et tools via le runtime, et participent aux workflows.

## 2.2 Skills

Les skills sont des capacités cognitives réutilisables. Elles encapsulent un travail répétable, borné, testable et sans effet de bord direct.

## 2.3 Tools

Les tools sont des interfaces techniques ou externes : fetch, read, transform, call service, write output, bounded actions. Ils doivent rester étroits, explicites et gouvernés.

## 2.4 Workflows

Les workflows structurent l’exécution : séquence, dépendances, patterns, checkpoints, validations et fallbacks.

## 2.5 Prompts

Les prompts cadrent les comportements, mais ne remplacent pas la logique runtime.

## 2.6 Templates

Les templates définissent des structures d’outputs réutilisables et versionnables.

## 2.7 Memory modules

Les modules mémoire gèrent la continuité, la capitalisation, les faits, les résumés, les cartes compactes, les traces et l’inspection du contexte injecté.

Ils ne décident pas seuls de la vérité métier. Ils stockent, exposent, relient, proposent, prévisualisent et appliquent les écritures mémoire validées.

## 2.8 Approval modules

Les modules d’approbation gèrent les demandes de validation humaine avant exécution d’actions sensibles.

Ils ne décident pas à la place de l’humain. Ils bloquent, tracent, notifient, expirent, escaladent et permettent la reprise ou l’abandon du workflow.

## 2.9 Browser modules

Les modules navigateur permettent la consultation, l’extraction, les tests de rendu et certaines interactions web contrôlées.

Ils ne doivent jamais devenir une capacité libre d’action web. Toute action à effet de bord doit passer par policy, approval et trace.

---

# 3. Repository Structure

```text
modules/
  agents/
  skills/
  tools/
  workflows/
  prompts/
  templates/

core/
  contracts/
  registry/
  decision/
  execution/
  state/
  policies/
  evaluation/
  learning/
  observability/
  memory/
  documents/
  llm/

domains/
  architecture/
  legal/
  software/
  consulting/

platform/
  api/
  ui/
  data/
  infra/
```

---

# 4. Module Discovery

Les modules sont découverts par manifests.

Répertoires typiques :

- `modules/agents/`
- `modules/skills/`
- `modules/tools/`
- `modules/workflows/`
- `domains/*/agents/`
- `domains/*/skills/`
- `domains/*/workflows/`

Un module est loadable si le dossier existe, le manifest est valide, les fichiers requis existent et les contrats passent la validation.

Les registries sont des index runtime, pas la source de vérité. La source de vérité reste filesystem + manifest.

---

# 5. Manifest Model

Champs recommandés :

- `id`
- `name`
- `type`
- `version`
- `description`
- `enabled`
- `layer`
- `domain`
- `inputs`
- `outputs`
- `dependencies`
- `constraints`
- `policy`
- `activation`
- `tags`

Les manifests doivent rester légers, explicites et lisibles par machine.

---

# 6. Module Contracts by Type

## 6.1 Agent contract

Un agent déclare rôle, responsabilités, limites, activation, inputs, outputs, veto éventuel et criticity triggers.

Structure habituelle :

```text
agent.py
manifest.yaml
SOUL.md
tests/
```

## 6.2 Skill contract

Une skill déclare scope, inputs, outputs, conditions d’usage, conditions d’évitement et failure modes.

Structure habituelle :

```text
skill.py
manifest.yaml
SKILL.md
tests/
```

## 6.3 Tool contract

Un tool déclare ce qu’il fait, quand l’utiliser, quand ne pas l’utiliser, son profil d’effet de bord, ses policy requirements et ses failure modes.

Structure habituelle :

```text
tool.py
manifest.yaml
README.md
tests/
```

## 6.4 Workflow contract

Un workflow déclare graphe ou séquence, agents, dépendances, pattern d’exécution, checkpoints, validations et fallback rules.

Structure habituelle :

```text
workflow.py
manifest.yaml
workflow.yaml
tests/
```

## 6.5 Prompt contract

Un prompt déclare scope, module cible, domaine applicable, contraintes et profil d’instruction.

## 6.6 Template contract

Un template déclare type d’artefact, sections attendues, variables, domaine éventuel et contraintes de sortie.

## 6.7 Memory contract

Un module mémoire doit déclarer :

- le type de mémoire concerné : session, project, agency, functional, raw, knowledge ;
- les objets manipulés : raw events, messages, facts, candidate facts, summaries, cards, traces ;
- les sources acceptées ;
- les règles de promotion ;
- les règles de rétractation ou supersession ;
- les modes preview / dry-run ;
- les outputs injectables dans le contexte ;
- les agents autorisés à valider ou arbitrer.

Un module mémoire ne doit pas promouvoir massivement des données sans scoring, source et validation.

## 6.8 Approval contract

Un module Approval doit déclarer :

- les types d’actions soumis à validation ;
- le modèle `ApprovalRequest` ;
- les statuts autorisés ;
- les règles d’expiration ;
- les règles d’escalade ;
- les assignees personne / équipe ;
- les outputs de décision ;
- l’audit log ;
- les conditions de reprise ou d’abandon de workflow.

Statuts minimaux :

- `pending`
- `approved`
- `rejected`
- `expired`
- `escalated`
- `cancelled`

Interfaces attendues :

- `approval.create_request`
- `approval.get_status`
- `approval.list_pending`
- `approval.decide`
- `approval.escalate`
- `approval.expire`
- `approval.audit_log`

Une décision d’approbation doit être idempotente et protégée contre les doubles décisions concurrentes.

## 6.9 Browser tool contract

Un Browser Tool doit déclarer :

- les modes supportés : lecture, screenshot, extraction, interaction ;
- le type de navigateur : sandbox, remote, local explicitement autorisé ;
- les actions autorisées sans approval ;
- les actions soumises à approval ;
- les traces produites ;
- les règles de stockage des screenshots ;
- les conditions d’arrêt : login wall, captcha, paiement, compte connecté, donnée sensible.

Interfaces attendues :

- `browser.open`
- `browser.screenshot`
- `browser.page_info`
- `browser.extract`
- `browser.click`
- `browser.type`
- `browser.upload`
- `browser.http_get`
- `browser.close`
- `browser.action_trace`

Règles :

- lecture avant action ;
- screenshot avant/après toute interaction significative ;
- HTTP direct avant automatisation lourde quand possible ;
- approval obligatoire pour tout effet de bord ;
- sandbox ou remote browser privilégié ;
- interdiction de modifier les helpers runtime sans revue.

---

# 7. Memory Module Responsibilities

## 7.1 Raw history

Stocke les messages, documents, tool outputs, événements, run traces et actions. Cette couche est la base de vérification.

Elle ne doit pas être modifiée par consolidation ordinaire.

## 7.2 Candidate facts

Stocke les faits proposés par extraction, réflexion, import ou analyse. Un candidate fact n’est pas encore une mémoire fiable.

Il doit inclure source, confidence, scope, subject, observer ou affaire, et justification minimale.

## 7.3 Active facts

Stocke les faits validés, durables, utiles et sourcés.

Un active fact doit pouvoir être rétracté, supersédé ou relié à une preuve.

## 7.4 Summaries

Stocke les résumés de session, workflow, affaire, document ou fenêtre temporelle.

Un summary est une couche dérivée. Il ne remplace pas les sources brutes.

## 7.5 Cards

Stocke les cartes compactes utilisées pour l’injection rapide dans les prompts.

Une card est une vue synthétique compacte. Elle ne doit pas grossir mécaniquement avec chaque active fact.

## 7.6 Context preview

Expose le contexte qui serait injecté dans un agent ou workflow avant exécution.

Un module de preview doit montrer :

- les facts utilisés ;
- les cards utilisées ;
- les summaries utilisés ;
- les documents ou chunks cités ;
- les traces ou décisions pertinentes ;
- les éléments exclus si utile.

---

# 8. Memory Module Interfaces

Interfaces attendues à terme :

- `memory.search_active_facts`
- `memory.list_candidate_facts`
- `memory.propose_candidate_fact`
- `memory.promote_fact`
- `memory.retract_fact`
- `memory.supersede_fact`
- `memory.generate_card_preview`
- `memory.replace_card`
- `memory.context_preview`
- `memory.consolidation_dry_run`
- `memory.apply_consolidation`
- `memory.route_post_run_memory`

Ces interfaces peuvent être exposées comme services internes, endpoints API ou tools gouvernés selon le niveau de maturité.

---

# 9. Browser Domain Skills

Les browser domain skills documentent les comportements réutilisables d’un site ou d’un service web.

Elles peuvent contenir :

- selectors stables ;
- URL patterns ;
- APIs observées ;
- pièges d’interface ;
- waits spécifiques ;
- stratégies d’extraction ;
- limites de sécurité.

Elles ne doivent jamais contenir :

- secrets ;
- cookies ;
- tokens ;
- données personnelles ;
- coordonnées pixel brutes comme stratégie principale ;
- narration d’un run spécifique.

---

# 10. Domain Overlay Rules

Le comportement métier appartient aux overlays.

Exemples :

- scoring de décision architecture ;
- politiques de citation juridique ;
- blast-radius software ;
- workflows chantier ;
- templates ACT, DET, AOR.

Les modules génériques ne doivent pas supposer un domaine professionnel particulier.

---

# 11. Activation and Enablement

Un module peut être :

- enabled ;
- disabled ;
- experimental ;
- deprecated plus tard.

La présence sur disque est différente de l’activation runtime.

L’activation dépend de criticity, workflow, domaine, risque d’effet de bord, type d’output, incertitude et configuration opérateur.

---

# 12. Module Testing

Tout module critique doit être testable.

Tests attendus : unit tests de skills, tool tests et mocks, agent tests, workflow integration tests, regression tests.

Les modules mémoire doivent être testés sur :

- non-promotion du bruit ;
- conservation des sources brutes ;
- dry-run avant consolidation ;
- rétractation et supersession ;
- preview du contexte injecté ;
- absence de croissance incontrôlée des cards.

Les modules Approval doivent être testés sur :

- double décision concurrente ;
- expiration ;
- rejet ;
- escalation ;
- reprise workflow après approval ;
- blocage workflow après reject ;
- audit log complet.

Les Browser Tools doivent être testés sur :

- navigation passive ;
- screenshot before/after ;
- blocage des actions à effet de bord sans approval ;
- arrêt sur login wall ou captcha ;
- trace complète d’action ;
- non-utilisation du navigateur personnel par défaut.

---

# 13. Versioning and Lifecycle

Skills, workflows, overlays, prompts, templates et politiques doivent évoluer avec versioning explicite lorsque la stabilité du runtime l’exige.

États possibles : draft, candidate, active, archived.

Les breaking changes doivent être explicites.

---

# 14. Governance Constraints for Modules

- aucun effet de bord non gouverné ;
- aucune logique métier cachée dans core ;
- aucune mutation silencieuse ;
- aucune dépendance implicite ;
- aucune activation décorative dans les runs critiques ;
- aucune mémoire durable non sourcée ;
- aucune consolidation mémoire sans dry-run pour les opérations sensibles ;
- aucune action sensible sans Approval Gate ;
- aucune action navigateur sans trace.

---

# 15. Hermes Console Expectations

La console doit exposer pour chaque module : id, type, domaine, enabled state, version, dépendances, métriques d’usage, échecs récents, contexte d’activation.

Pour la mémoire, la console doit exposer : candidate facts, active facts, cards, summaries, contexte injecté, promotions, rétractions, consolidations et erreurs de routage.

Pour les approvals, la console doit exposer : pending approvals, assignee, criticity, action description, agent reasoning, status, decision note, expiration, escalation et audit log.

Pour le browser tool, la console doit exposer : URL, action, screenshots avant/après, approval liée, statut, erreurs et traces.

---

# 16. Naming Rules

Folder names en `snake_case`, IDs stables, machine-friendly, indépendants des expérimentations de nommage.

L’identité mythologique et le rôle doivent rester séparables.

Exemple : `zeus` comme identité, `orchestrator` comme rôle.

---

# 17. Anti-Patterns

À éviter :

- un module qui fait tout ;
- un tool qui juge juridiquement ou politiquement ;
- une skill vague ;
- un workflow caché dans un prompt ;
- de la logique domaine dans core ;
- des dépendances non déclarées ;
- des effets de bord hors policy gate ;
- une activation silencieuse d’agents décoratifs ;
- des cards mémoire append-only ;
- une promotion automatique de raw output en mémoire durable ;
- un dashboard externe séparé comme source de vérité d’approbation ;
- un agent libre sur navigateur connecté ;
- une auto-modification de helpers pendant un run.

---

# 18. Final Rule

Les modules sont le tissu d’exécution de Pantheon OS.

Un bon module est explicite, borné, testable, découvrable, remplaçable et gouvernable.

Si un module ne peut pas être compris par son manifest, son contrat et ses tests, il est trop implicite pour la production.
