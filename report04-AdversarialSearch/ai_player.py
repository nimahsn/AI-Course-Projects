from board import State

class PlayerAlphaBeta():
    def __init__(self, black: bool) -> None:
        self.black = black
        self.markers_out = 9
        self.markers_in = 0
        self.markers_lost = 0
        self.markers_captured = 0
