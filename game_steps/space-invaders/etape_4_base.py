# ==========================================================
#  SPACE INVADERS – ÉTAPE 4 (base) : les tirs ennemis et les vies
# ==========================================================

# ---------- les images (à adapter : Codesters ajoute un suffixe aux images importées) ----------
IMG_BACKGROUND = "background_space_e4b"
IMG_PLAYER = "space_invaders_player_b44"
ROW_TYPES = [
    "alien_orbe_1_d12", "alien_orbe_1_d12",
    "alien_meduse_1_49b", "alien_meduse_1_49b",
    "alien_drone_1_f72"
]
IMG_PLAYER_LASER = "player_laser_320"
IMG_ALIEN_LASER = "alien_laser_xxx"          # tir_alien_1.png
IMG_HEART = "heart_5c9"


# ---------- le décor (créé en premier pour être derrière tout le reste) ----------
background = codesters.Sprite(IMG_BACKGROUND)
background.set_size(1.67)    # Codesters réduit le fond à ~300 px : x 1,67 = 500 px


# ---------- les réglages ----------
PLAYER_Y = -195
PLAYER_STEP = 20
# la flotte : 5 rangées (ROW_TYPES) de 8 colonnes, centrée
COLS = 8
GAP_X = 50
GAP_Y = 44
START_X = -(COLS - 1) * GAP_X / 2
START_Y = 200
PLAYER_LASER_SPEED = 14      # pixels par tic, vers le haut
ALIEN_LASER_SPEED = 6        # pixels par tic, vers le bas
ALIEN_FIRE_EVERY = 25        # un alien tire tous les 25 tics

score = 0
lives = 10
tick_count = 0

# ---------- les listes : tout ce qu'on devra retrouver plus tard ----------
invaders = []
player_lasers = []
alien_lasers = []


# ---------- l'affichage ----------
score_display = codesters.Text("Score: " + str(score), 170, 232, "white")
heart = codesters.Sprite(IMG_HEART, -205, -232)
lives_display = codesters.Text(str(lives), -175, -232, "red")

# Codesters ne sait pas changer un texte : on l'efface et on le recrée
def update_hud():
    global score_display
    global lives_display
    stage.remove_sprite(score_display)
    score_display = codesters.Text("Score: " + str(score), 170, 232, "white")
    stage.remove_sprite(lives_display)
    lives_display = codesters.Text(str(lives), -175, -232, "red")


# ---------- le joueur ----------
player = codesters.Sprite(IMG_PLAYER, 0, PLAYER_Y)

def left_key():
    if player.get_x() > -225:          # on ne sort pas de l'écran
        player.set_x(player.get_x() - PLAYER_STEP)

def right_key():
    if player.get_x() < 225:
        player.set_x(player.get_x() + PLAYER_STEP)


# ---------- fin de partie ----------
def game_over(message, color):
    end_text = codesters.Text(message, 0, 0, color)
    end_text.set_size(3)
    stage.remove_all_events()


# ---------- les tirs ----------
def remove_laser(laser):
    # on retire le tir de SA liste, puis de la scène
    if laser in player_lasers:
        player_lasers.remove(laser)
        stage.remove_sprite(laser)
    elif laser in alien_lasers:
        alien_lasers.remove(laser)
        stage.remove_sprite(laser)

def player_fire():
    laser = codesters.Sprite(IMG_PLAYER_LASER, player.get_x(), player.get_y() + 25)
    player_lasers.append(laser)

def alien_fire():
    shooter = random.choice(invaders)
    laser = codesters.Sprite(IMG_ALIEN_LASER, shooter.get_x(), shooter.get_y() - 20)
    alien_lasers.append(laser)

def move_lasers():
    # [:] fait une COPIE de la liste : on peut retirer des tirs
    # de la vraie liste pendant qu'on parcourt la copie
    for laser in player_lasers[:]:
        laser.set_y(laser.get_y() + PLAYER_LASER_SPEED)
        if laser.get_y() > 260:
            remove_laser(laser)
    for laser in alien_lasers[:]:
        laser.set_y(laser.get_y() - ALIEN_LASER_SPEED)
        if laser.get_y() < -260:
            remove_laser(laser)


# ---------- les aliens ----------
def invader_hit(sprite, hit_sprite):
    # sprite     = l'alien touché (le bon, donné par Codesters)
    # hit_sprite = ce qui l'a touché
    global score
    if hit_sprite in player_lasers and sprite in invaders:
        invaders.remove(sprite)
        stage.remove_sprite(sprite)
        remove_laser(hit_sprite)
        score += 10
        update_hud()
        if len(invaders) == 0:
            game_over("YOU WIN!!!", "green")

def spawn_invaders():
    for row in range(len(ROW_TYPES)):
        for col in range(COLS):
            x = START_X + col * GAP_X
            y = START_Y - row * GAP_Y
            invader = codesters.Sprite(ROW_TYPES[row], x, y)
            invader.event_collision(invader_hit)
            invaders.append(invader)


# ---------- le joueur touché ----------
def player_hit(sprite, hit_sprite):
    global lives
    if hit_sprite in alien_lasers:
        remove_laser(hit_sprite)
        lives -= 1
        update_hud()
        if lives <= 0:
            stage.remove_sprite(sprite)
            game_over("GAME OVER", "red")


# ---------- le battement du jeu ----------
# Codesters ne garde qu'UN SEUL event_interval :
# tout ce qui se répète passe par cette fonction.
def tick():
    global tick_count
    tick_count += 1
    move_lasers()
    if len(invaders) > 0 and tick_count % ALIEN_FIRE_EVERY == 0:
        alien_fire()


# ---------- c'est parti ----------
spawn_invaders()
player.event_collision(player_hit)

stage.event_key("left", left_key)
stage.event_key("right", right_key)
stage.event_key("space", player_fire)
stage.event_interval(tick, 0.05)
