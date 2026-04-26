# Pantheon OS — Architecture

> Document de référence.
> Pantheon OS adopte une trajectoire Hermes-backed : Pantheon définit la couche métier et la gouvernance, Hermes Agent exécute, OpenWebUI expose l’interface et les knowledge bases.

---

# 1. Décision architecturale

Pantheon OS n’est plus prioritairement conçu comme un runtime agentique autonome complet.

La trajectoire retenue est :

```text
OpenWebUI = interface chat + knowledge documentaire
Hermes Agent = runtime agentique + skills exécutables + tools + scheduler + gateway + mémoire opérationnelle
Pantheon OS = Domain Operating Layer + agents abstraits + workflows + skills contracts + mémoire validée + gouvernance
```

Formule de conception :

```text
Pantheon définit.
Hermes exécute.
OpenWebUI expose et retrouve.
```

Cette décision réduit les chantiers redondants : scheduler maison, gateway maison, terminal backend maison, runtime de skills maison, runtime agentique complet maison.

---

# 2. Vue d’ensemble

```text
Utilisateur
  ↓
OpenWebUI
  - chat
  - knowledge collections
  - RAG documentaire simple
  ↓
Hermes Agent
  - runtime agentique
  - skills exécutables
  - tools et toolsets
  - scheduler / cron
  - doctor / setup
  - gateways éventuelles
  - mémoire opérationnelle
  ↓
Pantheon OS
  - agents abstraits
  - domain overlays
  - workflows métier
  - skills contracts
  - knowledge policy
  - memory promotion rules
  - approval rules
  - documentation source de vérité
```

Pantheon reste le référentiel de gouvernance. Hermes ne redéfinit pas les agents, les règles ou les workflows officiels. OpenWebUI ne devient pas source de vérité des agents ou de la mémoire validée.

---

# 3. Domain Operating Layer

Un Domain Operating Layer est une couche contractuelle qui spécialise un runtime agentique généraliste pour un domaine professionnel.

Pantheon contient :

- les rôles cognitifs génériques ;
- les règles de gouvernance ;
- les overlays métier ;
- les workflows ;
- les définitions de skills ;
- les règles de mémoire ;
- les règles d’approbation ;
- les politiques de sources ;
- les formats de sortie ;
- la mémoire projet et agence validée.

Pantheon ne doit pas devenir un simple dossier de prompts. Chaque capacité importante doit être décrite par contrat lisible et versionnable.

---

# 4. Couches du système

## 4.1 OpenWebUI

Responsabilités :

- interface chat ;
- knowledge collections ;
- RAG documentaire simple ;
- accès utilisateur aux modèles ;
- consultation de corpus lourds : PDF, DOCX, Markdown, modèles, guides, références.

Ne doit pas porter :

- les agents officiels ;
- la mémoire projet validée ;
- les règles d’approbation ;
- les workflows de référence ;
- les skills critiques.

## 4.2 Hermes Agent

Responsabilités :

- exécuter les tâches ;
- charger et appliquer les skills ;
- utiliser tools et terminal backends autorisés ;
- gérer mémoire opérationnelle ;
- proposer des skills candidates ;
- scheduler des routines ;
- diagnostiquer l’environnement ;
- servir éventuellement de gateway Telegram, Discord, Slack, WhatsApp ou Signal.

Ne doit pas :

- promouvoir seul une mémoire durable comme vérité Pantheon ;
- modifier les règles Pantheon sans validation ;
- activer automatiquement une skill candidate ;
- accéder aux volumes ou secrets Pantheon sans politique explicite ;
- devenir un runtime concurrent non gouverné.

## 4.3 Pantheon OS

Responsabilités :

- définir les agents abstraits ;
- définir les domain overlays ;
- définir les workflows métier ;
- définir les skills contracts ;
- définir les policies ;
- définir la stratégie OpenWebUI Knowledge ;
- valider la mémoire projet et agence ;
- coordonner ChatGPT, Claude, Hermes et humains via `AI_LOG.md` ;
- suivre les références externes via `EXTERNAL_WATCHLIST.md`.

---

# 5. Agents abstraits

Les agents Pantheon sont neutres métier. Ils représentent des fonctions cognitives génériques.

Exemples :

- ZEUS : orchestration, arbitrage, routing ;
- ATHENA : planification, décomposition, stratégie ;
- ARGOS : extraction factuelle, preuves, contradictions ;
- THEMIS : conformité, procédure, légitimité, approval ;
- APOLLO : validation finale, confiance, qualité ;
- PROMETHEUS : contradiction, stress-test, anti-consensus ;
- HESTIA : mémoire projet ;
- MNEMOSYNE : mémoire agence et patterns ;
- IRIS : communication ;
- HEPHAESTUS : analyse technique.

Le métier n’est pas codé dans les agents. Le métier est injecté par domain overlay, workflow, skill et knowledge policy.

---

# 6. Domain overlays

Les domaines portent la spécialisation.

```text
domains/
  architecture/
    overlay.md
    rules.md
    knowledge_policy.md
    output_formats.md
    workflows/
    skills/
    templates/
  software/
  legal/
  consulting/
```

Un overlay peut définir :

- règles métier ;
- sources fiables ;
- workflows ;
- skills spécialisées ;
- templates ;
- formats de sortie ;
- exemples ;
- tests ;
- règles de validation.

Exemple : THEMIS reste abstrait. Dans `domains/architecture`, THEMIS vérifie mission, contrat, DOE, DGD, réception, CCTP, DPGF, ERP, SDIS, PLU ou responsabilité selon les règles du domaine.

---

# 7. Skills contracts

Pantheon définit les skills. Hermes les exécute.

