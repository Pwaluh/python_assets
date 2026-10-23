# ==========================================================
#  SPACE INVADERS – CODE À TROUS – VERSION FRANÇAISE
# ==========================================================
#  1. Remplace chaque ____ par le bon mot (le numéro du trou est en fin de ligne).
#  2. Mets le nom de tes images Codesters entre les guillemets "".
#  3. Lance le jeu : s'il y a une erreur, lis bien le numéro de ligne !
# ==========================================================

# ---------- les images : écris le nom que Codesters donne à chaque image ----------
IMG_FOND = ""            # fond_espace.png
IMG_JOUEUR = ""                # vaisseau_joueur.png
TYPES_RANGEES = [
    "", "",      # alien_orbe_1.png (2 rangées)
    "", "",      # alien_meduse_1.png (2 rangées)
    ""           # alien_drone_1.png
]
IMG_TIR_JOUEUR = ""          # tir_joueur.png
IMG_TIR_ALIEN = ""          # tir_alien_1.png
IMG_COEUR = ""                 # vie.png
IMG_BOUCLIER_INTACT = ""           # bouclier_intact.png
IMG_BOSS = ""                  # boss_1.png


# ---------- le décor (créé en premier pour être derrière tout le reste) ----------
fond = codesters.Sprite(IMG_FOND)
fond.set_size(1.67)    # Codesters réduit le fond à ~300 px : x 1,67 = 500 px


# ---------- les réglages ----------
JOUEUR_Y = -195
PAS_JOUEUR = 20
# la flotte : 5 rangées (TYPES_RANGEES) de 8 colonnes, centrée
COLONNES = 8
ECART_X = 50
ECART_Y = 44
DEPART_X = -(COLONNES - 1) * ECART_X / 2
DEPART_Y = 200
VITESSE_TIR_JOUEUR = 14      # pixels par tic, vers le haut
VITESSE_TIR_ALIEN = 6        # pixels par tic, vers le bas
TIR_ALIEN_TOUS_LES = 25        # un alien tire tous les 25 tics
TUILE = 24
COLONNES_BOUCLIER = 3
RANGEES_BOUCLIER = 2
ECART_BOUCLIERS = 120
NOMBRE_BOUCLIERS = 4
BOUCLIER_Y = -110
TIR_BOSS_TOUS_LES = 30

score = 0
vies = 10
boucliers = 2
degats_joueur = 2
vies_boss = 100
boss_en_vie = False
boss = None
compteur_tics = 0

# ---------- les listes : tout ce qu'on devra retrouver plus tard ----------
aliens = []
tirs_joueur = []
tirs_aliens = []
tuiles_bouclier = []


# ---------- l'affichage ----------
affichage_score = codesters.Text("Score: " + str(score), 170, 232, "white")
coeur = codesters.Sprite(IMG_COEUR, -205, -232)
affichage_vies = codesters.Text(str(vies), -175, -232, "red")
sprite_bouclier = codesters.Sprite(IMG_BOUCLIER_INTACT, 145, -232)
affichage_boucliers = codesters.Text(str(boucliers), 175, -232, "green")
affichage_vies_boss = codesters.Text("Boss: " + str(vies_boss), -165, 232, "greenyellow")
affichage_vies_boss.hide()

# Codesters ne sait pas changer un texte : on l'efface et on le recrée
def maj_affichage():
    ______ affichage_score          # trou 1
    global affichage_vies
    global affichage_boucliers
    stage.remove_sprite(affichage_score)
    affichage_score = codesters.Text("Score: " + str(score), 170, 232, "white")
    stage.remove_sprite(affichage_vies)
    affichage_vies = codesters.Text(str(vies), -175, -232, "red")
    stage.remove_sprite(affichage_boucliers)
    affichage_boucliers = codesters.Text(str(boucliers), 175, -232, "green")

___ maj_affichage_boss():         # trou 2
    global affichage_vies_boss
    stage.remove_sprite(affichage_vies_boss)
    affichage_vies_boss = codesters.Text("Boss: " + str(vies_boss), -165, 232, "greenyellow")


# ---------- le joueur ----------
joueur = codesters.Sprite(IMG_JOUEUR, 0, JOUEUR_Y)

def touche_gauche():
    __ joueur.get_x() > -225:          # on ne sort pas de l'écran   (trou 3)
        joueur.set_x(joueur.get_x() - PAS_JOUEUR)

def touche_droite():
    if joueur.get_x() < 225:
        joueur.______(joueur.get_x() + PAS_JOUEUR)     # trou 4


# ---------- fin de partie ----------
def fin_partie(message, couleur):
    texte_fin = codesters.Text(message, 0, 0, couleur)
    texte_fin.set_size(3)
    stage.remove_all_events()


# ---------- les tirs ----------
def retirer_tir(tir):
    # on retire le tir de SA liste, puis de la scène
    if tir in tirs_joueur:
        tirs_joueur.remove(tir)
        stage.remove_sprite(tir)
    ____ tir in tirs_aliens:       # trou 5
        tirs_aliens.remove(tir)
        stage.remove_sprite(tir)

def joueur_tire():
    tir = codesters.Sprite(IMG_TIR_JOUEUR, joueur.get_x(), joueur.get_y() + 25)
    tirs_joueur.______(tir)       # trou 6

def alien_tire():
    tireur = random.______(aliens)    # trou 7
    tir = codesters.Sprite(IMG_TIR_ALIEN, tireur.get_x(), tireur.get_y() - 20)
    tirs_aliens.append(tir)

