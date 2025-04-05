from copy import deepcopy
from ..board import Board


def can_line_win(game, line, sboard=None):

    count, pos = count_zeros_in_line(game, line)
    if count == 1:  # meaning one piece is missing
        storage = sboard.board if sboard else game.storage_board.board

        for row in storage:
            for piece in row:

                col, row = pos
                inversed_pos = row, col

                if piece != 0 and is_winning_move(game, inversed_pos, piece):

                    return pos
    return False


def count_zeros_in_line(game, line):
    count = 0
    pos = (-1, -1)

    if isinstance(game, Board):
        game = game.board
    else:
        game = game.game_board.board

    for col, row in line:
        if game[row][col] == 0:
            count += 1
            pos = (col, row)
    return count, pos


def update_pos_set(game, line, set, sboard=None):
    pos = can_line_win(game, line, sboard)
    if pos:
        set.update({pos})
    return set


def get_coor_selected_piece(storage_board, selected_piece):
    for i, row in enumerate(storage_board.board):
        for j, col in enumerate(row):
            if col == selected_piece:
                return (i, j)


def get_winning_moves(game, piece=None):

    moves = []
    for move in game.game_board.get_valid_moves():
        if is_winning_move(game, move, game.selected_piece if not piece else piece):
            moves.append(move)
    return moves


def is_winning_move(game, move, piece):
    '''Checks is a move is winning or not
    '''
    row, col = move

    if isinstance(game, Board):
        game_board_copy = deepcopy(game)
    else:
        game_board_copy = deepcopy(game.game_board)

    piece_copy = deepcopy(piece)

    game_board_copy.put_piece(piece_copy, row, col)
    return game_board_copy.winner()


def get_not_losing_moves(game):

    not_losing_moves = []
    valid_moves = game.storage_board.get_valid_moves()

    for move in valid_moves:
        game.selected_piece = game.storage_board.get_piece(move[0], move[1])
        losing_moves = get_winning_moves(game)
        if not losing_moves:
            not_losing_moves.append(move)

    return not_losing_moves
