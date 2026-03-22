# OS Projet

> L'intelligence opérationnelle d'une agence d'architecture, du premier crayon à la levée des réserves.

---

## Le problème

Une agence MOE produit en continu une masse critique d'information : diagnostics, notes de calculs, CCTP, courriers, comptes-rendus, situations financières, décisions de chantier. Cette information est éparpillée dans les boîtes mails, des dossiers partagés mal nommés, des tableurs sans cohérence — et dans la tête des collaborateurs.

On refait ce qui a déjà été fait. On cherche ce qu'on a pourtant déjà résolu. Et quand un collaborateur clé part, le savoir-faire part avec lui.

Les IA génératives impressionnent, mais hallucinent. Sur une question réglementaire précise, une IA sans sources vérifiées peut donner une réponse convaincante et fausse. Pour une agence MOE, c'est inacceptable.

---

## La réponse

**OS Projet est un système de mémoire et d'intelligence pour agence MOE — avec des sources verrouillées.**

Trois bases de connaissance, validées et maîtrisées par l'agence :

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

L'IA reçoit uniquement ces sources vérifiées comme contexte. Elle ne peut pas inventer ce qui ne s'y trouve pas.

**Résultat : une réponse chirurgicale, sourcée, applicable au contexte réel du projet.**

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

Voir [`DEVPLAN.md`](./DEVPLAN.md) — document de référence complet pour le développement.
