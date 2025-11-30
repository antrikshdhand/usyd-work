class Board:
    N_COLS = 7
    N_ROWS = 6

    def __init__(self, state):
        self.BOARD = [[0 for i in range(Board.N_COLS)] for j in range(Board.N_ROWS)]
        self.N_YELLOW = 0
        self.N_RED = 0

        self.parse_state_into_board(state)
        
    def parse_state_into_board(self, state):
        # Load the state string into the board matrix
        rows = state.split(",") # where rows[0] is the bottom row of the game
        for i in range(Board.N_ROWS):
            for j in range(Board.N_COLS):
                self.BOARD[Board.N_ROWS - i - 1][j] = rows[i][j] 
                if rows[i][j] == "r":
                    self.N_RED += 1
                elif rows[i][j] == "y":
                    self.N_YELLOW += 1
    
    ######## GETTERS AND SETTERS ########

    def get_n_red(self):
        return self.N_RED
    
    def get_n_yellow(self):
        return self.N_YELLOW

    def get_n_player_tokens(self, player):
        if player == "r":
            return self.get_n_red()
        elif player == "y":
            return self.get_n_yellow()

    def get_pos(self, i, j):
        return self.BOARD[i][j]
    
    def set_pos(self, i, j, player):
        self.BOARD[i][j] = player
    
    ###########################################
        
    def place_token_col(self, col, token):
        '''Places a token at the lowest free spot in the given column.'''

        if token == 'r':
            self.N_RED += 1
        elif token == 'y':
            self.N_YELLOW += 1

        for row in range(self.N_ROWS - 1, -1, -1):
            if self.BOARD[row][col] == '.':
                self.BOARD[row][col] = token
                return True

        return False
    
    def place_token(self, i, j, token):
        if token == 'r':
            self.N_RED += 1
        elif token == 'y':
            self.N_YELLOW += 1

        self.set_pos(i, j, token)

        return True
    
    def unplace_token(self, i, j, token):
        if token == 'r':
            self.N_RED -= 1
        elif token == 'y':
            self.N_YELLOW -= 1

        self.set_pos(i, j, '.')
    
    def is_full(self):
        '''
        Checks if the top row is full, therefore checking if the entire board
        is full.
        '''
        return all(self.board[0])

    def pprint(self):
        '''Pretty-prints the board for debugging purposes.'''

        print("--------------")
        for row in self.BOARD:
            print(' '.join(row))
        print("--------------")

    def to_string(self):
        '''Outputs the game board back to its original string representation.'''

        string = []
        for i in range(Board.N_ROWS):
            for j in range(Board.N_COLS):
                string.append(self.BOARD[Board.N_ROWS - i - 1][j])
            if i != Board.N_ROWS - 1:
                string.append(",")
                
        return "".join(string)
    
    def check_winner(self):
        winner = None
        for i in range(4, 8):
            if self.count_n_in_a_row(i, "r"):
                winner = "r"
                break
            elif self.count_n_in_a_row(i, "y"):
                winner = "y"
                break
            
        # If there is no winner, and all spaces on the board are filled = tie
        if (winner == None) and (self.N_YELLOW + self.N_RED == Board.N_COLS * Board.N_ROWS):
            return "t"
        
        return winner

    def count_n_in_a_row(self, n, player):
        total_count = 0

        # Check rows
        for row in self.BOARD:
            count = 0
            for position in row:
                #if position == ".":
                #    continue
                if position == player:
                    count += 1
                    if count == n:
                        #print(f"1 row {n}-in-a-row found for {player}")
                        total_count += 1
                    elif count > n:
                        #print("PREVIOUS COUNT CANCELLED")
                        total_count -= 1
                        break
                else:
                    count = 0

        # Check columns
        for i in range(Board.N_COLS):
            count = 0
            for j in range(Board.N_ROWS):
                #if self.BOARD[j][i] == ".":
                #    continue
                if self.BOARD[j][i] == player:
                    count += 1
                    if count == n:
                        #print(f"1 column {n}-in-a-row found for {player}")
                        total_count += 1
                    elif count > n:
                        #print("PREVIOUS COUNT CANCELLED")
                        total_count -= 1
                        break
                else:
                    count = 0
                    
        # Check diagonals

        # Top left to bottom right
        for j in range(self.N_COLS - (n - 1)):
            for i in range(self.N_ROWS - (n - 1)):
                count = 0
                for k in range(n):
                    #if self.BOARD[i + k][j + k] == ".":
                    #    continue
                    if self.BOARD[i + k][j + k] == player:
                        count += 1
                        if count == n:
                            #print("1 top left to bottom right n-in-a-row found")
                            total_count += 1
                        elif count > n:
                            total_count -= 1
                            break
                    else:
                        count = 0
                        break
                        
        # Bottom left to top right
        for i in range(Board.N_ROWS - (n - 1)):
            for j in range(Board.N_COLS - (n - 1)):
                count = 0
                for k in range(n):
                    #if self.BOARD[i + k][j - k + (n - 1)] == ".":
                    #    continue
                    if self.BOARD[i + k][j - k + (n - 1)] == player:
                        count += 1
                        if count == n:
                            #print(f"1 top left to bottom right {n}-in-a-row found")
                            total_count += 1
                        elif count > n:
                            total_count -= 1
                            break
                    else:
                        count = 0
                        break

        # if (player == "r"):
        #     print(player)
        #     print(f"Total count: {total_count}")
        return total_count 
    
    def count_bottom_top_diagonal_n_in_a_row(self, n, player, board):
        count = 0
        for i in range(Board.N_ROWS - (n - 1)):
            for j in range(Board.N_COLS - (n - 1)):
                diagonal = [board[i + k][j - k + (n - 1)] for k in range(n)]
                if all(cell == player and cell != '.' for cell in diagonal):
                    count += 1

        return count

    def fill_board_with_taken(self, n, player, board):
        for i in range(Board.N_ROWS - (n - 1)):
            for j in range(Board.N_COLS - (n - 1)):
                diagonal = [board[i + k][j - k + (n - 1)] for k in range(n)]
                if all(cell == player and cell != '.' for cell in diagonal):
                    for l in range(n):
                        board[i + l][j + l] = '#'