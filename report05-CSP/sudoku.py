from typing import Dict, List, Set, Tuple

class Sudoku():
    def __init__(self, init_board: List[List[int]], make_arc_consistency: bool = True) -> None: #init_board must be a 9x9 list of integers. 
        self.board = init_board
        self.neighbors = {}
        for i in range(9):
            for j in range(9):
                self.neighbors[(i,j)] = list(self.get_neighbors((i,j)))
        self.variables = set()
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.variables.add((i,j))
        self.domain: Dict[Tuple[int, int], Set[int]] = {}
        for var in self.variables:
            self.domain[var] = set(range(1, 10))
        if make_arc_consistency:
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] != 0:
                        for var in self.neighbors[(i,j)]:
                            if var in self.variables and self.board[i][j] in self.domain[var]:
                                self.domain[var].remove(self.board[i][j])
        
    def constraint_check(self, index, value) -> bool:
        for neighbor in self.neighbors[index]:
            if self.board[neighbor[0]][neighbor[1]] == value:
                return False
        return True

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
    
    def __repr__(self) -> str:
        s = ""
        for r in self.board:
            s+=str(r) + "\n"
        return s
    
