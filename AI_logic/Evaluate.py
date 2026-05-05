from Actions import *
import math

def evaluate(state):
    if state.player.hp<=0:
        return 1000
    elif state.dealer.hp<=0:
        return -1000
    else:
        return state.dealer.hp*10 - state.player.hp*10
    
def minimax(state, depth):
    if is_terminal(state) or depth == 0:
        return evaluate(state), []  # empty move list at leaf
    
    best_move = None
    best_sequence = []

    if state.turn == 'Player':
        best = -math.inf
        for action in get_actions(state):
            child = apply_action(state, action)
            value, sequence = minimax(child, depth - 1)

            if value > best:
                best = value
                best_move = action
                best_sequence = sequence  # best child's sequence

        return best, [best_move] + best_sequence  # prepend current best move

    else:
        best = math.inf
        for action in get_actions(state):
            child = apply_action(state, action)
            value, sequence = minimax(child, depth - 1)

            if value < best:
                best = value
                best_move = action
                best_sequence = sequence

        return best, [best_move] + best_sequence