### Documentation Utilisateur

---

## Introduction

Ce document fournit une description détaillée de l'utilisation et des fonctionnalités du jeu, en se concentrant sur les principaux composants du système, notamment les bases, les joueurs, les unités, les tourelles, et les différentes intelligences artificielles (IA). Ce jeu est développé en utilisant la bibliothèque Pygame et inclut plusieurs niveaux d'IA pour défier les joueurs.

---

## Table des Matières

1. [Installation](#installation)
2. [Lancement du Jeu](#lancement-du-jeu)
3. [Écran de Menu](#écran-de-menu)
4. [Joueurs et Bases](#joueurs-et-bases)
5. [Unités](#unités-et-tourelles)
    - [Unités](#unités)
    - [Système d'Amélioration](#système-damélioration)
6. [Interface Utilisateur (HUD)](#interface-utilisateur-hud)
7. [Niveaux d'IA](#niveaux-dia)
    - [EasyBot](#easybot)
    - [MediumBot](#mediumbot)
    - [HardBot](#hardbot)

---

## Installation

### Prérequis

- Python 3.x
- Pygame

### Étapes d'Installation

1. Clonez le dépôt du jeu depuis le repository Git.
2. Installez les dépendances nécessaires en utilisant pip :
   ```bash
   pip install -r requirements.txt
   ```
3. Assurez-vous que tous les fichiers de code (fichiers `.py`) sont placés dans les répertoires appropriés.

---

## Lancement du Jeu

Pour lancer le jeu, exécutez le fichier principal du jeu en utilisant Python. Par exemple :
```bash
python game.py
```

---

## Écran de Menu

### Description

L'écran de menu permet aux joueurs de choisir le mode de jeu et de démarrer une partie.

### Options Disponibles

- **Facile** : Démarre une partie contre une IA facile (EasyBot).
- **Intermédiaire** : Démarre une partie contre une IA de niveau intermédiaire (MediumBot).
- **Difficile** : Démarre une partie contre une IA difficile (HardBot).

---

## Joueurs et Bases

### Joueurs

Les joueurs sont représentés par la classe `Player`. Chaque joueur possède un nom, une équipe, des ressources (argent), et une base.

### Bases

Les bases sont représentées par la classe `Base`. Chaque base appartient à un joueur et contient des unités, des emplacements de tourelles, et d'autres propriétés spécifiques.

### Fonctionnalités des Bases

- **Unités** : Gère les unités disponibles pour la défense et l'attaque.
- **Tourelles** : Gère les emplacements de tourelles, leur déploiement et leur mise à jour.

---

### Unités

Les unités sont les forces de combat dans le jeu. Chaque type d'unité a ses propres caractéristiques et capacités. Voici les détails des différents types d'unités disponibles, leurs statistiques, leurs forces et leurs faiblesses.

#### Types d'Unités

1. **Infantry (Infanterie)**
    - **Nom** : Infantry
    - **Points de vie (HP)** : 100 (augmente avec l'âge)
    - **Prix** : 10
    - **Dégâts** : 10 (augmente avec l'âge)
    - **Vitesse d'attaque** : 0.5 seconde
    - **Portée** : 200 unités
    - **Valeur en or** : 5
    - **Vitesse de marche** : 1 (augmente avec l'âge)
    - **Temps de construction** : 1 seconde
    - **Faible contre** : AntiTank
    - **Description** : Unité de base rapide et économique, idéale pour des attaques rapides et pour occuper le terrain.

2. **Support (Soutien)**
    - **Nom** : Support
    - **Points de vie (HP)** : 80 (augmente avec l'âge)
    - **Prix** : 10
    - **Dégâts** : 5 (augmente avec l'âge)
    - **Vitesse d'attaque** : 0.5 seconde
    - **Portée** : 300 unités
    - **Valeur en or** : 2.5
    - **Vitesse de marche** : 2 (augmente avec l'âge)
    - **Temps de construction** : 7 secondes
    - **Faible contre** : Heavy
    - **Description** : Unité de soutien avec une attaque rapide, utile pour assister d'autres unités et cibler des ennemis spécifiques.

3. **Heavy (Lourd)**
    - **Nom** : Heavy
    - **Points de vie (HP)** : 300 (augmente avec l'âge)
    - **Prix** : 18
    - **Dégâts** : 5 (augmente avec l'âge)
    - **Vitesse d'attaque** : 0.7 seconde
    - **Portée** : 150 unités
    - **Valeur en or** : 10
    - **Vitesse de marche** : 1 (augmente avec l'âge)
    - **Temps de construction** : 3 secondes
    - **Faible contre** : AntiTank
    - **Description** : Unité lourde, avec des points de vie élevés, idéale pour des assauts frontaux.

4. **AntiTank**
    - **Nom** : AntiTank
    - **Points de vie (HP)** : 150 (augmente avec l'âge)
    - **Prix** : 18
    - **Dégâts** : 15 (augmente avec l'âge)
    - **Vitesse d'attaque** : 0.7 seconde
    - **Portée** : 150 unités
    - **Valeur en or** : 7.()
    - **Vitesse de marche** : 1 (augmente avec l'âge)
    - **Temps de construction** : 3 secondes
    - **Faible contre** : Infantry
    - **Description** : Spécialiste anti-char avec des attaques puissantes et une portée moyenne, conçu pour neutraliser les unités lourdes.

#### Système d'Amélioration

Le jeu dispose d'un système d'amélioration permettant aux joueurs d'améliorer leurs unités et leurs tourelles. Chaque amélioration augmente les statistiques de base de l'unité, comme les points de vie, les dégâts, et la vitesse.

- **Infantry** : Augmentation des points de vie et des dégâts.
- **Support** : Augmentation des dégâts et réduction du temps de rechargement.
- **Heavy** : Augmentation des points de vie et des dégâts.
- **AntiTank** : Augmentation des dégâts et de la portée.

Les unités peuvent être améliorées en fonction de l'âge de la base, avec chaque niveau d'âge offrant des multiplicateurs pour les statistiques de l'unité, augmentant ainsi leur efficacité au combat.

### Système d'Amélioration

Le jeu dispose d'un système d'amélioration permettant aux joueurs d'améliorer leurs unités et leurs tourelles.

#### Amélioration des Unités

Toutes les unités peuvent être amelioré sur 3 aspects :

- Dégats (+20% / niveau)
- Vie (+20% / niveau)
- Porté (+20% / niveau)

Le prix de chaque amélioration est de 10 or par défaut et augmente de 150% à chaque niveau.

Ces améliorations ne s'apppliquent qu'aux unités produites après l'amélioration.

Le joueur quant à lui peut améliorer les gold qu'il gagne à chaque élimination d'unité ennemie. (+20% / niveau)
Le prix de l'amélioration est de 10 or par défaut et augmente de 200% à chaque niveau.



#### Changement d'age

Le joueur peut changer d'age lorsque sa barre d'expérience est pleine. Chaque changement d'age augmente les 
statistiques de base de l'unité, comme les points de vie, les dégâts, et la vitesse de 20%.

Cette amélioration ne s'applique qu'aux unités produites après le changement d'age.

## Interface Utilisateur (HUD)

### Description

L'interface utilisateur (HUD) affiche des informations cruciales pour le joueur, telles que les ressources disponibles, les unités en cours de production, et les boutons d'action.

### Éléments du HUD

- **Barres de Santé** : Affiche l'état de santé des unités et des tourelles.
- **Boutons d'Actions** : Permet aux joueurs de sélectionner des unités, de les déployer, et de gérer les ressources.
- **Barre d'Expérience** : Affiche l'expérience accumulée par le joueur.

---

## Niveaux d'IA

### EasyBot

#### Description

L'IA facile (EasyBot) est conçue pour les débutants. Elle prend des décisions simples et prévisibles, offrant un défi modéré.

#### Comportement

- Effectue des actions de manière aléatoire, comme déployer des unités.
- Ne prend pas en compte des stratégies complexes.

### MediumBot

#### Description

L'IA intermédiaire (MediumBot) offre un défi plus important, avec des décisions plus stratégiques et réfléchies.

#### Comportement

- Évalue les unités ennemies et prend des décisions basées sur l'analyse de la situation.
- Utilise une mémoire pour suivre les unités alliées et ennemies.

### HardBot

#### Description

L'IA difficile (HardBot) est conçue pour les joueurs expérimentés. Elle utilise des stratégies avancées et s'adapte aux actions du joueur.

#### Comportement

- Utilise une mémoire détaillée pour analyser les forces et les faiblesses des unités ennemies.
- Prend des décisions stratégiques en fonction de l'état actuel du jeu.
