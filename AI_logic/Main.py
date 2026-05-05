from State import GameState
from Actions import get_actions, is_terminal, apply_action
from Evaluate import minimax

state = GameState()
state.shells = ['Blank','Live','Blank','Blank']

value, moves = minimax(state, 4)
print(moves)