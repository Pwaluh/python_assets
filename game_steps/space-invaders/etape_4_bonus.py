# ==========================================================
#  SPACE INVADERS – ÉTAPE 4 (bonus) : les tirs ennemis et les vies
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

# --- bonus 1 : l'écran d'accueil ---
def tutorial():
    text = "Welcome!!!\n Left / right (or Q / D) to move"
    text = text + "\n Space to shoot"
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
PLAYER_LASER_SPEED = 14      # pixels par tic, vers le haut
MAX_PLAYER_LASERS = 3        # bonus 3 : pas plus de 3 tirs à l'écran
POINTS = {                   # bonus 3 : chaque alien rapporte des points différents
    "alien_orbe_1_d12": 30,
    "alien_meduse_1_49b": 20,
    "alien_drone_1_f72": 10
}
ALIEN_LASER_SPEED = 6        # pixels par tic, vers le bas
ALIEN_FIRE_EVERY = 25        # un alien tire tous les 25 tics
LAND_Y = -165                # bonus 3 : si un alien descend jusqu'ici, c'est perdu

score = 0
lives = 10
tick_count = 0
direction = 1                # 1 = vers la droite, -1 = vers la gauche

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
    if len(player_lasers) >= MAX_PLAYER_LASERS:     # bonus 3
        return
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
        score += POINTS[sprite.get_name()]
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

# --- bonus 2 : la flotte avance ---
def fleet_delay():
    # bonus 4 : moins il reste d'aliens, plus la flotte va vite
    return 2 + len(invaders) // 5

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
        landed = False
        for invader in invaders:
            invader.set_y(invader.get_y() - 20)
            if invader.get_y() < LAND_Y:
                landed = True
        if landed:                     # bonus 3 : une seule fin de partie
            game_over("INVADED!!!", "red")
    # 3. sinon : toute la flotte avance
    else:
        for invader in invaders:
            invader.set_x(invader.get_x() + FLEET_STEP * direction)


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
    elif hit_sprite in invaders:       # bonus 4 : un alien percute le joueur
        game_over("GAME OVER", "red")


# ---------- le battement du jeu ----------
# Codesters ne garde qu'UN SEUL event_interval :
# tout ce qui se répète passe par cette fonction.
def tick():
    global tick_count
    tick_count += 1
    move_lasers()
    if len(invaders) > 0 and tick_count % fleet_delay() == 0:
        move_fleet()
    if len(invaders) > 0 and tick_count % ALIEN_FIRE_EVERY == 0:
        alien_fire()


# ---------- c'est parti ----------
spawn_invaders()
player.event_collision(player_hit)

stage.event_key("left", left_key)
stage.event_key("right", right_key)
stage.event_key("q", left_key)
stage.event_key("d", right_key)
stage.event_key("space", player_fire)
stage.event_interval(tick, 0.05)
