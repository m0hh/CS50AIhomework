from tictactoe import initial_state, player, actions, result, winner, terminal,minimax


EMPTY = None
X = "X"
O = "O"

#a = player(initial_state())

b = [[X, O,X ],
    [O, X, X],
    [O, X,EMPTY]]

#bb = player(b)


#print(bb)

#print(actions(b))

#r =  result(b, (0,1))
#print(r)
#win = winner(b)

#print(win)

print(minimax(b))

