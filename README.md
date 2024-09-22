# Monte Carlo Tree Search (MCTS) Framework

This repository provides a basic framework for implementing a Monte Carlo Tree Search (MCTS) algorithm in Python. MCTS is a heuristic search algorithm used in decision-making processes, particularly in games and simulations, to explore possible future moves. It combines random sampling of the search space with a tree structure to balance exploration and exploitation using the Upper Confidence Bound (UCB) formula.

### Key Components:
- **Node Class**: Represents each state in the search tree, storing important information like visit count, reward, and parent/child relationships.
- **MCTS Class**: Manages the search process by selecting nodes, expanding them with potential future states, simulating outcomes, and backpropagating the results to update the tree.

### Extend the Framework:
To integrate the MCTS algorithm with your specific problem or game, you need to modify or implement the following four methods:

1. **`simulate(self, node: Node) -> int`**: Simulate the game from a given node and return the result (e.g., win/loss/tie or score).
2. **`create_node(self, state) -> Node`**: Define how a new node is created based on the current state, you can store some other information in the node.
3. **`generate_future_states(self, state) -> list`**: Generate possible future states from the current state.
4. **`is_terminal(self, state) -> bool`**: Determine if a given state represents a terminal state in the game (e.g., win/loss/tie condition).

By overloading these methods, you can customize this MCTS framework to suit a wide variety of decision-making problems, such as board games, pathfinding, or resource management tasks.

### Example: Tic-Tac-Toe
As an example, this repository includes an implementation of Tic-Tac-Toe (3x3 grid). You can explore how MCTS can be applied to this simple game by modifying the methods for simulating the game, generating future states, and determining terminal conditions.
