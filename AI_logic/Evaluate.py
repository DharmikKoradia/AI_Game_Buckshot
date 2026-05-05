from Actions import get_actions, apply_action, is_terminal
import math


def evaluate(state):
    """
    Heuristic from the Player's perspective.
    Positive  → good for Player.
    Negative  → good for Dealer.
    """
    if state.player.hp <= 0:
        return -1000          # Player is dead → worst outcome
    elif state.dealer.hp <= 0:
        return 1000           # Dealer is dead → best outcome
    else:
        # More dealer HP remaining is bad; more player HP is good.
        return state.player.hp * 10 - state.dealer.hp * 10


def get_shell_probs(state):
    """Returns (p_live, p_blank) from the remaining unfired shells."""
    remaining = state.shells[state.shell_index:]
    total = len(remaining)
    if total == 0:
        return 0.0, 0.0
    return remaining.count('Live') / total, remaining.count('Blank') / total


def expected_value(state, action, depth, alpha, beta):
    """
    For a player who doesn't know the current shell, compute the
    expected minimax value of `action` by branching on both possible
    shell outcomes weighted by their probability.
    """
    remaining = state.shells[state.shell_index:]
    total = len(remaining)
    if total == 0:
        return evaluate(state)

    p_live  = remaining.count('Live')  / total
    p_blank = remaining.count('Blank') / total
    ev = 0.0

    if p_live > 0:
        live_state = state.copy()
        live_state.shells[live_state.shell_index] = 'Live'
        child = apply_action(live_state, action)
        val, _ = minimax(child, depth - 1, alpha, beta)
        ev += p_live * val

    if p_blank > 0:
        blank_state = state.copy()
        blank_state.shells[blank_state.shell_index] = 'Blank'
        child = apply_action(blank_state, action)
        val, _ = minimax(child, depth - 1, alpha, beta)
        ev += p_blank * val

    return ev


def minimax(state, depth, alpha=-math.inf, beta=math.inf):
    """
    Minimax with Alpha-Beta pruning.

    alpha : best score the maximiser (Player) is already guaranteed
    beta  : best score the minimiser (Dealer) is already guaranteed

    Pruning:
      - Maximiser prunes when value >= beta  (the minimiser above would never
        allow this branch because it already has something better).
      - Minimiser prunes when value <= alpha (the maximiser above would never
        allow this branch because it already has something better).

    Returns (score, move_sequence).
    """
    if is_terminal(state) or depth == 0:
        return evaluate(state), []

    best_move = None
    best_sequence = []

    if state.turn == 'Player':          # Maximising player
        best = -math.inf
        for action in get_actions(state):
            child = apply_action(state, action)
            value, sequence = minimax(child, depth - 1, alpha, beta)

            if value > best:
                best = value
                best_move = action
                best_sequence = sequence

            alpha = max(alpha, best)
            if best >= beta:            # Beta cut-off
                break

        return best, [best_move] + best_sequence

    else:
        # Dealer doesn't know the shell — picks based on expected value
        best = math.inf
        for action in get_actions(state):
            value = expected_value(state, action, depth, alpha, beta)

            if value < best:
                best = value
                best_move = action

            beta = min(beta, best)
            if best <= alpha:           # Alpha cut-off
                break

        return best, [best_move]