# ==========================================================
#  ÉTAPE 5 (base) : la victoire et la défaite
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

# --- étape 3 : les zombies ---
zombies = []                # la liste des zombies vivants
respawn_list = [-270, 270]  # ils arrivent par le haut ou par le bas
ZOMBIE_SPEED = 3            # pixels par tic
tick_count = 0

# --- étape 5 : les points de vie ---
hp = 10
hp_display = codesters.Text("PV : " + str(hp), -170, -200, "red")


# Angle (en degrés) pour regarder de (x, y) vers (x_dest, y_dest)
def rotate_character(x_dest, y_dest, x, y):
    angle = math.atan2(y_dest - y, x_dest - x)
    return math.degrees(angle)

# --- étape 1 : faire glisser le monde ---
def move_world(dx, dy):
    for item in world + zombies:
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

# --- étape 3 : un nouveau zombie ---
def zombie_respawn():
    zombie = codesters.Sprite("zombie_1_873", random.randint(-270, 270), random.choice(respawn_list))
    zombie.event_collision(zombie_collision)
    zombies.append(zombie)

# --- étape 3 : chaque zombie fait un pas vers le joueur ---
def move_zombies():
    for zombie in zombies:
        degrees = rotate_character(player.get_x(), player.get_y(), zombie.get_x(), zombie.get_y())
        angle = math.radians(degrees)
        zombie.set_position(zombie.get_x() + math.cos(angle) * ZOMBIE_SPEED,
                            zombie.get_y() + math.sin(angle) * ZOMBIE_SPEED)

# --- étape 4 : tirer vers la souris ---
def shoot():
    angle = rotate_character(stage.mouse_x(), stage.mouse_y(), player.get_x(), player.get_y())
    x = player.get_x()
    y = player.get_y()
    bullet = codesters.Sprite("bullet_1e9", x, y)
    bullet.rotate_about(angle, x, y)
    bullet.move_forward(1000)
    stage.remove_sprite(bullet)

# --- étape 4 : une balle touche un zombie ---
def zombie_collision(sprite, hit_sprite):
    if hit_sprite.get_name() == "bullet_1e9":
        if sprite in zombies:
            zombies.remove(sprite)   # on l'enlève aussi de la liste !
        stage.remove_sprite(sprite)
        stage.remove_sprite(hit_sprite)

# --- étape 5 : le joueur touche quelque chose ---
def player_collision(sprite, hit_sprite):
    global hp, hp_display
    name = hit_sprite.get_name()
    if name == "zombie_1_873":
        if hit_sprite in zombies:
            zombies.remove(hit_sprite)
        stage.remove_sprite(hit_sprite)
        hp = hp - 1
        stage.remove_sprite(hp_display)
        hp_display = codesters.Text("PV : " + str(hp), -170, -200, "red")
        if hp == 0:
            stage.remove_sprite(sprite)
            codesters.Text("You Lose!!!", 0, 0, "red").set_size(4)
            stage.remove_all_events()
    if name == "helicopter_dfe":
        codesters.Text("You Win!!!", 0, 0, "green").set_size(4)
        stage.remove_all_events()
        stage.remove_sprite(sprite)

# Le battement du jeu : appelé toutes les 0,05 seconde.
# Codesters ne garde qu'UN SEUL event_interval : tout ce qui doit
# se répéter va donc dans cette fonction.
def tick():
    global tick_count
    tick_count = tick_count + 1
    if tick_count % 20 == 0:        # 20 tics x 0,05 s = 1 seconde
        zombie_respawn()
    move_zombies()


# ---------------- événements ----------------
stage.event_interval(tick, 0.05)
stage.event_click(shoot)
player.event_collision(player_collision)
stage.event_key("z", up_key)
stage.event_key("q", left_key)
stage.event_key("d", right_key)
stage.event_key("s", down_key)
