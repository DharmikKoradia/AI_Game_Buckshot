from Actions import *
import math

def evaluate(state):
    if state.player.hp<=0:
        return 1000
    elif state.dealer.hp<=0:
        return -1000
    else:
        return state.dealer.hp*10 - state.player.hp*10
    
def minimax(state,depth,AI_turn):
    if is_terminal(state) or depth == 0:
        return evaluate(state)
    
    if AI_turn:
        best = -math.inf
        for action in get_actions(state):
            child = apply_action(state,action)
            score = minimax(child,depth-1,False)
            best = max(best,score)
        return best
    
    else:
        best = math.inf
        for action in get_actions(state):
            child = apply_action(state,action)
            score = minimax(child,depth-1,True)
            best = min(score,best)
        return best
        