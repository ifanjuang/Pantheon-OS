# MEMORY.md

## 1. OBJECTIF

Définir les règles de gestion des mémoires dans ARCEUS.

---

## 2. TYPES DE MÉMOIRE

### 2.1 Mémoire Projet (Hestia)

Contient :
- décisions validées
- contraintes
- hypothèses
- dettes décisionnelles

Règles :
- toujours liée à une affaire
- jamais polluée par d’autres projets

---

### 2.2 Mémoire Agence (Mnémosyne)

Contient :
- patterns
- erreurs récurrentes
- optimisations

Règles :
- transversal
- pas de détail projet inutile

---

### 2.3 Mémoire Fonctionnelle

Contient :
- tâches
- urgences
- flux actifs

Règles :
- temporaire
- nettoyée régulièrement

---

## 3. STRUCTURE D’UNE ENTRÉE MÉMOIRE

Chaque entrée contient :

- ID
- type (projet / agence / fonctionnelle)
- source
- date
- agents impliqués
- criticité
- contenu structuré
- liens

---

## 4. DETTE DÉCISIONNELLE

Chaque entrée peut inclure :

- statut D0 à D3
- condition de levée
- phase de révision

---

## 5. RÈGLES CRITIQUES

- ne jamais mélanger mémoire agence et projet
- toute décision C4/C5 → mémoire projet obligatoire
- toute répétition → mémoire agence

---