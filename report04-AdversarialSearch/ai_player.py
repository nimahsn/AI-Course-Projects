from typing import Tuple
from board import Board
import math

class PlayerAlphaBeta():
    def __init__(self, black: bool, opponent: "PlayerAlphaBeta" = None, cut_off_depth: int = 3) -> None:
        self.black = black
        self.markers_out = 9
        self.markers_in = 0
        self.markers_lost = 0
        self.markers_captured = 0
        self.opponent = opponent
        self.cut_depth = cut_off_depth

    def alpha_beta_search(self, state: "Board") -> "Board":
        score, new_state = self.max_value(state, -math.inf, math.inf)

    def max_value(self, state: "Board", alpha: int, beta: int) -> Tuple[int, "Board"]:
        if self.cut_off_test(state):
            pass
        v = (-math.inf, None)
        for new_state in state.get_all_moves(self):
            (score_minval, state_minval) = self.min_value(new_state, alpha, beta)
            max_value = max(v[0], score_minval)
            if max_value == v[0]:
                pass
            elif max_value == score_minval:
                v = (score_minval, state_minval)
            if v[0] >= beta:
                return v
            alpha = max(alpha, v[0])
        return v
            

    def min_value(self, state: "Board", alpha: int, beta: int) -> Tuple[int, "Board"]:
        if self.cut_off_test(state):
            pass
        v = (math.inf, None)
        for new_state in state.get_all_moves(self.opponent):
            (score_maxval, state_maxval) = self.max_value(new_state, alpha, beta)
            min_value = min(v[0], score_maxval)
            if min_value == v[0]:
                pass
            elif min_value == score_maxval:
                v = (score_maxval, state_maxval)
            if v[0] <= alpha: return v
            beta = min(beta, v[0])
        return v
            

    def cut_off_test(self, state: "Board", d: int) -> bool:
        if state.is_terminal:
            return True
        if d == self.cut_depth:
            return True
        return False