import pygame
import os
import math
import subprocess
import sys

# Initialisation de Pygame
pygame.init()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
HOVER_COLOR = (255, 140, 0)
TITLE_COLOR = (255, 69, 0)

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quarto")

# Chargement des images
background = pygame.image.load('assets/fonts/bg.jpg')
flag_fr = pygame.image.load('assets/images/france.png')
flag_es = pygame.image.load('assets/images/spain.png')
flag_fr = pygame.transform.scale(flag_fr, (50, 30))
flag_es = pygame.transform.scale(flag_es, (50, 30))

# Positions des drapeaux
flag_fr_rect = flag_fr.get_rect(topleft=(20, 20))
flag_es_rect = flag_es.get_rect(topleft=(80, 20))

# Textes selon la langue
languages = {
    "fr": {
        "start": "Lancer une partie",
        "rules": "Règles du jeu",
        "report": "Rapport du projet"
    },
    "es": {
        "start": "Iniciar una partida",
        "rules": "Reglas del juego",
        "report": "Informe del proyecto"
    }
}
current_language = "fr"

# Polices
font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 100)

# Fonction pour dessiner un bouton
def draw_button(text, x, y, is_hovered):
    button_rect = pygame.Rect(x, y, 300, 50)
    color = HOVER_COLOR if is_hovered else GRAY
    pygame.draw.rect(screen, color, button_rect, border_radius=10)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect

# Animation
running = True
time_counter = 0

while running:
    screen.blit(background, (0, 0))

    # Titre flottant
    title_y = 100 + math.sin(time_counter * 0.05) * 10
    title_surf = title_font.render("QUARTO", True, TITLE_COLOR)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, title_y))
    screen.blit(title_surf, title_rect)

    mouse_pos = pygame.mouse.get_pos()

    # Drapeaux
    is_hover_fr = flag_fr_rect.collidepoint(mouse_pos)
    is_hover_es = flag_es_rect.collidepoint(mouse_pos)

    if current_language == "fr" or is_hover_fr:
        pygame.draw.rect(screen, BLACK, flag_fr_rect.inflate(6, 6), border_radius=5)
    screen.blit(flag_fr, flag_fr_rect.topleft)

    if current_language == "es" or is_hover_es:
        pygame.draw.rect(screen, BLACK, flag_es_rect.inflate(6, 6), border_radius=5)
    screen.blit(flag_es, flag_es_rect.topleft)

    # Boutons
    start_button = draw_button(languages[current_language]["start"], 390, 300, pygame.Rect(390, 300, 300, 50).collidepoint(mouse_pos))
    rules_button = draw_button(languages[current_language]["rules"], 390, 370, pygame.Rect(390, 370, 300, 50).collidepoint(mouse_pos))
    report_button = draw_button(languages[current_language]["report"], 390, 440, pygame.Rect(390, 440, 300, 50).collidepoint(mouse_pos))

    pygame.display.flip()
    time_counter += 1

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture de Quarto")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if flag_fr_rect.collidepoint(event.pos):
                current_language = "fr"
                print("Langue changée en Français")
            elif flag_es_rect.collidepoint(event.pos):
                current_language = "es"
                print("Langue changée en Espagnol")

            if start_button.collidepoint(event.pos):
                print("Lancement de la partie...")
                pygame.quit()
                subprocess.run(["python", os.path.join(os.path.dirname(__file__), "choix.py")])
                sys.exit()

            elif rules_button.collidepoint(event.pos):
                print("Affichage des règles du jeu...")
                import rules
                rules.rules_loop(current_language)

            elif report_button.collidepoint(event.pos):
                print("Affichage du rapport du projet...")
                # On remonte d’un niveau depuis src/ pour atteindre Quarto.pdf
                pdf_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Quarto.pdf"))
                try:
                    if sys.platform.startswith("linux"):
                        subprocess.run(["xdg-open", pdf_path])
                    elif sys.platform == "darwin":
                        subprocess.run(["open", pdf_path])
                    elif sys.platform == "win32":
                        os.startfile(pdf_path)
                except Exception as e:
                    print("Erreur lors de l’ouverture du PDF :", e)


