from typing import Dict, List, Tuple
from copy import deepcopy
# from ai_player import PlayerAlphaBeta


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
    (4,2):[(4,1), (4,3), (2,2), (6,2)],
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

mill_dict = {
    (1,1): [[(1,4), (1,7)], [(4,1), (7,1)]],
    (1,4): [[(1,1), (1,7)], [(2,4), (3,4)]],
    (1,7): [[(1,4), (1,1)], [(4,7), (7,7)]],
    (2,2): [[(2,4), (2,6)], [(4,2), (6,2)]],
    (2,4): [[(2,2), (2,6)], [(1,4), (3,4)]],
    (2,6): [[(2,2), (2,4)], [(4,6), (6,6)]],
    (3,3): [[(3,4), (3,5)], [(4,3), (5,4)]],
    (3,4): [[(3,3), (3,5)], [(2,4), (1,4)]],
    (3,5): [[(3,3), (3,4)], [(4,5), (5,5)]],
    (4,1): [[(1,1), (7,1)], [(4,2), (4,3)]],
    (4,2): [[(4,1), (4,3)], [(2,2), (6,2)]],
    (4,3): [[(4,1), (4,2)], [(3,3), (5,3)]],
    (4,5): [[(4,6), (4,7)], [(3,5), (5,5)]],
    (4,6): [[(4,5), (4,7)], [(2,6), (6,6)]],
    (4,7): [[(4,5), (4,6)], [(1,7), (7,7)]],
    (5,3): [[(3,3), (4,3)], [(5,4), (5,5)]],
    (5,4): [[(5,3), (5,5)], [(6,4), (7,4)]],
    (5,5): [[(5,3), (5,4)], [(3,5), (4,5)]],
    (6,2): [[(6,4), (6,6)], [(4,2), (2,2)]],
    (6,4): [[(5,4), (7,4)], [(6,2), (6,6)]],
    (6,6): [[(6,2), (6,4)], [(4,6), (2,6)]],
    (7,1): [[(4,1), (1,1)], [(7,4), (7,7)]],
    (7,4): [[(7,1), (7,7)], [(6,4), (5,4)]],
    (7,7): [[(7,1), (7,4)], [(4,7), (1,7)]]
}

positions = [
    (1,1), (1,4), (1,7),
    (2,2), (2,4), (2,6),
    (3,3), (3,4), (3,5),
    (4,1), (4,2), (4,3), (4,5), (4,6), (4,7),
    (5,3), (5,4), (5,5),
    (6,2), (6,4), (6,6),
    (7,1), (7,4), (7,7)
]

ACTION_PLACE = 1
ACTION_PLACE_MILL = 2
ACTION_MOVE = 3
ACTION_MOVE_MILL = 4
ACTIION_FLY = 5
ACTION_FLY_MILL = 6