Une skill Pantheon doit définir :

- objectif ;
- inputs ;
- outputs ;
- agents mobilisés ;
- sources autorisées ;
- risques ;
- approval requis ;
- format attendu ;
- exemples ;
- tests ;
- état : draft, candidate, active, archived.

Structure cible :

```text
skills/
  generic/
  architecture/
    cctp_audit/
      SKILL.md
      manifest.yaml
      examples.md
      tests.md
  software/
```

Une skill créée automatiquement par Hermes reste candidate. Elle ne devient active qu’après validation dans Pantheon.

---

# 8. Workflows

Les workflows décrivent les séquences de travail. Ils sont définis dans Pantheon et peuvent être exécutés par Hermes comme procédure.

```text
workflows/
  generic/
  architecture/
  software/
```

Un workflow doit définir :

- id ;
- domaine ;
- agents mobilisés ;
- steps ;
- inputs ;
- outputs ;
- points de validation ;
- risques ;
- fallback ;
- mémoire cible.

LangGraph reste une option ultérieure pour exécuter formellement des workflows complexes. Il n’est pas la priorité tant que Hermes peut exécuter les procédures avec contexte Pantheon.

---

# 9. Knowledge layer

OpenWebUI peut porter les knowledge collections. Pantheon définit la politique.

```text
knowledge/
  openwebui_collections.md
  source_policy.md
  document_taxonomy.md
```

Règles :

- documents lourds dans OpenWebUI Knowledge ;
- décisions, règles et statuts dans Pantheon ;
- aucune collection OpenWebUI ne remplace les Markdown de référence ;
- les sources obsolètes doivent être marquées ;
- les sources projet doivent être séparées des sources agence ;
- les sources réglementaires doivent être distinguées des modèles internes.

---

# 10. Memory model

La mémoire est séparée.

| Type | Emplacement | Statut |
|---|---|---|
| Mémoire documentaire | OpenWebUI Knowledge | consultable |
| Mémoire opérationnelle | Hermes Agent | vivante, pratique, non souveraine |
| Mémoire validée | Pantheon OS | source de vérité |

Structure cible Pantheon :

```text
memory/
  project/
    facts.md
    decisions.md
    risks.md
  agency/
    patterns.md
    clauses.md
    preferences.md
  candidates/
    pending_facts.md
    pending_skills.md
    pending_rules.md
```

Règle :

```text
Hermes peut apprendre.
Pantheon valide.
OpenWebUI documente.
```

Toute promotion mémoire doit être traçable. Une mémoire opérationnelle Hermes ne devient pas automatiquement vérité Pantheon.

---

# 11. Approval discipline

Le système démarre avec une discipline documentaire et opératoire. Un module logiciel d’Approval Gate peut rester utile plus tard si le besoin l’exige.

Règles minimales :

- diagnostic : autorisé ;
- modification de fichier : validation requise ;
- envoi email : validation requise ;
- suppression : confirmation explicite ;
- commande shell hors allowlist : validation requise ;
- promotion mémoire : validation requise ;
- activation skill candidate : validation requise ;
- action web à effet de bord : validation requise ;
- accès secrets / volumes / Docker socket : interdit sans politique explicite.

---

# 12. Hermes Integration Layer

Pantheon doit fournir à Hermes des contextes contrôlés.

```text
hermes/
  context/
    pantheon_context.md
    agents_context.md
    rules_context.md
    domain_architecture.md
  exports/
    skills/
    prompts/
    workflows/
```

Objectifs :

- permettre à Hermes de charger les rôles Pantheon ;
- exposer les règles de validation ;
- exporter les skills candidates ou actives ;
- éviter la redéfinition divergente des agents ;
- garder Pantheon comme référence officielle.

---

# 13. Exploitation NAS

Pantheon doit tenir compte d’un environnement existant : Portainer, OpenWebUI, PostgreSQL, Ollama sur PC LAN.

Règles :

- ne jamais écraser une stack existante ;
- détecter avant d’installer ;
- générer `.env` sans écraser ;
- proposer un dry-run ;
- ne pas réutiliser automatiquement un volume existant ;
- garder OpenWebUI existant si présent ;
- isoler Hermes Lab avant intégration ;
- ne pas exposer inutilement PostgreSQL ;
- ne pas utiliser de tags Docker instables en production.

---

# 14. Code existant

Le dépôt contient encore des éléments de l’ancienne architecture autonome : FastAPI, registries, workflows, approvals, Installer UI, manifests, tests.

Ces éléments sont désormais à classer :

- à conserver comme outils d’intégration ;
- à simplifier ;
- à archiver ;
- à réorienter vers Hermes-backed Pantheon ;
- à supprimer si redondants après validation documentaire.

Aucune suppression automatique n’est décidée par ce fichier. Un audit post-pivot doit précéder toute modification du code.

---

# 15. Contraintes de conception

- pas de second runtime de vérité ;
- pas d’agents métier figés dans le core ;
- pas de skill active sans contrat ;
- pas de mémoire validée sans source ;
- pas de modification sensible sans validation ;
- pas d’installation Hermes globale non isolée ;
- pas de duplication inutile des fonctions Hermes ;
- pas de knowledge OpenWebUI qui remplace les Markdown ;
- pas de workflow caché dans un prompt.

---

# 16. Résultat cible

Pantheon OS devient une couche contractuelle métier, portable et maintenable, qui spécialise Hermes Agent et OpenWebUI pour produire un assistant professionnel gouverné.

La valeur de Pantheon n’est plus de reconstruire tout le runtime. Sa valeur est de définir une méthode, des rôles, des règles, des skills et une mémoire fiable pour l’agence.
