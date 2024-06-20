
import random
import GameState as GS
#Constant Variable for assigning mode
ARCADE_MODE = 'arcade'
FREE_PLAY_MODE = 'free_play'
LETTERS_SET = ['R', 'I', 'C', 'O', '*']


                
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
        if mode == ARCADE_MODE:
            print("Turn:", game_state.turn)
            print("Coins:", game_state.coins)
            print("Score:", game_state.score)
            print("Board:")
        elif mode == FREE_PLAY_MODE:
            print("Turn:", game_state.turn)
            print("Score:", game_state.score)
            print("Profit:", game_state.profit)
            print("Upkeep:", game_state.upkeep)
        
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
        else:
            print("Invalid move. Try again.")
            OLD = True


        # Print the updated board after each turn




def start_new_game(mode):
    if mode == ARCADE_MODE:
        return GS.GameState(mode, board_size=20, coins=16)
    elif mode == FREE_PLAY_MODE:
        return GS.GameState(mode, board_size=5, coins=0)
    

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