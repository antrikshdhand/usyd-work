import math
from Board import *
from utility import EVALUATION, UTILITY 

class Game:

    def __init__(self, state=".......,.......,.......,.......,.......,.......", turn="red") -> None:
        self.board = Board(state)
        
        if turn == "red":
            self.CURRENT_TURN = "r"
        elif turn == "yellow":
            self.CURRENT_TURN = "y"
    
    def switch_turn(self):
        self.CURRENT_TURN = 'y' if self.CURRENT_TURN == 'r' else 'r'
    
    def get_current_turn(self):
        return self.CURRENT_TURN

    def get_next_turn(self, current_turn):
        if current_turn == "r":
            return "y"
        else:
            return "r"
    
    def make_move(self, col):
        if not 0 <= col < self.board.N_COLS or self.board.get_pos(0, col) != '.':
            return False
        return self.board.place_token(col, self.CURRENT_TURN)    
    
    def get_possible_moves(self):
        '''
        The function goes through all the columns in the game board and finds
        the 'lowest' unfilled position, where lowest = highest i index
        (closest to the ground).
        '''
        moves = []
        for j in range(Board.N_COLS):
            # Start iterating from the bottom of the board
            for i in range(Board.N_ROWS - 1, -1, -1):
                pos = self.board.get_pos(i, j)
                if pos == ".":
                    moves.append((i, j))
                    break
        return moves
    
    def minimax(self, curr_depth, max_depth, curr_turn, is_maximising, a, b):
        total_nodes_examined = 1
        
        # Base condition: if there is a win or a tie, return the utility score
        utility = UTILITY(self)
        if utility != None:
            # print("WIN or TIE")
            return utility, total_nodes_examined
        
        # print("NO WIN OR TIE")
        
        # If the depth has been reached, evaluate the game at this stage
        if curr_depth == max_depth:
            # print("DEPTH REACHED")
            return EVALUATION(self), total_nodes_examined

        # print("DEPTH NOT REACHED YET")
        
        ### Run minimax on all available spots ###
        possible_moves = self.get_possible_moves()
        
        if is_maximising:
            best_score = -math.inf
            for move in possible_moves:
                self.board.set_pos(move[0], move[1], curr_turn)
                
                score, nodes_examined = self.minimax(curr_depth + 1, max_depth, self.get_next_turn(curr_turn), False, a, b)
                total_nodes_examined += nodes_examined 
                
                self.board.set_pos(move[0], move[1], ".")
                best_score = max(best_score, score)
                a = max(a, score)
                if b <= a:
                    break
            return best_score, total_nodes_examined
        else:
            best_score = math.inf
            for move in possible_moves:
                self.board.set_pos(move[0], move[1], curr_turn)
                
                score, nodes_examined = self.minimax(curr_depth + 1, max_depth, self.get_next_turn(curr_turn), True, a, b)
                total_nodes_examined += nodes_examined
                
                self.board.set_pos(move[0], move[1], ".")
                best_score = min(best_score, score)
                b = min(b, score)
                if b <= a:
                    break
            return best_score, total_nodes_examined
        
    def get_best_move(self, max_depth):
        # Larger positive score for red
        if self.CURRENT_TURN == "r":
            best_score = -math.inf
        # Larger negative score for yellow
        else:
            best_score = math.inf

        best_move = None
        total_nodes_examined = 1
        
        possible_moves = self.get_possible_moves()
        # print("Possible moves:")
        # print(possible_moves)
        for move in possible_moves:
            self.board.set_pos(move[0], move[1], self.CURRENT_TURN)
            
            # print(f"Entering minimax on move {move}")
            score, nodes_examined = self.minimax(1, max_depth, self.get_next_turn(self.CURRENT_TURN), False, -math.inf, math.inf)
            total_nodes_examined += nodes_examined

            # print(f"score = {score}")
            # print()
            
            self.board.set_pos(move[0], move[1], ".")

            if self.CURRENT_TURN == "r":
                if (score > best_score):
                    best_score = score
                    best_move = move
            else:
                if (score < best_score):
                    best_score = score
                    best_move = move
        score, total_nodes_examined = self.minimax(0, max_depth, self.CURRENT_TURN, True, -math.inf, math.inf)
        return best_move, total_nodes_examined
    
    def play(self):
        print("Welcome to Connect-4. Human plays as red ('r') and AI plays as yellow ('y').")

        winner = None
        while True:
            self.board.pprint()

            if self.CURRENT_TURN == "r":
                col_input = input(f"Player {self.CURRENT_TURN}, enter column (1 - 7) to drop token: ")
                try:
                    col = int(col_input) - 1
                except ValueError:
                    print("Invalid input. Please only enter integers from 1 - 7.")

                if self.make_move(col):
                    self.switch_turn()
                else:
                    print("Invalid move! Try again.")
            else:
                print("Computer is thinking ...")
                best_move, total_nodes_examined = self.get_best_move(max_depth=3)
                print(f"Computer picked column {best_move[1] + 1}")
                if self.make_move(best_move[1]):
                    self.switch_turn()
                else:
                    print("Oops! Something went wrong.")
            
            # Check if game over
            winner = self.board.check_winner()
            if winner != None:
                break

        self.board.pprint()

        if winner == 't':
            print("It's a tie!")
        else:
            print(f"Player {winner} wins!")