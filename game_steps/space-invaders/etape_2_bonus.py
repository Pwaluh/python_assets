# ==========================================================
#  SPACE INVADERS – ÉTAPE 2 (bonus) : les aliens
# ==========================================================

# ---------- les images (à adapter : Codesters ajoute un suffixe aux images importées) ----------
IMG_BACKGROUND = "background_space_e4b"
IMG_PLAYER = "space_invaders_player_b44"
ROW_TYPES = [
    "alien_orbe_1_d12", "alien_orbe_1_d12",
    "alien_meduse_1_49b", "alien_meduse_1_49b",
    "alien_drone_1_f72"
]


# ---------- le décor (créé en premier pour être derrière tout le reste) ----------
background = codesters.Sprite(IMG_BACKGROUND)
background.set_size(1.67)    # Codesters réduit le fond à ~300 px : x 1,67 = 500 px

# --- bonus 1 : l'écran d'accueil ---
def tutorial():
    text = "Welcome!!!\n Left / right (or Q / D) to move"
    guide = codesters.Text(text, 0, 0, "white")
    stage.wait(3)
    stage.remove_sprite(guide)

tutorial()


# ---------- les réglages ----------
PLAYER_Y = -195
PLAYER_STEP = 20
# la flotte : 5 rangées (ROW_TYPES) de 8 colonnes, centrée
COLS = 8
GAP_X = 50
GAP_Y = 44
START_X = -(COLS - 1) * GAP_X / 2
START_Y = 200
FLEET_STEP = 10              # bonus 2 : la flotte avance de 10 px à chaque pas

tick_count = 0
direction = 1                # 1 = vers la droite, -1 = vers la gauche

# ---------- les listes : tout ce qu'on devra retrouver plus tard ----------
invaders = []


# ---------- le joueur ----------
player = codesters.Sprite(IMG_PLAYER, 0, PLAYER_Y)

def left_key():
    if player.get_x() > -225:          # on ne sort pas de l'écran
        player.set_x(player.get_x() - PLAYER_STEP)

def right_key():
    if player.get_x() < 225:
        player.set_x(player.get_x() + PLAYER_STEP)


# ---------- les aliens ----------
def spawn_invaders():
    for row in range(len(ROW_TYPES)):
        for col in range(COLS):
            x = START_X + col * GAP_X
            y = START_Y - row * GAP_Y
            invader = codesters.Sprite(ROW_TYPES[row], x, y)
            invaders.append(invader)

# --- bonus 2 : la flotte avance ---
def fleet_delay():
    return 8                           # un pas tous les 8 tics

def move_fleet():
    global direction
    # 1. est-ce qu'un alien touche un bord ?
    hit_edge = False
    for invader in invaders:
        x = invader.get_x() + FLEET_STEP * direction
        if x > 230 or x < -230:
            hit_edge = True
    # 2. au bord : toute la flotte descend et repart dans l'autre sens
    if hit_edge:
        direction = -direction
        for invader in invaders:
            invader.set_y(invader.get_y() - 20)
    # 3. sinon : toute la flotte avance
    else:
        for invader in invaders:
            invader.set_x(invader.get_x() + FLEET_STEP * direction)


# ---------- le battement du jeu ----------
# Codesters ne garde qu'UN SEUL event_interval :
# tout ce qui se répète passe par cette fonction.
def tick():
    global tick_count
    tick_count += 1
    if len(invaders) > 0 and tick_count % fleet_delay() == 0:
        move_fleet()


# ---------- c'est parti ----------
spawn_invaders()

stage.event_key("left", left_key)
stage.event_key("right", right_key)
stage.event_key("q", left_key)
stage.event_key("d", right_key)
stage.event_interval(tick, 0.05)
