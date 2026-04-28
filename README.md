# Pantheon OS

Pantheon OS est une couche de gouvernance pour structurer, sécuriser et industrialiser l’usage des agents IA.

Il ne remplace pas les modèles. Il organise leur utilisation.

---

# Principe

```text
Pantheon définit.
Hermes exécute.
OpenWebUI expose et retrouve.
```

Pantheon OS est un Domain Operating Layer. Il définit les agents, les domaines, les skills, les workflows, les mémoires et les règles d’évolution. L’exécution est déléguée à Hermes Agent. L’interface et la knowledge documentaire restent portées par OpenWebUI.

---

# Domain packages

Les capacités sont regroupées par domaine.

```text
domains/
  general/
  architecture_fr/
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

`general` contient les capacités invariantes : triage, vérification de sources, création de skills/workflows, contrôle Hermes, memory promotion, prompt system design.

`architecture_fr` contient les capacités métier francophones : CCTP, devis, DPGF, notices, chantier, PLU, ERP/SDIS, responsabilités et marchés travaux.

---

# Skills et workflows

Une skill décrit une capacité réutilisable.

Un workflow décrit une procédure structurée.

Pantheon ne crée pas directement une nouvelle capacité. Il vérifie d’abord :

1. les skills Pantheon existantes ;
2. les workflows Pantheon existants ;
3. les skills Hermes built-in ou optional ;
4. les noms proches ;
5. les risques et validations.

Toute nouvelle capacité commence en `candidate`.

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
SESSION → CANDIDATES → REVIEW → PROJECT ou SYSTEM
```

Aucune mémoire n’est promue automatiquement.

---

# Confidentialité

Privacy by default.

Les documents Pantheon ne doivent jamais contenir d’informations issues de conversations privées, projets réels, clients, entreprises, chantiers, adresses ou situations identifiables.

Les exemples doivent être fictifs, neutres et non traçables.

---

# Évolution des skills

Chaque skill peut contenir :

```text
SKILL.md
manifest.yaml
examples.md
tests.md
UPDATES.md
```

Règle :

```text
résultat utile → UPDATES.md → review → optimisation → validation → SKILL.md
```

XP possible uniquement si une amélioration réelle, un blocage détecté ou une remédiation utile est formalisée.

Pas d’auto-upgrade. Pas d’auto-level.

---

# État

Pantheon OS est en cours de structuration.

La documentation est la source de vérité. Le code implémente cette structure, pas l’inverse.
