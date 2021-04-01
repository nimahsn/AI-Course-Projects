from typing import List, Tuple
import copy

class Car:
    def __init__(self, loc: List[int], target: tuple) -> None:
        self.loc = loc
        self.target = target
        self.init_loc = loc
        self.waiting_for: int = False
        self.dont_remove = False
    
    def check_target(self) -> bool:
        if self.loc == self.target:
            return True
        else:
            return False
    
    def manhattan_distance(self) -> int:
        return abs(self.target[0] - self.loc[0]) + abs(self.target[1] - self.loc[1])
    
    def __str__(self) -> str:
        return str(self.loc)+"->"+str(self.target)

    def __repr__(self) -> str:
        return str(self.loc)+"->"+str(self.target)

class State:
    def __init__(self, cars: List["Car"], n: int) -> None:
        self.cars: List["Car"] = cars
        self.n = n
    
    def move(self, directions: List) -> bool:
        hopped = [False]*self.n
        moved = [False]*self.n
        inner = [None]*self.n
        grid = [inner[:] for _ in range(self.n)]
        for (i, car) in enumerate(self.cars):
            grid[car.loc[0]][car.loc[1]] = i
        self.stays = 0

        def calc_next_loc(index):
            car = self.cars[i]
            dir = directions[i]
            next_loc = car.loc
            if dir == "up":
                next_loc[0] += 1
            elif dir == "down":
                next_loc[0] -= 1
            elif dir == "right":
                next_loc[1] += 1
            elif dir == "left":
                next_loc[1] -= 1
            else : # don't move
                pass
            return next_loc            

        def move_recursive(index: int, next_loc: Tuple[int, int], stay_check = False) -> bool:
            if moved[index]:
                return True
            car = self.cars[index]
            dir = directions[index]
            
            if next_loc[0] >= self.n or next_loc[1] >= self.n or next_loc[0] < 0 or next_loc[1] < 0: # out of bound
                return False

            if grid[next_loc[0]][next_loc[1]] != None and not moved[grid[next_loc[0]][next_loc[1]]]:
                j = grid[next_loc[0]][next_loc[1]]
                car.waiting_for = j

                if self.cars[j].waiting_for == False:
                    if not move_recursive(grid[next_loc[0]][next_loc[1]], calc_next_loc(index)):
                        return False
                else:
                    grid[car.loc[0]][car.loc[1]] = None
                    grid[next_loc[0]][next_loc[1]] = i
                    self.cars[j].dont_remove = True
                    car.waiting_for = False
                    moved[i] = True
                    return True
            
            if grid[next_loc[0]][next_loc[1]] == None:
                if not car.dont_remove:
                    grid[car.loc[0]][car.loc[1]] = None
                    car.dont_remove = False
                car.waiting_for = False
                car.loc = next_loc
                grid[car.loc[0]][car.loc[1]] = index
                moved[index] = True
                return True
            else:
                if directions[grid[next_loc[0]][next_loc[1]]] != "stay":
                    return False
                elif stay_check == False:
                    ii = grid[next_loc[0]][next_loc[1]]
                    if hopped[ii]:
                        return False
                    else:
                        # return False
                        if dir == "up":
                            next_loc[0] += 1
                        elif dir == "down":
                            next_loc[0] -= 1
                        elif dir == "right":
                            next_loc[1] += 1
                        elif dir == "left":
                            next_loc[1] -= 1
                        hopped[ii] = True
                        self.stays += 1
                        return move_recursive(index, next_loc, True)
                else:
                    return False
        
        for i in range(self.n):
            # print(4)
            car = self.cars[i]
            dir = directions[i]
            next_loc = car.loc
            if dir == "up":
                next_loc[0] += 1
            elif dir == "down":
                next_loc[0] -= 1
            elif dir == "right":
                next_loc[1] += 1
            elif dir == "left":
                next_loc[1] -= 1
            else : # don't move
                moved[i] = True
            if not move_recursive(i, next_loc):
                return -1
                
        return self.stays

                            
    def check_goal_state(self) -> bool:
        for car in self.cars:
            if not car.check_target():
                return False
        return True

    def sum_manhattan_distance(self) -> int:
        return sum([car.manhattan_distance() for car in self.cars])
    
    def max_manhattan_distance(self) -> int:
        return max([car.manhattan_distance() for car in self.cars])

    def min_manhattan_distance(self) -> int:
        return min([car.manhattan_distance() for car in self.cars if car.manhattan_distance()!=0])

    def __eq__(self, o: "State") -> bool:
        if not isinstance(o, State):
            return False
        if all([car1.loc == car2.loc and car1.target == car2.target for (car1, car2) in zip(self.cars, o.cars)]):
            return True
        else:
            return False

    def __str__(self) -> str:
        inner = [0]*self.n
        grid = [inner[:] for _ in range(self.n)]
        for (i, car) in enumerate(self.cars):
            grid[car.loc[0]][car.loc[1]] = i+1
        s = ""
        for row in grid:
            s += "\n" + str(row)
        return s




