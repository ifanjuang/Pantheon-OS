# Examples — rich_elicitation

All examples are fictional and generic.

The skill should reduce ambiguity without turning every request into a survey.

---

## 1. Long report request

User request:

```text
Fais-moi un rapport complet sur ce sujet.
```

Trigger assessment:

```yaml
elicitation_trigger:
  ambiguous_dimensions:
    - target_reader
    - depth
    - format
    - source_scope
  material_to_output: true
  user_cost_if_wrong: high
  can_reasonably_assume: false
  recommended_action: ask
```

Question block:

```text
Avant de produire un rapport complet, trois choix vont fortement changer la structure et le niveau de recherche.

Q1. Qui est le lecteur principal ?
- Décideur non technique (Recommended)
- Équipe projet
- Expert métier
- Public externe

Q2. Quel niveau de profondeur faut-il viser ?
- Synthèse structurée
- Rapport complet exploitable (Recommended)
- Analyse exhaustive avec annexes
- Version courte orientée décision

Q3. Quelle base de sources utiliser ?
- Documents fournis uniquement
- Documents fournis + Knowledge projet (Recommended)
- Recherche web officielle élargie
- Benchmark large avec sources externes
```

---

## 2. Simple rewrite — no trigger

User request:

```text
Améliore ce mail en le rendant plus humain.
```

Trigger assessment:

```yaml
elicitation_trigger:
  ambiguous_dimensions:
    - tone_minor
  material_to_output: false
  user_cost_if_wrong: low
  can_reasonably_assume: true
  recommended_action: proceed_with_assumptions
```

Action:

```text
Do not ask. Rewrite directly and preserve intent.
```

---

## 3. CCTP complete request

User request:

```text
Rédige un CCTP complet pour ce projet.
```

Trigger assessment:

```yaml
elicitation_trigger:
  ambiguous_dimensions:
    - source_boundary
    - lot_structure
    - market_type
    - responsibility_level
  material_to_output: true
  user_cost_if_wrong: high
  can_reasonably_assume: false
  recommended_action: route_to_workflow
```

Question block:

```text
Un CCTP complet dépend d’abord des pièces disponibles et de la structure des lots. Je cadre ces points avant de rédiger.

Q1. Quelle base faut-il utiliser ?
- Programme et plans fournis uniquement
- Plans + DPGF + diagnostics (Recommended)
- Ancien CCTP comme base à refondre
- Meilleure version provisoire avec limites visibles

Q2. Quelle structure de lots faut-il viser ?
- Lots classiques bâtiment
- Lots adaptés au projet existant (Recommended)
- Un seul lot entreprise générale
- À définir après inventaire des sources

Q3. Quel niveau de sortie ?
- Trame de CCTP
- Première version complète candidate (Recommended)
- Version marché très détaillée
- Analyse préalable avant rédaction
```

Escalation:

```text
Route to Deliverable Contract / CCTP workflow if accepted.
```

---

## 4. Technical choice

User request:

```text
Quel outil je devrais utiliser pour ça ?
```

Question block:

```text
Le bon choix dépend surtout de ton niveau de risque acceptable et de l’usage final. Je clarifie ces points avant de recommander.

Q1. Quelle priorité domine ?
- Simplicité et maintenance (Recommended)
- Puissance maximale
- Rapidité de mise en place
- Expérimentation sans engagement

Q2. Où l’outil sera-t-il utilisé ?
- Local seulement
- NAS / Docker local (Recommended)
- Cloud public
- À décider après comparaison

Q3. Quel niveau de risque est acceptable ?
- Très faible, stable uniquement (Recommended)
- Moyen, si sandboxé
- Élevé, pour test rapide
- Je ne sais pas encore
```

---

## 5. User asks not to be interrupted

User request:

```text
Fais au mieux, ne me pose pas de questions.
```

Action:

```text
Do not trigger rich elicitation.
Proceed with assumptions and state them clearly.
```

Expected assumption block:

```text
Je pars sur une version structurée, exploitable, avec un niveau de détail standard. Les points incertains sont marqués comme hypothèses.
```

---

## 6. Follow-up round

Round 1 answer:

```text
Reader = client externe.
Depth = rapport complet.
Sources = web officiel élargi.
```

Round 2 question block:

```text
Comme le rapport est destiné à un lecteur externe, il faut cadrer le niveau de prudence et le format de livraison.

Q1. Le rapport doit-il inclure une position claire ou rester analytique ?
- Analytique avec recommandations prudentes (Recommended)
- Position forte et assumée
- Comparaison neutre sans conclusion

Q2. Quel format final faut-il viser ?
- Markdown structuré
- PDF exportable
- Dossier avec annexes (Recommended)
- Présentation synthétique
```

---

## 7. Max rounds reached

After Round 3:

```text
Je poursuis avec les éléments disponibles. Les points encore incertains seront indiqués comme hypothèses plutôt que de prolonger les questions.
```

---

## 8. Evidence Pack relationship

Consequential final Evidence Pack may include:

```yaml
clarification_summary:
  questions_asked: 3
  user_selected:
    target_reader: client_externe
    depth: rapport_complet
    source_scope: official_web_plus_project_knowledge
  assumptions_retained:
    - no_external_send_without_review
  unresolved_ambiguities: []
```
