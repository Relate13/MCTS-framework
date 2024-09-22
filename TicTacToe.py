from copy import deepcopy
import random
from MonteCarloTreeSearch import MonteCarloTreeSearch, Node


def print_board(board):
    """Prints the current state of the board with extra spacing for better visibility"""
    for row in board:
        print("  " + "  |  ".join(row))
        print("-----------------")


def check_winner(board, player):
    """Checks if the current player has won"""
    # Check rows
    for row in board:
        if all([cell == player for cell in row]):
            return True
    # Check columns
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
        return True
    return False


def is_full(board):
    """Checks if the board is full (tie condition)"""
    return all([cell != ' ' for row in board for cell in row])


def get_opponent_id(current_player):
    assert current_player in ['X', 'O']
    return 'X' if current_player == 'O' else 'O'


class BoardWrapper:
    def __init__(self, board, player):
        self.board = deepcopy(board)
        self.player = player

    def get_available_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

    def get_child(self, move):
        board = deepcopy(self.board)
        board[move[0]][move[1]] = self.player
        return BoardWrapper(board, get_opponent_id(self.player))

    def get_all_children(self):
        return [self.get_child(move) for move in self.get_available_moves()]

    def get_random_child(self):
        return self.get_child(random.choice(self.get_available_moves()))


class MctsAgent(MonteCarloTreeSearch):

    def __init__(self, state: BoardWrapper):
        super().__init__(state)
        self.player = state.player

    def create_node(self, state: BoardWrapper):
        return Node(state, player=state.player)

    def simulate(self, node: Node):
        state: BoardWrapper = node.state
        while not self.is_terminal(state):
            state = state.get_random_child()
        if check_winner(state.board, self.player):
            return 1
        elif check_winner(state.board, get_opponent_id(self.player)):
            return -1
        return 0

    def generate_future_states(self, state: BoardWrapper) -> list:
        return state.get_all_children()

    def is_terminal(self, state) -> bool:
        return check_winner(state.board, 'X') or check_winner(state.board, 'O') or is_full(state.board)


def main():
    """Main function to handle the game loop"""
    # Initialize the board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'

    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")

        # Input position
        if current_player == 'X':
            try:
                row, col = map(int, input("Enter row and column (0-2), format: row,col: ").split(","))
            except ValueError:
                print("Invalid input. Please enter in 'row,col' format.")
                continue

            # Check if input is valid
            if row not in range(3) or col not in range(3):
                print("Row or column is out of range. Please enter values between 0 and 2.")
                continue
            if board[row][col] != ' ':
                print("This position is already taken. Please choose another.")
                continue

            # Update the board
            board[row][col] = current_player
        elif current_player == 'O':
            state = BoardWrapper(board, current_player)
            agent = MctsAgent(state)
            new_state, search = agent.search(time_limit=0.5)
            print("MCTS search completed, number of iterations:", search)
            board = new_state.board

        # Check if current player has won
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        # Check if the board is full (tie)
        if is_full(board):
            print_board(board)
            print("It's a tie!")
            break

        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'


if __name__ == "__main__":
    main()
