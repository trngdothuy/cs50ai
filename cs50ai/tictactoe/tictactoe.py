"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

stepX = 0
stepO = 0


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # X goes 1st, check each cell in board
    global stepX
    global stepO

    # if stepX == 0:
    #     stepX += 1
    #     return X
    # else:
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == X:
                stepX += 1
            elif board[i][j] == O:
                stepO += 1
    if stepX > stepO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # i = row, j = cell -- 0 1 2

    actionList = set()

    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if board[i][j] == EMPTY:
                actionList.add((i, j))

    return actionList


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # return state (not simply update board but a deep copy)
    result = copy.deepcopy(board)
    if board[action[0]][action[1]] != EMPTY:
        raise Exception('Invalid move')
    elif action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise Exception('Out of range')
    result[action[0]][action[1]] = player(board)
    return result


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # return X or O or None
    # loop through each row
    for i in range(0, 3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        # each column
        elif board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
    # 2 diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[1][1] != EMPTY:
        return board[1][1]
    elif board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[1][1] != EMPTY:
        return board[1][1]
    # draw?
    # ongoing?
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # return boolean over = true or not
    if winner(board) is not None:
        return True
    else: # check if all filled:
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if board[i][j] != EMPTY :
                    return True
                else:
                    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    if player(board) == X:
        value, action = max_value(board)
        return action
    else:
        value, action = min_value(board)
        return action



def max_value(board):
# max picks action a in actions(s) that produces highest value of min-value(result(s, a))
    if terminal(board):
        return utility(board), None

    # lowest possible => always better than the initial value
    max_value = float('-inf')
    max_action = None

    for action in actions(board):
        # choose the highest value, return value, action
        # value = max(value, min_value(result(board, action)))
        value, action = min_value(result(board, action))
        if value > max_value:
            max_value = value
            max_action = action

    return max_value, max_action

def min_value(board):
    if terminal(board):
        return utility(board), None

    # highest possible => always lower than initial value
    min_value = float('inf')
    min_action = None

    for action in actions(board):
        value, action = max_value(result(board, action))
        if value < min_value:
            min_value = value
            min_action = action

    return min_value, min_action
