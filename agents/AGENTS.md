# AGENTS.md — Panthéon ARCEUS : hiérarchie, flux, articulations

---

## Hiérarchie

```
                          ┌─────────────────┐
                          │      ZEUS        │
                          │  Orchestrateur   │
                          │  Arbitrage C3-C5 │
                          └────────┬────────┘
                                   │ distribue / juge / synthétise
              ┌────────────────────┼───────────────────────┐
              │                    │                        │
    ┌─────────▼──────────┐         │             ┌─────────▼──────────┐
    │       HERMÈS        │         │             │       THÉMIS        │
    │  Point d'entrée     │         │             │  Veto contractuel   │
    │  Routing C1-C5      │         │             └────────────────────┘
    └─────────────────────┘         │
                                    │
    ────────────── FAMILLES ─────────────────────────────────────────
    
    PERCEPTION         ANALYSE              CADRAGE
    ──────────         ───────              ───────
    ● Hermès (P)       ● Athéna (P)         ● Thémis (P, veto)
    ○ Argos (S)        ● Héphaïstos (P,veto)○ Chronos (S)
                       ○ Prométhée (S)      ○ Arès (S)
                       ○ Apollon (S)
                       ○ Dionysos (S)

    CONTINUITÉ         COMMUNICATION        PRODUCTION
    ──────────         ─────────────        ──────────
    ● Hestia (P)       ○ Iris (S)           ● Dédale (P)
    ○ Mnémosyne (S)    ○ Aphrodite (S)
    
    ● = Primaire (sollicité systématiquement dans sa famille)
    ○ = Secondaire (sollicité selon contexte / criticité)
```

---

## Les 16 agents — rôle, rang et position

| # | Agent | Famille | Rang | Rôle | Veto | Trigger d'invocation |
|---|-------|---------|------|------|------|----------------------|
| 0 | **Zeus** | Orchestrateur | P | Planifie, distribue, arbitre, synthétise | Global | Automatique C3-C5 |
| 1 | **Hermès** | Perception | P | Point d'entrée, qualification C1-C5, routing | — | Toute demande entrante |
| 2 | **Argos** | Perception | S | Constat visuel objectif (photos, plans) | — | Photo/plan soumis |
| 3 | **Athéna** | Analyse | P | Structuration des problèmes, scénarios, décisions | — | Toute analyse C2+ |
| 4 | **Héphaïstos** | Analyse | P | Faisabilité technique, DTU, matériaux | Technique | Question technique, validation Dionysos |
| 5 | **Prométhée** | Analyse | S | Contre-analyse, biais, adversarial | — | **Systématique C4+** ; sur demande C3 |
| 6 | **Apollon** | Analyse | S | Recherche web+RAG, vérification normative, cohérence | — | Mode 1: sur demande ; **Mode 2: auto C4+** |
| 7 | **Dionysos** | Analyse | S | Pensée latérale, rupture créative | — | Blocage multi-contraintes ; exploration C4+ |
| 8 | **Thémis** | Cadrage | P | Réglementation, contrat MOE, déontologie | Contractuel | Toute décision engageante (C3+) |
| 9 | **Chronos** | Cadrage | S | Délais légaux, planning, impacts cascade | — | Impact planning détecté |
| 10 | **Arès** | Cadrage | S | Action terrain rapide, décisions réversibles C3 | — | Urgence terrain ; Chronos BLOQUANT |
| 11 | **Hestia** | Continuité | P | Mémoire projet (décisions, dettes D0-D3) | — | Injection auto chaque session ; écriture post-décision |
| 12 | **Mnémosyne** | Continuité | S | Mémoire agence (patterns, leçons cross-projets) | — | Injection auto chaque session ; écriture post-orchestration |
| 13 | **Iris** | Communication | S | Emails humains, courriers, relances | — | Post-synthèse si communication MOA requise |
| 14 | **Aphrodite** | Communication | S | Marketing, réseaux sociaux, storytelling | — | Post-projet ; jalon marketing |
| 15 | **Dédale** | Production | P | Dossiers complets (PC, DCE, DOE, marchés) | — | Post-synthèse si dossier requis |

**Rang P (Primaire)** : sollicité systématiquement quand sa famille est impliquée.
**Rang S (Secondaire)** : sollicité selon le contexte, la criticité ou sur demande explicite.

---

## Flux types

### Flux C1-C2 — Simple (sans Zeus)

```
Humain
  → Hermès (qualifie C1/C2, identifie 1-2 agents)
    → Agent(s) cible(s)
      → Réponse directe
```

