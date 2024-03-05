# Import the random and math module
from asciicards import show_card, show_hand, create_deck
import math
import os
#Define clear command
def cls():
    os.system("cls")


def get_score(hand):
    """Return the total value of a given hand"""
    score = 0
    num_aces = 0
    for card in hand:
        if card["Rank"] == "A":
            num_aces += 1
        score += card["Value"]
    if score == 11 and num_aces == 1:
        return 21
    while score < 11 and num_aces > 0:
        score += 10
        num_aces -= 1
    return score

def play_game():
    os.system("color 2")
    """Play a game of blackjack"""
    print("Welcome to Blackjack with ASCII Art Cards!")
    deck = create_deck()
    player_chips = 100
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
                    break
            except ValueError:
                continue
            if bet % 5 != 0 or bet > player_chips:
                bet = 0
        if bet == 0:
            break
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]
        showncard = dealer_hand[0]
        print(f"\nDealer's Hand:\n{show_card(showncard)}\n\nYour Hand:\n{show_hand(player_hand)}\nYour Hand's Value:{get_score(player_hand)}")
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
                    player_chips += math.floor(bet*1.5)
                    break
                print("21! You win!")
                player_chips += bet
                break
            choice = input("Hit or stand? ")
            if choice.lower() == "hit":
                player_hand.append(deck.pop())
                print(f"\nDealer's Hand:\n{show_card(dealer_hand[0])}\n\nYour Hand:\n{show_hand(player_hand)}\nYour Hand's Value:{get_score(player_hand)}")
            else:
                while dealer_score < 17:
                    dealer_hand.append(deck.pop())
                    dealer_score = get_score(dealer_hand)
                print(f"\nDealer's Hand:\n{show_hand(dealer_hand)}\nDealer's Hand Value:\n{get_score(dealer_hand)}")
                if player_score == 21 and len(player_hand) == 2:
                    if dealer_score == 21 and len(dealer_hand) == 2:
                        pass
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
                print(f"You now have {player_chips} Copper.\n")
                break
cls()
play_game()
os.system("color 7")
