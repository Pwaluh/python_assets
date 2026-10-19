# Le jeu de tir, étape par étape

Le jeu se construit en **5 étapes**. Chaque étape existe en deux versions :

- **`etape_N_base.py`** : le minimum pour que l'étape marche ;
- **`etape_N_bonus.py`** : la base, plus un petit bonus pour les élèves qui avancent vite.

Chaque fichier est un **programme complet** qu'on peut copier dans Codesters et lancer tel quel.

Il y a deux parcours :

```
base  :  1 base  → 2 base  → 3 base  → 4 base  → 5 base
bonus :  1 bonus → 2 bonus → 3 bonus → 4 bonus → 5 bonus
```

Un élève peut passer d'un parcours à l'autre à n'importe quelle étape : il suffit de repartir du fichier de l'étape suivante.

> Les noms des images (`world_f41`, `player_df3`, `zombie_1_873`…) sont ceux du projet Codesters d'origine. Si les élèves importent les images eux-mêmes, Codesters leur donnera d'autres noms : il faut alors les remplacer dans le code, y compris dans les `get_name()` des collisions.

---

## Étape 1 : le joueur et ses déplacements

**Objectif :** le soldat se déplace avec Z Q S D, et la map glisse quand il arrive au bord.

**Base**
- La map (`set_size(6.8)` pour retrouver sa vraie taille de 2048 px) et le joueur.
- La liste `world` : tout ce qui est dans le monde et doit glisser avec la map.
- `move_world(dx, dy)` déplace tout ce qui est dans `world`.
- Les 4 touches suivent la même règle : dans le carré du centre, le joueur bouge ; au bord du carré, le monde glisse ; au bord de la map, le joueur peut aller jusqu'au bord de l'écran.

**Bonus :** le réticule suit la souris et le soldat la regarde (`atan2`).

**À tester :** aller dans les 4 directions jusqu'au bord de la map, sans jamais voir le vide autour.

**Pages :** *La carte qui glisse* (`world_scrolling_explained.html`), *Viser un zombie* (`aim_explained.html`) pour le bonus.

---

## Étape 2 : l'hélicoptère

**Objectif :** un hélicoptère attend dans un coin de la map. C'est l'objectif du joueur.

**Base**
- L'hélico est placé en (850, 850), en haut à droite de la map.
- `world.append(helicopter)` : il glisse avec la map, donc il reste au même endroit du décor.

**Bonus :** le rotor tourne. On crée la fonction `tick()`, appelée toutes les 0,05 seconde, qui augmente l'angle du rotor.

**À tester :** aller jusqu'à l'hélico. Il doit rester posé au même endroit du décor pendant que la map glisse.

---

## Étape 3 : les zombies

**Objectif :** des zombies apparaissent et poursuivent le joueur.

**Base**
- La liste `zombies`, et `move_world` déplace aussi les zombies.
- `tick()` compte les tics : tous les 20 tics (1 seconde), un nouveau zombie apparaît en haut ou en bas de l'écran.
- `move_zombies()` : chaque zombie calcule l'angle vers le joueur avec `atan2`, puis fait un pas dans cette direction avec `cos` et `sin`.

**Bonus**
- Les zombies regardent le joueur (`set_rotation`).
- Pas plus de 8 zombies en même temps (`MAX_ZOMBIES`).

**À tester :** les zombies suivent le joueur quand il bouge, et ne glissent pas sur le décor quand la map défile.

**À savoir :** Codesters ne garde qu'**un seul** `stage.event_interval`. Tout ce qui doit se répéter va donc dans `tick()`. Le `%` (modulo) permet de faire une action seulement une fois sur 20.

---

## Étape 4 : le tir

**Objectif :** un clic tire une balle vers la souris, et la balle tue les zombies.

**Base**
- `shoot()` crée une balle sur le joueur, la tourne vers la souris et la fait avancer.
- `zombie_collision()` : quand une balle touche un zombie, les deux disparaissent. Il faut aussi **retirer le zombie de la liste `zombies`**, sinon `move_zombies` essaierait de déplacer un sprite supprimé.

**Bonus**
- La balle part du bout du canon : `position_canon(angle)` avance de 32 px avec `cos` / `sin`, puis fait un pas de côté de 1,5 px.
- Un flash apparaît au bout du canon.

**À tester :** tirer dans toutes les directions. En bonus, la balle doit sortir du fusil et pas du casque.

**Pages :** *Le bout du canon* (`muzzle_explained.html`) et *Le pas de côté* (`side_offset_explained.html`).

---

## Étape 5 : la victoire et la défaite

**Objectif :** le joueur perd des PV quand un zombie le touche, perd à 0 PV et gagne en touchant l'hélico.

**Base**
- `hp = 10`, affiché en texte (`PV : 10`).
- `player_collision()` : un zombie qui touche le joueur disparaît et enlève 1 PV. À 0, « You Lose!!! ». En touchant l'hélico, « You Win!!! ».
- `stage.remove_all_events()` arrête le jeu à la fin.

**Bonus :** un cœur à côté des PV.

**À tester :** se laisser toucher 10 fois pour perdre, puis relancer et aller jusqu'à l'hélico pour gagner.
