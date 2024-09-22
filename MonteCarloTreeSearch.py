import math
import random
import time


class Node:
    def __init__(self, state, parent=None, player=None):
        self.expanded = False
        self.is_terminal = False
        self.state = state
        self.parent = parent
        self.player = player
        self.children = []
        self.n = 0
        self.t = 0

    def add_child(self, child: 'Node'):
        self.children.append(child)
        child.parent = self

    def backpropagation(self, reward):
        self.n += 1
        self.t += reward
        if self.parent:
            self.parent.backpropagation(reward)


class MonteCarloTreeSearch:

    def __init__(self, state):
        self.root = self._create_node(state)
        # expand the root node
        self.expand(self.root)

    def search(self, iterations=2 ** 31 - 1, time_limit=0.9):
        start_time = time.time()
        search = 0
        for _ in range(iterations):
            if time.time() - start_time > time_limit:
                break
            current = self.select(self.root)
            if current.n != 0:
                current = self.expand(current)
            reward = self.simulate(current)
            current.backpropagation(reward)
            search += 1
        return self.make_choice().state, search

    def select(self, node: Node) -> Node:
        # get the best child node
        while not node.is_terminal:
            if node.expanded:
                node = self.get_best_child(node)
            else:
                return node  # reached leaf node
        return node

    def expand(self, node: Node) -> Node:
        if node.is_terminal:
            return node
        for state in self.generate_future_states(node.state):
            node.add_child(self._create_node(state))
        node.expanded = True
        if not node.children:
            print('No children')
        return node.children[0]

    def _create_node(self, state) -> Node:
        node = self.create_node(state)
        node.is_terminal = self.is_terminal(state)
        return node

    def get_best_child(self, node: Node) -> Node:
        # perform minimax on the children of the node
        best_children = []
        best_score = float('-inf')
        multiplier = 1 if node.player == self.root.player else -1
        for child in node.children:
            score = ucb(child.t * multiplier, child.n, node.n)
            if score > best_score:
                best_score = score
                best_children = [child]
            elif score == best_score:
                best_children.append(child)
        return random.choice(best_children)

    def make_choice(self):
        best_child = []
        most_visits = float('-inf')
        for child in self.root.children:
            if child.n > most_visits:
                most_visits = child.n
                best_child = [child]
            elif child.n == most_visits:
                best_child.append(child)
        return random.choice(best_child)

    def simulate(self, node: Node) -> int:
        pass

    def create_node(self, state) -> Node:
        pass

    def generate_future_states(self, state) -> list:
        pass

    def is_terminal(self, state) -> bool:
        pass


def ucb(value, n, N, C=2):
    """Upper Confidence Bound for Trees (UCB) formula.
    Arguments:
        value -- value of the node
        n -- number of visits of the node
        N -- number of visits of the parent node
    """
    return value / n + C * math.sqrt(math.log(N) / n) if n != 0 else float('inf')
