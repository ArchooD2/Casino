from asciicards import show_card, show_hand, create_deck
import math,os,random

# Global shoe to persist across games
shoe = []
discard_pile = []

def cls():
    os.system("cls")

def get_score(hand):
    score = 0
    num_aces = 0
    for card in hand:
        if card["Rank"] == "A":
            num_aces += 1
        score += card["Value"]
    while score <= 11 and num_aces > 0:
        score += 10
        num_aces -= 1
    return score

def reshuffle_shoe():
    """Create a new 6-deck shoe and shuffle"""
    global shoe
    shoe = create_deck(6)
    random.shuffle(shoe)

def deal_card():
    """Deal a card from the shoe, reshuffling if necessary"""
    global shoe
    if len(shoe) == 0:  # If the shoe is empty, reshuffle
        reshuffle_shoe()
    return shoe.pop()

def play_bj(chips=0):
    os.system("color 2")
    print("Welcome to Blackjack with ASCII Art Cards!")
    global shoe
    player_chips = chips if chips else 100

    # Initialize the shoe if it's empty
    if len(shoe) == 0:
        reshuffle_shoe()

    while True:
        print(f"You have {player_chips} Copper.")
        if player_chips == 0:
            input("You have no more chips! Press enter to leave.")
            break
        bet = 0
        while bet == 0 or bet > player_chips:
            try:
                bet = int(input("Enter your bet (in Copper, increments of 5, or '0' to quit): "))
                if bet == 0:
                    return player_chips
            except ValueError:
                continue
            if bet % 5 != 0 or bet > player_chips:
                bet = 0
        if bet == 0:
            break

        # Deal initial hands
        player_hand = [deal_card(), deal_card()]
        dealer_hand = [deal_card(), deal_card()]
        shown_card = dealer_hand[0]

        print(f"\nDealer's Hand:\n{show_card(shown_card)}")
        print(f"\nYour Hand:\n{show_hand(player_hand)}")
        print(f"Your Hand's Value: {get_score(player_hand)}")

        while True:
            player_score = get_score(player_hand)
            dealer_score = get_score(dealer_hand)

            if player_score > 21:
                print("Bust! Dealer wins.")
                player_chips -= bet
                break
            elif player_score == 21:
                if len(player_hand) == 2:
                    print("BlackJack! You Win!!")
                    player_chips += math.floor(bet * 1.5)
                    break
                print("21! You win!")
                player_chips += bet
                break

            choice = input("Hit or stand? ").lower()
            if choice == "hit":
                player_hand.append(deal_card())
                print(f"\nYour Hand:\n{show_hand(player_hand)}")
                print(f"Your Hand's Value: {get_score(player_hand)}")
            else:
                # Dealer logic
                print(f"\nDealer's Hand:\n{show_hand(dealer_hand)}")
                while dealer_score < 17:
                    dealer_hand.append(deal_card())
                    dealer_score = get_score(dealer_hand)
                print(f"\nDealer's Final Hand:\n{show_hand(dealer_hand)}")
                print(f"Dealer's Hand Value: {dealer_score}")

                if dealer_score > 21:
                    print("Dealer busts! You win!")
                    player_chips += bet
                elif dealer_score > player_score:
                    print("Dealer wins.")
                    player_chips -= bet
                elif dealer_score < player_score:
                    print("You win!")
                    player_chips += bet
                else:
                    print("It's a push!")
                break

        print(f"You now have {player_chips} Copper.\n")
        input("Press enter to continue...")
    return player_chips

if __name__ == "__main__":
    chips = 100
    while True:
        cls()
        chips = play_bj(chips)
        os.system("color 7")
