import sys
import os
import pygame as pg
from pygame import freetype
from quarto.constants import HEIGHT, WIDTH, FONT
from quarto.partie import Game

# Initialisation de Pygame
pg.init()

# Chargement du fond d'écran
background_path = os.path.join("assets", "fonts", "bg.jpg")
if os.path.exists(background_path):
    background = pg.image.load(background_path)
else:
    print(f"❌ Image de fond introuvable : {background_path}")
    background = None  # fallback si le fond est absent

# Création de la fenêtre
win = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Quarto!")

# Chargement de la police
GAME_FONT = freetype.SysFont(FONT, 24)

# FPS
fps = 60


def main():
    run = True
    clock = pg.time.Clock()
    game = Game(win, GAME_FONT)

    # Debug console
    print(game.game_board.__repr__())
    print(game.storage_board.__repr__())

    while run:
        clock.tick(fps)

        # Dessin du fond d'écran
        if background:
            win.blit(background, (0, 0))
        else:
            win.fill((73, 67, 54))  # fallback au BG si image absente

        if not game.winner():
            if not game.is_human_turn():
                game.select()  # IA si besoin

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    print("Click:", pos)

                    clicked_arrow = game.is_arrow_clicked(pos)
                    if clicked_arrow:
                        game.swap_players(clicked_arrow)

                    row, col = game.get_row_col_from_mouse(pos)
                    if (row, col) != (-1, -1) and game.is_human_turn():
                        game.select(row, col)
                        print(game.__repr__())

        else:
            # Affiche le bouton "RESET"
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    print("Click:", pos)
                    if game.is_reset_clicked(pos):
                        game.reset()

        # Mise à jour des composants du jeu
        game.update()

    pg.quit()
    sys.exit()


if __name__ == '__main__':
    main()
