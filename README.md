# Stage Python – jeux sur Codesters

Ressources pour le stage Python sur Codesters : les sprites des jeux, des pages qui expliquent comment les jeux fonctionnent, et le code étape par étape.

Lien direct d'une image (pour l'importer dans Codesters) :

```
https://raw.githubusercontent.com/Pwaluh/stages/master/sprites/NOM_DU_JEU/NOM_DU_FICHIER.png
```

Par exemple : `https://raw.githubusercontent.com/Pwaluh/stages/master/sprites/space-invaders/vaisseau_joueur.png`

## `sprites/topdown-shooter/`

Les images du jeu de tir vu de dessus. Tous les personnages regardent vers la **droite** (angle 0°).

| Fichier | Taille | Rôle |
|---|---|---|
| `soldat_joueur.png` | 64 × 64 | le joueur |
| `soldat_ennemi.png` | 64 × 64 | soldat ennemi |
| `zombie_1.png`, `zombie_2.png`, `zombie_3.png` | 64 × 64 | les zombies |
| `helicoptere_corps.png` | 192 × 192 | l'hélico (objectif de victoire) |
| `helicoptere_rotor.png` | 192 × 192 | le rotor, à faire tourner par-dessus le corps |
| `balle.png`, `balle_trainee.png` | 16 × 8, 32 × 8 | les balles |
| `flash_tir.png` | 32 × 32 | flash au bout du canon |
| `reticule.png`, `reticule_rouge.png` | 64 × 64 | le viseur |
| `coeur_plein.png`, `coeur_moitie.png`, `coeur_vide.png` | 32 × 32 | les points de vie |
| `map_ferme.png` | 2048 × 2048 | la map : un champ avec une ferme en ruine |
| `apercu.png` | — | aperçu de tous les sprites (pas utilisé dans le jeu) |

Codesters réduit les grandes images pour les faire tenir dans la scène : la map s'affiche à environ 300 px, il faut donc lui donner `map.set_size(6.8)` pour retrouver sa vraie taille.

## `sprites/space-invaders/`

Les images du remake de shoot'em up spatial, en pixel art. Les animations ont **2 images** (`_1` et `_2`) à alterner.

| Fichier | Taille | Rôle |
|---|---|---|
| `vaisseau_joueur.png` | 39 × 36 | le vaisseau du joueur |
| `flamme_1.png`, `flamme_2.png` | 15 × 15 | flamme du réacteur, sous le vaisseau |
| `alien_meduse_1.png`, `alien_meduse_2.png` | 36 × 30 | aliens de la rangée du haut |
| `alien_drone_1.png`, `alien_drone_2.png` | 39 × 30 | aliens des rangées du milieu |
| `alien_orbe_1.png`, `alien_orbe_2.png` | 36 × 30 | aliens des rangées du bas |
| `soucoupe_1.png`, `soucoupe_2.png` | 48 × 24 | soucoupe bonus |
| `tir_joueur.png` | 9 × 18 | laser du joueur |
| `tir_alien_1.png`, `tir_alien_2.png` | 15 × 18 | tir des aliens |
| `explosion_1.png`, `explosion_2.png` | 39 × 33 | explosion |
| `bouclier_intact.png`, `bouclier_abime.png`, `bouclier_casse.png` | 24 × 24 | une tuile de bouclier en 3 états |
| `vie.png` | 26 × 24 | icône de vie |
| `boss_1.png`, `boss_2.png` | 72 × 42 | le boss |
| `fond_espace.png` | 500 × 500 | fond étoilé, à la taille de la scène |
| `apercu.png`, `exemple_scene.png` | — | aperçus (pas utilisés dans le jeu) |

Les boucliers sont faits de tuiles : on en assemble plusieurs, et à chaque impact la tuile passe de `intact` à `abime`, puis `casse`, puis disparaît.

## `game_design_explained/`

Des pages interactives à ouvrir dans le navigateur pour expliquer les jeux aux élèves.

### `topdown-shooter/`

- `aim_explained.html` : **Viser un zombie** – comment `atan2` donne l'angle pour que le soldat regarde la cible.
- `world_scrolling_explained.html` : **La carte qui glisse** – pourquoi l'hélico, les zombies et les balles doivent bouger en même temps que la map.
- `muzzle_explained.html` : **Le bout du canon** – comment `cos` et `sin` font partir la balle du bout du fusil, quel que soit l'angle.
- `side_offset_explained.html` : **Le pas de côté** – le petit décalage sur le côté quand le fusil n'est pas pile dans l'axe du soldat.

### `space-invaders/`

- `shield_wall_explained.html` : **Le mur de boucliers** – construire le mur tuile par tuile avec des `while` imbriqués, et le centrer quel que soit l'écart.
- `alien_fleet_explained.html` : **La flotte d'aliens** – placer les aliens par rangée et colonne, et les ranger dans une liste pour les faire bouger et savoir lequel est touché.
- `tick_explained.html` : **Le battement du jeu** – la fonction `tick()` : un seul `event_interval`, le compteur de tics et le modulo pour ce qui arrive de temps en temps.

## `game_steps/`

Le code des jeux étape par étape, chaque étape en version **base** et **bonus**. Chaque dossier a son propre guide (`README.md`).

- `topdown-shooter/` : 5 étapes (joueur, hélico, zombies, tir, victoire/défaite).
- `space-invaders/` : 6 étapes (joueur, aliens, tir, tirs ennemis et vies, protections, boss).
