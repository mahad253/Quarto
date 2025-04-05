import pygame as pg

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1200, 900  # Taille de la fenêtre pygame
SQUARE_SIZE = WIDTH // 12  # Taille des cases (12 colonnes dans la largeur)
BOARDOUTLINE = SQUARE_SIZE // 10

# Plateau de jeu (4x4)
GROWS, GCOLS = 4, 4
GXOFFSET = WIDTH // 2 - SQUARE_SIZE * GCOLS // 2  # Centrage horizontal
GYOFFSET = SQUARE_SIZE  # Décalage vertical

# Plateau de sélection des pièces (8x2)
SCOLS, SROWS = 8, 2
SXOFFSET = WIDTH // 2 - SQUARE_SIZE * SCOLS // 2
SYOFFSET = HEIGHT - SQUARE_SIZE * (SROWS + 1)

# Texte d'état
TXT_X, TXT_Y = (55, 200)

# Bouton reset
RESET_X = TXT_X
RESET_Y = TXT_Y + 50
RESET_WIDTH = 200
RESET_HEIGHT = 70

# Coordonnées des flèches de sélection de joueur
X_LEFT_ARROWS = 930
X_RIGHT_ARROWS = 1075
Y_TOP_ARROWS = TXT_Y + 60
Y_BOT_ARROWS = Y_TOP_ARROWS + 50

# =========================
# === THÈME MARRON 🍫 ===
# =========================

# Couleurs du plateau (cases)
GREEN = pg.Color((101, 67, 33))   # Marron foncé
LGREEN = pg.Color((181, 101, 29)) # Marron clair
DGREEN = pg.Color('darkgreen')    # utilisé pour les coups valides

# Couleurs des pions et interface
LBEIGE = pg.Color('moccasin')     # beige clair
BEIGE = pg.Color('tan')           # beige
LBROWN = pg.Color('darkgoldenrod')# marron doré clair
BROWN = pg.Color('saddlebrown')   # marron standard
DBROWN = pg.Color((41, 21, 10))   # marron très foncé

# Texte
WHEAT = pg.Color('wheat')
PAYAYA = pg.Color('papayawhip')
LGRAY = pg.Color((150, 150, 150))

# Fond général
BG = (73, 67, 54)

# Police d’écriture
FONT = "freesansbold.ttf"

# Joueurs
PLAYER1 = "Joueur 1"
PLAYER2 = "Joueur 2"
AI1 = "AI1"
AI2 = "AI2"
TIE = "TIE"
