from abc import abstractclassmethod, abstractmethod
from typing import List 
from random import randint
from copy import deepcopy

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

class NQueens(Problem):
    def __init__(self, n:int, init_queens: List[int] = None) -> None:
        super().__init__()
        self.n = n
        self.queens = init_queens
        if init_queens is None:
            self.queens = []
            for _ in range(n):
                self.queens.append(randint(0, n-1))

    
    def get_all_childs(self):
        for i in range(self.n):
            curr = self.queens[i]
            for j in range(0, self.n):
                if j==curr:
                    continue
                new_qs = deepcopy(self.queens)
                new_qs[i] = j
                yield NQueens(self.n, new_qs)
    
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

    def is_goad(self) -> bool:
        return self.get_cost() == 0

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