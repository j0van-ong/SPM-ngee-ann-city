
import random

#Constant Variable for assigning mode
ARCADE_MODE = 'arcade'
FREE_PLAY_MODE = 'free_play'

#Class for Gamestate object, used to initialize the attributes taken in. Self is used to refer to current object edited
class GameState:
    def __init__(self, mode, board_size, coins):
        self.mode = mode
        self.board = [[' ' for _ in range(board_size)] for _ in range(board_size)]
        self.coins = coins
        self.score = 0
        self.turn = 1

    ''' Function to print out grid size, will be called when play_game starts
    def print_board(self):
        size = len(self.board)
        print('+' + '---+' * size)
        for row in self.board:
            for cell in row:
                print('|', cell, end=' ')
            if row == self.board[-1]:  #Check if it's the last row
                print('|')  #Print the last '|' if it's the last row
            else:
                print('  |')
            print('+' + '---+' * size)
    '''
    #Function to print out grid size, will be called when play_game starts
    def print_board(self):
        size = len(self.board)
        print('+' + '---+' * size)
        for row in self.board:
            for cell in row:
                print('|', cell, end=' ')
            print('|')  # Always print the last '|'
            print('+' + '---+' * size)
                
def printMainMenu():
    print("----------------------------------\n"
        "-       | Ngee Ann City |        -\n"
        "----------------------------------\n"
        "-  (1) Start New Arcade Game     -\n"
        "-  (2) Start New Free Play Game  -\n"
        "-  (3) Load New Saved Game       -\n"
        "-  (4) Display High Scores       -\n"
        "-  (0) Exit Game                 -\n"
        "----------------------------------")
    print()


def play_game(mode):
    game_state = start_new_game(mode)
    
    print("Turn:", game_state.turn)
    print("Coins:", game_state.coins)
    print("Score:", game_state.score)
    print("Board:")
    game_state.print_board()
    coordinatesTest(game_state)



def start_new_game(mode):
    if mode == ARCADE_MODE:
        return GameState(mode, board_size=20, coins=16)
    elif mode == FREE_PLAY_MODE:
        return GameState(mode, board_size=5, coins=0)
    
# TO TEST GRID COORDINATE PRINTING SYSTEM
def coordinatesTest(game_state):
    x = int(input("Row coordinate: "))
    y = int(input("Column coordinate: "))
    game_state.board[x][y] = "X"
    game_state.print_board()


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



