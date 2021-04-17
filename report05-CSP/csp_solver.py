from abc import abstractmethod

class BactrackBase():
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
    def remove_value(self, csp, var):
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
        if self.is_complete(csp): return csp
        var = self.select_unassigned_variable(csp)
        for value in self.order_domain_values(csp, var):
            if self.is_consistent(csp, var, value):
                self.add_assignment(csp, var, value)
                inferences = self.inference(csp, var, value)
                if inferences:
                    self.apply_inferences(csp, inferences)
                    result = self.backtrack(csp)
                    if result:
                        return result
            self.remove_value(csp, var)
            self.revert_inference(self, inferences)
        return False