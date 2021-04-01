import copy
import queue
from typing import List, Tuple
from node import Node
from queue import Queue
from state import State, Car
from heapq import heapify, heappop, heappush
from itertools import product
 
class ParkingSolver:
    def __init__(self, n: int) -> None:
        self.n = n
        self.frontier_heap: List[Tuple[int, int, "Node"]] = []
        heapify(self.frontier_heap)
        self.explored_set = []
        self.__entry_i = 0

    def explore_nodes(self, node: "Node"):
        dirs = ["up", "right", "left", "down", "stay"]
        for action in product(dirs, repeat=self.n):
            state = copy.deepcopy(node.state)
            result = state.move(action)
            if result == -1:
                continue
            if state in self.explored_set:
                continue
            self.explored_set.append(state)
            g_n = node.g_n + self.n
            for ac in action:
                if ac == "stay":
                    g_n -= 1
            g_n += result
            new_node = Node(state, self.n, node, depth=node.depth + 1, g_n=g_n)
            heappush(self.frontier_heap, (new_node.total_cost, self.__entry_i, new_node))
            self.__entry_i+=1

        
    def ast_search(self, initial_state: "State"):
        init_node = Node(initial_state, self.n, None, 0, 0)
        heappush(self.frontier_heap, (init_node.total_cost, self.__entry_i, init_node))
        self.explored_set.append(init_node.state)
        self.__entry_i +=1
        while self.frontier_heap:
            popped_node: "Node" = heappop(self.frontier_heap)[2]
            if popped_node.state.check_goal_state():
                print("\n\n")
                print(self.__entry_i)
                return popped_node
            self.explore_nodes(popped_node)

        else:
            print("Dead End!")


def print_route(node: "Node"):
    if node == None:
        return
    print_route(node.parent)
    print(node.state)
            
n = 4
solver = ParkingSolver(n)
cars = [Car(loc=[i, 0], target=[n-i-1, n-1]) for i in range(n)]
state: "State" = State(cars=cars, n=n)
final_state = solver.ast_search(state)
print(final_state.depth)
print_route(final_state)
print(final_state.g_n)
