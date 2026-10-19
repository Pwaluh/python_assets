# ==========================================================
#  SPACE INVADERS – ÉTAPE 6 (base) : le boss
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
IMG_SHIELD_FULL = "shield_full_97b"
IMG_BOSS = "boss_xxx"                        # boss_1.png


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
TILE = 24
SHIELD_COLS = 3
SHIELD_ROWS = 2
SHIELD_GAP = 120
SHIELD_COUNT = 4
SHIELD_Y = -110
BOSS_FIRE_EVERY = 30

score = 0
lives = 10
shield = 2
player_damage = 2
boss_lives = 100
boss_is_alive = False
boss = None
tick_count = 0

# ---------- les listes : tout ce qu'on devra retrouver plus tard ----------
invaders = []
player_lasers = []
alien_lasers = []
shield_tiles = []


# ---------- l'affichage ----------
score_display = codesters.Text("Score: " + str(score), 170, 232, "white")
heart = codesters.Sprite(IMG_HEART, -205, -232)
lives_display = codesters.Text(str(lives), -175, -232, "red")
shield_sprite = codesters.Sprite(IMG_SHIELD_FULL, 145, -232)
shield_display = codesters.Text(str(shield), 175, -232, "green")
boss_lives_display = codesters.Text("Boss: " + str(boss_lives), -165, 232, "greenyellow")
boss_lives_display.hide()

# Codesters ne sait pas changer un texte : on l'efface et on le recrée
def update_hud():
    global score_display
    global lives_display
    global shield_display
    stage.remove_sprite(score_display)
    score_display = codesters.Text("Score: " + str(score), 170, 232, "white")
    stage.remove_sprite(lives_display)
    lives_display = codesters.Text(str(lives), -175, -232, "red")
    stage.remove_sprite(shield_display)
    shield_display = codesters.Text(str(shield), 175, -232, "green")

def update_boss_display():
    global boss_lives_display
    stage.remove_sprite(boss_lives_display)
    boss_lives_display = codesters.Text("Boss: " + str(boss_lives), -165, 232, "greenyellow")


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
            spawn_boss()

def spawn_invaders():
    for row in range(len(ROW_TYPES)):
        for col in range(COLS):
            x = START_X + col * GAP_X
            y = START_Y - row * GAP_Y
            invader = codesters.Sprite(ROW_TYPES[row], x, y)
            invader.event_collision(invader_hit)
            invaders.append(invader)


# ---------- les protections ----------
def make_tile(image, x, y):
    tile = codesters.Sprite(image, x, y)
    tile.event_collision(tile_hit)
    shield_tiles.append(tile)
    return tile

def destroy_tile(tile):
    if tile in shield_tiles:
        shield_tiles.remove(tile)
        stage.remove_sprite(tile)

def tile_hit(sprite, hit_sprite):
    # sprite = la tuile, hit_sprite = ce qui la touche
    # (les tirs du joueur traversent les protections)
    if hit_sprite in alien_lasers:
        remove_laser(hit_sprite)
        destroy_tile(sprite)

def build_shield(x, y):
    tiles = []
    row = 0
    while row < SHIELD_ROWS:
        col = 0
        while col < SHIELD_COLS:
            tile_x = x + (col - (SHIELD_COLS - 1) / 2) * TILE
            tile_y = y + row * TILE
            tiles.append(make_tile(IMG_SHIELD_FULL, tile_x, tile_y))
            col += 1
        row += 1
    return tiles

def build_wall(center_x, y, count):
    wall = []
    start_x = center_x - (count - 1) * SHIELD_GAP / 2
    k = 0
    while k < count:
        wall = wall + build_shield(start_x + k * SHIELD_GAP, y)
        k += 1
    return wall

def build_key():
    global shield
    if shield > 0:
        shield -= 1
        update_hud()
        build_shield(player.get_x(), player.get_y() + 45)   # juste devant le joueur


# ---------- le boss ----------
def spawn_boss():
    global boss, boss_is_alive
    boss = codesters.Sprite(IMG_BOSS, 0, 150)
    boss.event_collision(boss_hit)
    boss_is_alive = True
    boss_lives_display.show()

def boss_hit(sprite, hit_sprite):
    global boss_lives, boss_is_alive, score
    if hit_sprite in player_lasers and boss_is_alive:
        remove_laser(hit_sprite)
        boss_lives -= player_damage
        update_boss_display()
        if boss_lives <= 0:            # <= et pas == : on peut passer sous 0
            boss_is_alive = False
            stage.remove_sprite(sprite)
            score += 500
            update_hud()
            game_over("YOU WIN!!!", "green")

def boss_fire():
    # le boss vise le joueur, à 40 pixels près
    x = player.get_x() + random.randint(-40, 40)
    laser = codesters.Sprite(IMG_ALIEN_LASER, x, boss.get_y() - 25)
    alien_lasers.append(laser)


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
    if boss_is_alive:
        if tick_count % BOSS_FIRE_EVERY == 0:
            boss_fire()


# ---------- c'est parti ----------
spawn_invaders()
build_wall(0, SHIELD_Y, SHIELD_COUNT)
player.event_collision(player_hit)

stage.event_key("left", left_key)
stage.event_key("right", right_key)
stage.event_key("space", player_fire)
stage.event_key("z", build_key)
stage.event_interval(tick, 0.05)
