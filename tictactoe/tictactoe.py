"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

class Node():
    def __init__(self, state, parent, action, utility):
        pass

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

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
    a = sum(x.count(X) for x in board)
    b = sum(o.count(O) for o in board)

    if a == b:
        return X
    elif a > b:
        return O
    else:
        return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    a = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                a.add((i,j))
    return a


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newboard = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    if newboard[i][j] == EMPTY:
        newboard[i][j] = player(newboard)
        return newboard
    else:
        raise Exception


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    countrow = {}
    countcolumn = {}
    countdiagonal = {}
    countad = {}

    for i in range(len(board)):
        for j in range(len(board[0])):
            if j != 2  and board[i][j] == board [i][j+1] and board[i][j] in (X,O):
                row = i
                a =  countrow.get(board[i][j] + str(row))
                if a == None:
                    countrow[board[i][j] + str(row)] = 1
                countrow[board[i][j] + str(row)] += 1
            if i != 2 and board[i][j] == board[i+1][j] and board[i][j] in (X,O):
                column = j
                b =  countcolumn.get(board[i][j] + str(column))
                if b == None:
                    countcolumn[board[i][j] + str(column)] = 1
                countcolumn[board[i][j] + str(column)] += 1
            if i == j and i != 2 and j != 2 and board[i][j] == board[i+1][j+1] and board[i][j] in (X,O):
                c = countdiagonal.get(board[i][j] + "d")
                if c == None:
                    countdiagonal[board[i][j] + "d"] = 1
                countdiagonal[board[i][j] + "d"] += 1
            if ((i == 0 and j == 2) or (i == 1 and j == 1)) and board[i][j] == board[i+1][j-1] and board[i][j] in (X,O):
                d = countad.get(board[i][j] + "ad")
                if d == None:
                    countad[board[i][j] + "ad"] = 1
                countad[board[i][j] + "ad"] += 1 

    if 3 in countrow.values():
        winner = list(countrow.keys())[list(countrow.values()).index(3)]
        return winner[0]
    elif 3 in countcolumn.values():
        winner = list(countcolumn.keys())[list(countcolumn.values()).index(3)]
        return winner[0]
    elif 3 in countdiagonal.values():
        winner = list(countdiagonal.keys())[list(countdiagonal.values()).index(3)]
        return winner[0]
    elif 3 in countad.values():
        winner = list(countad.keys())[list(countad.values()).index(3)]
        return winner[0]
    else:
        return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    t = winner(board)
    empty = sum(e.count(EMPTY) for e in board)
    
    if t in (X,O):
        return True
    elif empty == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def maxvalue(board):
    v = float('-inf')
    if terminal(board) == True:
        return utility(board)
    for a in actions(board):
        v = max(v, minvalue(result(board,a)))
    return v

def minvalue(board):
    v = float('inf')
    if terminal(board) == True:
        return utility(board)
    for a in actions(board):
        v = min(v, maxvalue(result(board,a)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board) == True:
        return None


    elif player(board) == X:
        ac = actions(board)
        goal = None
        mx = float('-inf')

        for a in ac:
            mxtemp = minvalue(result(board,a))
            if mxtemp > mx:
                mx = mxtemp
                goal = a
        return goal

            
    
    
    elif player(board) == O:
        ac = actions(board)
        goal = None
        mn = float('inf')

        for a in ac:
            mntemp = maxvalue(result(board,a))
            if mntemp < mn:
                mn = mntemp
                goal = a
        return goal
    else:
        print("Something went wrong")
        return None
        
    



