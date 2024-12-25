from asciicards import create_deck, show_card, show_hand
from counterutils import getcount, truecount
import random

def card_counting_practice():
    print("Welcome to Card Counting Practice!")
    print("Instructions: Observe the cards and mentally calculate the running count.")
    print("At intervals, you'll be asked for the count.")
    print("--------------------------------------------------\n")

    # Initialize a shuffled deck
    num_decks = 6  # Typical blackjack uses 6 decks
    deck = create_deck(num_decks)
    discard_pile = []

    # Start the practice
    running_count = 0
    cards_drawn = 0
    while len(deck) > 0:
        # Draw a random number of cards (1-3) to simulate play
        num_draw = random.randint(1, 3)
        drawn_cards = deck[:num_draw]
        deck = deck[num_draw:]
        discard_pile.extend(drawn_cards)
        cards_drawn += num_draw
        # Display the drawn cards
        print(show_hand(drawn_cards))
        print(f"\n{num_draw} card(s) were drawn.\n")
        # Update the running count
        running_count += getcount(drawn_cards)
        input("Press Enter to continue...\n")
        # Periodically ask the user for the running count
        if cards_drawn >= 13:  # Every 13 cards
            user_count = input("What is the running count? (Enter your answer): ")
            try:
                user_count = int(user_count)
                if user_count == running_count:
                    print("Correct! Great job!\n")
                else:
                    print(f"Incorrect. The correct running count is {running_count}.\n")
            except ValueError:
                print(f"Invalid input. The correct running count is {running_count}.\n")

            # Optionally show the true count
            true_count_value = truecount(running_count, deck + discard_pile)
            print(f"The true count (adjusted for decks remaining) is {true_count_value:.2f}.\n")

            # Ask to continue or quit
            continue_practice = input(f"Continue from {running_count}? (y/n): ").strip().lower()
            if continue_practice != 'y':
                print("Thanks for practicing! See you next time.")
                break
            cards_drawn = 0

    print("Deck is finished. Practice session complete!")

if __name__ == "__main__":
    card_counting_practice()
