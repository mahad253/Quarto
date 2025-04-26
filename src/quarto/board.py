import itertools
import pygame as pg
from .constants import DBROWN, SQUARE_SIZE
from .pieces.piece import Piece
from .pieces.types import Coloration, Hole, Shape, Size

class Board:

    def __init__(self, name, storage, rows, cols, x_offset, y_offset, board_outline, light_color, dark_color):
        self.__name__ = name
        self.storage = storage
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.pieces_count = 0
        self.rows = rows
        self.cols = cols
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.board_outline = board_outline
        self.__colors = (light_color, dark_color)
        self.__init_pieces()
        self.selected_square = None

    def __init_pieces(self):
        if self.storage:
            row = 0
            for c in Coloration:
                col = 0
                for h in Hole:
                    for sh in Shape:
                        for si in Size:
                            self.board[row][col] = Piece(row, col, c, sh, si, h)
                            col += 1
                row += 1
        print("Initialization:")
        print(self.__repr__())

    def get_piece(self, row, col):
        return self.board[row][col]

    def put_piece(self, piece, row, col):
        self.board[row][col] = piece
        piece.move_to_gameboard(row, col)

    def move_to_gameboard(self, game_board, piece, row, col):
        try:
            self.board[piece.row][piece.col] = 0
            game_board.put_piece(piece, row, col)
            return piece
        except AttributeError:
            print("Type not valid.")

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        if (x < self.x_offset + self.cols * SQUARE_SIZE and x > self.x_offset and
                y < self.y_offset + self.rows * SQUARE_SIZE and y > self.y_offset):
            row = (y - self.y_offset) // SQUARE_SIZE
            col = (x - self.x_offset) // SQUARE_SIZE
            print(f'Clicked cell: {self.__name__}[{row},{col}]')
            return row, col
        return -1, -1

    def winner(self):
        return (self.__check_all_lines() or self.__check_small_squares() or
                self.__check_large_squares() or self.__check_rotated_squares())

    def get_winning_level(self):
        if self.__check_all_lines():
            return 1
        elif self.__check_small_squares():
            return 2
        elif self.__check_large_squares():
            return 3
        elif self.__check_rotated_squares():
            return 4
        else:
            return None

    def is_full(self):
        return all(piece != 0 for row in self.board for piece in row)

    def __is_winning_line(self, pieces):
        if 0 in pieces:
            return False
        attrs = [all(getattr(pieces[0], attr) == getattr(p, attr) for p in pieces)
                 for attr in ("hole", "size", "shape", "coloration")]
        return any(attrs)

    def __check_all_lines(self):
        for row in self.board:
            if self.__is_winning_line(row):
                return True
        for col in range(self.cols):
            if self.__is_winning_line([self.board[row][col] for row in range(self.rows)]):
                return True
        if self.__is_winning_line([self.board[i][i] for i in range(self.cols)]):
            return True
        if self.__is_winning_line([self.board[i][self.cols - i - 1] for i in range(self.cols)]):
            return True
        return False

    def __check_small_squares(self):
        for r in range(self.rows - 1):
            for c in range(self.cols - 1):
                square = [self.board[r][c], self.board[r][c+1],
                          self.board[r+1][c], self.board[r+1][c+1]]
                if self.__is_winning_line(square):
                    return True
        return False

    def __check_large_squares(self):
        for r in range(self.rows - 2):
            for c in range(self.cols - 2):
                square = [self.board[r][c], self.board[r][c+2],
                          self.board[r+2][c], self.board[r+2][c+2]]
                if self.__is_winning_line(square):
                    return True
        return False

    def __check_rotated_squares(self):
        rotated_patterns = [
            [(0, 1), (1, 0), (2, 1), (1, 2)],
            [(0, 1), (2, 0), (3, 2), (1, 3)]
        ]
        for i in range(self.rows):
            for j in range(self.cols):
                for pattern in rotated_patterns:
                    try:
                        pieces = [self.board[i + dx][j + dy] for dx, dy in pattern]
                        if self.__is_winning_line(pieces):
                            return True
                    except IndexError:
                        continue
        return False

    def get_valid_moves(self, verbose=False):
        moves = [(row, col) for row in range(self.rows)
                 for col in range(self.cols)
                 if (self.board[row][col] == 0 if not self.storage else self.board[row][col] != 0)]
        if verbose:
            print("moves = [" + ", ".join(map(str, moves)) + "]")
        return moves

    def draw(self, win):
        self.__draw_cells(win)
        for row in self.board:
            for piece in row:
                if piece != 0:
                    piece.draw(win)

    def __draw_cells(self, win):
        pg.draw.rect(win, DBROWN, (self.x_offset - self.board_outline, self.y_offset - self.board_outline,
                                   SQUARE_SIZE * self.cols + 2 * self.board_outline,
                                   SQUARE_SIZE * self.rows + 2 * self.board_outline))
        iter_colors = itertools.cycle(self.__colors)

        for x in range(self.cols):
            for y in range(self.rows):
                rect = (x * SQUARE_SIZE + self.x_offset, y * SQUARE_SIZE + self.y_offset,
                        SQUARE_SIZE, SQUARE_SIZE)
                color = next(iter_colors)
                if self.selected_square == (x, y):
                    pg.draw.rect(win, DBROWN, rect)
                else:
                    pg.draw.rect(win, color, rect)
            next(iter_colors)



    def __repr__(self):
        return self.__name__ + ":\n" + "\n".join(
            " ".join(str(cell) if cell != 0 else "----" for cell in row) for row in self.board
        )

    def display(self, depth):
        tab = "\t" * abs(2 - depth)
        return tab + self.__name__ + ":\n" + "\n".join(
            tab + " ".join(str(cell) if cell != 0 else "----" for cell in row)
            for row in self.board
        )
