# ==========================================================
#  SPACE INVADERS (BONUS) – CODE À TROUS – VERSION FRANÇAISE
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
IMG_TIR_ALIEN = ""           # tir_alien_1.png
IMG_COEUR = ""                 # vie.png
IMG_BOUCLIER_INTACT = ""           # bouclier_intact.png
IMG_BOUCLIER_ABIME = ""        # bouclier_abime.png
IMG_BOUCLIER_CASSE = ""         # bouclier_casse.png
IMG_BOSS = ""                  # boss_1.png


# ---------- le décor (créé en premier pour être derrière tout le reste) ----------
fond = codesters.Sprite(IMG_FOND)
fond.set_size(1.67)    # Codesters réduit le fond à ~300 px : x 1,67 = 500 px

# --- bonus 1 : l'écran d'accueil ---
def tutoriel():
    texte = "Bienvenue !!!\n Gauche / droite (ou Q / D) pour bouger"
    texte = texte + "\n Espace pour tirer"
    texte = texte + "\n Z pour poser un bouclier devant toi"
    guide = codesters.____(texte, 0, 0, "white")     # trou 1
    stage.____(3)                     # trou 2
    stage.remove_sprite(guide)

tutoriel()


# ---------- les réglages ----------
JOUEUR_Y = -195
PAS_JOUEUR = 20
# la flotte : 5 rangées (TYPES_RANGEES) de 8 colonnes, centrée
COLONNES = 8
ECART_X = 50
ECART_Y = 44
DEPART_X = -(COLONNES - 1) * ECART_X / 2
DEPART_Y = 200
PAS_FLOTTE = 10              # bonus 2 : la flotte avance de 10 px à chaque pas
VITESSE_TIR_JOUEUR = 14      # pixels par tic, vers le haut
MAX_TIRS_JOUEUR = 3        # bonus 3 : pas plus de 3 tirs à l'écran
POINTS = {                   # bonus 3 : chaque alien rapporte des points différents
    "": 30,                  # même nom que l'orbe dans TYPES_RANGEES
    "": 20,                  # même nom que la méduse
    "": 10                   # même nom que le drone
}
VITESSE_TIR_ALIEN = 6        # pixels par tic, vers le bas
TIR_ALIEN_TOUS_LES = 25        # un alien tire tous les 25 tics
ATTERRISSAGE_Y = -165                # bonus 3 : si un alien descend jusqu'ici, c'est perdu
TUILE = 24
COLONNES_BOUCLIER = 3
RANGEES_BOUCLIER = 2
ECART_BOUCLIERS = 120
NOMBRE_BOUCLIERS = 4
BOUCLIER_Y = -110
TIR_BOSS_TOUS_LES = 30
VITESSE_BOSS = 2               # bonus 6 : le boss se déplace

score = 0
vies = 10
boucliers = 2
degats_joueur = 2
vies_boss = 100
boss_en_vie = False
boss = None
compteur_tics = 0
direction = 1                # 1 = vers la droite, -1 = vers la gauche
direction_boss = 1
clignotement_boss = 0

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
    global affichage_score
    global affichage_vies
    global affichage_boucliers
    stage.remove_sprite(affichage_score)
    affichage_score = codesters.Text("Score: " + str(score), 170, 232, "white")
    stage.remove_sprite(affichage_vies)
    affichage_vies = codesters.Text(str(vies), -175, -232, "red")
    stage.remove_sprite(affichage_boucliers)
    affichage_boucliers = codesters.Text(str(boucliers), 175, -232, "green")

def maj_affichage_boss():
    global affichage_vies_boss
    stage.remove_sprite(affichage_vies_boss)
    affichage_vies_boss = codesters.Text("Boss: " + str(vies_boss), -165, 232, "greenyellow")


# ---------- le joueur ----------
joueur = codesters.Sprite(IMG_JOUEUR, 0, JOUEUR_Y)

def touche_gauche():
    if joueur.get_x() > -225:          # on ne sort pas de l'écran
        joueur.set_x(joueur.get_x() _ PAS_JOUEUR)     # trou 3

def touche_droite():
    if joueur.get_x() < 225:
        joueur.set_x(joueur.get_x() + PAS_JOUEUR)


