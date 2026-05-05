from Actions import get_actions, apply_action, is_terminal
import math


def evaluate(state):
    """
    Heuristic from the Player's perspective.
    Positive  → good for Player.
    Negative  → good for Dealer.
    """
    if state.player.hp <= 0:
        return -1000
    elif state.dealer.hp <= 0:
        return 1000
    else:
        return state.player.hp * 10 - state.dealer.hp * 10


def get_shell_probs(state):
    """Returns (p_live, p_blank) from the remaining unfired shells."""
    remaining = state.shells[state.shell_index:]
    total = len(remaining)
    if total == 0:
        return 0.0, 0.0
    return remaining.count('Live') / total, remaining.count('Blank') / total


def expected_value_for_action(state, action, depth, alpha, beta):
    """
    Neither player knows the current shell — compute the expected minimax
    value of `action` by branching on BOTH possible shell outcomes,
    weighted by their probability.

    This is used for BOTH the Player and the Dealer, making the search
    fair: neither side gets to cheat by peeking at shell_index.
    """
    remaining = state.shells[state.shell_index:]
    total = len(remaining)

    # Edge case: no shells left, just evaluate
    if total == 0:
        return evaluate(state)

    p_live  = remaining.count('Live')  / total
    p_blank = remaining.count('Blank') / total
    ev = 0.0

    # Branch: what if the next shell is Live?
    if p_live > 0:
        live_state = state.copy()
        live_state.shells[live_state.shell_index] = 'Live'
        child = apply_action(live_state, action)
        val, _ = minimax(child, depth - 1, alpha, beta)
        ev += p_live * val

    # Branch: what if the next shell is Blank?
    if p_blank > 0:
        blank_state = state.copy()
        blank_state.shells[blank_state.shell_index] = 'Blank'
        child = apply_action(blank_state, action)
        val, _ = minimax(child, depth - 1, alpha, beta)
        ev += p_blank * val

    return ev


def minimax(state, depth, alpha=-math.inf, beta=math.inf):
    """
    Minimax with Alpha-Beta pruning — FAIR version.

    NEITHER the Player nor the Dealer knows the next shell's type.
    Both sides choose actions based on expected value over the
    probability distribution of remaining shells.

    This prevents the AI from cheating while still playing optimally
    given the information both sides actually have.

    Returns (score, move_sequence).
    """
    if is_terminal(state) or depth == 0:
        return evaluate(state), []

    best_move = None
    best_sequence = []

    if state.turn == 'Player':          # Maximising — Player wants highest score
        best = -math.inf
        for action in get_actions(state):
            # Use expected value: Player doesn't know the next shell
            value = expected_value_for_action(state, action, depth, alpha, beta)

            if value > best:
                best = value
                best_move = action
                best_sequence = []      # Expected-value branches have no single sequence

            alpha = max(alpha, best)
            if best >= beta:            # Beta cut-off
                break

        return best, [best_move] + best_sequence

    else:                               # Minimising — Dealer wants lowest score
        best = math.inf
        for action in get_actions(state):
            # Use expected value: Dealer doesn't know the next shell either
            value = expected_value_for_action(state, action, depth, alpha, beta)

            if value < best:
                best = value
                best_move = action

            beta = min(beta, best)
            if best <= alpha:           # Alpha cut-off
                break

        return best, [best_move]