from Board import *

# "player" as a function parameter is always "y" or "r". The only time a player 
# is referenced with their full colour is in the connect_four_mm() function.

# All these functions are called with GAME not BOARD or STATE

def NUM_IN_A_ROW(count, game, player):
    return game.board.count_n_in_a_row(count, player)

def SCORE(game, player):
    return game.board.get_n_player_tokens(player) + \
            10 * NUM_IN_A_ROW(2, game, player) + \
            100 * NUM_IN_A_ROW(3, game, player) + \
            1000 * NUM_IN_A_ROW(4, game, player) + \
            1000 * NUM_IN_A_ROW(5, game, player) + \
            1000 * NUM_IN_A_ROW(6, game, player) + \
            1000 * NUM_IN_A_ROW(7, game, player) 
            
def EVALUATION(game):
    #print(f"red_tokens:{game.board.get_n_player_tokens('r')}, y_tokens: {game.board.get_n_player_tokens('y')}")
    score_r = SCORE(game, "r")
    score_y = SCORE(game, "y")
    #print(f"score_r: {score_r}, score_y: {score_y}")
    return score_r - score_y

def UTILITY(game):
    winner = game.board.check_winner()
    if winner == "r":
        return 10000
    elif winner == "t":
        return 0
    elif winner == "y":
        return -10000
    else:
        return None