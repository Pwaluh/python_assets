# Stage Python – jeu de tir top-down

Ressources pour le stage Python sur Codesters : les sprites du jeu et des pages qui expliquent comment le jeu fonctionne.

## `sprites/`

Les images du jeu, au format PNG. Tous les personnages regardent vers la **droite** (angle 0°).

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

Lien direct d'une image (pour l'importer dans Codesters) :

```
https://raw.githubusercontent.com/Pwaluh/stages/master/sprites/NOM_DU_FICHIER.png
```

Codesters réduit les grandes images pour les faire tenir dans la scène : la map s'affiche à environ 300 px, il faut donc lui donner `map.set_size(6.8)` pour retrouver sa vraie taille.

## `game_design_explained/`

Des pages interactives à ouvrir dans le navigateur pour expliquer le jeu aux élèves.

- `aim_explained.html` : **Viser un zombie** – comment `atan2` donne l'angle pour que le soldat regarde la cible.
- `world_scrolling_explained.html` : **La carte qui glisse** – pourquoi l'hélico, les zombies et les balles doivent bouger en même temps que la map.
