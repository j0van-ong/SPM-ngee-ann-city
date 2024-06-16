class GameState:
    def __init__(self, mode, board_size, coins):
        self.mode = mode
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.coins = coins
        self.score = 0
        self.turn = 1

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
                self.board[row][col] = letter
                return True
            else:
                print("That cell is already occupied.")
                return False
        else:
            print("Invalid coordinate.")
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
