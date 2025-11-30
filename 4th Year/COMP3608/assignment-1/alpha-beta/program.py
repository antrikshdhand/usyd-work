from Game import *

def connect_four_ab(state, turn, max_depth):
    # Create a new Connect-4 game
    game = Game(state, turn)

    # Run minimax
    best_move, total_nodes_examined = game.get_best_move(max_depth)

    return f"{best_move[1]}\n{total_nodes_examined}"
    
if __name__ == '__main__':
    
    print(connect_four_ab(".......,.......,.......,.......,.......,.......", "red", 4))
    
    # game = Game()
    # game.play()