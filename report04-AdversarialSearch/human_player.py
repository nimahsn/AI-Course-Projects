from copy import deepcopy
import board as b

class HumanPlayer:
    def __init__(self, black) -> None:
        self.black = black

    def _get_action_input(self, phase):
        pos_1 = None
        pos_2 = None
        pos_3 = None
        if phase == 1:
            x_y = input("Enter target x and y:")
            x = int(x_y[0])
            y = int(x_y[2])
            pos_1 = (x,y)
            return pos_1
            # x_y = input("")
        if phase == 2 or phase == 3:
            x_y = input("Enter origin x and y:")
            x = int(x_y[0])
            y = int(x_y[2])
            pos_1 = (x,y)
            x_y = input("Enter destination x and y:")
            x = int(x_y[0])
            y = int(x_y[2])
            pos_2 = (x,y)
            return (pos_1, pos_2)
    
    def _get_mill_input(self):
            x_y = input("Enter x and y to capture:")
            x = int(x_y[0])
            y = int(x_y[2])
            pos_1 = (x,y)
            return pos_1
    
    def _prompt_and_move_phase1(self, board: "b.Board"):
        pos = self._get_action_input(1)
        while pos not in b.positions or board.pos_marker_dict[pos] is not None:
            print("invalid position")
            pos = self._get_action_input(1)
        
        board_copy = deepcopy(board)
        board_copy.pos_marker_dict[pos] = b.Marker(self.black, pos)
        board_copy.last_move_type = b.ACTION_PLACE
        board_copy.last_move_is_black = self.black
        if self.black:
            board_copy.black_markers_out -= 1
            board_copy.black_markers_in += 1
        else:
            board_copy.white_marker_out -= 1
            board_copy.white_markers_in += 1

        if board_copy.white_marker_out == 0 and board_copy.black_markers_out == 0:
            board_copy.phase = 2
        
        if board_copy.is_mill(pos, self.black):
            capt = self._get_mill_input()
            while capt not in b.positions or board_copy.pos_marker_dict[capt] is None or board_copy.pos_marker_dict[capt].black == self.black:
                print("invalid capture")
                capt = self._get_mill_input()
            board_copy.pos_marker_dict[capt] = None
            if self.black:
                board_copy.black_mills += 1
                board_copy.white_markers_in -= 1
                board_copy.last_move_type = b.ACTION_PLACE_MILL
                if board.is_mill(capt, not self.black):
                    board_copy.white_mills -= 1
            else:
                board_copy.white_mills += 1
                board_copy.black_markers_in -= 1
                board_copy.last_move_type = b.ACTION_PLACE_MILL
                if board.is_mill(capt, not self.black):
                    board_copy.black_mills -= 1
        return board_copy

    def _prompt_and_move_phase2(self, board: "b.Board"):
        pos_old, pos_new = self._get_action_input(2)
        while pos_old not in b.positions\
            or pos_new not in b.positions\
                or board.pos_marker_dict[pos_old] is None\
                    or board.pos_marker_dict[pos_new] is not None\
                        or board.pos_marker_dict[pos_old].black != self.black\
                            or pos_new not in b.adjacent_dict[pos_old]:
            print("invalid positions")
            pos_old, pos_new = self._get_action_input(2)
        
        bcp = deepcopy(board)
        bcp.last_move_type = b.ACTION_MOVE
        bcp.last_move_is_black = self.black
        if bcp.is_mill(pos_old, self.black):
            if self.black:
                bcp.black_mills -= 1
            else:
                bcp.white_mills += 1
        bcp.pos_marker_dict[pos_old] = None
        bcp.pos_marker_dict[pos_new] = b.Marker(self.black, pos_new)
        if bcp.is_mill(pos_new, self.black):
            capt = self._get_mill_input()
            while capt not in b.positions or bcp.pos_marker_dict[capt] is None or bcp.pos_marker_dict[capt].black == self.black:
                print("invalid capture")
                capt = self._get_mill_input()
            bcp.pos_marker_dict[capt] = None
            if self.black:
                bcp.black_mills += 1
                bcp.white_markers_in -= 1
                bcp.last_move_type = b.ACTION_MOVE_MILL
                if board.is_mill(capt, not self.black):
                    bcp.white_mills -= 1
            else:
                bcp.white_mills += 1
                bcp.black_markers_in -= 1
                bcp.last_move_type = b.ACTION_MOVE_MILL
                if board.is_mill(capt, not self.black):
                    bcp.black_mills -= 1
            if bcp.white_markers_in == 3 or bcp.black_markers_in == 3:
                bcp.phase = 3
        return bcp
        
    def _prompt_and_move_phase3(self, board: "b.Board"):
        if self.black and board.black_markers_in > 3:
            return self._prompt_and_move_phase2(board)
        elif not self.black and board.white_markers_in >3:
            return self._prompt_and_move_phase2(board)

        pos_old, pos_new = self._get_action_input(3)
        while pos_old not in b.positions\
            or pos_new not in b.positions\
                or board.pos_marker_dict[pos_old] is None\
                    or board.pos_marker_dict[pos_new] is not None\
                        or board.pos_marker_dict[pos_old].black != self.black:
            print("invalid positions")
            pos_old, pos_new = self._get_action_input(3)
        
        bcp = deepcopy(board)
        bcp.last_move_type = b.ACTIION_FLY
        bcp.last_move_is_black = self.black
        if bcp.is_mill(pos_old, self.black):
            if self.black:
                bcp.black_mills -= 1
            else:
                bcp.white_mills -= 1
        bcp.pos_marker_dict[pos_old] = None
        bcp.pos_marker_dict[pos_new] = b.Marker(self.black, pos_new)
        if bcp.is_mill(pos_new, self.black):
            capt = self._get_mill_input()
            while capt not in b.positions or bcp.pos_marker_dict[capt] is None or bcp.pos_marker_dict[capt].black == self.black:
                print("invalid capture")
                capt = self._get_mill_input()  
            bcp.pos_marker_dict[capt] = None
            if self.black:
                bcp.black_mills += 1
                bcp.white_markers_in -= 1
                bcp.last_move_type = b.ACTION_FLY_MILL
                if board.is_mill(capt, not self.black):
                    bcp.white_mills -= 1
            else:
                bcp.white_mills += 1
                bcp.black_markers_in -= 1
                bcp.last_move_type = b.ACTION_FLY_MILL
                if board.is_mill(capt, not self.black):
                    bcp.black_mills -= 1
        return bcp

    def prompt_and_move(self, board: "b.Board") -> "b.Board":
        if board.phase == 1:
            return self._prompt_and_move_phase1(board)
        elif board.phase == 2:
            return self._prompt_and_move_phase2(board)
        else:
            return self._prompt_and_move_phase3(board)