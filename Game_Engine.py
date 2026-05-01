
import random
import math
import sys
import os

#importing BOSS_DK's files :]
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AI_logic'))

from State import GameState, Player
from Actions import get_actions, is_terminal, apply_action
from Evaluate import evaluate, minimax


#shell manage, 

def load_shells(state):
    """
    Loads a fresh round of shells into the shotgun.

    Rules:
    - 2 to 8 total shells per round
    - At least 1 Live and at least 1 Blank guaranteed
    - Order is randomized (nobody knows the sequence)
    - shell_index resets to 0

    Returns:
        (live_count, blank_count) — so the UI can announce them
    """
    total = random.randint(2, 8)
    live_count = random.randint(1, total - 1)   # guarantees at least 1 blank
    blank_count = total - live_count

    shells = ['Live'] * live_count + ['Blank'] * blank_count
    random.shuffle(shells)

    state.shells = shells
    state.shell_index = 0

    return live_count, blank_count


#Game state after round fire

def execute_shot(state, target):
    """
    Fires the current shell at the chosen target.
    This modifies the REAL game state (not a copy).

    Args:
        state:  the live GameState object
        target: 'self' or 'opponent'

    Returns:
        (shell_type, damage_dealt, turn_changed)
        shell_type  : 'Live' or 'Blank'
        damage_dealt: bool — did someone lose HP?
        turn_changed: bool — does the turn switch to the other player?
    """
    shell = state.shells[state.shell_index]
    state.shell_index += 1

    shooter = state.turn
    damage_dealt = False
    turn_changed = False

    if target == 'opponent':
        if shell == 'Live':
            # Shooter hits the OTHER player
            if shooter == 'Player':
                state.dealer.hp -= 1
            else:
                state.player.hp -= 1
            damage_dealt = True
        # Shooting opponent ALWAYS switches turn (live or blank)
        state.turn = 'Dealer' if shooter == 'Player' else 'Player'
        turn_changed = True

    elif target == 'self':
        if shell == 'Live':
            # Shooter hits THEMSELVES
            if shooter == 'Player':
                state.player.hp -= 1
            else:
                state.dealer.hp -= 1
            damage_dealt = True
            # Live self-shot: turn switches
            state.turn = 'Dealer' if shooter == 'Player' else 'Player'
            turn_changed = True
        else:
            # Blank self-shot: shooter gets ANOTHER turn (no switch)
            turn_changed = False

    return shell, damage_dealt, turn_changed


#Ai move selection (baaki hai,samja nhi gpt code baadmein karunga after tera ai engine hojaye ;[ )


#game state chek 

def check_round_over(state):
    """Returns True if all shells in the current round have been fired."""
    return state.shell_index >= len(state.shells)


def check_game_over(state):
    """
    Checks if someone has died.
    Returns:
        'player_wins'  — if dealer HP <= 0
        'dealer_wins'  — if player HP <= 0
        None           — game still going
    """
    if state.dealer.hp <= 0:
        return 'player_wins'
    elif state.player.hp <= 0:
        return 'dealer_wins'
    return None
