class GameState: 
    def __init__(self, mode, board_size, coins):
        self.mode = mode
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.coins = coins
        self.score = 0
        self.turn = 1
        self.profit = 0
        self.upkeep = 0

    #Function to print out grid size, will be called when play_game starts
    def print_board(self):
        size = len(self.board)
        print('+' + '---+' * size)
        for row in self.board:
            for cell in row:
                print('|', cell, end=' ')
            print('|')
            print('+' + '---+' * size)

    def place_letter(self, coord, letter):
        row, col = self.convert_coord(coord)
        if row is not None and col is not None:
            if self.board[row][col] == ' ':
                if self.is_adjacent_to_letter(row, col) or self.turn == 1:  # Allow placing on first turn without adjacency check and logic of scores to be applied 
                    self.board[row][col] = letter
                    self.update_coins_and_scores(row,col,letter)
                    return True
                else:
                    print("You can only place letters next to existing letters.")
                    return False
            else:
                print("That cell is already occupied.")
                return False
        else:
            print("Invalid coordinate.")
            return False

    def demolish_building(self, coord):
        row, col = self.convert_coord(coord)
        if row is not None and col is not None:
            if self.board[row][col] != ' ':
                if self.coins >= 1:
                    self.board[row][col] = ' '
                    self.coins -= 1
                    print(f"Building at {coord} demolished. You have {self.coins} coins left.")
                    return True
                else:
                    print("Not enough coins to demolish the building.")
                    return False
            else:
                print("No building to demolish at the given coordinate.")
                return False
        else:
            print("Invalid coordinate.")
            return False   
     
    def update_coins_and_scores(self,row,col,letter):
        adjacent_r_count = 0
        adjacent_c_count = 0
        adjacent_o_count = 0
        next_i_count = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1,1), (1,1), (-1,-1), (1,-1)]  # Up, Down, Left, Right, Upper right, Bottom left, Upper left, Bottom Right
        next_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # Scan every row and column
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < len(self.board) and 0 <= c < len(self.board) and self.board[r][c] != ' ' and self.turn != 1: #For all turns other the first turn to have a adjacency check
                if letter == "O" and self.board[r][c] == "O":
                    self.score += 1
                elif letter == "I":
                    if self.board[r][c] == "R":
                        adjacent_r_count += 1
                elif letter == "C":
                    if self.board[r][c] == "C":
                        adjacent_c_count += 1
                    if self.board[r][c] == "R":
                        adjacent_r_count += 1
                elif letter == "R":
                    if self.board[r][c] == "R":
                        adjacent_r_count += 1
                    if self.board[r][c] == "C":
                        adjacent_c_count += 1
                    if self.board[r][c] == "O":
                        adjacent_o_count += 1
        # Directions that are next to each other
        for dr, dc in next_directions:
            r, c = row + dr, col + dc
            if 0 <= r < len(self.board) and 0 <= c < len(self.board) and self.board[r][c] != ' ':
                if letter == "R" and self.board[r][c] == "I":
                    next_i_count += 1
        # Code for first turn scoring, only I is able to earn points on its own so only I code is needed
        if letter == "I":
            self.score += 1
        if letter == "C" and adjacent_c_count>0:
            self.score += adjacent_c_count
        if letter in ["I", "C"] and adjacent_r_count > 0:
            self.coins += adjacent_r_count
        if letter == "R" and next_i_count > 0:
            self.score += next_i_count
        if letter == "R" and adjacent_r_count > 0:
            self.score += adjacent_r_count
        if letter == "R" and adjacent_c_count > 0:
            self.score += adjacent_c_count
        if letter == "R" and adjacent_o_count > 0:
            self.score += 2 * (adjacent_o_count)

    def is_adjacent_to_letter(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dr, dc in directions:
            r, c = row + dr, col + dc #looks up, down, left, right by minusing or adding the rows and cols coordinates
            if 0 <= r < len(self.board) and 0 <= c < len(self.board) and self.board[r][c] != ' ':#checks if row and col coord is in grid and if there is letters around it
                return True
        return False
    
    def convert_coord(self, coord):
        if len(coord) != 2:
            return None, None
        row = ord(coord[0].lower()) - ord('a')
        col = int(coord[1]) - 1
        if 0 <= row < len(self.board) and 0 <= col < len(self.board):
            return row, col
        else:
            return None, None
