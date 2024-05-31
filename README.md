### `base.py`

#### Description
Le fichier `base.py` définit la classe `Base`, qui représente la base d'un joueur dans le jeu. Cette classe gère les propriétés et les comportements de la base, y compris les unités, les emplacements de tourelles, et les mises à jour de l'état de la base au fil du temps.

#### Utilité
La classe `Base` est utilisée pour créer et gérer la base de chaque joueur, en stockant des informations telles que les unités disponibles, les emplacements de tourelles, et les propriétés spécifiques à chaque base comme le nom, le propriétaire et l'âge.

#### Fonctionnement général
- **Initialisation** : Lors de la création d'une base, diverses propriétés comme le nom, le propriétaire, les unités, les emplacements de tourelles et les prix des prochains emplacements sont initialisés.
- **Gestion des emplacements de tourelles** : La base gère les emplacements disponibles pour les tourelles, y compris les positions et les coûts associés.
- **Mises à jour** : La base peut être mise à jour avec de nouvelles unités et emplacements au fur et à mesure que le jeu progresse.

---

### `game.py`

#### Description
Le fichier `game.py` contient la classe `Game`, qui représente le cœur du jeu. Cette classe gère les joueurs, l'état du jeu, l'affichage, et les interactions entre les différentes entités du jeu.

#### Utilité
La classe `Game` est essentielle pour orchestrer le déroulement du jeu, en initialisant les joueurs, en gérant le cycle de jeu, et en coordonnant les interactions entre les bases, les unités, et les joueurs.

#### Fonctionnement général
- **Initialisation** : Crée les instances des joueurs, initialise l'écran et les éléments graphiques du jeu.
- **Cycle de jeu** : Gère la boucle principale du jeu, en mettant à jour l'état des joueurs, les bases, et en vérifiant les conditions de victoire ou de défaite.
- **Interactions** : Coordonne les interactions entre les différentes entités du jeu comme les attaques, les mouvements et les mises à jour des unités et des bases.

---

### `hud.py`

#### Description
Le fichier `hud.py` définit la classe `HUD`, qui gère l'affichage de l'interface utilisateur (HUD) pendant le jeu.

#### Utilité
La classe `HUD` est utilisée pour afficher des informations cruciales aux joueurs, telles que les barres de santé, les boutons d'actions, et les ressources disponibles.

#### Fonctionnement général
- **Initialisation** : Configure les éléments graphiques du HUD, y compris les polices, les boutons et les barres de progression.
- **Affichage** : Gère l'affichage des informations à l'écran, en mettant à jour les éléments du HUD en fonction des actions et de l'état du jeu.
- **Interactions utilisateur** : Traite les interactions avec les éléments du HUD, comme les clics sur les boutons.

---

### `menu.py`

#### Description
Le fichier `menu.py` contient la classe `Menu`, qui gère l'écran de menu principal du jeu.

#### Utilité
La classe `Menu` est utilisée pour afficher les options de jeu et permettre aux joueurs de choisir le mode de jeu et de démarrer une partie.

#### Fonctionnement général
- **Initialisation** : Crée les éléments graphiques du menu, y compris les boutons pour sélectionner le mode de jeu.
- **Affichage** : Affiche l'écran de menu et les options disponibles.
- **Navigation** : Permet aux joueurs de naviguer dans les options de menu et de démarrer une nouvelle partie.

---

### `players.py`

#### Description
Le fichier `players.py` définit la classe `Player`, qui représente un joueur dans le jeu.

#### Utilité
La classe `Player` est utilisée pour stocker et gérer les informations spécifiques à chaque joueur, telles que le nom, l'équipe, les ressources, et la base du joueur.

#### Fonctionnement général
- **Initialisation** : Configure les propriétés du joueur comme le nom, l'équipe, l'âge et les ressources.
- **Gestion des ressources** : Gère les ressources du joueur et les interactions avec la base et les unités.
- **Interactions** : Coordonne les actions du joueur, telles que l'achat d'unités et l'interaction avec les éléments du jeu.

---

### `base_ai.py`

#### Description
Le fichier `base_ai.py` contient la classe `AIBot`, qui sert de base pour les différents niveaux d'intelligence artificielle (IA) dans le jeu.

#### Utilité
La classe `AIBot` est utilisée comme classe de base pour toutes les IA du jeu. Elle définit les méthodes et les propriétés communes que toutes les IA doivent implémenter ou utiliser.

#### Fonctionnement général
- **Initialisation** : La classe initialise l'IA avec un joueur spécifique.
- **Méthodes abstraites** : Elle contient des méthodes abstraites comme `perform_actions` et `spawn_unit` que les sous-classes doivent implémenter pour définir le comportement spécifique de l'IA.
- **Gestion des ressources** : Fournit des méthodes pour vérifier les ressources disponibles du joueur.

---

### `easy_bot.py`

#### Description
Le fichier `easy_bot.py` contient la classe `EasyBot`, qui représente une IA de niveau facile dans le jeu.

#### Utilité
La classe `EasyBot` est utilisée pour créer une IA de niveau facile, qui a des comportements simplistes et prévisibles, idéal pour les nouveaux joueurs ou pour des parties moins difficiles.

#### Fonctionnement général
- **Initialisation** : Configure l'IA avec un joueur spécifique.
- **Actions de jeu** : L'IA effectue des actions simples, comme décider de manière aléatoire de déployer des unités.
- **Déploiement des unités** : Choisit de manière aléatoire parmi les types d'unités disponibles pour les déployer.

---

### `medium_bot.py`

#### Description
Le fichier `medium_bot.py` contient la classe `MediumBot`, qui représente une IA de niveau intermédiaire dans le jeu.

#### Utilité
La classe `MediumBot` est utilisée pour créer une IA de niveau intermédiaire, qui a des comportements plus stratégiques que l'IA facile, offrant un défi modéré aux joueurs.

#### Fonctionnement général
- **Initialisation** : Configure l'IA avec un joueur spécifique et initialise une mémoire des unités.
- **Actions de jeu** : L'IA évalue les unités ennemies et décide des actions à entreprendre en conséquence.
- **Déploiement des unités** : Choisit des unités à déployer en fonction de la situation actuelle du jeu et de la mémoire des unités.

---

### `hard_bot.py`

#### Description
Le fichier `hard_bot.py` contient la classe `HardBot`, qui représente une IA de niveau difficile dans le jeu.

#### Utilité
La classe `HardBot` est utilisée pour créer une IA de niveau difficile, qui a des comportements très stratégiques et adaptatifs, offrant un défi significatif aux joueurs expérimentés.

#### Fonctionnement général
- **Initialisation** : Configure l'IA avec un joueur spécifique et initialise une mémoire pour suivre les unités alliées et ennemies.
- **Actions de jeu** : L'IA utilise une mémoire avancée pour évaluer les forces et les faiblesses des unités ennemies et décide des actions stratégiques en conséquence.
- **Déploiement des unités** : Déploie des unités en fonction d'une analyse approfondie de la situation de jeu et des unités présentes.