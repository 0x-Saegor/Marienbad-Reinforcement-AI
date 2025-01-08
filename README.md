# Marienbad Game with Reinforcement Learning AI

This repository contains an implementation of the **Marienbad game**, enhanced with an Artificial Intelligence (AI) that learns optimal strategies through **reinforcement learning**.

## Features
- **Marienbad Game Logic**: A flexible implementation of the classic game rules.
- **Reinforcement Learning AI**: The AI uses a reward-based mechanism to improve its gameplay over time.
- **Customizable Gameplay**: Play against the AI or simulate matches between the AI and the playing algorithm (whether it is playing randomly or to win).
- **Visualization**: Graphs to track the AI's learning progress over time.

### Key Dependencies
- `random` to retrieve the next move choice for the AI, it uses the weights and probabilities.
- `matplotlib` for visualizations.

## How to Play
1. Clone the repository:

   ```bash
   git clone https://github.com/0x-Saegor/Marienbad-Reinforcement-AI.git
   cd Marienbad-Reinforcement-AI
   ```

2. Run the game:

   ```bash
   python marienbad.py
   ```

3. Follow the prompts to:
   - Play against the AI.
   - Play against another player
   - Simulate multiple AI matches

## AI Training
The AI uses reinforcement learning to improve its strategies:
1. **Initialization**: AI starts with no knowledge of the game.
2. **Exploration**: Plays random moves to explore game states.
3. **Learning**: Rewards and penalties adjust the AI's strategy based on outcomes.

## Game Rules
- The game begins with several rows of objects (e.g., matches).
- Players take turns removing any number of objects from a single row (1 is the minimum to remove).
- The player that will take the last object wins the game.

## Example Output
```
Current Board:
Row 1: |
Row 2: |||
Row 3: |||||
Row 4: |||||||

Your Turn:
Choose a row and number of objects to remove.
```

## Contributions
Contributions are welcome! If you find a bug or want to propose an improvement :
1. Fork the repository.
2. Create a new branch for your feature.
3. Submit a pull request.
