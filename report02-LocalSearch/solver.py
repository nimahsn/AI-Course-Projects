from heapq import heapify, heappop, heappush
from problems import NQueens, Problem
import math

class HillClimb:
    def __init__(self) -> None:
        pass

    def solve(self, problem: Problem):
        while True:
            if problem.is_goal():
                return problem
            min_child = None
            min_cost = math.inf
            for child in problem.get_all_childs():
                new_cost = child.get_cost()
                if new_cost < min_cost:
                    min_child = child
                    min_cost = new_cost
            if min_cost < problem.get_cost():
                problem = min_child
            else:
                return problem
                

class BeamSearch:
    def __init__(self, k: int) -> None:
        self.k = k
        self.heap = []
        heapify(self.heap)
        pass
  
    def solve(self, prblem: Problem):
        pass

hl = HillClimb()
print(hl.solve(NQueens(8)))