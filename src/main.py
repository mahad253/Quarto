import pygame
import os
import math  # Pour l'effet de flottement
import subprocess
import sys  # Permet de quitter proprement le programme

# Initialisation de Pygame
pygame.init()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
HOVER_COLOR = (255, 140, 0)  # Orange pour le hover
TITLE_COLOR = (255, 69, 0)  # Rouge/orange inspiré du fond

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quarto")

# Chargement des images
background = pygame.image.load('assets/fonts/bg.jpg')
flag_fr = pygame.image.load('assets/images/france.png')
flag_es = pygame.image.load('assets/images/spain.png')

# Redimensionner les images des drapeaux
flag_fr = pygame.transform.scale(flag_fr, (50, 30))
flag_es = pygame.transform.scale(flag_es, (50, 30))

# Positions des drapeaux
flag_fr_rect = flag_fr.get_rect(topleft=(20, 20))
flag_es_rect = flag_es.get_rect(topleft=(80, 20))

# Définition des textes selon la langue
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

current_language = "fr"  # Langue par défaut

# Police d'écriture
font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 100)  # Plus grand pour le titre

# Fonction pour créer un bouton avec hover
def draw_button(text, x, y, is_hovered):
    button_rect = pygame.Rect(x, y, 300, 50)
    color = HOVER_COLOR if is_hovered else GRAY  # Change la couleur si hover
    pygame.draw.rect(screen, color, button_rect, border_radius=10)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect

running = True
time_counter = 0  # Compteur de temps pour l'effet flottant

while running:
    screen.blit(background, (0, 0))

    # Effet de flottement (mouvement haut-bas)
    title_y = 100 + math.sin(time_counter * 0.05) * 10  # Le texte monte et descend doucement

    # Affichage du titre flottant
    title_surf = title_font.render("QUARTO", True, TITLE_COLOR)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, title_y))
    screen.blit(title_surf, title_rect)

    # Récupération de la position de la souris
    mouse_pos = pygame.mouse.get_pos()

    # Vérifier si la souris est sur un drapeau
    is_hover_fr = flag_fr_rect.collidepoint(mouse_pos)
    is_hover_es = flag_es_rect.collidepoint(mouse_pos)

    # Affichage des drapeaux avec contour noir si sélectionné ou hover
    if current_language == "fr" or is_hover_fr:
        pygame.draw.rect(screen, BLACK, flag_fr_rect.inflate(6, 6), border_radius=5)
    screen.blit(flag_fr, flag_fr_rect.topleft)

    if current_language == "es" or is_hover_es:
        pygame.draw.rect(screen, BLACK, flag_es_rect.inflate(6, 6), border_radius=5)
    screen.blit(flag_es, flag_es_rect.topleft)

    # Dessiner les boutons avec hover
    start_button = draw_button(languages[current_language]["start"], 390, 300, start_button.collidepoint(mouse_pos) if 'start_button' in locals() else False)
    rules_button = draw_button(languages[current_language]["rules"], 390, 370, rules_button.collidepoint(mouse_pos) if 'rules_button' in locals() else False)
    report_button = draw_button(languages[current_language]["report"], 390, 440, report_button.collidepoint(mouse_pos) if 'report_button' in locals() else False)

    pygame.display.flip()

    time_counter += 1  # Incrémentation du compteur pour l'animation

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture de Quarto")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si un drapeau est cliqué
            if flag_fr_rect.collidepoint(event.pos):
                current_language = "fr"
                print("Langue changée en Français")
            elif flag_es_rect.collidepoint(event.pos):
                current_language = "es"
                print("Langue changée en Espagnol")

            # Vérifier si un bouton est cliqué
            if start_button.collidepoint(event.pos):
                print("Lancement de la partie...")
                pygame.quit()  # Fermer la fenêtre du menu
                subprocess.run(["python", os.path.join(os.path.dirname(__file__), "jeu.py")])  # Ouvrir party.py
                sys.exit()  # Quitter proprement
            elif rules_button.collidepoint(event.pos):
                print("Afficher les règles")
            elif report_button.collidepoint(event.pos):
                print("Afficher le rapport du projet")
