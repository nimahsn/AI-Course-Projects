from state import State

class Node:
    def __init__(self, state: "State", n: int, parent: "Node", depth: int, g_n: int) -> None:
        self.state = state
        self.n = n
        self.parent = parent
        self.depth = depth
        self.heuristic_cost = state.sum_manhattan_distance()
        self.g_n = g_n
        self.total_cost = g_n + self.heuristic_cost