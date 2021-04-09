from typing import List, Tuple


adjacent_dict = {
    (1,1): [(4,1), (1,4)],
    (1,4):[(1,1),(1,7),(2,4)],
    (1,7):[(1,4),(4,7)],
    (2,2):[(2,4),(4,2)],
    (2,4):[(2,2), (2,6), (1,4), (3,4)],
    (2,6):[(2,4), (4,6)],
    (3,3):[(3,4), (4,3)],
    (3,4):[(2,4), (3,3), (3,5)],
    (3,5):[(3,4), (4,5)],
    (4,1):[(4,2), (1,1), (7,1)],
    (4,2):[(4,1), (4,3), (3,2), (6,2)],
    (4,3):[(4,2), (3,3), (5,3)],
    (4,5):[(3,5), (5,5), (4,6)],
    (4,6):[(4,5), (2,6), (6,6), (4,7)],
    (4,7):[(4,6), (1,7), (7,7)],
    (5,3):[(4,3), (5,4)],
    (5,4):[(5,3), (6,4), (5,5)],
    (5,5):[(5,4), (4,5)],
    (6,2):[(4,2), (6,4)],
    (6,4):[(6,2), (6,6), (5,4), (7,4)],
    (6,6):[(6,4), (4,6)],
    (7,1):[(4,1), (7,4)],
    (7,4):[(7,1), (7,7), (6,4)],
    (7,7):[(7,4), (4,7)]
}

positoins = [
    (1,1), (1,4), (1,7),
    (2,2), (2,4), (2,6),
    (3,3), (3,4), (3,5),
    (4,1), (4,2), (4,3), (4,5), (4,6), (4,7),
    (5,3), (5,4), (5,5),
    (6,2), (6,4), (6,6),
    (7,1), (7,4), (7,7)
]

class Board:
    def __init__(self, phase: int, black_markers: List["Marker"] = [], white_markers: List["Marker"] = []) -> None:
        self.blacks: List["Marker"] = black_markers
        self.whites: List["Marker"] = white_markers
        self.phase = phase
    
    def get_all_moves(self, black: bool):
        if self.phase == 1:
            for move in self.get_all_moves_phase1(black):
                yield move
        elif self.phase == 2:
            for move in self.get_all_moves_phase2(black):
                yield move
        else:
            for move in self.get_all_moves_phase3(black):
                yield move

    def get_all_moves_phase1(self, black: bool):
        pass

    def get_all_moves_phase2(self, black: bool):
        pass

    def get_all_moves_phase3(self, black: bool):
        pass

class Marker:
    def __init__(self, black: bool, position: Tuple[int, int], in_game: bool = False) -> None:
        self.black = black
        self.in_game = in_game
        self.position = position
    
    def get_moves(self):
        for adj in adjacent_dict[positoins]:
            yield adj
