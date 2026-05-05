import time
import os
import sys

# ─── Make AI_logic importable ─────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AI_logic'))

from State import GameState
from Game_Engine import (
    load_shells, get_ai_move, execute_shot,
    check_round_over, check_game_over
)


# ═══════════════════════════════════════════════════
#                    HELPERS
# ═══════════════════════════════════════════════════

def clear_screen():
    """Clears the terminal for a clean look."""
    os.system('cls' if os.name == 'nt' else 'clear')


def slow_print(text, delay=0.03):
    """Prints text character by character for dramatic effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # newline


# ═══════════════════════════════════════════════════
#                  DISPLAY
# ═══════════════════════════════════════════════════

def show_status(state, live_count, blank_count):
    """Shows the current game status dashboard."""
    shells_remaining = len(state.shells) - state.shell_index
    print("\n" + "=" * 50)
    print("         ⚡ BUCKSHOT ROULETTE ⚡")
    print("=" * 50)
    print(f"  🧑 YOU (Player):  {'❤️ ' * state.player.hp}  ({state.player.hp} HP)")
    print(f"  🤖 DEALER (AI):   {'❤️ ' * state.dealer.hp}  ({state.dealer.hp} HP)")
    print("-" * 50)
    print(f"  🔫 Shells remaining: {shells_remaining}")
    print(f"  💀 Live: {live_count}  |  ⬜ Blank: {blank_count}")
    print("=" * 50)


# ═══════════════════════════════════════════════════
#                 PLAYER TURN
# ═══════════════════════════════════════════════════

def player_turn(state):
    """Handles the player's turn — shows options and gets input."""
    print("\n🎯 YOUR TURN")
    print("-" * 30)
    print("  [1] 🔫 Shoot the DEALER")
    print("  [2] 🔫 Shoot YOURSELF")
    print("-" * 30)

    while True:
        choice = input("  Your choice (1 or 2): ").strip()
        if choice in ('1', '2'):
            break
        print("  ❌ Invalid! Enter 1 or 2.")

    if choice == '1':
        target = 'opponent'
        target_name = 'Dealer'
    else:
        target = 'self'
        target_name = 'yourself'

    print(f"\n  You aim at {target_name}...")
    time.sleep(1)

    shell, damage, turn_changed = execute_shot(state, target)

    if shell == 'Live':
        slow_print("  💥 BANG! It was LIVE!")
        if target == 'self':
            slow_print(f"  😵 You take 1 damage! ({state.player.hp} HP left)")
        else:
            slow_print(f"  🎯 Dealer takes 1 damage! ({state.dealer.hp} HP left)")
    else:
        slow_print("  💨 *click* — It was BLANK.")
        if target == 'self':
            slow_print("  😎 You get another turn!")

    time.sleep(0.5)


# ═══════════════════════════════════════════════════
#                 DEALER TURN
# ═══════════════════════════════════════════════════

def dealer_turn(state):
    """Handles the AI dealer's turn — thinks and acts."""
    print("\n🤖 DEALER'S TURN")
    print("-" * 30)
    slow_print("  The Dealer studies the shotgun...")
    time.sleep(0.8)

    # Ask the AI what to do
    ai_action = get_ai_move(state)

    # ── Map AI actions to engine targets ──────────
    # AI actions are named from the *entity* perspective:
    #   'shoot_player' → Dealer shoots YOU   → target = 'opponent'
    #   'shoot_dealer' → Dealer shoots SELF  → target = 'self'
    if ai_action == 'shoot_player':
        target = 'opponent'
        slow_print("  The Dealer aims at YOU... 😰")
    elif ai_action == 'shoot_dealer':
        target = 'self'
        slow_print("  The Dealer aims at ITSELF... 🤔")
    else:
        # Fallback (shouldn't happen with current actions, but safe default)
        target = 'opponent'
        slow_print("  The Dealer aims at YOU...")

    time.sleep(1)

    shell, damage, turn_changed = execute_shot(state, target)

    if shell == 'Live':
        slow_print("  💥 BANG! It was LIVE!")
        if target == 'opponent':
            slow_print(f"  😵 You take 1 damage! ({state.player.hp} HP left)")
        else:
            slow_print(f"  🤖 Dealer takes 1 damage! ({state.dealer.hp} HP left)")
    else:
        slow_print("  💨 *click* — It was BLANK.")
        if target == 'self':
            slow_print("  🤖 Dealer gets another turn!")

    time.sleep(0.5)


# ═══════════════════════════════════════════════════
#                  MAIN GAME
# ═══════════════════════════════════════════════════

def main():
    """Main game loop — the heart of everything."""
    clear_screen()

    # ── Title Screen ──────────────────────────────
    print("\n" + "=" * 50)
    print("     💀 BUCKSHOT ROULETTE 💀")
    print("        ⚡ AI EDITION ⚡")
    print("=" * 50)
    print("\n  You sit across from the Dealer.")
    print("  A shotgun lies on the table between you.")
    print("  Only one of you will walk away.\n")
    input("  Press ENTER to begin...")

    # ── Create the game state ─────────────────────
    state = GameState()
    round_num = 0

    # ── GAME LOOP ─────────────────────────────────
    while True:
        # Load new shells at start or when round is over
        round_num += 1
        clear_screen()

        print(f"\n  ═══ ROUND {round_num} ═══")
        slow_print("  🔫 The Dealer loads the shotgun...")
        time.sleep(0.5)

        live_count, blank_count = load_shells(state)

        slow_print(f"  Loaded: {live_count} Live 💀 and {blank_count} Blank ⬜")
        print(f"  Total: {live_count + blank_count} shells")
        time.sleep(1)

        # ── ROUND LOOP — play until shells run out or someone dies ──
        while True:
            show_status(state, live_count, blank_count)

            # Check if someone died
            result = check_game_over(state)
            if result:
                break

            # Check if shells are exhausted
            if check_round_over(state):
                slow_print("\n  🔄 All shells fired! Reloading...")
                time.sleep(1)
                break

            # Play the current turn
            if state.turn == 'Player':
                player_turn(state)
            else:
                dealer_turn(state)

        # ── Check for game over ───────────────────
        result = check_game_over(state)
        if result:
            clear_screen()
            print("\n" + "=" * 50)
            if result == 'player_wins':
                print("  🏆 YOU WIN! 🏆")
                print("  The Dealer slumps over. You survive.")
            else:
                print("  💀 YOU LOSE 💀")
                print("  The Dealer grins. Everything fades.")
            print("=" * 50)

            # Ask to play again
            again = input("\n  Play again? (y/n): ").strip().lower()
            if again == 'y':
                state = GameState()
                round_num = 0
                continue
            else:
                print("\n  Thanks for playing! 👋")
                break


if __name__ == '__main__':
    main()
