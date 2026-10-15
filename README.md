# Buckshot Roulette — AI Game

A Python implementation of a Buckshot Roulette-style game featuring a game engine and an AI dealer that uses minimax search to choose its moves.

## Overview

This project explores game logic and adversarial decision-making in a turn-based environment. The AI evaluates possible future game states and selects moves using a depth-3 minimax search.

## Features

- **Game engine:** Handles shell rounds, player health, turn transitions, and game-over conditions.
- **AI opponent:** Uses depth-3 minimax search to evaluate possible future states and select dealer moves.
- **Game-state evaluation:** Considers possible outcomes when choosing a move.
- **Turn-based gameplay:** Models the sequence of actions between the player and the dealer.

## Tech Stack

- **Language:** Python
- **AI algorithm:** Minimax search
- **Concepts:** Game trees, state transitions, adversarial decision-making, conditional logic

## How It Works

The game engine maintains the current game state and processes actions as the game progresses.

The dealer's AI uses minimax search to explore possible future states up to a depth of three. It evaluates the resulting states and selects a move according to the search logic implemented in the project.

## Project Structure

The repository contains the game engine and AI logic in separate Python files, keeping gameplay management separate from move selection.

<!-- Update this section to match the actual filenames in the repository. -->

## Getting Started

### Prerequisites

- Python 3 installed
- Any additional dependencies required by the project

### Run

1. Clone the repository:

   ```bash
   git clone https://github.com/DharmikKoradia/AI_Game_Buckshot.git
   cd AI_Game_Buckshot
   ```

2. Install any required dependencies, if applicable.

3. Run the project's main Python entry point.

   Replace the command below with the actual entry-point filename:

   ```bash
   python <entry_point>.py
   ```

## What I Learned

- Structuring a game engine around state transitions.
- Applying minimax search to an adversarial decision-making problem.
- Separating AI decision logic from game mechanics.
- Reasoning about future game states when selecting moves.

## Future Improvements

- Add automated tests for game-state transitions and AI decisions.
- Compare minimax decisions against a simple baseline strategy.
- Improve move evaluation and document the AI's decision-making process.
- Add example gameplay screenshots or a short demo.

## Author

**Dharmik Koradia**

[GitHub Profile](https://github.com/DharmikKoradia)
