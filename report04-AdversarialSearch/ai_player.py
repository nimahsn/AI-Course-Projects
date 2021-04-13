from typing import List, Tuple
from board import Board, Marker, ACTION_FLY_MILL, ACTION_MOVE, ACTION_MOVE_MILL, ACTION_PLACE, ACTION_PLACE_MILL, ACTIION_FLY, positions, mill_dict
import math
from random import shuffle

class PlayerAlphaBeta():
    def __init__(self, black: bool, evaluator: "Evaluator", cut_off_depth: int = 3, opponent: "PlayerAlphaBeta" = None) -> None:
        self.black = black
        self.markers_out = 9
        self.markers_in = 0
        self.markers_lost = 0
        self.markers_captured = 0
        self.opponent = opponent
        self.cut_depth = cut_off_depth
        self.evaluator = evaluator
        self._alpha = 0
        self._beta = 0
        self.crashes = []

    def alpha_beta_search(self, state: "Board") -> "Board":
        # self._alpha = -math.inf
        # self._beta = math.inf
        score, new_state = self.max_value(state, -math.inf, math.inf, 1)
        return score, new_state

    def max_value(self, state: "Board", alpha: int, beta: int, depth: int) -> Tuple[int, "Board"]:
        if self.cut_off_test(state, depth):
            return (self.evaluator.evaluate(state, self.black), state)
        v = (-math.inf, None)
        all_s = list(state.get_all_moves(self.black))
        shuffle(all_s)
        for new_state in all_s:
            (score_minval, _) = self.min_value(new_state, alpha, beta, depth+1)
            max_value = max(v[0], score_minval)
            if max_value == v[0]:
                pass
            elif max_value == score_minval:
                v = (score_minval, new_state)
            if v[0] >= beta:
                return v
            alpha = max(alpha, v[0])
        return v
            

    def min_value(self, state: "Board", alpha: int, beta: int, depth: int) -> Tuple[int, "Board"]:
        if self.cut_off_test(state, depth):
            return (self.evaluator.evaluate(state, self.black), state)
        v = (math.inf, None)
        all_s = list(state.get_all_moves(self.opponent.black))
        shuffle(all_s)
        for new_state in all_s:
            (score_maxval, _) = self.max_value(new_state, alpha, beta, depth+1)
            min_value = min(v[0], score_maxval)
            if min_value == v[0]:
                pass
            elif min_value == score_maxval:
                v = (score_maxval, new_state)
            if v[0] <= alpha: return v
            beta = min(beta, v[0])
        return v
            

    def cut_off_test(self, state: "Board", d: int) -> bool:
        if state.is_terminal():
            return True
        if d == self.cut_depth:
            return True
        return False

class Evaluator:
    def __init__(self) -> None:
        pass

    def register_players(self, black_player: "PlayerAlphaBeta", white_player: "PlayerAlphaBeta"= None):
        self.black_player = black_player
        self.white_player = white_player
        self.black_markers: List["Marker"] = []
        self.white_markers: List["Marker"] = []
    
    def _eval_diff_markers_in(self, board: "Board", black: bool) -> int:
        diff = board.black_markers_in - board.white_markers_in
        if black:
            return diff
        else:
            return -diff
    
    def _eval_last_mill(self, board: "Board", black: bool) -> int:
        score = 0
        type = board.last_move_type
        if type == ACTION_FLY_MILL or type == ACTION_MOVE_MILL or type == ACTION_PLACE_MILL:
            if black == board.last_move_is_black:
                score = 1
            else:
                score = -1
        return score
    
    def _eval_diff_blocked_markers(self, board: "Board", black: bool) -> int:
        blocked_whites = 0
        blocked_blacks = 0
        for pos in positions:
            m = board.pos_marker_dict[pos]
            if m is None:
                continue
            if all([board.pos_marker_dict[adj_pos] != None for adj_pos in m.get_moves()]):
                if m.black:
                    blocked_blacks += 1
                else:
                    blocked_whites += 1
        if black:
            return blocked_whites - blocked_blacks
        else:
            return blocked_blacks - blocked_whites

    def _eval_win(self, board: "Board", black: bool) -> int:
        if board.phase == 2:
            if len(list(board.get_all_moves(black))) == 0:
                return -1
            elif len(list(board.get_all_moves(not black))) == 0:
                return 1
        score = 0
        if board.phase != 3:
            return score
        if black:
            if board.white_markers_in == 2:
                score = 1
            elif board.black_markers_in == 2:
                score -1
        else:
            if board.black_markers_in == 2:
                score = 1
            elif board.white_markers_in == 2:
                score = -1
        return score

    def _eval_diff_double(self, board: "Board", black: bool):
        white_doubles = 0
        black_doubles = 0
        for pos in positions:
            m = board.pos_marker_dict[pos]
            if m is None:
                continue
            adjs = m.get_moves()
            for mill_list in mill_dict[pos]:
                for mill_marker in mill_list:
                    if mill_marker in adjs:
                        if m.black == board.pos_marker_dict[mill_marker]:
                            if m.black:
                                black_doubles += 1
                            else:
                                white_doubles += 1
        if black:
            return (black_doubles - white_doubles) / 2
        else:
            return (white_doubles - black_doubles) / 2

    def _eval_diff_mill_count(self, board: "Board", black: bool):
        if black:
            return board.black_mills - board.white_mills
        else:
            return board.white_mills - board.black_mills

    def evaluate(self, board: "Board", black: bool):
        if board.phase == 1:
            return 20*self._eval_last_mill(board, black) +\
                25*self._eval_diff_mill_count(board, black) +\
                    2*self._eval_diff_blocked_markers(board, black) +\
                        5*self._eval_diff_markers_in(board, black) +\
                            8*self._eval_diff_double(board, black)

        elif board.phase == 2:
            return 15*self._eval_last_mill(board, black) +\
                35*self._eval_diff_mill_count(board, black) +\
                    10*self._eval_diff_blocked_markers(board, black) +\
                        15*self._eval_diff_markers_in(board, black) +\
                            2000*self._eval_win(board, black)

        elif board.phase == 3:
            return 3000*self._eval_win(board, black) +\
                18*self._eval_last_mill(board, black)
