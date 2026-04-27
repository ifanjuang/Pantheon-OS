# Pantheon OS

Pantheon OS est un système pour structurer, sécuriser et industrialiser l’usage des agents IA.

Il ne remplace pas les modèles. Il organise leur utilisation.

---

# Principe

```text
Pantheon définit.
Hermes exécute.
OpenWebUI expose et retrouve.
```

Pantheon OS est un Domain Operating Layer. Il définit les agents, les domaines, les skills, les workflows, les mémoires, les policies et les règles d’évolution. L’exécution est déléguée à Hermes Agent. L’interface et les documents sont portés par OpenWebUI.

---

# Pourquoi

Les outils IA deviennent vite instables quand tout est mélangé : prompt, mémoire, règles, actions, documents et décisions.

Pantheon impose une séparation claire :

```text
agents      = raisonnement
skills      = capacités
workflows   = méthode
domains     = spécialisation
memory      = connaissance validée
knowledge   = sources documentaires
policies    = règles transversales
```

---

# Architecture simple

```text
OpenWebUI
  interface + knowledge documentaire

Pantheon OS
  agents abstraits
  domain packages
  skills
  workflows
  memory
  policies

Hermes Agent
  exécution
  tools
  scheduler
  gateway
  mémoire opérationnelle
```

---

# Domain packages

Les capacités métier sont regroupées par domaine.

```text
domains/
  general/
  architecture/
  software/
```

Chaque domaine suit la même structure :

```text
domains/{domain}/
  domain.md
  skills/
  workflows/
  templates/
```

`general` contient les capacités invariantes : vérification de sources, triage de changement, création de skills/workflows, memory promotion, prompt system design, analyse de repos externes, communication générale.

Les domaines métier contiennent les capacités spécialisées. Par exemple, `architecture` contient les skills et workflows liés aux CCTP, devis, DPGF, notices, chantier, PLU, ERP/SDIS et responsabilités.

---

# Mémoire

Pantheon distingue quatre niveaux :

```text
session     = contexte temporaire
candidates  = propositions non validées
project     = contexte projet validé
system      = règles, méthodes et patterns validés
```

Cycle :

```text
SESSION → CANDIDATES → validation → PROJECT ou SYSTEM
```

Aucune mémoire n’est promue automatiquement.

---

# Création à la volée

Si une skill ou un workflow n’existe pas, Pantheon ne bricole pas directement.

Il doit :

1. vérifier l’existant ;
2. vérifier le nom proposé ;
3. chercher les capacités proches ;
4. proposer une capacité candidate ;
5. attendre validation ;
6. créer les fichiers seulement après accord.

Les propositions passent par `domains/general`.

---

# Évolution des skills

Une skill n’est jamais modifiée directement après un bon résultat.

Règle :

```text
résultat utile → UPDATES.md → review → optimisation → validation → level éventuel
```

Chaque skill peut contenir :

```text
SKILL.md
manifest.yaml
examples.md
tests.md
UPDATES.md
```

L’XP est accordée uniquement si une amélioration réelle, un blocage détecté ou une remédiation utile est formalisée. L’XP ne déclenche pas automatiquement un changement de level.

---

# Confidentialité

Privacy by default.

Les documents Pantheon ne doivent jamais contenir d’informations issues de conversations privées, de projets réels, de clients, d’entreprises, de chantiers, d’adresses ou de situations identifiables.

Les exemples doivent être fictifs, neutres et non traçables.

---

# Statut

Pantheon OS est en cours de structuration.

La documentation est la source de vérité. Le code implémente cette structure, pas l’inverse.
