
import random

#Constant Variable for assigning mode
ARCADE_MODE = 'arcade'
FREE_PLAY_MODE = 'free_play'
LETTERS_SET = ['R', 'I', 'C', 'O', '*']

#Class for Gamestate object, used to initialize the attributes taken in. Self is used to refer to current object edited
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
        
    def update_coins_and_scores(self,row,col,letter):
        adjacent_r_count = 0
        adjacent_c_count = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1,1), (1,1), (-1,-1), (1,-1)]  # Up, Down, Left, Right, Upper right, Bottom left, Upper left, Bottom Right 
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
        # Code for first turn scoring, only I is able to earn points on its own so only I code is needed
        if letter == "I":
            self.score += 1
        if letter == "C" and adjacent_c_count>0:
            self.score+=adjacent_c_count
        if letter in ["I", "C"] and adjacent_r_count > 0:
            self.coins += adjacent_r_count

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
                
def printMainMenu():
    print("----------------------------------\n"
        "-       | Ngee Ann City |        -\n"
        "----------------------------------\n"
        "-  (1) Start New Arcade Game     -\n"
        "-  (2) Start New Free Play Game  -\n"
        "-  (3) Load Saved Game       -\n"
        "-  (4) Display High Scores       -\n"
        "-  (0) Exit Game                 -\n"
        "----------------------------------")
    print()

def play_game(mode):
    OLD = False 
    game_state = start_new_game(mode)
    while True:
        print("Turn:", game_state.turn)
        print("Coins:", game_state.coins)
        print("Score:", game_state.score)
        print("Board:")
        game_state.print_board()
        if OLD == False:
            letter_options = random.sample(LETTERS_SET, 2)
        old_options = letter_options
        if OLD  == True:
            letter_options = old_options
        print(f"Choose a letter to place: {letter_options[0]} or {letter_options[1]}")
        letter = None
        while letter not in letter_options:
            letter = input(f"Enter your choice ({letter_options[0]}/{letter_options[1]}): ").upper()
            if letter not in letter_options:
                print("Invalid choice. Please select one of the given options.")
        coord = input("Enter the coordinate to place a letter (e.g., 'a1'): ")
        if game_state.place_letter(coord, letter):
            game_state.turn += 1
            game_state.coins -=1
            OLD = False
        else:
            print("Invalid move. Try again.")
            OLD = True


        # Print the updated board after each turn





def start_new_game(mode):
    if mode == ARCADE_MODE:
        return GameState(mode, board_size=20, coins=16)
    elif mode == FREE_PLAY_MODE:
        return GameState(mode, board_size=5, coins=0)
    

'''Start of code main program'''
while True:
    printMainMenu()

    try:
        option = int(input("Enter your option: "))
        assert option >= 0 and option <= 4 
    except ValueError:
        print('Option must be a integer, not a string or float')  
        continue
    except AssertionError:
        print('Option must be within option range') 
        continue
    except:
        print('Unknown error, option must be integer and within the range')
    if option == 0:
        print('Goodbye!')
        break
    elif option == 1:
        play_game(ARCADE_MODE)
    elif option == 2:
        play_game(FREE_PLAY_MODE)