Exemples : question normative (Apollon), vérification calendrier (Chronos), info projet (Hestia).

---

### Flux C3-C5 — Orchestration Zeus

```
Humain
  → Hermès (qualifie C3/C4/C5, reformule par agent)
    → Zeus : plan_agents
      → [HITL humain si C4/C5]
        → dispatch_subtasks (parallèle, cascade, arena, solo)
          → veto_check (Thémis / Héphaïstos)
            → [HITL + interruption si veto C4/C5]
              → Zeus : judge
                → [Apollon Mode 2 si C4+ : cohérence finale]
                  → synthesize (Mnémosyne par défaut)
                    → Réponse finale
                      → [Iris si comms MOA] [Dédale si dossier] [Hestia écriture]
```

---

### Flux veto

```
Thémis ou Héphaïstos émet {"veto": true, "motif": "...", "condition_levee": "..."}
  → veto_check détecte le veto
    → Si C4/C5 : interrupt() → validation humaine obligatoire
    → Si C3 : Zeus juge si on continue ou bloque
    → Veto persisté : veto_agent + veto_motif dans orchestra_runs
```

---

### Flux mémoire

```
Pré-run (injection automatique) :
  Toute session → système injecte Hestia (projet) + Mnémosyne (agence) dans le prompt

Post-orchestration (écriture) :
  Zeus / Hermès → Hestia : décisions structurées (scope='projet', affaire_id=<uuid>)
  Arès → Hestia : actions terrain immédiates (scope='projet')
  Système → Mnémosyne : leçons généralisables (scope='agence', affaire_id=NULL)

Invalidation temporelle :
  Quand un fait est dépassé → valid_until = now(), superseded_by = nouvelle leçon
  get_agent_memories() filtre automatiquement les faits invalidés
```

---

## Communications agent-à-agent

### Matrice complète des interactions

| De → Vers | Quand | Ce qui transite | Pattern |
|-----------|-------|-----------------|---------|
| **Hermès → Zeus** | Demande C3-C5 | Qualification + agents suggérés + criticité | routing |
| **Hermès → Agent direct** | Demande C1-C2 | Question reformulée avec contexte projet | solo |
| **Zeus → Agents** | Distribution | Instructions spécifiques par agent, rôle attendu | parallel/cascade |
| **Zeus → Humain** | HITL C4/C5 | Plan d'agents + motif de validation demandée | interrupt |
| **Argos → Héphaïstos** | Photo / plan soumis | Constat objectif brut → interprétation technique | cascade |
| **Héphaïstos → Argos** | Constat ambigu | Demande de clarification visuelle (angle, détail) | feedback |
| **Athéna → Prométhée** | Scénario structuré | Hypothèses → contre-analyse adversariale | cascade |
| **Athéna → Thémis** | Décision engageante | Scénario → vérification contractuelle/réglementaire | cascade |
| **Athéna → Chronos** | Scénarios avec délais | Vérification faisabilité temporelle par option | cascade |
| **Dionysos → Héphaïstos** | Option créative | Validation faisabilité technique avant intégration | cascade |
| **Dionysos → Athéna** | Option validée | Option latérale → structuration en scénario | cascade |
| **Prométhée → Apollon** | Failles logiques | Claims non vérifiés → recherche de sources | cascade |
| **Héphaïstos → Thémis** | Question DTU/AT | Faisabilité technique → validation réglementaire | cascade |
| **Apollon → tous** | Sur demande Zeus | Références normatives, extraits de documents RAG | parallel |
| **Apollon → Zeus** | Phase cohérence (C4+) | Vérification croisée contradictions entre agents | cascade |
| **Chronos → Arès** | Deadline BLOQUANT | Contrainte calendaire → action C3 terrain | cascade |
| **Chronos → Thémis** | Délai légal dépassé | Alerte BLOQUANT → veto contractuel possible | cascade |
| **Arès → Chronos** | Post-action terrain | Retour réel → recalibrage planning | feedback |
| **Arès → Hestia** | Post-action C3 | Écriture immédiate de l'action + résultat | écriture |
| **Thémis → Dédale** | Dossier requis | Contraintes contractuelles → structure du dossier | cascade |
| **Hestia → tous** | Chaque session | Mémoire projet injectée en contexte système | injection |
| **Mnémosyne → Zeus** | Orchestration C3+ | Patterns agence pertinents injectés dans le plan | injection |
| **Zeus → Iris** | Post-synthèse validée | Décision → rédaction email/courrier MOA | post-traitement |
| **Zeus → Dédale** | Post-synthèse validée | Décision → production dossier complet | post-traitement |
| **Zeus / Hermès → Hestia** | Post-décision C3+ | Décision structurée → écriture mémoire projet | écriture |

