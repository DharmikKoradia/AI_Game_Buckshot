from State import GameState
from Actions import get_actions, is_terminal, apply_action
state = GameState()
state.shells = ['Live','Blank','Live','Live']


s2 = state.copy()


