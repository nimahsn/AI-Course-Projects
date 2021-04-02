from abc import abstractmethod
from itertools import product
from typing import List, Tuple 
from random import randint
from copy import deepcopy
import pandas as pd
import numpy as np
from numpy.random import permutation

class Problem:
    @abstractmethod
    def get_all_childs(self) -> "Problem":
        pass

    @abstractmethod
    def get_cost(self) -> int:
        pass
    
    @abstractmethod
    def is_goal(self) -> bool:
        pass

    @abstractmethod
    def get_random_child(self) -> "Problem":
        pass

class NQueens(Problem):
    def __init__(self, n: int, queens: List[int] = None, init_queens: List[int] = None) -> None:
        super().__init__()
        self.n = n
        self.queens = queens
        if queens is None:
            self.queens = []
            for _ in range(n):
                self.queens.append(randint(0, n-1))
        self.init_queens = init_queens
        if (init_queens is None):
            self.init_queens = self.queens
    
    def get_all_childs(self):
        for i in range(self.n):
            curr = self.queens[i]
            for j in range(0, self.n):
                if j==curr:
                    continue
                new_qs = deepcopy(self.queens)
                new_qs[i] = j
                yield NQueens(self.n, new_qs, init_queens=self.init_queens)
    
    def get_cost(self) -> int:
        attacks = 0
        for curr_column in range(self.n):
            curr_row = self.queens[curr_column]
            for next_column in range(curr_column + 1, self.n):
                next_row = self.queens[next_column]
                if (next_row == curr_row):
                    attacks += 1
                    continue
                if abs(next_column - curr_column) == abs(next_row - curr_row):
                    attacks += 1
                    continue
        return attacks

    def is_goal(self) -> bool:
        return self.get_cost() == 0

    def get_random_child(self) -> "Problem":
        rand_col = randint(0, self.n-1)
        rand_row = randint(0, self.n-1)
        new_qs = deepcopy(self.queens)
        new_qs[rand_col] = rand_row
        return NQueens(self.n, new_qs, self.init_queens)


    def __repr__(self) -> str:
        s = ""
        for row in range(self.n):
            for col in range(self.n):
                if (self.queens[col] == row):
                    s+="| # |"
                else:
                    s+="|   |"
            s+="\n"+("-"*self.n*5)+"\n"
        s+="\n cost= {}".format(self.get_cost())
        return s

class TravellingSalesPerson(Problem):
    def __init__(self, n: int, cities_routes: "np.ndarray", current_answer: List[Tuple[int, int]] = None):
        super().__init__()
        self.n = n
        self.cities = cities_routes
        self.curr_answer = current_answer
        if current_answer is None:
            self.curr_answer = self.generate_random_solution()

    def get_all_childs(self) -> "Problem":
        for swap in product(list(range(self.n)), repeat=2):
            if swap[0] == swap[1]:
                continue
            new_sol = deepcopy(self.curr_answer)
            new_sol[swap[0]], new_sol[swap[1]] = new_sol[swap[1]], new_sol[swap[0]]
            yield TravellingSalesPerson(self.n, self.cities, new_sol)
        

    def get_random_child(self) -> "Problem":
        first_index = randint(0, self.n-1)
        second_index = first_index
        while second_index==first_index:
            second_index = randint(0, self.n-1)
        new_sol = deepcopy(self.curr_answer)
        new_sol[first_index], new_sol[second_index] = new_sol[second_index], new_sol[first_index]
        return TravellingSalesPerson(self.n, self.cities, new_sol)

    def get_cost(self) -> int:
        curr = self.curr_answer[0]
        cost = 0
        for next in self.curr_answer[1:]:
            cost += self.cities[curr][next]
            curr = next
        cost += self.cities[self.curr_answer[0]][curr]
        return cost

    def is_goal(self) -> bool:
        return False

    
    def load_from_file(path: str) -> "TravellingSalesPerson":
        matrix = pd.read_csv(path, delim_whitespace=True, header=None).to_numpy()
        return TravellingSalesPerson(matrix.shape[0] ,matrix)   

    def generate_random_solution(self) -> List[int]:
        return permutation(range(self.n))