---

## Articulations clés

### Argos ↔ Héphaïstos : perception ↔ analyse technique

Argos ne cause jamais. Il décrit ce qu'il voit avec certitude géométrique.
Héphaïstos prend ce constat et l'interprète techniquement (DTU, pathologies, matériaux).
Sans Argos, Héphaïstos peut analyser sur description textuelle mais perd en précision visuelle.

**Feedback loop** : si le constat d'Argos est ambigu (photo sombre, angle insuffisant, détail manquant), Héphaïstos peut demander une clarification à Argos avant de finaliser son analyse.

### Athéna ↔ Prométhée : construction ↔ déconstruction

Athéna structure le problème et propose des scénarios.
Prométhée les attaque : hypothèses cachées, biais de confirmation, angles morts.
Le couple Athéna/Prométhée produit une analyse robuste double face.

**Règle** : pour C4+, Prométhée est systématiquement invoqué après Athéna. Son rapport est transmis à Apollon pour vérification des sources avant synthèse Zeus.

### Dionysos → Héphaïstos → Athéna : créativité → faisabilité → structuration

Dionysos propose des options latérales quand les chemins classiques sont bloqués.
Héphaïstos valide la faisabilité technique de chaque option créative.
Seules les options techniquement faisables remontent à Athéna pour intégration en scénarios.

**Trigger** : Zeus invoque Dionysos quand Athéna identifie un blocage multi-contraintes (toutes les options classiques présentent un risque élevé) ou systématiquement pour les orchestrations en pattern `exploration`.

### Thémis + Héphaïstos : les deux vetos

Thémis vérifie la légalité et la responsabilité contractuelle du MOE.
Héphaïstos vérifie la faisabilité technique (DTU, AT, compatibilité matériaux).
Leurs vetos sont indépendants. Les deux peuvent coexister sur une même décision C5.

**Priorité des vetos** : si les deux émettent un veto simultané, le veto technique (Héphaïstos) prime pour l'ordre de résolution — on ne peut pas régler le contractuel si le technique est infaisable.

### Chronos ↔ Arès : calendrier ↔ action terrain

Chronos identifie les contraintes temporelles et les alertes BLOQUANT/URGENT.
Arès traduit ces contraintes en actions terrain réversibles (C3) sans attendre Zeus.
Pour les décisions engageantes, Arès remonte à Zeus.

**Feedback loop** : après chaque action terrain, Arès rapporte le temps réel à Chronos pour recalibrage du planning. Arès écrit immédiatement l'action dans Hestia (pas en post-orchestration).

### Athéna → Chronos : scénarios → faisabilité temporelle

Avant de finaliser ses scénarios, Athéna peut solliciter Chronos pour vérifier la faisabilité temporelle de chaque option (délais légaux, jalons, chemin critique). Chronos annote chaque scénario avec son impact planning.

### Prométhée → Apollon : failles → sources

Quand Prométhée identifie des claims non vérifiés ou des hypothèses fragiles dans une analyse, il signale les points à vérifier. Apollon recherche les sources (RAG + web) pour confirmer ou infirmer. Si la source n'existe pas, l'objection de Prométhée est classée critique.

### Thémis → Dédale : contraintes → structure dossier

Avant l'assemblage d'un dossier par Dédale, Thémis fournit les contraintes contractuelles applicables (obligations MOE, pièces contractuelles requises, clauses spécifiques). Dédale structure le dossier en conséquence.

### Hestia + Mnémosyne : les deux mémoires persistantes

Hestia = mémoire par affaire (décisions, hypothèses, dettes D1-D3 de ce projet).
Mnémosyne = mémoire transversale (patterns agence, précédents cross-projets).
Zeus consulte les deux avant de planifier une orchestration complexe.

**Protocole d'écriture Hestia** :
- Zeus / Hermès écrit après chaque décision C3+
- Arès écrit immédiatement après chaque action terrain C3
- Thémis écrit après chaque veto émis
- Format : `[DATE] [CATÉGORIE] [SOURCE] Objet / Contenu / Impliqués / À revoir si`

**Protocole d'écriture Mnémosyne** :
- Le système extrait automatiquement les leçons après chaque run agent complété
- Les leçons sont catégorisées : technique, planning, budget, contractuel, general
- Scope 'agence' = transversal, scope 'projet' = spécifique à l'affaire

**Invalidation temporelle** :
- Un fait obsolète est marqué `valid_until = now()` + `superseded_by = <nouvelle leçon>`
- Seuls les faits valides (`valid_until IS NULL`) sont injectés dans les prompts

