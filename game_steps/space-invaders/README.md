# Space invaders, étape par étape

Le jeu se construit en **6 étapes**. Chaque étape existe en deux versions :

- **`etape_N_base.py`** : le minimum pour que l'étape marche ;
- **`etape_N_bonus.py`** : la base, plus un ou deux bonus pour les élèves qui avancent vite.

Chaque fichier est un **programme complet** qu'on peut copier dans Codesters et lancer tel quel.

```
base  :  1 base  → 2 base  → 3 base  → 4 base  → 5 base  → 6 base
bonus :  1 bonus → 2 bonus → 3 bonus → 4 bonus → 5 bonus → 6 bonus
```

> **Avant de lancer** : les noms d'images en haut de chaque fichier (`IMG_...`) sont ceux de Codesters. Ceux qui finissent par `_xxx` sont à remplacer par le nom que Codesters donne à l'image importée (tir alien, bouclier abîmé et cassé, boss).

Deux règles reviennent dans tout le jeu :

1. **Tout sprite qu'on devra retoucher plus tard est rangé dans une liste quand on le crée**, et retiré quand il disparaît (`invaders`, `player_lasers`, `alien_lasers`, `shield_tiles`).
2. **Celui qui reçoit le coup gère la collision** : l'alien (`invader_hit`), la tuile (`tile_hit`), le joueur (`player_hit`), le boss (`boss_hit`).

---

## Étape 1 : le joueur

**Objectif :** le vaisseau se déplace de gauche à droite sans sortir de l'écran.

**Base**
- Le fond est créé en premier pour être derrière tout le reste. `set_size(1.67)` : Codesters réduit les grandes images à environ 300 px.
- `left_key` / `right_key` déplacent le joueur, avec une limite à ±225.

**Bonus :** un écran d'accueil (`tutorial`) qui explique les touches, et les touches Q / D en plus des flèches.

---

## Étape 2 : les aliens

**Objectif :** une flotte de 5 rangées × 8 colonnes.

**Base**
- `ROW_TYPES` : quelle image pour quelle rangée.
- Deux boucles imbriquées : `row`, puis `col`. La position est **calculée** : `x = START_X + col * GAP_X`.
- `START_X` est calculé pour que la flotte soit centrée.
- Chaque alien est rangé dans la liste `invaders`.

**Bonus :** la flotte avance de gauche à droite et descend en arrivant au bord. C'est le premier `tick()`.

**Page :** *La flotte d'aliens* (`alien_fleet_explained.html`), et *Le battement du jeu* pour le `tick`.

---

## Étape 3 : le tir

**Objectif :** la barre d'espace tire, et un tir détruit l'alien touché.

**Base**
- `player_fire()` crée un tir et le range dans `player_lasers`.
- `tick()` fait monter les tirs et supprime ceux qui sortent de l'écran (`move_lasers`).
- `invader_hit()` : Codesters donne l'alien touché. On le retire de `invaders`, on retire le tir, et on gagne 10 points.
- Quand `len(invaders) == 0` : « YOU WIN!!! ».

**Bonus**
- 3 tirs maximum à l'écran : on ne peut plus mitrailler sans viser.
- Chaque type d'alien rapporte un nombre de points différent (`POINTS`).
- Si la flotte atteint le bas, c'est perdu.

---

## Étape 4 : les tirs ennemis et les vies

**Objectif :** les aliens tirent, et le joueur a 10 vies.

**Base**
- `alien_fire()` : un alien au hasard tire, tous les 25 tics.
- `player_hit()` : un tir ennemi enlève une vie. À 0, « GAME OVER ».
- Le cœur et le nombre de vies s'affichent en bas à gauche.

**Bonus**
- Moins il reste d'aliens, plus la flotte va vite (`fleet_delay`).
- Un alien qui percute le joueur fait perdre la partie.

---

## Étape 5 : les protections

**Objectif :** des protections arrêtent les tirs ennemis.

**Base**
- Au départ, un mur de 4 protections (`build_wall`, voir la page *Le mur de boucliers*).
- La touche Z pose une protection juste devant le joueur, 2 fois maximum.
- Un tir ennemi détruit la tuile touchée. Les tirs du joueur traversent ses propres protections.

**Bonus**
- Une tuile s'abîme avant de disparaître : pleine, puis abîmée, puis cassée (`NEXT_STATE`).
- Un alien qui arrive sur une protection l'écrase.

**Page :** *Le mur de boucliers* (`shield_wall_explained.html`).

---

## Étape 6 : le boss

**Objectif :** quand tous les aliens sont morts, un boss arrive. On le bat pour gagner.

**Base**
- `spawn_boss()` est appelé quand `len(invaders) == 0`.
- `boss_hit()` : chaque tir enlève `player_damage` points de vie au boss. On gagne à `<= 0` (et pas `== 0`, au cas où on passe sous zéro).
- Le boss vise le joueur, à 40 pixels près.

**Bonus**
- Le boss se déplace de gauche à droite et tire d'un de ses trois canons.
- Le boss clignote quand il est touché (`set_opacity`, remis à 1 après 3 tics).

---

## Comment ces fichiers ont été vérifiés

Chaque fichier a tourné sur une simulation de Codesters avec de vraies collisions :
- un joueur automatique qui vise et esquive gagne ses 10 parties sur 10 dès l'étape 3 ;
- un joueur immobile perd à partir de l'étape 4 (dès l'étape 3 en bonus).

Deux points restent à vérifier dans le vrai Codesters : le nom des touches `"left"` / `"right"`, et le fait que `remove_all_events()` arrête aussi les collisions.
