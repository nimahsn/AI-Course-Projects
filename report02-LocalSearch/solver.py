from heapq import heapify, heappop, heappush, heapreplace
from typing import List, Sequence
from problems import NQueens, Problem
import math

class HillClimb:
    def __init__(self) -> None:
        pass

    def solve(self, problem: "Problem"):
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
    def __init__(self, beam: int) -> None:
        self.k = beam
  
    def solve(self, initial_states: List["Problem"]):
        sequence = [None]*self.k
        for i,prob in enumerate(initial_states):
            sequence[i] = (prob.get_cost(), i, prob)
        entry = self.k        
        sequence.sort()

        while True:
            if sequence[0][2].is_goal():
                return sequence[0][2]
            heap = []
            updated = False
            for state in sequence:
                heappush(heap, state)
                for child in state[2].get_all_childs():
                    child_cost = child.get_cost()
                    if child_cost < state[0]:
                        heappush(heap, (child_cost, entry, child))
                        entry += 1
                        updated = True
            if not updated:
                return sequence[0][2]
            for i in range(self.k):
                sequence[i] = heappop(heap)
            del heap