# ---------- fin de partie ----------
def fin_partie(message, couleur):
    texte_fin = codesters.Text(message, 0, 0, couleur)
    texte_fin.set_size(3)
    stage.remove_all_events()


# ---------- les tirs ----------
def retirer_tir(tir):
    # on retire le tir de SA liste, puis de la scène
    if tir __ tirs_joueur:        # trou 4
        tirs_joueur.remove(tir)
        stage.remove_sprite(tir)
    elif tir in tirs_aliens:
        tirs_aliens.remove(tir)
        stage.remove_sprite(tir)

def joueur_tire():
    if len(tirs_joueur) __ MAX_TIRS_JOUEUR:     # bonus 3   (trou 5)
        ______                        # trou 6
    tir = codesters.Sprite(IMG_TIR_JOUEUR, joueur.get_x(), joueur.get_y() + 25)
    tirs_joueur.append(tir)

def alien_tire():
    tireur = random.choice(aliens)
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
    if touche_par in tirs_joueur ___ sprite in aliens:     # trou 7
        aliens.remove(sprite)
        stage.remove_sprite(sprite)
        retirer_tir(touche_par)
        score += POINTS[sprite.________()]     # trou 8
        maj_affichage()
        if len(aliens) == 0:
            creer_boss()

def creer_aliens():
    for rangee in range(len(TYPES_RANGEES)):
        for colonne in range(COLONNES):
            x = DEPART_X + colonne * ECART_X
            y = DEPART_Y - rangee * ECART_Y
            alien = codesters.Sprite(TYPES_RANGEES[rangee], x, y)
            alien.event_collision(alien_touche)
            aliens.append(alien)

# --- bonus 2 : la flotte avance ---
def delai_flotte():
    # bonus 4 : moins il reste d'aliens, plus la flotte va vite
    return 2 + len(aliens) // 5

def bouger_flotte():
    global direction
    # 1. est-ce qu'un alien touche un bord ?
    bord_touche = _____                  # trou 9
    for alien in aliens:
        x = alien.get_x() + PAS_FLOTTE * direction
        if x > 230 __ x < -230:       # trou 10
            bord_touche = True
    # 2. au bord : toute la flotte descend et repart dans l'autre sens
    if bord_touche:
        direction = -direction
        atterri = False
        for alien in aliens:
            alien.set_y(alien.get_y() - 20)
            if alien.get_y() < ATTERRISSAGE_Y:
                atterri = True
        if atterri:                     # bonus 3 : une seule fin de partie
            fin_partie("ENVAHIS !!!", "red")
    # 3. sinon : toute la flotte avance
    ____:                             # trou 11
        for alien in aliens:
            alien.set_x(alien.get_x() + PAS_FLOTTE * direction)


# ---------- les protections ----------
def creer_tuile(image, x, y):
    tuile = codesters.Sprite(image, x, y)
    tuile.event_collision(tuile_touchee)
    tuiles_bouclier.append(tuile)
    return tuile

def detruire_tuile(tuile):
    if tuile in tuiles_bouclier:
        tuiles_bouclier.remove(tuile)
        stage.remove_sprite(tuile)

# --- bonus 5 : une tuile s'abîme avant de disparaître ---
ETAT_SUIVANT = {
    IMG_BOUCLIER_INTACT: IMG_BOUCLIER_ABIME,
    IMG_BOUCLIER_ABIME: IMG_BOUCLIER_CASSE
}

def abimer_tuile(tuile):
    if tuile in tuiles_bouclier:
        nom = tuile.get_name()
        x = tuile.get_x()
        y = tuile.get_y()
        detruire_tuile(tuile)
        if nom in ETAT_SUIVANT:         # après "cassé" : rien, la tuile a disparu
            creer_tuile(__________[nom], x, y)     # trou 12

def tuile_touchee(sprite, touche_par):
    # sprite = la tuile, touche_par = ce qui la touche
    # (les tirs du joueur traversent les protections)
    if touche_par in tirs_aliens:
        retirer_tir(touche_par)
        ___________(sprite)           # trou 13
    elif touche_par in aliens:       # bonus 5 : un alien écrase la protection
        detruire_tuile(sprite)

