# ==========================================================
#  SPACE INVADERS – ÉTAPE 1 (bonus) : le joueur
# ==========================================================

# ---------- les images (à adapter : Codesters ajoute un suffixe aux images importées) ----------
IMG_BACKGROUND = "background_space_e4b"
IMG_PLAYER = "space_invaders_player_b44"


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


# ---------- les listes : tout ce qu'on devra retrouver plus tard ----------


# ---------- le joueur ----------
player = codesters.Sprite(IMG_PLAYER, 0, PLAYER_Y)

def left_key():
    if player.get_x() > -225:          # on ne sort pas de l'écran
        player.set_x(player.get_x() - PLAYER_STEP)

def right_key():
    if player.get_x() < 225:
        player.set_x(player.get_x() + PLAYER_STEP)


# ---------- c'est parti ----------

stage.event_key("left", left_key)
stage.event_key("right", right_key)
stage.event_key("q", left_key)
stage.event_key("d", right_key)
