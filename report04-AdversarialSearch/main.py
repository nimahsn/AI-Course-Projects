from board import *
from ai_player import PlayerAlphaBeta, Evaluator
from human_player import HumanPlayer

def ai_vs_ai(depth=4):
    b = Board()
    evalu = Evaluator()
    player_black = PlayerAlphaBeta(black = True, cut_off_depth=depth, evaluator=evalu)
    player_white = PlayerAlphaBeta(black = False, cut_off_depth=depth, evaluator=evalu,  opponent=player_black)
    player_black.opponent = player_white
    player = player_black
    while not b.is_terminal():
        print("phase: "+str(b.phase))
        score, b= player.alpha_beta_search(b)
        action= ""
        if b.last_move_type == ACTION_MOVE:
            action = "move"
        elif b.last_move_type == ACTION_MOVE_MILL:
            action = "move_mill"
        elif b.last_move_type == ACTION_PLACE:
            action = 'place'
        elif b.last_move_type == ACTION_PLACE_MILL:
            action = 'place mill'
        elif b.last_move_type == ACTIION_FLY:
            action = 'fly'
        elif b.last_move_type == ACTION_FLY_MILL:
            action = 'fly mill'

        if player.black:
            print("turn: black")
            player = player_white
        else:
            print("turn: white")
            player = player_black
        print(score)
        print("action: "+action)
        print(b)
        print("next phase: "+ str(b.phase))
    print("Terminal state")

def human_vs_ai(depth=5):
    b = Board()
    evalu = Evaluator()
    player_black_ai = PlayerAlphaBeta(black = True, cut_off_depth=depth, evaluator=evalu)
    player_white_human = HumanPlayer(black = False)
    player_black_ai.opponent = player_white_human

    ##
    while not b.is_terminal():
        print("phase: " + str(b.phase))
        print("pc turn (black)")
        print(b)
        score, b = player_black_ai.alpha_beta_search(b)
        action= ""
        if b.last_move_type == ACTION_MOVE:
            action = "move"
        elif b.last_move_type == ACTION_MOVE_MILL:
            action = "move_mill"
        elif b.last_move_type == ACTION_PLACE:
            action = 'place'
        elif b.last_move_type == ACTION_PLACE_MILL:
            action = 'place mill'
        elif b.last_move_type == ACTIION_FLY:
            action = 'fly'
        elif b.last_move_type == ACTION_FLY_MILL:
            action = 'fly mill'
        print("action: "+action)
        print("---------------------------------------------")
        if b.is_terminal():
            print(b)
            break
        print("phase: "+ str(b.phase))
        print("your turn (white)")
        print(b)
        b = player_white_human.prompt_and_move(b)
        print("---------------------------------------------")
    print("terminal state")

    