# ARCEUS — Agent Engineering Principles

## 1. Agents are not chatbots

Un agent n’est pas un système de réponse.  
C’est un système qui :

- décide quoi faire
- utilise des outils
- gère les erreurs
- sait quand s’arrêter

Toute logique purement conversationnelle est insuffisante.

---

## 2. Planning > Execution

Une mauvaise planification produit :

- des actions incorrectes
- des erreurs répétées
- une confiance artificielle

Chaque workflow doit :

- structurer le problème
- définir les étapes
- expliciter les objectifs

---

## 3. Tool design is critical

Un tool doit définir :

- ce qu’il fait
- quand l’utiliser
- quand ne pas l’utiliser

Exemple incorrect :
"analyse un devis"

Exemple correct :
"identifie les postes manquants, incohérences, omissions techniques, sans conclure juridiquement"

---

## 4. Memory must be externalized

Ne jamais dépendre uniquement du contexte conversationnel.

Trois niveaux obligatoires :

- mémoire projet (Hestia)
- mémoire agence (Mnémosyne)
- mémoire fonctionnelle

---

## 5. Memory is selective

Tout ne doit pas être mémorisé.

Le système doit décider :

- bruit → ignorer
- tâche → mémoire fonctionnelle
- décision → mémoire projet
- pattern → mémoire agence

---

## 6. Context management

Ne jamais laisser le contexte grossir indéfiniment.

Toujours :

- résumer
- extraire
- structurer

---

## 7. Error handling first

Chaque tool doit gérer :

- échec API
- timeout
- incohérence données

Un agent ne doit jamais :

- boucler silencieusement
- s’arrêter sans expliquer

---

## 8. Evaluation must be explicit

Un agent fonctionne uniquement si :

- il passe des cas réels métier
- il est testé en conditions dégradées

Exemples :

- devis incomplet
- photo ambiguë
- conflit contractuel
- demande imprécise

---

## 9. Latency is UX

Réponse rapide obligatoire :

1. compréhension rapide
2. traitement profond en second temps

---

## 10. Reversibility levels

Chaque action doit être classée :

- note interne (réversible)
- mémoire (semi-réversible)
- email envoyé (irréversible)
- décision contractuelle (critique)

---

## 11. Human in the loop

Obligatoire pour :

- décisions C4/C5
- envoi email
- modification données projet
- documents officiels

---

## 12. Case resolution is mandatory

Avant toute action :

- identifier l’affaire
- identifier le lot
- identifier la phase

---

## 13. Draft-first policy

Toujours :

- proposer un brouillon
- valider
- ensuite seulement exécuter

---

## 14. Agents must ask questions

Si doute :

- demander clarification
- ne pas deviner
- ne pas sur-mémoriser

---

## 15. Stress testing required

Tester :

- inputs incomplets
- contradictions
- erreurs outils
- multi-utilisateurs
- groupes (WhatsApp / Telegram)

---

## 16. Final rule

Un bon agent :

- est fiable
- est explicable
- est contrôlable

Un agent non gouverné est inutilisable en production.

---