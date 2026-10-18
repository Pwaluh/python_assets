# ==========================================================
#  ÉTAPE 2 (base) : l'hélicoptère
# ==========================================================
import math
# random est déjà disponible dans Codesters

# --- étape 1 : la map et le joueur ---
map = codesters.Sprite("world_f41")
map.set_size(6.8)   # Codesters réduit la map à ~300 px : x 6,8 = 2048 px
world = [map]       # tout ce qui est DANS LE MONDE et glisse avec la map

# --- étape 2 : l'hélicoptère, dans un coin de la map ---
helicopter = codesters.Sprite("helicopter_dfe", 850, 850)
world.append(helicopter)

player = codesters.Sprite("player_df3")


# --- étape 1 : faire glisser le monde ---
def move_world(dx, dy):
    for item in world:
        item.set_position(item.get_x() + dx, item.get_y() + dy)

# Les 4 directions marchent pareil :
#   dans le carré du centre  -> le joueur bouge
#   au bord du carré         -> le monde glisse
#   au bord de la map        -> le joueur bouge jusqu'au bord de l'écran

def up_key():
    y = player.get_y()
    if y < 100:
        player.move_up(20)
    elif map.get_y() > -774:
        move_world(0, -20)
    elif y < 220:
        player.move_up(20)

def down_key():
    y = player.get_y()
    if y > -100:
        player.move_down(20)
    elif map.get_y() < 774:
        move_world(0, 20)
    elif y > -220:
        player.move_down(20)

def right_key():
    x = player.get_x()
    if x < 100:
        player.move_right(20)
    elif map.get_x() > -774:
        move_world(-20, 0)
    elif x < 220:
        player.move_right(20)

def left_key():
    x = player.get_x()
    if x > -100:
        player.move_left(20)
    elif map.get_x() < 774:
        move_world(20, 0)
    elif x > -220:
        player.move_left(20)


# ---------------- événements ----------------
stage.event_key("z", up_key)
stage.event_key("q", left_key)
stage.event_key("d", right_key)
stage.event_key("s", down_key)
