# ==========================================================
#  SPACE INVADERS (BONUS) – CODE À TROUS
# ==========================================================
#  1. Remplace chaque ____ par le bon mot (le numéro du trou est en fin de ligne).
#  2. Mets le nom de tes images Codesters entre les guillemets "".
#  3. Lance le jeu : s'il y a une erreur, lis bien le numéro de ligne !
# ==========================================================

# ---------- les images : écris le nom que Codesters donne à chaque image ----------
IMG_BACKGROUND = ""            # fond_espace.png
IMG_PLAYER = ""                # vaisseau_joueur.png
ROW_TYPES = [
    "", "",      # alien_orbe_1.png (2 rangées)
    "", "",      # alien_meduse_1.png (2 rangées)
    ""           # alien_drone_1.png
]
IMG_PLAYER_LASER = ""          # tir_joueur.png
IMG_ALIEN_LASER = ""           # tir_alien_1.png
IMG_HEART = ""                 # vie.png
IMG_SHIELD_FULL = ""           # bouclier_intact.png
IMG_SHIELD_DAMAGED = ""        # bouclier_abime.png
IMG_SHIELD_BROKEN = ""         # bouclier_casse.png
IMG_BOSS = ""                  # boss_1.png


# ---------- le décor (créé en premier pour être derrière tout le reste) ----------
background = codesters.Sprite(IMG_BACKGROUND)
background.set_size(1.67)    # Codesters réduit le fond à ~300 px : x 1,67 = 500 px

# --- bonus 1 : l'écran d'accueil ---
def tutorial():
    text = "Welcome!!!\n Left / right (or Q / D) to move"
    text = text + "\n Space to shoot"
    text = text + "\n Z to build a shield in front of you"
    guide = codesters.____(text, 0, 0, "white")     # trou 1
    stage.____(3)                     # trou 2
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
    "": 30,                  # même nom que l'orbe dans ROW_TYPES
    "": 20,                  # même nom que la méduse
    "": 10                   # même nom que le drone
}
ALIEN_LASER_SPEED = 6        # pixels par tic, vers le bas
ALIEN_FIRE_EVERY = 25        # un alien tire tous les 25 tics
LAND_Y = -165                # bonus 3 : si un alien descend jusqu'ici, c'est perdu
TILE = 24
SHIELD_COLS = 3
SHIELD_ROWS = 2
SHIELD_GAP = 120
SHIELD_COUNT = 4
SHIELD_Y = -110
BOSS_FIRE_EVERY = 30
BOSS_SPEED = 2               # bonus 6 : le boss se déplace

score = 0
lives = 10
shield = 2
player_damage = 2
boss_lives = 100
boss_is_alive = False
boss = None
tick_count = 0
direction = 1                # 1 = vers la droite, -1 = vers la gauche
boss_direction = 1
boss_flash = 0

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
        player.set_x(player.get_x() _ PLAYER_STEP)     # trou 3

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
    if laser __ player_lasers:        # trou 4
        player_lasers.remove(laser)
        stage.remove_sprite(laser)
    elif laser in alien_lasers:
        alien_lasers.remove(laser)
        stage.remove_sprite(laser)

def player_fire():
    if len(player_lasers) __ MAX_PLAYER_LASERS:     # bonus 3   (trou 5)
        ______                        # trou 6
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
    if hit_sprite in player_lasers ___ sprite in invaders:     # trou 7
        invaders.remove(sprite)
        stage.remove_sprite(sprite)
        remove_laser(hit_sprite)
        score += POINTS[sprite.________()]     # trou 8
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

# --- bonus 2 : la flotte avance ---
def fleet_delay():
    # bonus 4 : moins il reste d'aliens, plus la flotte va vite
    return 2 + len(invaders) // 5

def move_fleet():
    global direction
    # 1. est-ce qu'un alien touche un bord ?
    hit_edge = _____                  # trou 9
    for invader in invaders:
        x = invader.get_x() + FLEET_STEP * direction
        if x > 230 __ x < -230:       # trou 10
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
    ____:                             # trou 11
        for invader in invaders:
            invader.set_x(invader.get_x() + FLEET_STEP * direction)


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