def bouger_tirs():
    # [:] fait une COPIE de la liste : on peut retirer des tirs
    # de la vraie liste pendant qu'on parcourt la copie
    for tir in tirs_joueur[:]:
        tir.set_y(tir.get_y() + VITESSE_TIR_JOUEUR)
        if tir.get_y() > 260:
            retirer_tir(tir)
    for tir in tirs_aliens[:]:
        tir.set_y(tir.get_y() - VITESSE_TIR_ALIEN)
        if tir.get_y() < -260:
            retirer_tir(tir)


# ---------- les aliens ----------
def alien_touche(sprite, touche_par):
    # sprite     = l'alien touché (le bon, donné par Codesters)
    # touche_par = ce qui l'a touché
    global score
    if touche_par in tirs_joueur and sprite in aliens:
        aliens.______(sprite)       # trou 8
        stage.remove_sprite(sprite)
        retirer_tir(touche_par)
        score += 10
        maj_affichage()
        if ___(aliens) == 0:        # trou 9
            creer_boss()

def creer_aliens():
    for rangee in range(len(TYPES_RANGEES)):
        for colonne in range(COLONNES):
            x = DEPART_X + colonne * ECART_X
            y = DEPART_Y - rangee * ECART_Y
            alien = codesters.Sprite(TYPES_RANGEES[rangee], x, y)
            alien.event_collision(__________)     # trou 10
            aliens.append(alien)


# ---------- les protections ----------
def creer_tuile(image, x, y):
    tuile = codesters.Sprite(image, x, y)
    tuile.event_collision(tuile_touchee)
    tuiles_bouclier.append(tuile)
    ______ tuile                       # trou 11

def detruire_tuile(tuile):
    if tuile in tuiles_bouclier:
        tuiles_bouclier.remove(tuile)
        stage.remove_sprite(tuile)

def tuile_touchee(sprite, touche_par):
    # sprite = la tuile, touche_par = ce qui la touche
    # (les tirs du joueur traversent les protections)
    if touche_par in tirs_aliens:
        retirer_tir(touche_par)
        detruire_tuile(sprite)

def construire_bouclier(x, y):
    tuiles = []
    rangee = 0
    _____ rangee < RANGEES_BOUCLIER:          # trou 12
        colonne = 0
        while colonne < COLONNES_BOUCLIER:
            tuile_x = x + (colonne - (COLONNES_BOUCLIER - 1) / 2) * TUILE
            tuile_y = y + rangee * TUILE
            tuiles.append(creer_tuile(IMG_BOUCLIER_INTACT, tuile_x, tuile_y))
            colonne __ 1                  # trou 13
        rangee += 1
    return tuiles

def construire_mur(centre_x, y, nombre):
    mur = []
    debut_x = centre_x - (nombre - 1) * ECART_BOUCLIERS / 2
    k = 0
    while k < nombre:
        mur = mur + construire_bouclier(debut_x + k * ECART_BOUCLIERS, y)
        k += 1
    return mur

def touche_bouclier():
    global boucliers
    if boucliers _ 0:                    # trou 14
        boucliers -= 1
        maj_affichage()
        construire_bouclier(joueur.get_x(), joueur.get_y() + 45)   # juste devant le joueur


# ---------- le boss ----------
def creer_boss():
    global boss, boss_en_vie
    boss = codesters.Sprite(IMG_BOSS, 0, 150)
    boss.event_collision(boss_touche)
    boss_en_vie = ____              # trou 15
    affichage_vies_boss.show()

def boss_touche(sprite, touche_par):
    global vies_boss, boss_en_vie, score
    if touche_par in tirs_joueur and boss_en_vie:
        retirer_tir(touche_par)
        vies_boss -= _____________   # trou 16
        maj_affichage_boss()
        if vies_boss __ 0:            # on peut passer sous 0 !   (trou 17)
            boss_en_vie = False
            stage.remove_sprite(sprite)
            score += 500
            maj_affichage()
            fin_partie("GAGNÉ !!!", "green")

def boss_tire():
    # le boss vise le joueur, à 40 pixels près
    x = joueur.get_x() + random.randint(-40, 40)
    tir = codesters.Sprite(IMG_TIR_ALIEN, x, boss.get_y() - 25)
    tirs_aliens.append(tir)


# ---------- le joueur touché ----------
def joueur_touche(sprite, touche_par):
    global vies
    if touche_par in tirs_aliens:
        retirer_tir(touche_par)
        vies -= 1
        maj_affichage()
        if vies <= 0:
            stage.remove_sprite(sprite)
            _________("PERDU !!!", "red")     # trou 18


# ---------- le battement du jeu ----------
# Codesters ne garde qu'UN SEUL event_interval :
# tout ce qui se répète passe par cette fonction.
def tic():
    global compteur_tics
    compteur_tics += 1
    ___________()                     # trou 19
    if len(aliens) > 0 and compteur_tics % TIR_ALIEN_TOUS_LES == 0:
        alien_tire()
    if boss_en_vie:
        if compteur_tics % TIR_BOSS_TOUS_LES == 0:
            boss_tire()


# ---------- c'est parti ----------
creer_aliens()
construire_mur(0, BOUCLIER_Y, NOMBRE_BOUCLIERS)
joueur.event_collision(joueur_touche)

stage.event_key("left", touche_gauche)
stage.event_key("right", touche_droite)
stage.event_key("_____", joueur_tire)     # trou 20
stage.event_key("z", touche_bouclier)
stage.event_interval(____, 0.05)          # trou 21
