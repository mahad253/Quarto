import pygame
import os
import sys

pygame.init()

WIDTH, HEIGHT = 1080, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont(None, 28)
TITLE_FONT = pygame.font.SysFont(None, 42)

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
        " Les 4 niveaux de victoire :",
        "- Niveau 1 : alignement horizontal, vertical ou diagonal",
        "- Niveau 2 : carré 2x2 (ex : a1,a2,b1,b2)",
        "- Niveau 3 : carré 3x3 (ex : a1,a3,c1,c3)",
        "- Niveau 4 : losange tournant (ex : a2,b1,c2,b3)",
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
        " Los 4 niveles de victoria :",
        "- Nivel 1 : línea (horizontal, vertical o diagonal)",
        "- Nivel 2 : cuadrado 2x2 (ej: a1,a2,b1,b2)",
        "- Nivel 3 : cuadrado 3x3 (ej: a1,a3,c1,c3)",
        "- Nivel 4 : diamante rotado (ej: a2,b1,c2,b3)",
        "",
        " ¡Diviértete y disfruta del juego!"
    ]
}

def draw_centered_text(surface, text, x_center, y, font, color):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(x_center, y))
    surface.blit(rendered, rect)


def draw_box_with_text(surface, x, y, width, height, lines, font, title=None):
    box_color = (0, 0, 0, 180)
    box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    box_surface.fill(box_color)
    surface.blit(box_surface, (x, y))

    padding = 10
    text_y = y + padding
    if title:
        title_surface = font.render(title, True, WHITE)
        surface.blit(title_surface, (x + padding, text_y))
        text_y += 40

    for i, line in enumerate(lines):
        line_surface = font.render(line, True, WHITE)
        surface.blit(line_surface, (x + padding, text_y + i * 30))


def rules_loop(language):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Règles du jeu")
    clock = pygame.time.Clock()

    # Fond
    background = pygame.image.load("assets/fonts/bg.jpg")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    rules = RULES[language]

    # Découpage en blocs
    blocks = []
    block = []
    for line in rules:
        if line.strip() == "":
            if block:
                blocks.append(block)
                block = []
        else:
            block.append(line)
    if block:
        blocks.append(block)

    # Calcul dimensions totales
    box_width = WIDTH - 200
    box_height = 180
    box_spacing = 20
    content_height = len(blocks) * (box_height + box_spacing)
    scroll_y = 0
    scroll_speed = 20

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Titre
        draw_centered_text(screen, "QUARTO", WIDTH // 2, 30, TITLE_FONT, WHITE)

        # Affichage des boîtes dans surface scrollable
        for i, block in enumerate(blocks):
            x = 100
            y = 80 + i * (box_height + box_spacing) - scroll_y
            if -box_height < y < HEIGHT:
                draw_box_with_text(screen, x, y, box_width, box_height, block, FONT)

        # Message retour
        back = FONT.render("ESC pour revenir", True, WHITE)
        screen.blit(back, (WIDTH - 250, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_DOWN:
                    scroll_y = min(scroll_y + scroll_speed, content_height - HEIGHT + 100)
                elif event.key == pygame.K_UP:
                    scroll_y = max(scroll_y - scroll_speed, 0)
            elif event.type == pygame.MOUSEWHEEL:
                scroll_y = max(0, min(content_height - HEIGHT + 100, scroll_y - event.y * scroll_speed))