def construire_bouclier(x, y):
    tuiles = []
    rangee = 0
    while rangee < RANGEES_BOUCLIER:
        colonne = 0
        while colonne < COLONNES_BOUCLIER:
            tuile_x = x + (colonne - (COLONNES_BOUCLIER - 1) / 2) * TUILE
            tuile_y = y + rangee * TUILE
            tuiles.append(creer_tuile(IMG_BOUCLIER_INTACT, tuile_x, tuile_y))
            colonne += 1
        rangee += 1
    return tuiles

def construire_mur(centre_x, y, nombre):
    mur = []
    debut_x = centre_x - (nombre - 1) * ECART_BOUCLIERS / 2
    k = _                             # trou 14
    while k < nombre:
        mur = mur + construire_bouclier(debut_x + k * ECART_BOUCLIERS, y)
        k += 1
    return mur

def touche_bouclier():
    global boucliers
    if boucliers > 0:
        boucliers __ 1                   # trou 15
        maj_affichage()
        construire_bouclier(joueur.get_x(), joueur.get_y() + 45)   # juste devant le joueur


# ---------- le boss ----------
def creer_boss():
    global boss, boss_en_vie
    boss = codesters.Sprite(IMG_BOSS, 0, 150)
    boss.event_collision(boss_touche)
    boss_en_vie = True
    affichage_vies_boss.____()         # trou 16

def boss_touche(sprite, touche_par):
    global vies_boss, boss_en_vie, score
    global clignotement_boss
    if touche_par in tirs_joueur and boss_en_vie:
        retirer_tir(touche_par)
        vies_boss -= degats_joueur
        maj_affichage_boss()
        sprite.___________(0.5)        # bonus 6 : le boss clignote quand il est touché   (trou 17)
        clignotement_boss = 3                 # ... pendant 3 tics
        if vies_boss <= 0:            # <= et pas == : on peut passer sous 0
            boss_en_vie = False
            stage.remove_sprite(sprite)
            score += 500
            maj_affichage()
            fin_partie("GAGNÉ !!!", "green")

# --- bonus 6 : le boss se déplace et tire d'un de ses trois canons ---
def bouger_boss():
    global direction_boss
    x = boss.get_x() + __________ * direction_boss     # trou 18
    if x > 200 or x < -200:
        direction_boss = -direction_boss
    else:
        boss.set_x(x)

def boss_tire():
    decalage = random.choice([-25, 0, 25])
    tir = codesters.Sprite(IMG_TIR_ALIEN, boss.get_x() + decalage, boss.get_y() - 25)
    ____________.append(tir)        # trou 19


# ---------- le joueur touché ----------
def joueur_touche(sprite, touche_par):
    global vies
    if touche_par in tirs_aliens:
        retirer_tir(touche_par)
        vies -= 1
        maj_affichage()
        if vies <= 0:
            stage.remove_sprite(sprite)
            fin_partie("PERDU !!!", "red")
    elif touche_par in ________:       # bonus 4 : un alien percute le joueur   (trou 20)
        fin_partie("PERDU !!!", "red")


# ---------- le battement du jeu ----------
# Codesters ne garde qu'UN SEUL event_interval :
# tout ce qui se répète passe par cette fonction.
def tic():
    global compteur_tics
    global clignotement_boss
    compteur_tics += 1
    bouger_tirs()
    if len(aliens) > 0 and compteur_tics % delai_flotte() == 0:
        bouger_flotte()
    if len(aliens) > 0 and compteur_tics % TIR_ALIEN_TOUS_LES == 0:
        alien_tire()
    if boss_en_vie:
        _________()                   # trou 22
        if clignotement_boss > 0:
            clignotement_boss -= 1
            if clignotement_boss __ 0:       # trou 21
                boss.set_opacity(1)
        if compteur_tics % TIR_BOSS_TOUS_LES == 0:
            boss_tire()


# ---------- c'est parti ----------
creer_aliens()
construire_mur(0, BOUCLIER_Y, NOMBRE_BOUCLIERS)
joueur.event_collision(joueur_touche)

stage.event_key("left", touche_gauche)
stage.event_key("right", touche_droite)
stage.event_key("q", ________)     # trou 23
stage.event_key("d", touche_droite)
stage.event_key("space", joueur_tire)
stage.event_key("_", touche_bouclier)    # trou 24
stage.event_interval(tic, 0.05)
