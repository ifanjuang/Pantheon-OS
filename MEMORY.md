# MEMORY — Pantheon OS

> Source de vérité sur la gestion de la mémoire dans le système.  
> La mémoire est un composant structurant, contrôlé et validé.

---

# 1. Principe fondamental

La mémoire n’est pas un stockage passif.

C’est un système de connaissance contrôlé.

Une information ne devient mémoire que si :

- elle est utile  
- elle est vérifiée  
- elle est validée  

---

# 2. Niveaux de mémoire

Pantheon distingue 4 niveaux stricts :

text SESSION CANDIDATE PROJECT SYSTEM 

---

## 2.1 Session

Nature :

- temporaire  
- non persistée  

Contenu :

- contexte en cours  
- hypothèses  
- réflexion  
- éléments intermédiaires  

Agents :

- ZEUS  
- ATHENA  

Règle :

La mémoire session disparaît après la conversation.

---

## 2.2 Candidate

Nature :

- persistée  
- non validée  

Contenu :

- faits potentiels  
- patterns détectés  
- règles proposées  
- skills candidates  

Agents :

- ARGOS → collecte  
- THEMIS → validation  

Règle :

Aucune donnée candidate n’est considérée comme fiable.

---

## 2.3 Project

Nature :

- spécifique à un projet  

Contenu :

- faits validés  
- décisions  
- contraintes  
- risques  

Agent :

- HESTIA  

Règle :

Non généralisable.

---

## 2.4 System

Nature :

- globale  
- validée  
- réutilisable  

Contenu :

- règles  
- méthodes  
- patterns  
- standards  

Agent :

- MNEMOSYNE  

Règle :

Toute donnée système doit être validée explicitement.

---

# 3. Cycle de vie de l’information

text SESSION → CANDIDATE → VALIDATION (THEMIS) → PROJECT ou SYSTEM 

---

# 4. Règles de promotion

Une information peut être promue si :

- source identifiable  
- utilité réelle  
- cohérence avec le système  
- absence de contradiction  

Validation obligatoire :

- THEMIS  
- éventuellement validation humaine  

---

# 5. Règles de rejet

Une information doit être rejetée si :

- non vérifiable  
- redondante  
- obsolète  
- contradictoire  
- trop spécifique  

---

# 6. Interaction avec les skills

Les skills :

- lisent la mémoire  
- proposent des mises à jour  

Elles ne doivent jamais :

- modifier directement la mémoire  
- promouvoir une information  

---

# 7. Interaction avec les workflows

Les workflows :

- peuvent générer des candidates  
- peuvent déclencher une validation  

Mais :

La promotion reste contrôlée.

---

# 8. Séparation mémoire / knowledge

text Memory = connaissance validée Knowledge = sources documentaires 

Knowledge (OpenWebUI) :

- documents  
- normes  
- fichiers  

Memory (Pantheon) :

- décisions  
- règles  
- patterns  

---

# 9. Risques

Sans contrôle :

- pollution de la mémoire  
- règles incorrectes  
- dérives logiques  
- perte de fiabilité  

Pantheon impose :

text validation > accumulation 

---

# 10. Exemple

Situation :

Analyse répétée de devis.

Session :

“souvent la VMC est oubliée”

Candidate :

pattern détecté

Validation :

THEMIS confirme

System :

règle ajoutée :

“vérifier systématiquement la VMC”

---

# 11. Résumé

text session   = réflexion candidate = proposition project   = contexte system    = vérité 

---

FIN DU FICHIER