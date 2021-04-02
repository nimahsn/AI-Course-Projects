from heapq import heapify, heappop, heappush, heapreplace
from typing import Callable, List, Sequence
from problems import Problem
from random import random
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

class SimulatedAnnealing:
    def __init__(self, min_temp: float = 1e-6, max_iter: int = 1000, scale_factor: int = 1.01) -> None:
        self.max_iter = max_iter
        self.min_temp = min_temp
        self.scale = scale_factor    

    def solve(self, problem: Problem, init_temp: int):
        iter = 0
        for temp in self.scheduler(init_temp, self.scale):
            if problem.is_goal() or iter >= self.max_iter or temp < self.min_temp:
                return problem
            # print("iter: {}, temp: {}, cost: {}".format(iter, temp, problem.get_cost()))
            iter += 1
            random_child = problem.get_random_child()
            new_cost = random_child.get_cost()
            curr_cost = problem.get_cost()
            if new_cost < curr_cost:
                problem = random_child
                continue
            else:
                prob = math.exp((curr_cost - new_cost)/temp)
                toss = random()
                if (toss <= prob):
                    problem = random_child
                continue
    
    def scheduler(self, init_temp: int, scale: float):
        # iter = 1
        new_temp = init_temp
        while True:
            new_temp = new_temp/scale
            # iter += 1
            yield new_temp
