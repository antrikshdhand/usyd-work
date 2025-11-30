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
            row = rows[i]
            for j in range(Board.N_COLS):
                position = row[j]
                self.BOARD[Board.N_ROWS - i - 1][j] = position
                
                if position == "r":
                    self.N_RED += 1
                elif position == "y":
                    self.N_YELLOW += 1
    
    ######## /* GETTERS AND SETTERS */ ########

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
        
    def place_token(self, col, token):
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
        if self.count_n_in_a_row(4, "r"):
            winner = "r"
        elif self.count_n_in_a_row(4, "y"):
            winner = "y"
            
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
                if position == player:
                    count += 1
                    if count == n:
                        #print("1 row n-in-a-row found")
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
                position = self.BOARD[j][i]
                if position == player:
                    count += 1
                    if count == n:
                        #print("1 column n-in-a-row found")
                        total_count += 1
                    elif count > n:
                        #print("PREVIOUS COUNT CANCELLED")
                        total_count -= 1
                        break
                else:
                    count = 0
                    
        # Check diagonals
        #if n > 6:
        #   return total_count

        # Check top left to bottom right
        for i in range(self.N_ROWS - (n - 1)):
            for j in range(self.N_COLS - (n - 1)):
                count = 0
                for k in range(n):
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

        # Check bottom left to top right
        for i in range(Board.N_ROWS - (n - 1)):
            for j in range(Board.N_COLS - (n - 1)):
                count = 0
                for k in range(n):
                    if self.BOARD[i + k][j - k + (n - 1)] == player:
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
        return total_count