import pygame as pg
import os
import sys
from .players.agents import AI_level1, AI_level2, AI_level3
from .players.human import Human
from .board import Board
from .constants import (
    BOARDOUTLINE, SQUARE_SIZE,
    GROWS, GCOLS, GXOFFSET, GYOFFSET,
    SROWS, SCOLS, SXOFFSET, SYOFFSET,
    LGREEN, GREEN, DGREEN, BROWN, DBROWN, WHEAT, PAYAYA, LGRAY,
    PLAYER1, PLAYER2, AI1, AI2, TIE,
    RESET_X, RESET_Y, RESET_WIDTH, RESET_HEIGHT,
    TXT_X, TXT_Y,
)

class Game:
    def __init__(self, win, font, ia_level=None):
        self.ia_level = ia_level  # "Niveau 1", "Niveau 2", "Minimax" ou None
        self.__init_game()
        self.win = win
        self.font = font
        self.large_font = pg.font.Font(None, 60)

        self.avatar1 = pg.transform.scale(pg.image.load(os.path.join("assets", "images", "user.png")), (60, 60))
        self.avatar2 = pg.transform.scale(pg.image.load(os.path.join("assets", "images", "user.png")), (60, 60))

    def update(self):
        self.game_board.draw(self.win)
        self.storage_board.draw(self.win)
        self.__draw_turn_txt()
        self.__draw_players_txt()
        pg.display.update()

    def __init_game(self):
        self.selected_piece = None
        self.game_board = Board("Plateau", False, GROWS, GCOLS, GXOFFSET, GYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
        self.storage_board = Board("Réserve", True, SROWS, SCOLS, SXOFFSET, SYOFFSET, BOARDOUTLINE, LGREEN, GREEN)
        self.turn = True
        self.pick = True
        self.valid_moves = []

        self.player1 = Human("Joueur 1")

        if self.ia_level == "Niveau 1":
            self.player2 = AI_level1("IA - Niveau 1")
        elif self.ia_level == "Niveau 2":
            self.player2 = AI_level2("IA - Niveau 2")
        elif self.ia_level == "Minimax":
            self.player2 = AI_level3("IA - Minimax")
        else:
            self.player2 = Human("Joueur 2")

    def reset(self):
        print("La partie est réinitialisée.")
        self.__init_game()
        print(self)

    def select(self, row=-1, col=-1):
        if self.turn:
            return self.player1.select(self, row, col)
        else:
            return self.player2.select(self, row, col)

    def winner(self):
        if self.game_board.winner():
            self.__draw_reset_button()
            return self.__get_player1() if self.turn else self.__get_player2()
        elif self.game_board.is_full():
            self.__draw_reset_button()
            return TIE
        return None

    def move(self, row, col):
        if self.selected_piece and (row, col) in self.valid_moves:
            self.storage_board.move_to_gameboard(self.game_board, self.selected_piece, row, col)
        else:
            return False
        return True

    def __draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pg.draw.circle(self.win, DGREEN,
                           (self.game_board.x_offset + int(SQUARE_SIZE * col) + SQUARE_SIZE // 2,
                            self.game_board.y_offset + int(SQUARE_SIZE * row) + SQUARE_SIZE // 2), 15)

    def __draw_turn_txt(self):
        if self.winner():
            txt = "Égalité ! Personne n’a gagné." if self.winner() == TIE else f"{self.__get_player1() if self.turn else self.__get_player2()} a gagné !!"
        else:
            txt = f"{self.__get_player1() if self.turn else self.__get_player2()}, {'choisis une' if self.pick else 'pose la'} pièce !"

        text_surface = self.large_font.render(txt, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.win.get_width() // 2, 40))
        self.win.blit(text_surface, text_rect)

    def __draw_reset_button(self):
        rect_outline = pg.Rect(RESET_X - BOARDOUTLINE, RESET_Y - BOARDOUTLINE,
                               RESET_WIDTH + 2 * BOARDOUTLINE, RESET_HEIGHT + 2 * BOARDOUTLINE)
        pg.draw.rect(self.win, DBROWN, rect_outline)

        rect = pg.Rect(RESET_X, RESET_Y, RESET_WIDTH, RESET_HEIGHT)
        pg.draw.rect(self.win, BROWN, rect)

        text_surface_reset, text_rect = self.font.render("RECOMMENCER", (0, 0, 0))
        text_rect.center = rect.center
        self.win.blit(text_surface_reset, text_rect)

    def __draw_players_txt(self):
        base_x = GXOFFSET + GCOLS * SQUARE_SIZE + 80
        base_y = 160

        self.win.blit(self.avatar1, (base_x, base_y))
        text_surface1, _ = self.font.render(self.__get_player1(), (150, 200, 255) if self.turn else (255, 255, 255))
        self.win.blit(text_surface1, (base_x + 70, base_y + 15))

        self.win.blit(self.avatar2, (base_x, base_y + 100))
        text_surface2, _ = self.font.render(self.__get_player2(), (255, 255, 255) if self.turn else (255, 180, 150))
        self.win.blit(text_surface2, (base_x + 70, base_y + 115))

    def get_row_col_from_mouse(self, pos):
        return self.storage_board.get_row_col_from_mouse(pos) if self.pick else self.game_board.get_row_col_from_mouse(pos)

    def is_reset_clicked(self, pos):
        x, y = pos
        return RESET_X < x < RESET_X + RESET_WIDTH and RESET_Y < y < RESET_Y + RESET_HEIGHT

    def is_arrow_clicked(self, pos):
        return None

    def is_human_turn(self):
        if (self.turn and isinstance(self.player1, Human)) or (not self.turn and isinstance(self.player2, Human)):
            return True
        return False

    def end_turn(self, selected_square=None):
        self.storage_board.selected_square = selected_square
        self.__change_turn()
        self.__change_pick_move()

    def __change_turn(self):
        if self.pick:
            self.turn = not self.turn

    def __change_pick_move(self):
        self.pick = not self.pick

    def __get_player1(self):
        return self.player1.__name__

    def __get_player2(self):
        return self.player2.__name__

    def __repr__(self):
        return self.game_board.__repr__() + self.storage_board.__repr__() + "\n"
