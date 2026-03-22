# OS Projet

> L'intelligence opérationnelle d'une agence d'architecture, du premier crayon à la levée des réserves.

---

## Ce qu'OS Projet apporte

**OS Projet est le système de mémoire et d'intelligence conçu pour les agences MOE.**

Il enregistre ce que vous faites déjà, le comprend, le relie, et le rend accessible à tout moment par une simple question en langage naturel. Chaque acte de travail — poser une question technique, tenir une réunion, déposer un calcul, noter une observation de chantier — alimente automatiquement la mémoire du projet et de l'agence.

L'IA répond en s'appuyant exclusivement sur trois bases de connaissance validées et maîtrisées par l'agence :

```
┌─────────────────────────────────────────────────────────────────┐
│  BASE GÉNÉRALE — Connaissance normative & réglementaire         │
│  DTU, Eurocodes, RT/RE2020, NF, avis techniques CSTB,          │
│  fiches fournisseurs — vérifiés, versionnés                     │
├─────────────────────────────────────────────────────────────────┤
│  BASE PROJET — Documents propres à l'affaire                    │
│  PLU de la commune, programme, études de sol, diagnostics,      │
│  règlements spécifiques, pièces contractuelles                  │
├─────────────────────────────────────────────────────────────────┤
│  BASE AGENCE — Mémoire capitalisée de l'agence                  │
│  Notes de calculs, solutions retenues, produits qualifiés,      │
│  détails constructifs éprouvés                                  │
└─────────────────────────────────────────────────────────────────┘
```

L'IA travaille exclusivement sur ces sources vérifiées. La puissance de raisonnement des meilleurs modèles — déduction, induction, synthèse — est pleinement exploitée, sur des données que l'agence maîtrise et valide.

**Résultat : une réponse chirurgicale, sourcée, applicable au contexte réel du projet.**

---

## Ce que ça change concrètement

| Avant | Avec OS Projet |
|-------|----------------|
| Rechercher un email envoyé il y a 6 mois | "Retrouve la réponse de Bâti+ sur le recalage de planning" → 3 secondes |
| Chercher sur Google une réponse DTU | La réponse vient de la base normative vérifiée — avec la référence exacte |
| CR de réunion jamais à jour | L'agent extrait les décisions et alimente automatiquement le planning |
| Le savoir-faire repose sur les personnes | Il est capitalisé dans la base agence, persistante et interrogeable |

---

## Phases couvertes

```
Faisabilité → ESQ → APS → APD → PRO → DCE → ACT → EXE → OPR/AOR → GPA
```

---

## Stack technique

| Composant | Choix |
|-----------|-------|
| API | FastAPI + Python |
| Base de données | PostgreSQL + pgvector |
| Stockage fichiers | MinIO (S3-compatible, self-hosted) |
| IA | Ollama (local) ou OpenAI (cloud) — switchable via `.env` |
| Interface | OpenWebUI + OpenClaw PWA (terrain) |
| Auth | JWT HS256 — 4 rôles : admin / moe / collaborateur / lecteur |
| Déploiement | Docker Compose — local ou serveur privé (OVH) |

Données souveraines. Zéro cloud obligatoire.

---

## Roadmap

| Phase | Nom | Périmètre |
|-------|-----|-----------|
| **v0** | **Fondation** | Socle — auth, 3 bases RAG, upload docs, multi-projet, OpenClaw PWA |
| **v1** | **Mémoire** | Journal chantier, meeting → CR auto, capitalisation BASE AGENCE, alertes SMTP |
| **v2** | **Pilote** | Planning + impacts cascade, finance/situations, génération docs, Notion/Slack |
| **v3** | **Agents** | Agents proactifs — risques, anomalies, suggestions automatiques |
| **v4** | **Plateforme** | Portail client MOA (lecteur), multi-tenant, API publique |

---

## Documentation technique

| Fichier | Contenu |
|---------|---------|
| [`DEVPLAN.md`](./DEVPLAN.md) | Référence complète de développement — modules, BDD, API, agents |
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Flux de données, formats inter-modules, modularité |
| [`INSTALL.md`](./INSTALL.md) | Installation, configuration, maintenance, production |
