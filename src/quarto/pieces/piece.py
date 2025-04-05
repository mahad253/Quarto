import pygame as pg
from ..constants import SQUARE_SIZE, SXOFFSET, SYOFFSET, GXOFFSET, GYOFFSET, DBROWN
from .types import Shape, Size, Hole, Coloration


class Piece:

    PADDING = 15
    OUTLINE = 2
    INNER_PADDING = 3

    def __init__(self, row, col, coloration, shape, size, hole):

        self.row = row
        self.col = col

        self.size = size
        self.coloration = coloration
        self.shape = shape
        self.hole = hole

        self.x = 0
        self.y = 0
        self.calc_pos(True)

    def calc_pos(self, init=False):

        if(init):  # when we first initialize the game
            self.x = SQUARE_SIZE * self.col + SXOFFSET + SQUARE_SIZE // 2
            self.y = SQUARE_SIZE * self.row + SYOFFSET + SQUARE_SIZE // 2
        else:  # when a piece is being put on the board
            self.x = SQUARE_SIZE * self.col + GXOFFSET + SQUARE_SIZE // 2
            self.y = SQUARE_SIZE * self.row + GYOFFSET + SQUARE_SIZE // 2

    def move_to_gameboard(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def draw(self, win):

        radius = SQUARE_SIZE // 2 - self.PADDING
        if(self.size == Size.LITTLE):
            radius -= radius // 3
        if(self.shape == Shape.CIRCLE):
            pg.draw.circle(win, DBROWN, (self.x, self.y), radius + self.OUTLINE)
            pg.draw.circle(win, self.coloration.value, (self.x, self.y), radius)
            if(self.hole == Hole.WITH):
                pg.draw.circle(win, DBROWN, (self.x, self.y), int(radius * 0.8))  # TODO: tweak the colors
        else:
            rect = (self.x - radius, self.y - radius, radius * 2, radius * 2)
            rect_outline = (self.x - (radius + self.OUTLINE), self.y - (radius + self.OUTLINE),
                            (radius + self.OUTLINE) * 2, (radius + self.OUTLINE) * 2)
            pg.draw.rect(win, DBROWN, rect_outline)  # the outline
            pg.draw.rect(win, self.coloration.value, rect)
            if(self.hole == Hole.WITH):
                rect_hole = (self.x - int(radius) // 1.5, self.y - int(radius) // 1.5, int(radius * 4 / 3), int(radius * 4 / 3))
                pg.draw.rect(win, DBROWN, rect_hole)

    def __repr__(self, verbose=False):

        if(verbose):
            return(str(self.size) + ", " + str(self.coloration) + ", " + str(self.shape) +
                   ", " + str(self.hole))
        else:
            return(str("X" if(self.size == Size.TALL) else "O") +
                   str("X" if(self.coloration == Coloration.BEIGE) else "O") +
                   str("X" if(self.shape == Shape.SQUARE) else "O") +
                   str("X" if(self.hole == Hole.WITHOUT) else "O"))
