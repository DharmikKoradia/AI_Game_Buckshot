from State import GameState
from Actions import get_actions, is_terminal, apply_action
from Evaluate import minimax

state = GameState()
state.shells = ['Live','Live','Blank','Blank']
