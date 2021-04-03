from heapq import heapify, heappop, heappush, heapreplace
from typing import Callable, List, Sequence, Tuple
from problems import Problem
from random import random
import math
import time

class SolverLog:
    def __init__(self) -> None:
        self.depth = 0
        self.nodes = 0
        self.costs = []
        self.elapsed_time = 0
        self.temperatures=[]
        

class HillClimb:
    def __init__(self, save_log = False) -> None:
        self.save_log = save_log

    def solve(self, problem: "Problem") -> "Problem":
        if self.save_log:
            log = SolverLog()
            log.costs = [problem.get_cost()]
            start_time_ns = time.time_ns()
        while True:
            if problem.is_goal():
                if self.save_log:
                    log.elapsed_time = time.time_ns() - start_time_ns
                    self.log = log
                return problem
            min_child = None
            min_cost = math.inf
            for child in problem.get_all_childs():
                new_cost = child.get_cost()
                if new_cost < min_cost:
                    min_child = child
                    min_cost = new_cost
            if min_cost < problem.get_cost():
                if self.save_log:
                    log.depth += 1
                    log.costs.append(min_cost)
                problem = min_child
            else:
                if self.save_log:
                    log.elapsed_time = time.time_ns() - start_time_ns
                    self.log = log
                return problem
                

class BeamSearch:
    def __init__(self, beam: int, save_log = False) -> None:
        self.save_log = save_log
        self.k = beam
  
    def solve(self, initial_states: List["Problem"]) -> "Problem":
        if self.save_log:
            log = SolverLog()
            start_time_ns = time.time_ns()
        sequence = [None]*self.k
        for i,prob in enumerate(initial_states):
            sequence[i] = (prob.get_cost(), i, prob)
        entry = self.k        
        sequence.sort()
        if self.save_log:
            l=[]
            for prob in sequence:
                l.append(prob[0])
            log.costs.append(l)

        while True:
            if sequence[0][2].is_goal():
                if self.save_log:
                    log.elapsed_time = time.time_ns() - start_time_ns
                    self.log = log
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
                if self.save_log:
                    log.elapsed_time = time.time_ns() - start_time_ns
                    self.log = log
                return sequence[0][2]
            for i in range(self.k):
                sequence[i] = heappop(heap)
            if self.save_log:
                log.depth += 1
                l = []
                for problem in sequence:
                    l.append(problem[0])
                log.costs.append(l)

class SimulatedAnnealing:
    def __init__(self, min_temp: float = 1e-6, max_iter: int = 1000, scale_factor: int = 1.01, save_log = False) -> None:
        self.max_iter = max_iter
        self.min_temp = min_temp
        self.scale = scale_factor
        self.save_log = save_log

    def solve(self, problem: Problem, init_temp: int):
        if self.save_log:
            log = SolverLog()
            start_time_ns = time.time_ns()
        iter = 0
        curr_cost = problem.get_cost()

        for temp in self.scheduler(init_temp, self.scale):
            if self.save_log:
                log.costs.append(curr_cost)
                log.depth += 1
                log.temperatures.append(temp)
            if problem.is_goal() or iter >= self.max_iter or temp < self.min_temp:
                if self.save_log:
                    log.elapsed_time = time.time_ns() - start_time_ns
                    self.log = log
                return problem
            # print("iter: {}, temp: {}, cost: {}".format(iter, temp, problem.get_cost()))
            iter += 1
            random_child = problem.get_random_child()
            new_cost = random_child.get_cost()
            curr_cost = problem.get_cost()
            if new_cost < curr_cost:
                problem = random_child
                curr_cost = new_cost
                continue
            else:
                prob = math.exp((curr_cost - new_cost)/temp)
                toss = random()
                if (toss <= prob):
                    problem = random_child
                    curr_cost = new_cost
                elif self.save_log:
                    log.depth -= 1
                continue
    
    def scheduler(self, init_temp: int, scale: float):
        # iter = 1
        new_temp = init_temp
        while True:
            new_temp = new_temp/scale
            # iter += 1
            yield new_temp