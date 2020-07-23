"""
Tic Tac Toe Player
"""

import math
from random import randrange

X = "X"
O = "O"
EMPTY = None


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
    xCount = 0
    oCount = 0

    for row in board:
        xCount += row.count(X)
        oCount += row.count(O)
    
    if xCount <= oCount:
        return X
    return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()

    for rowIndex, row in enumerate(board):
        for cellIndex, cell in enumerate(row):
            if cell == EMPTY:
                actions.add((rowIndex, cellIndex))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    p = player(board)
    newboard = [row.copy() for row in board]

    row, cell = action

    if row > 2 or row < 0 or cell > 2 or cell < 0:
        raise Exception("Invalid Move, Move outside of board")

    if newboard[row][cell] == EMPTY:
        newboard[row][cell] = p
        return newboard

    raise Exception("Invalid Move")



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # BETTER IMPLEMENTATION NEEDED

    # [row0, row1, row2, col0, col1, col2, dia1, dia2]
    xCount = [0,0,0,0,0,0,0,0]
    oCount = [0,0,0,0,0,0,0,0]

    for rowIndex, row in enumerate(board):
        # if row.count(X) == 3 or row.count(O) == 3:
        #     return X if row[0] == X else O
        
        for cellIndex, cell in enumerate(row):
            if cell == X:
                xCount[rowIndex] += 1
                xCount[cellIndex + 3] += 1
            elif cell == O:
                oCount[rowIndex] += 1 
                oCount[cellIndex + 3] += 1 
        
        # check dia1
        if board[rowIndex][rowIndex] == X:
            xCount[6] += 1
        elif board[rowIndex][rowIndex] == O:
            oCount[6] += 1

        # check dia2
        if board[rowIndex][abs(rowIndex-2)] == X:
            xCount[7] += 1
        elif board[rowIndex][abs(rowIndex-2)] == O:
            oCount[7] += 1

        if 3 in xCount:
            return X
        elif 3 in oCount:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If there is a winner return True
    if winner(board) is not None:
        return True
    
    # If all fields are filled out return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # If no possible moves, return none
    if terminal(board):
        return None
    
    # Select random position to start
    if board == initial_state():
        return (randrange(3),randrange(3))
    
    # check if we are playing for max or for min    
    mom = player(board)
    possActions = []

    # Playing for min score
    if mom == O:
        # List of all possible actions & their score
        possActions = [(action, maxValue(result(board, action))) for action in actions(board) ]

        # select the best action from the list
        bestAction = possActions[0]
        for action in possActions:
            if action[-1] < bestAction[-1]:
                bestAction = action
        # return action in tuple
        return bestAction[0]
    
    # Playing for max score
    if mom == X:
        # List of all possible actions & their score
        possActions = [(action, minValue(result(board, action))) for action in actions(board) ]

        # select the best action from the list
        bestAction = possActions[0]
        for action in possActions:
            if action[-1] > bestAction[-1]:
                bestAction = action
        # return action in tuple
        return bestAction[0]


def maxValue(board):
    if terminal(board):
        return utility(board)
    v = -10000000

    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v

def minValue(board):
    if terminal(board):
        return utility(board)
    v = 100000000
    for action in actions(board):
        v=min(v, maxValue(result(board, action)))
    return v

# board = [
#         [X, X, O],
#         [EMPTY, X, X],
#         [EMPTY, O, O]]

# print(minimax(board))