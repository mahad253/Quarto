import pygame as pg
import sys
import subprocess
import os

# Initialisation
pg.init()

# Dimensions
LARGEUR = 960
HAUTEUR = 540
BG = pg.image.load("assets/fonts/bg.jpg")
BG = pg.transform.scale(BG, (LARGEUR, HAUTEUR))

# Couleurs
ORANGE = (255, 102, 0)
GRIS_FONCE = (60, 60, 60)
GRIS_CLAIR = (200, 200, 200)

# Fenêtre
win = pg.display.set_mode((LARGEUR, HAUTEUR))
pg.display.set_caption("Quarto - Choix du mode de jeu")

# Police
FONT = pg.font.SysFont("Arial", 36)

# Classe Bouton
class Button:
    def __init__(self, text, x, y, width=300, height=50):
        self.text = text
        self.rect = pg.Rect(x, y, width, height)
        self.color = GRIS_FONCE
        self.hovered = False

    def draw(self, surface):
        color = GRIS_CLAIR if self.hovered else self.color
        pg.draw.rect(surface, color, self.rect, border_radius=10)
        text_surf = FONT.render(self.text, True, ORANGE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_hovered(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Classe Dropdown
class Dropdown:
    def __init__(self, x, y, options):
        self.options = options
        self.active = False
        self.selected = None
        self.rect = pg.Rect(x, y, 300, 50)
        self.option_rects = [pg.Rect(x, y + 50 * (i + 1), 300, 50) for i in range(len(options))]

    def draw(self, surface):
        if self.active:
            for i, opt in enumerate(self.options):
                r = self.option_rects[i]
                pg.draw.rect(surface, GRIS_CLAIR, r, border_radius=10)
                opt_text = FONT.render(opt, True, ORANGE)
                surface.blit(opt_text, opt_text.get_rect(center=r.center))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and self.active:
            for i, r in enumerate(self.option_rects):
                if r.collidepoint(event.pos):
                    self.selected = self.options[i]
                    return True
        return False

# Création des boutons
btn_pvp = Button("Joueur vs Joueur", LARGEUR // 2 - 150, 200)
btn_pvai = Button("Joueur vs IA", LARGEUR // 2 - 150, 300)
dropdown = Dropdown(LARGEUR // 2 - 150, 300, ["Niveau 1", "Niveau 2", "Minimax"])

# Boucle principale
running = True
dropdown_visible = False

while running:
    win.blit(BG, (0, 0))
    mouse_pos = pg.mouse.get_pos()

    # Affichage des boutons
    for btn in [btn_pvp, btn_pvai]:
        btn.is_hovered(mouse_pos)
        btn.draw(win)

    # Affichage de la liste déroulante
    if dropdown_visible:
        dropdown.draw(win)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if btn_pvp.is_clicked(event.pos):
                pg.quit()
                subprocess.run(["python", os.path.join(os.path.dirname(__file__), "jeu.py")])
                sys.exit()

            elif btn_pvai.is_clicked(event.pos):
                dropdown_visible = True
                dropdown.active = True

            elif dropdown_visible:
                if dropdown.handle_event(event):
                    niveau = dropdown.selected
                    pg.quit()
                    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "jeu.py"), niveau])
                    sys.exit()

    pg.display.update()

pg.quit()
sys.exit()