# --- bonus 5 : une tuile s'abîme avant de disparaître ---
NEXT_STATE = {
    IMG_SHIELD_FULL: IMG_SHIELD_DAMAGED,
    IMG_SHIELD_DAMAGED: IMG_SHIELD_BROKEN
}

def damage_tile(tile):
    if tile in shield_tiles:
        name = tile.get_name()
        x = tile.get_x()
        y = tile.get_y()
        destroy_tile(tile)
        if name in NEXT_STATE:         # après "cassé" : rien, la tuile a disparu
            make_tile(__________[name], x, y)     # trou 12

def tile_hit(sprite, hit_sprite):
    # sprite = la tuile, hit_sprite = ce qui la touche
    # (les tirs du joueur traversent les protections)
    if hit_sprite in alien_lasers:
        remove_laser(hit_sprite)
        ___________(sprite)           # trou 13
    elif hit_sprite in invaders:       # bonus 5 : un alien écrase la protection
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
    k = _                             # trou 14
    while k < count:
        wall = wall + build_shield(start_x + k * SHIELD_GAP, y)
        k += 1
    return wall

def build_key():
    global shield
    if shield > 0:
        shield __ 1                   # trou 15
        update_hud()
        build_shield(player.get_x(), player.get_y() + 45)   # juste devant le joueur


# ---------- le boss ----------
def spawn_boss():
    global boss, boss_is_alive
    boss = codesters.Sprite(IMG_BOSS, 0, 150)
    boss.event_collision(boss_hit)
    boss_is_alive = True
    boss_lives_display.____()         # trou 16

def boss_hit(sprite, hit_sprite):
    global boss_lives, boss_is_alive, score
    global boss_flash
    if hit_sprite in player_lasers and boss_is_alive:
        remove_laser(hit_sprite)
        boss_lives -= player_damage
        update_boss_display()
        sprite.___________(0.5)        # bonus 6 : le boss clignote quand il est touché   (trou 17)
        boss_flash = 3                 # ... pendant 3 tics
        if boss_lives <= 0:            # <= et pas == : on peut passer sous 0
            boss_is_alive = False
            stage.remove_sprite(sprite)
            score += 500
            update_hud()
            game_over("YOU WIN!!!", "green")

# --- bonus 6 : le boss se déplace et tire d'un de ses trois canons ---
def move_boss():
    global boss_direction
    x = boss.get_x() + __________ * boss_direction     # trou 18
    if x > 200 or x < -200:
        boss_direction = -boss_direction
    else:
        boss.set_x(x)

def boss_fire():
    offset = random.choice([-25, 0, 25])
    laser = codesters.Sprite(IMG_ALIEN_LASER, boss.get_x() + offset, boss.get_y() - 25)
    ____________.append(laser)        # trou 19


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
    elif hit_sprite in ________:       # bonus 4 : un alien percute le joueur   (trou 20)
        game_over("GAME OVER", "red")


# ---------- le battement du jeu ----------
# Codesters ne garde qu'UN SEUL event_interval :
# tout ce qui se répète passe par cette fonction.
def tick():
    global tick_count
    global boss_flash
    tick_count += 1
    move_lasers()
    if len(invaders) > 0 and tick_count % fleet_delay() == 0:
        move_fleet()
    if len(invaders) > 0 and tick_count % ALIEN_FIRE_EVERY == 0:
        alien_fire()
    if boss_is_alive:
        _________()                   # trou 22
        if boss_flash > 0:
            boss_flash -= 1
            if boss_flash __ 0:       # trou 21
                boss.set_opacity(1)
        if tick_count % BOSS_FIRE_EVERY == 0:
            boss_fire()


# ---------- c'est parti ----------
spawn_invaders()
build_wall(0, SHIELD_Y, SHIELD_COUNT)
player.event_collision(player_hit)

stage.event_key("left", left_key)
stage.event_key("right", right_key)
stage.event_key("q", ________)     # trou 23
stage.event_key("d", right_key)
stage.event_key("space", player_fire)
stage.event_key("_", build_key)    # trou 24
stage.event_interval(tick, 0.05)
