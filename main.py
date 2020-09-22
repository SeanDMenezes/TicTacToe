import random
from players import HumanText, HumanGraphical, AI
from board import Text, Graphical

def setup(game):
    try:
        p1, p2 = game.choose_mode()
    except Exception:
        game.exit_message()
        return
    play(game, p1, p2)

def play(game, p1, p2):
    cur_player = p1
    game.display()
    while True:
        game.display_turn(cur_player.symbol)
        cur_move = cur_player.get_move(game, cur_player.symbol)
        if cur_move == -1:
            game.exit_message()
            return
        game.place_piece(cur_move, cur_player.symbol)
        game.display()
        if game.check_win(cur_player.symbol):
            game.display_win(cur_player.symbol)
            break
        elif game.check_draw():
            game.display_draw()
            break
        
        if cur_player == p1:
            cur_player = p2
        else:
            cur_player = p1

    if game.play_again():
        game.clear()
        play(game, p2, p1)
    else:
        game.exit_message()
        return


setup(Text()) # play on the command line
setup(Graphical()) # play using pygame