class Board:
    def __init__(self, phase: int = 1, dict_markers = None) -> None:
        self.pos_marker_dict: Dict[Tuple[int, int], "Marker"] = dict_markers
        if self.pos_marker_dict == None:
            self.pos_marker_dict = {}
            for pos in positions:
                self.pos_marker_dict[pos] = None
        self.phase = phase
        self.black_markers_out = 9
        self.white_marker_out = 9
        self.black_markers_in = 0
        self.white_markers_in = 0
        self.white_markers_captured = 0
        self.black_markers_captured = 0
        self.white_mills = 0
        self.black_mills = 0
        self.last_move_is_black: bool = None
        self.last_move_type: int = None
    
    def get_all_moves(self, player):
        if self.phase == 1:
            for move in self.get_all_moves_phase1(player):
                yield move
        elif self.phase == 2:
            for move in self.get_all_moves_phase2(player):
                yield move
        else:
            for move in self.get_all_moves_phase3(player):
                yield move

    def get_all_moves_phase1(self, player):
        for pos in positions:
            if self.pos_marker_dict[pos] is None:
                new_marker = Marker(black=player.black, position=pos)
                # action = Action(place_action, marker=new_marker, new_pos=pos)
                # yield action
                board_cpy = deepcopy(self)
                board_cpy.last_move_is_black = player.black
                board_cpy.pos_marker_dict[pos] = new_marker
                if player.black:
                    board_cpy.black_markers_in += 1
                    board_cpy.black_markers_out -= 1
                else:
                    board_cpy.white_markers_in += 1
                    board_cpy.white_marker_out -= 1

                if board_cpy.black_markers_out == 0 and b.white_marker_out == 0:
                    board_cpy.phase = 2 

                if board_cpy.is_mill(pos, player.black):
                    if player.black:
                        board_cpy.black_mills += 1
                    else:
                        board_cpy.white_mills += 1                   

                    for b in board_cpy.remove_opp_marker(player):
                        b.last_move_type = ACTION_PLACE_MILL
                        yield b
                    continue
                board_cpy.last_move_type = ACTION_PLACE
                yield board_cpy
        

    def get_all_moves_phase2(self, player):
        black = player.black
        for pos in positions:
            if self.pos_marker_dict[pos] is None:
                continue
            m = self.pos_marker_dict[pos]
            if m.black != black:
                continue
            lost_mill = self.is_mill(pos, black)
            for new_pos in m.get_moves:
                if self.pos_marker_dict[new_pos] is not None:
                    continue
                bcp = deepcopy(self)
                bcp.last_move_is_black = black
                if lost_mill:
                    if black:
                        bcp.black_mills -= 1
                    else:
                        bcp.white_mills -= 1
                new_m = Marker(black, new_pos)
                bcp.pos_marker_dict[new_pos] = new_m
                bcp.pos_marker_dict[pos] = None
                if bcp.is_mill(pos, black):
                    if black:
                        bcp.black_mills += 1
                    else:
                        bcp.white_mills += 1
                    for b in bcp.remove_opp_marker(player):
                        b.last_move_type = ACTION_MOVE_MILL
                        yield b
                    continue
                bcp.last_move_type = ACTION_MOVE
                yield bcp

    def get_all_moves_phase3(self, player):
        black = player.black
        if black and self.black_markers_in > 3:
            for b in self.get_all_moves_phase2(player):
                yield b
        elif not black and self.white_markers_in > 3:
            for b in self.get_all_moves_phase2(player):
                yield b
        else:
            for pos in positions:
                if self.pos_marker_dict[pos] is None:
                    continue
                m = self.pos_marker_dict[pos]
                if m.black != black:
                    continue
                lost_mill = self.is_mill(pos, black)
                for new_pos in positions:
                    if self.pos_marker_dict[new_pos] is not None:
                        continue
                    bcp = deepcopy(self)
                    bcp.last_move_is_black = black
                    if lost_mill:
                        if black:
                            bcp.black_mills -= 1
                        else:
                            bcp.white_mills -= 1
                    new_m = Marker(black, new_pos)
                    bcp.pos_marker_dict[new_pos] = new_m
                    bcp.pos_marker_dict[pos] = None
                    if bcp.is_mill(pos, black):
                        for b in bcp.remove_opp_marker(player):
                            b.last_move_type = ACTION_FLY_MILL
                            yield b
                        continue
                    bcp.last_move_type = ACTIION_FLY
                    yield bcp
                    

    def is_mill(self, position, black) -> bool:
        for l in mill_dict[position]:
            if self.pos_marker_dict[l[0]] is not None\
                and self.pos_marker_dict[l[1]] is not None\
                    and self.pos_marker_dict[l[0]].black == black\
                        and self.pos_marker_dict[l[1]].black == black:
                return True
        return False


    def remove_opp_marker(self, player) -> "Board":
        black = player.black
        found = False
        l=[]
        for pos in positions:
            m = self.pos_marker_dict[pos]
            if m is None or m.black==black:
                continue
            if self.is_mill(pos, not black):
                l.append(pos)
                continue
            found = True
            bcp = deepcopy(self)
            bcp.pos_marker_dict[pos] = None
            if black:
                bcp.white_markers_in -= 1
                bcp.white_markers_captured +=1
            else:
                bcp.black_markers_in -= 1
                bcp.black_markers_captured +=1
            if bcp.phase == 2 and (bcp.white_markers_in == 2 or bcp.black_markers_in == 2):
                bcp.phase = 3
            yield bcp
        if found == False:
            for pos in l:
                bcp = deepcopy(self)
                bcp.pos_marker_dict[pos] = None
                if black:
                    bcp.white_markers_in -= 1
                    bcp.white_markers_captured +=1
                    bcp.white_mills -= 1
                else:
                    bcp.black_markers_in -= 1
                    bcp.black_markers_captured +=1
                    bcp.black_mills += 1
                if bcp.phase == 2 and (bcp.white_markers_in == 2 or bcp.black_markers_in == 2):
                    bcp.phase = 3
                yield bcp
    
    def is_terminal(self):
        if self.phase == 3 and (self.white_markers_in == 2 or self.black_markers_in == 2):
            return True
        else: return False


class Action:
    def __init__(self, type, marker, new_pos, capture: "Marker"=None) -> None:
        self.type = type
        self.marker = marker
        self.new_pos = new_pos
        self.capture_marker = capture
class Marker:
    def __init__(self, black: bool, position: Tuple[int, int] = None, in_game: bool = True) -> None:
        self.black = black
        self.in_game = in_game
        self.position = position
    
    def get_moves(self):
        for adj in adjacent_dict[self.position]:
            yield adj
