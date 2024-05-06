import os

def clear_screen():
    os.system("cls")

def play_blackjack(chips=0):
    # Importing and calling the function to play Blackjack
    from blackjack.BJMain import play_bj
    return play_bj(chips)

def play_luigi_poker(chips=0):
    # Importing and calling the function to play Luigi Poker
    from luigi_poker.luigi_poker import play_luigi_poker as plp
    return plp(chips)

def main_menu(chips=0):
    clear_screen()
    print(f"Welcome to the Casino! You have {chips} Copper.")
    print("1. Play Blackjack (BJ)")
    print("2. Play Luigi Poker")
    choice = input("Enter the number of the game you want to play: ")
    return choice

if __name__ == "__main__":
    os.system("color 2")  # Setting console text color to green
    chips = 100
    while True:
        if chips <= 0:
            print(f"You have {chips} Copper.")
            print("You're kicked out.")
        choice = main_menu(chips)
        if choice == "1":
            chips = play_blackjack(chips)
        elif choice == "2":
            chips = play_luigi_poker(chips)
        else:
            print("Invalid choice. Please enter 1 or 2.")
            input("Press Enter to continue...")
