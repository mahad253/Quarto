from copy import deepcopy

from ..constants import GROWS, GCOLS
from .utils import update_pos_set

EVAL_TIE = 0  #  this draw value only matters in the endgame, where the heuristic doesn't matter anymore
EVAL_WIN = 9

MAX_DEPTH = 4


def minimax(game_state, depth: int, max_player: bool, alpha=float('-inf'), beta=float('inf'), verbose=True):

    if verbose:
        print("\n\n", "\t" * abs(2 - depth), "ENTERING MINIMAX DEPTH", depth, "MAX =", max_player)
        print("\t" * abs(2 - depth), "Game State:")
        print(game_state[0].display(depth))
        print(game_state[1].display(depth))
        print("\t" * abs(2 - depth), "Selected_piece:" + str(game_state[2]))

    # Terminal state or max depth reached
    if depth == 0 or game_state[0].winner():
        if verbose:
            print("\t" * abs(2 - depth), "State_eval:", state_eval(game_state), "\n\n")
        return state_eval(game_state) * (-1 if max_player else 1), game_state
        # FIXME: this line is the most unconventional one. But it also makes sense: without it, winning would be as

    best_move = None

    # If we are trying to maximize the evaluation
    if max_player:
        max_eval = float('-inf')
        for child in get_all_possible_states(game_state):
            evaluation = minimax(child, depth - 1, False, alpha, beta)[0]
            max_eval = max(max_eval, evaluation)

            if max_eval == evaluation:
                if verbose:
                    print("\t" * abs(3 - depth), "max_evaluation updated:", max_eval)
                best_move = child

            if alpha and beta:
                alpha = max(alpha, max_eval)
                if verbose:
                    print("\t" * abs(3 - depth), "alpha =", alpha, "beta =", beta)
                if beta <= alpha:
                    break

            # Some debugging
            if verbose:
                print("\t" * abs(3 - depth), "evaluation ", evaluation)

        return max_eval, best_move

    else:
        min_eval = float('inf')
        for child in get_all_possible_states(game_state):
            evaluation = minimax(child, depth - 1, True, alpha, beta)[0]
            min_eval = min(min_eval, evaluation)

            # Assigning the new value
            if min_eval == evaluation:
                if verbose:
                    print("\t" * abs(3 - depth), "min_evaluation updated:", min_eval)
                best_move = child

            # Pruning
            if alpha and beta:
                beta = min(beta, min_eval)
                if verbose:
                    print("\t" * abs(3 - depth), "alpha =", alpha, "beta =", beta)
                if beta <= alpha:
                    break

            # Some debugging
            if verbose:
                print("\t" * abs(3 - depth), "evaluation ", evaluation)

        return min_eval, best_move


def state_eval(game_state):

    if game_state[0].winner():
        return EVAL_WIN
    elif game_state[0].is_full():
        return EVAL_TIE
    else:
        return 0  # FIXME: the heuristic doesn't work


def heuristic(game_state):

    h = set()  # heuristics value

    # Rows and columns
    for col in range(GCOLS):
        row_line = []
        col_line = []

        for row in range(GROWS):
            col_line.append((col, row))
            row_line.append((row, col))

        h = update_pos_set(game_state[0], row_line, h, game_state[1])
        h = update_pos_set(game_state[0], col_line, h, game_state[1])

    top_left_diagonal_line = []
    top_right_diagonal_line = []

    for col in range(GCOLS):
        top_left_diagonal_line.append((col, col))
        top_right_diagonal_line.append((GCOLS - col - 1, col))

    h = update_pos_set(game_state[0], top_right_diagonal_line, h, game_state[1])
    h = update_pos_set(game_state[0], top_left_diagonal_line, h, game_state[1])


    return len(h)


def get_all_possible_states(game_state):
    '''
    Function that generates a list of possible states from the given game_state

    game_state -- a tuple of three elements :
        - [0] the game_board, a Board object that holds the current played pieces
        - [1] the storage_board, a Board object that holds the pieces available to pick
        - [2] the selected_piece coordinates, a tuple of (x, y) coordinates that correspond to an available piece
        on the storage_board. This is the piece that has to be put on the game_board.

    Returns
    a list of possible game_state (as described higher) after a move is made.
    '''
    possible_states_after_move = []

    for position_played in get_all_submoves(game_state, False):  #  for each cell where we can put the selected piece
        for piece_picked in get_all_submoves(game_state, True):  #  and each available piece left
            temp_game_state = deepcopy(game_state)  #  we copy the current game_state
            new_game_state = simulate_move(temp_game_state, position_played, piece_picked)  #  and play the move given
            possible_states_after_move.append(new_game_state)

    return possible_states_after_move


def get_all_submoves(game_state, pick):
    '''
    Function that returns all the valid moves depending on the stage of the turn defined by pick

    pick -- boolean, if it's time to pick a piece, True. If it's time to put a piece on the game_board, False
    game_state -- a tuple of three elements :
        - [0] the game_board, a Board object that holds the current played pieces
        - [1] the storage_board, a Board object that holds the pieces available to pick
        - [2] the selected_piece coordinates, a tuple of (x, y) coordinates that correspond to an available piece
        on the storage_board. This is the piece that has to be put on the game_board.

    Returns
    a list of tuples that correspond either to game_board coordinates if pick == False, or to a set of
    storage_board coordinates if pick == True
    '''
    if pick:
        valid_moves = game_state[1].get_valid_moves()  # built-in method to get the available pieces on the storage_board
        #  the current selected_piece is removed from the valid pieces to pick as it will be played on the game_board
        valid_moves.remove(game_state[2])
        return valid_moves  # all the moves possible
    else:
        return game_state[0].get_valid_moves()  # built-in method to get the available pieces on the game_board


def simulate_move(game_state, position_played, piece_picked):
    '''
    Function that simulates a move, i.e. that takes as input a game_state, a position played for the current selected_piece
    and a new picked piece, and makes a new game_state by playing the move.

    game_state -- a tuple of three elements :
        - [0] the game_board, a Board object that holds the current played pieces
        - [1] the storage_board, a Board object that holds the pieces available to pick
        - [2] the selected_piece coordinates, a tuple of (x, y) coordinates that correspond to an available piece
        on the storage_board. This is the piece that has to be put on the game_board.
    position_played -- a tuple of (x, y) coordinates that correspond to where we want to put the piece on the game_board
    piece_picked -- a tuple of (x, y) coordinates that correspond to where we want to take the piece from the storage_board

    Returns
    the game_state after the specified move
    '''
    game_board, game_storage, selected_piece_coor = game_state
    selected_piece = game_storage.board[selected_piece_coor[0]][selected_piece_coor[1]]
    game_storage.board[selected_piece_coor[0]][selected_piece_coor[1]] = 0
    game_board.put_piece(selected_piece, position_played[0], position_played[1])

    return game_state[0], game_state[1], piece_picked
