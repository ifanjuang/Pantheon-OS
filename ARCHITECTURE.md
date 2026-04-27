# ARCHITECTURE — Pantheon OS

> Document de référence technique.  
> Décrit l’architecture réelle du système et la séparation des responsabilités.

---

# 1. Principe global

Pantheon OS est un Domain Operating Layer.

Il ne gère pas l’exécution.  
Il définit :

- la logique  
- les méthodes  
- les règles  
- la mémoire  

---

# 2. Architecture en couches

Le système repose sur trois couches distinctes :

text id="q8bqjh" INTERFACE → OpenWebUI  DOMAIN LAYER → Pantheon OS  RUNTIME → Hermes Agent 

---

## 2.1 OpenWebUI (interface)

Rôle :

- interaction utilisateur  
- stockage documentaire  
- recherche (RAG)  

Contenu :

- documents  
- fichiers  
- knowledge collections  

Limites :

- ne définit pas les agents  
- ne stocke pas la mémoire validée  
- ne décide pas  

---

## 2.2 Pantheon OS (domain layer)

Rôle :

- définir le système  
- structurer la logique  
- garantir la cohérence  

Composants :

- agents  
- skills  
- workflows  
- mémoire  
- règles  

Pantheon :

text id="tq7n0m" ne fait pas n’exécute pas ne stocke pas massivement 

Il décrit.

---

## 2.3 Hermes Agent (runtime)

Rôle :

- exécuter les skills  
- orchestrer les actions  
- utiliser les tools  
- gérer la mémoire opérationnelle  

Responsabilités :

- appels modèles  
- gestion des tokens  
- accès outils  
- exécution réelle  

---

# 3. Flux de fonctionnement

text id="9dj8mn" Utilisateur → OpenWebUI → Pantheon (workflow + agents + skills) → Hermes (exécution) → résultat → validation → mémoire (si applicable) 

---

# 4. Composants Pantheon

## 4.1 Agents

Rôle :

- raisonnement  
- structuration  
- validation  

Caractéristiques :

- abstraits  
- non métier  
- réutilisables  

---

## 4.2 Skills

Rôle :

- exécution logique métier  

Caractéristiques :

- inputs / outputs définis  
- scope précis  
- réutilisables  

---

## 4.3 Workflows

Rôle :

- enchaîner les étapes  
- orchestrer agents et skills  

Caractéristiques :

- déterministes  
- explicites  
- validables  

---

## 4.4 Domains

Rôle :

- spécialisation métier  

Contenu :

- règles  
- contraintes  
- conventions  

---

## 4.5 Memory

Structure :

text id="hfsm7z" session candidate project system 

Rôle :

- capitalisation  
- cohérence  
- traçabilité  

---

## 4.6 Knowledge

Rôle :

- sources documentaires  

Implémentation :

- OpenWebUI  

---

# 5. Séparation des responsabilités

text id="v3tq9r" Pantheon ≠ exécution Hermes ≠ définition OpenWebUI ≠ logique 

---

# 6. Interaction Pantheon / Hermes

Pantheon fournit :

- contexte  
- règles  
- workflows  
- sélection des skills  

Hermes exécute :

- appels modèles  
- outils  
- actions  

---

# 7. Gestion des décisions

Les décisions passent par :

text id="8ntwkh" ARGOS → données THEMIS → règles PROMETHEUS → contradiction APOLLO → validation ZEUS → arbitrage 

---

# 8. Gestion de la mémoire

Cycle :

text id="lrb9y3" SESSION → CANDIDATE → validation → PROJECT ou SYSTEM 

Aucune promotion automatique.

---

# 9. Gestion des risques

Risques principaux :

- hallucination  
- dérive mémoire  
- mauvaise validation  
- mélange responsabilités  

Réponse :

- agents spécialisés  
- validation obligatoire  
- séparation stricte  
- workflows explicites  

---

# 10. Modules techniques actuels

Implémentation minimale :

text id="e0f9p7" FastAPI (Domain API) → expose agents, skills, workflows  Docker / Portainer → déploiement  OpenWebUI → interface  Ollama (PC) → modèles 

---

# 11. Legacy

Présent dans le repo :

- ancien runtime FastAPI  
- registry dynamique  
- workflow loader  
- approval API  

Statut :

text id="r5smy9" à auditer non supprimé non prioritaire 

---

# 12. Règles d’évolution

Toute évolution doit :

- partir des Markdown  
- respecter la séparation des couches  
- éviter les duplications  
- rester simple  

---

# 13. Résumé

text id="6q1kw1" Pantheon = structure Hermes = exécution OpenWebUI = interface 

---

FIN DU FICHIER