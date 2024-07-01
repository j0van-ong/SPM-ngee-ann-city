import random
from GameState import GameState as GS
from Residential import Residential
from Commercial import Commercial
from Industry import Industry
from Road import Road
from Park import Park

# Constant Variable for assigning mode
ARCADE_MODE = 'arcade'
FREE_PLAY_MODE = 'free_play'
LETTERS_SET = ['R', 'I', 'C', 'O', '*']


def printMainMenu():
    print("----------------------------------\n"
          "-       | Ngee Ann City |        -\n"
          "----------------------------------\n"
          "-  (1) Start New Arcade Game     -\n"
          "-  (2) Start New Free Play Game  -\n"
          "-  (3) Load Saved Game           -\n"
          "-  (4) Display High Scores       -\n"
          "-  (0) Exit Game                 -\n"
          "----------------------------------")
    print()


def play_game(mode):
    OLD = False
    game_state = start_new_game(mode)
    letter_options = []

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

        if game_state.turn == 1 or not any(any(cell for cell in row) for row in game_state.board):
            can_demolish = False
        else:
            can_demolish = True

        print("\nChoose an action: ")
        print("  (P)lace a building")
        if can_demolish:
            print("  (D)emolish a building: ")
        print("  (S)ave game")
        print("  (E)xit game")

        action = input("Your choice: ").upper()

        while action not in ['P', 'D', 'S', 'E'] or (action == 'D' and not can_demolish):
            print("Invalid choice. Please select valid option.")
            action = input("Your choice: ").upper()

        if action == 'E':
            print("Exiting the game...")
            break

        if action == 'S':
            #Add save game method
            print("Game saved.")
            break

        if action == 'D':
            coord = input("Enter the coordinate to demolish a building (e.g., 'a1'): ")
            if game_state.demolish_building(coord):
                game_state.end_turn()
                continue
            else:
                print("Invalid move. Try again.")
                OLD = True
                continue


        if mode == FREE_PLAY_MODE:
            letter_options = LETTERS_SET
        elif not OLD:
            letter_options = random.sample(LETTERS_SET, 2)

        print(f"Choose a building to place: {' or '.join(letter_options)}")
        letter = None
        while letter not in letter_options:
            letter = input(f"Enter your choice ({'/'.join(letter_options)}): ").upper()
            if letter not in letter_options:
                print("Invalid choice. Please select one of the given options.")
        
        coord = input("Enter the coordinate to place a letter (e.g., 'a1'): ")
        building = create_building(letter)
        if game_state.place_building(coord, building):
            game_state.turn += 1  # increase the turn
            if mode == ARCADE_MODE:
                game_state.coins -= 1  # deduct one coin after placing a building
                if game_state.coins <= 1:  # check if coins are more than 1
                    print("Game Over! You ran out of coins.")
                    print("\nFinal Score:", game_state.score)
                    break
        else:
            print("Invalid move. Try again.")
            OLD = True
        game_state.end_turn()


def create_building(letter):
    if letter == 'R':
        return Residential()
    elif letter == 'C':
        return Commercial()
    elif letter == 'I':
        return Industry()
    elif letter == 'O':
        return Road()
    elif letter == '*':
        return Park()
    else:
        return None


def start_new_game(mode):
    if mode == ARCADE_MODE:
        return GS(mode, board_size=20, coins=16)
    elif mode == FREE_PLAY_MODE:
        return GS(mode, board_size=5, coins=0)


'''Start of code main program'''
while True:
    printMainMenu()

    try:
        option = int(input("Enter your option: "))
        assert option >= 0 and option <= 4
    except ValueError:
        print('Option must be an integer, not a string or float')
        continue
    except AssertionError:
        print('Option must be within option range')
        continue
    except:
        print('Unknown error, option must be an integer and within the range')
    if option == 0:
        print('Goodbye!')
        break
    elif option == 1:
        play_game(ARCADE_MODE)
    elif option == 2:
        play_game(FREE_PLAY_MODE)
