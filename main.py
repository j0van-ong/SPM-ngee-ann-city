
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
    game_state = start_new_game(mode)
    while True:
        print("Turn:", game_state.turn)
        print("Coins:", game_state.coins)
        print("Score:", game_state.score)
        print("Board:")
        game_state.print_board()

        letter_options = random.sample(LETTERS_SET, 2)
        print(f"Choose a letter to place: {letter_options[0]} or {letter_options[1]}")
        letter = None
        while letter not in letter_options:
            letter = input(f"Enter your choice ({letter_options[0]}/{letter_options[1]}): ").upper()
            if letter not in letter_options:
                print("Invalid choice. Please select one of the given options.")
        coord = input("Enter the coordinate to place a letter (e.g., 'a1'): ")
        if game_state.place_letter(coord, letter):
            game_state.turn += 1
        else:
            print("Invalid move. Try again.")

        # Print the updated board after each turn
        print("Board:")
        game_state.print_board()





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