# SKILLS.md

## 1. OBJECTIF

Ce document définit l’ensemble des skills utilisés dans ARCEUS.

Un skill est une fonction spécialisée appelée par un agent pour exécuter une tâche précise.

Un skill :
- a une entrée claire
- produit une sortie structurée
- ne prend jamais de décision finale

---

## 2. STRUCTURE STANDARD D’UN SKILL

Chaque skill doit définir :

- Nom
- Agent responsable
- Entrée
- Traitement
- Sortie
- Limites

---

## 3. SKILLS TECHNIQUES (HÉPHAÏSTOS)

### analyse_devis
Entrée : devis entreprise  
Sortie :
- oublis
- incohérences
- écarts de prix
- risques techniques  

---

### analyse_dtu
Entrée : détail technique  
Sortie :
- conformité
- écarts
- points sensibles  

---

### analyse_detail_constructif
Entrée : description / plan  
Sortie :
- couches
- cohérence
- points faibles  

---

### analyse_pathologie
Entrée : description ou image  
Sortie :
- type de désordre
- causes probables
- gravité  

---

## 4. SKILLS CONTRACTUELS (THÉMIS)

### analyse_contrat
Entrée : CCAP / marché  
Sortie :
- obligations
- responsabilités
- risques  

---

### verification_situation
Entrée : facture entreprise  
Sortie :
- cohérence
- anomalies
- validation possible  

---

### analyse_litige
Entrée : échange + contexte  
Sortie :
- position MOE
- risques
- stratégie  

---

## 5. SKILLS CHANTIER

### analyse_photo (ARGOS)
Entrée : image  
Sortie :
- description détaillée
- défauts visibles
- niveau certitude  

---

### generation_cr_chantier
Entrée : notes / voix  
Sortie :
- CR structuré
- décisions
- actions  

---

### suivi_reserves
Entrée : liste réserves  
Sortie :
- état
- priorité
- évolution  

---

## 6. SKILLS CONCEPTION (ATHÉNA)

### structuration_probleme
Entrée : demande brute  
Sortie :
- reformulation
- axes d’analyse  

---

### generation_scenarios
Entrée : problème  
Sortie :
- options
- avantages
- risques  

---

## 7. SKILLS PLANNING (CHRONOS)

### analyse_planning
Sortie :
- incohérences
- conflits  

---

### impact_retard
Sortie :
- conséquences
- priorités  

---

## 8. SKILLS TRANSVERSE

### scoring_decision
Sortie :
- score global
- axes faibles  

---

### classification_criticite
Sortie :
- C1 à C5  

---

## 9. RÈGLES

- un skill = une fonction
- sortie toujours structurée
- testable indépendamment
- jamais décisionnel

---