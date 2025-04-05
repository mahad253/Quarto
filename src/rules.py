import pygame
import os
import sys

pygame.init()

WIDTH, HEIGHT = 1080, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont(None, 28)
TITLE_FONT = pygame.font.SysFont(None, 42)

# Règles multilingues
RULES = {
    "fr": [
        " RÈGLES DU JEU QUARTO",
        "",
        " Objectif :",
        "Aligner 4 pièces ayant au moins UNE caractéristique commune :",
        "- Hauteur : grande ou petite",
        "- Couleur : foncée ou claire",
        "- Forme : ronde ou carrée",
        "- Pleine ou creuse",
        "",
        " Tour de jeu :",
        "1. Choisissez une pièce pour l’adversaire.",
        "2. Il la place sur le plateau.",
        "3. Puis il choisit une pièce pour vous.",
        "",
        " Fin :",
        "- Alignement valide : victoire.",
        "- Plateau plein sans alignement : égalité.",
        "",
        " Bon jeu et amusez-vous !"
    ],
    "es": [
        " REGLAS DEL JUEGO QUARTO",
        "",
        " Objetivo:",
        "Alinear 4 piezas que compartan al menos UNA característica común:",
        "- Altura: alta o baja",
        "- Color: oscuro o claro",
        "- Forma: redonda o cuadrada",
        "- Llena o hueca",
        "",
        " Turno de juego:",
        "1. Elige una pieza para tu oponente.",
        "2. Él la coloca en el tablero.",
        "3. Luego elige una pieza para ti.",
        "",
        " Fin del juego:",
        "- Alineación válida : victoria.",
        "- Tablero lleno sin alineación : empate.",
        "",
        " ¡Diviértete y disfruta del juego!"
    ]
}


def draw_centered_text(surface, text, x_center, y, font, color):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(x_center, y))
    surface.blit(rendered, rect)


def rules_loop(language):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Règles du jeu")

    # Fond
    background = pygame.image.load("assets/fonts/bg.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Titre centré
        titre = "Règles du jeu" if language == "fr" else "Reglas del juego"
        draw_centered_text(screen, titre, WIDTH // 2, 50, TITLE_FONT, WHITE)

        # Affichage ligne par ligne
        start_y = 120
        line_height = 32

        for i, line in enumerate(RULES[language]):
            draw_centered_text(screen, line, WIDTH // 2, start_y + i * line_height, FONT, WHITE)

        # Indication retour
        back = FONT.render(" ESC pour revenir", True, WHITE)
        screen.blit(back, (WIDTH - 250, HEIGHT - 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