### Apollon : vérificateur transversal

Mode 1 (recherche) : il cherche et sourcifie sur demande d'un autre agent ou de Zeus.
Mode 2 (cohérence) : **automatique pour C4+**, appelé par Zeus après les résultats agents et avant la synthèse finale. Il détecte les contradictions entre agents, vérifie la couverture de la demande, et signale les claims non sourcés.

---

## Résolution de conflits intra-famille

### Famille Analyse — conflits entre agents

| Conflit | Résolution |
|---------|------------|
| Athéna propose, Héphaïstos dit infaisable | Héphaïstos prime (veto technique). Dionysos cherche une alternative. |
| Athéna propose, Prométhée trouve des failles | Zeus juge la gravité. Si faille critique → complément demandé. |
| Dionysos propose, Héphaïstos valide, Thémis refuse | Thémis prime (veto contractuel). Option retirée des scénarios. |
| Apollon trouve des contradictions entre agents | Zeus demande un complément aux agents contradictoires. Max 1 cycle. |

### Famille Cadrage — conflits entre agents

| Conflit | Résolution |
|---------|------------|
| Chronos dit URGENT, Thémis dit hors contrat | Thémis prime. Chronos ajuste le planning en intégrant le temps d'avenant. |
| Arès veut agir, Chronos dit trop tard | Arès escalade à Zeus si l'action est irréversible. Sinon Arès agit. |
| Thémis et Héphaïstos émettent un veto simultané | Héphaïstos prime pour l'ordre de résolution. Les deux vetos sont persistés. |

---

## Patterns d'orchestration

### Solo
Un seul agent exécute la tâche. Utilisé pour C1-C2 ou sous-tâches simples.

### Parallel
Agents indépendants travaillent simultanément sur la même instruction. Zeus consolide.

### Cascade
Agents en séquence — chaque agent reçoit le contexte des précédents.
Typique : Argos → Héphaïstos, Athéna → Prométhée → Apollon.

### Arena
Agents en parallèle sur la même question + juge qui arbitre.
Apollon juge les faits/normes ; Zeus juge les arbitrages stratégiques.

### Exploration (nouveau)
Pipeline créatif pour recherche de solutions alternatives :
Dionysos (options latérales) → Prométhée (critique) → Apollon (vérification sources)
Zeus invoque ce pattern quand toutes les options classiques présentent un risque élevé.

---

## Criticité C1-C5 — référence commune

| Niveau | Nature | Zeus | HITL | Veto | Agents secondaires auto |
|--------|---------|------|------|------|------------------------|
| C1 | Information pure | ✗ | ✗ | ✗ | — |
| C2 | Question | ✗ | ✗ | ✗ | — |
| C3 | Décision réversible | optionnel | ✗ | ✗ | Chronos si planning |
| C4 | Décision engageante | ✓ | ✓ | ✗ | Prométhée + Apollon Mode 2 |
| C5 | Risque majeur | ✓ | ✓ | ✓ | Prométhée + Apollon Mode 2 + Dionysos |

---

## Règles communes à tous les agents

- Ne jamais inventer un chiffre (coût, délai, surface, article, norme) → `[NON VÉRIFIÉ]`
- Si l'information est absente des documents → le dire explicitement
- Veto émis → stopper, formuler `{"veto": true, "motif": "...", "condition_levee": "..."}`
- Décision engageante sans Thémis → escalader, ne pas décider seul
- Leçon utile en fin de session → la signaler pour Hestia (projet) ou Mnémosyne (agence)
- **Timeout** : si un agent ne produit pas de résultat dans les 90s, Zeus continue avec les résultats partiels
- **Contradiction** : si deux agents fondamentalement en désaccord, Zeus invoque le pattern arena avec Apollon comme juge
- **Complément** : Zeus peut demander un cycle de compléments (max 1) si les résultats sont insuffisants

---

## Contexte métier injecté automatiquement

À chaque run, le système injecte dans le prompt système :
- Typology, région, budget, honoraires, phase courante, ABF, zones de risque (depuis `affaires`)
- Mémoire projet Hestia : décisions validées, dettes D1-D3 (scope='projet', valid_until IS NULL)
- Mémoire agence Mnémosyne : patterns pertinents, catégorisés (scope='agence', valid_until IS NULL)

Phases loi MOP : **ESQ → APS → APD → PRO → ACT → VISA → DET → AOR**

Interlocuteurs : MOA (particuliers, collectivités, promoteurs), entreprises, BET, BC, ABF, DREAL, mairie.
