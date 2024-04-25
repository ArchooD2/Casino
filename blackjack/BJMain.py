from asciicards.asciicards import show_card, show_hand, create_deck
import math
import os

def cls():
    os.system("cls")

def get_score(hand):
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
    print("Welcome to Blackjack with ASCII Art Cards!")
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
        deck = create_deck()
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
                # Try to deal with IndexError
                try:
                    player_hand.append(deck.pop())
                    print(f"\nDealer's Hand:\n{show_card(dealer_hand[0])}\n\nYour Hand:\n{show_hand(player_hand)}\n\nYour Hand's Value:{get_score(player_hand)}")
                except IndexError as e:
                    print(f"Error: Deck is empty. Report this: \ndealer_hand:{dealer_hand}\nplayer_hand:{player_hand}\n{e}")
                    break
            else:
                while dealer_score < 17 or (dealer_score >= 17 and dealer_score == (sum(card["Value"] for card in dealer_hand) + 10)) or (dealer_score == 21 and any(card["Rank"] == "A" for card in dealer_hand) and any(card["Value"] == "10" for card in dealer_hand) and len(dealer_hand) == 2): #some bullshit
                    # Try to deal with IndexError
                    try:
                        dealer_hand.append(deck.pop())
                        dealer_score = get_score(dealer_hand)
                    except IndexError as e:
                        print(f"Error: Deck is empty. Report this: \ndealer_hand:{dealer_hand}\nplayer_hand:{player_hand}\n{e}")
                        break
                print(f"\nDealer's Hand:\n{show_hand(dealer_hand)}\nDealer's Hand Value:\n{get_score(dealer_hand)}")
                if player_score == 21 and len(player_hand) == 2:
                    print("Blackjack!")
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
