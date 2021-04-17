from typing import List, Tuple

class Sudoku():
    def __init__(self, init_board: List[List[int]]) -> None: #init_board must be a 9x9 list of integers. 
        self.board = init_board
        self.neighbors = {}
        for i in range(9):
            for j in range(9):
                self.neighbors[(i,j)] = [self.get_neighbors((i,j))]
        self.variables = set()
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.variables.add((i,j))
        self.out_of_domain_dict = {}
        for var in self.variables:
            self.out_of_domain_dict[var] = []

    def get_domain(self, index):
        d = list(range(1,10))
        for out in self.out_of_domain_dict[index]:
            d.remove(out)
        return d
        
    def constraint_check(self, index, value) -> bool:
        for neighbor in self.neighbors[index]:
            if self.board[neighbor[0]][neighbor[1]] == value:
                return False

    @staticmethod
    def get_neighbors(index: Tuple[int, int]):
        for i in range(9):
            if i == index[0]:
                continue
            yield (i, index[1])
        for j in range(9):
            if j == index[1]:
                continue
            yield (index[0], j)

        r = index[0] - index[0]%3
        c = index[1] - index[1]%3
        for i in range(r, r+3):
            if i == index[0]:
                continue
            for j in range(c, c+3):
                if j == index[1]:
                    continue
                yield (i,j)
    
