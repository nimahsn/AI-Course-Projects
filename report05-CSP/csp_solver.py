from abc import abstractmethod
from sudoku import Sudoku

class BactrackBase():
    def __init__(self) -> None:
        self.discovered_nodes = 0
        self.failed_branches = 0

    @abstractmethod
    def is_complete(self, csp):
        pass

    @abstractmethod
    def select_unassigned_variable(self, csp):
        pass

    @abstractmethod
    def order_domain_values(self, csp, var):
        pass
    
    @abstractmethod
    def is_consistent(self, csp, var, value):
        pass

    @abstractmethod
    def inference(self, csp, var, value):
        pass

    @abstractmethod
    def remove_assignment(self, csp, var):
        pass

    @abstractmethod
    def add_assignment(self, csp, var, value):
        pass

    @abstractmethod
    def apply_inferences(self, csp, inferences):
        pass

    @abstractmethod
    def revert_inference(self, csp, inferences):
        pass

    def backtrack(self, csp):
        self.discovered_nodes += 1
        if self.is_complete(csp): return csp
        var = self.select_unassigned_variable(csp)
        for value in self.order_domain_values(csp, var):
            inferences = None
            if self.is_consistent(csp, var, value):
                self.add_assignment(csp, var, value)
                inferences = self.inference(csp, var, value)
                if inferences != False:
                    self.apply_inferences(csp, inferences)
                    result = self.backtrack(csp)
                    if result:
                        return result
            self.remove_assignment(csp, var)
            if inferences:
                self.revert_inference(csp, inferences)
        self.failed_branches += 1
        return False

class SudokuBacktrackForwardMRV(BactrackBase):
    def __init__(self) -> None:
        super().__init__()
        self.forward_check_omits = 0
        self.forward_check_cut = 0
        
    def is_complete(self, csp: "Sudoku"):
        if len(csp.variables) == 0:
            return True
        return False

    def select_unassigned_variable(self, csp: "Sudoku"):
        return min(csp.variables, key=lambda var: len(csp.domain[var]))        

    def order_domain_values(self, csp: "Sudoku", var):
        return csp.domain[var]
    
    def is_consistent(self, csp: "Sudoku", var, value):
        return csp.constraint_check(var, value)

    def inference(self, csp: "Sudoku", var, value):
        forward_check_domain = {}
        for neighbor in csp.neighbors[var]:
            if neighbor not in csp.variables:
                continue
            if value not in csp.domain[neighbor]:
                continue
            elif len(csp.domain[neighbor]) == 1:
                self.forward_check_cut += 1
                return False
            else:
                forward_check_domain[neighbor] = value
        self.forward_check_omits += len(forward_check_domain)
        return forward_check_domain

    def remove_assignment(self, csp: "Sudoku", var):
        csp.board[var[0]][var[1]] = 0
        csp.variables.add(var)
    
    def add_assignment(self, csp: "Sudoku", var, value):
        csp.board[var[0]][var[1]] = value
        csp.variables.remove(var)

    def apply_inferences(self, csp: "Sudoku", inferences: dict):
        for var in inferences.keys():
            csp.domain[var].remove(inferences[var])

    def revert_inference(self, csp: "Sudoku", inferences: dict):
        for var in inferences.keys():
            csp.domain[var].add(inferences[var])
