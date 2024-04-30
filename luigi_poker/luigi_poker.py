from asciicards import show_hand, create_deck
from itertools import combinations
import random, os
def cls():
    os.system("cls")
def evaluate_hand(hand):
    """Evaluate the value of a poker hand"""
    values = {'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
    suits = ['♥', '♦', '♣', '♠']

    # Count the occurrences of each rank and suit
    rank_counts = {}
    suit_counts = {}
    for card in hand:
        rank = card["Rank"]
        suit = card["Suit"]
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
        suit_counts[suit] = suit_counts.get(suit, 0) + 1

    # Check for flush
    flush = any(count >= 5 for count in suit_counts.values())

    # Check for straight
    sorted_ranks = sorted(values[rank] for rank in rank_counts)
    straight = any(sorted_ranks[i] == sorted_ranks[i + 4] - 4 for i in range(len(sorted_ranks) - 4))

    # Check for straight flush
    straight_flush = straight and flush

    # Determine hand value
    if straight_flush:
        return 900 + max(sorted_ranks)
    elif any(count == 4 for count in rank_counts.values()):
        return 800 + max(values[rank] for rank, count in rank_counts.items() if count == 4)
    elif all(count == 3 for count in rank_counts.values()):
        return 700 + max(values[rank] for rank in rank_counts)
    elif flush:
        return 600 + max(sorted_ranks)
    elif straight:
        return 500 + max(sorted_ranks)
    elif any(count == 3 for count in rank_counts.values()):
        return 400 + max(values[rank] for rank, count in rank_counts.items() if count == 3)
    elif sum(count == 2 for count in rank_counts.values()) == 2:
        return 300 + max(values[rank] for rank, count in rank_counts.items() if count == 2)
    elif any(count == 2 for count in rank_counts.values()):
        return 200 + max(values[rank] for rank, count in rank_counts.items() if count == 2)
    else:
        return max(sorted_ranks)


def compare_hands(player_hand, opponent_hand):
    """Compare hands and determine the winner"""
    player_hand_value = evaluate_hand(player_hand)
    opponent_hand_value = evaluate_hand(opponent_hand)
    print("\nYour hand:", show_hand(player_hand), "Value:", player_hand_value)
    print("Opponent's hand:", show_hand(opponent_hand), "Value:", opponent_hand_value)
    
    if player_hand_value > opponent_hand_value:
        return "W"
    elif player_hand_value < opponent_hand_value:
        return "L"
    else:
        return "T"

def sophisticated_cpu_discard_phase(player_hand, deck):
    """CPU discards and replaces cards based on a sophisticated strategy"""
    print("CPU's hand:")
    print(show_hand(player_hand))

    # Evaluate the current hand
    hand_value = evaluate_hand(player_hand)

    # Determine which cards to keep and which to discard based on hand value
    if hand_value >= 600:  # If flush or better, keep the hand
        print("CPU decides to keep the hand.")
        return player_hand, deck
    
    # If not flush or better, consider discarding and replacing cards
    discard_indices = []
    for i, card in enumerate(player_hand):
        # If the card contributes minimally to the hand value, consider discarding it
        if evaluate_hand(player_hand[:i] + player_hand[i+1:]) < hand_value:
            discard_indices.append(i)

    # If no cards were found to discard, keep the hand
    if not discard_indices:
        print("CPU decides to keep the hand.")
        return player_hand, deck

    # Otherwise, discard the identified cards and replace them from the deck
    print("CPU decides to discard cards at indices:", discard_indices)
    for index in discard_indices:
        player_hand[index] = deck.pop(0)

    return player_hand, deck

def luigi_cheat_discard_phase(player_hand, deck):
    # Evaluate the current hand
    hand_value = evaluate_hand(player_hand)

    # Generate all possible subsets of card indices to discard
    discard_combinations = []
    for r in range(1, len(player_hand) + 1):
        discard_combinations.extend(combinations(range(len(player_hand)), r))

    # Initialize variables to track the best discard combination and resulting hand value
    best_discard_indices = None
    best_hand_value = hand_value

    # Iterate through all discard combinations
    for discard_indices in discard_combinations:
        testdeck = deck.copy()
        # Create a copy of the player's hand
        temp_hand = player_hand[:]
        # Discard cards at the selected indices
        for index in discard_indices:
            temp_hand[index] = testdeck.pop(0)
        # Evaluate the hand value after discarding
        new_hand_value = evaluate_hand(temp_hand)
        # Update the best discard combination if the new hand value is higher
        if new_hand_value > best_hand_value:
            best_discard_indices = discard_indices
            best_hand_value = new_hand_value

    # Discard cards at the best discard indices and replace them from the deck
    if best_discard_indices:
        print("Luigi decides to discard cards at indices:", best_discard_indices)
        for index in best_discard_indices:
            player_hand[index] = deck.pop(0)
    else:
        print("Luigi decides not to discard any cards.")

    return player_hand, deck


def discard_phase(player_hand, deck):
    """Allow player to discard and replace cards"""
    print("Your hand:")
    print(show_hand(player_hand))
    discard_indices = input("Enter the indices of the cards you want to discard (e.g., 1 3 4), or press Enter to keep all: ")
    if discard_indices:
        discard_indices = [int(i) - 1 for i in discard_indices.split()]
        for index in discard_indices:
            player_hand[index] = deck.pop(0)
    return player_hand, deck

# Main game loop
def play_luigi_poker(chips=0):
    print("Welcome to Luigi Poker!")
    hard = True if input("Easy or Hard? (e,E,Easy,easy/h,H,hard,Hard)").lower().startswith('h') else False
    player_chips = chips if chips else 100
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
        for i in range(chips):
            random.shuffle(deck)
        player_hand = [deck.pop(0) for _ in range(5)]
        opponent_hand = [deck.pop(0) for _ in range(5)]

        # Discard phase
        player_hand, deck = discard_phase(player_hand, deck)
        if hard == True:
            opponent_hand, deck = luigi_cheat_discard_phase(opponent_hand, deck)
        else:
            opponent_hand, deck = sophisticated_cpu_discard_phase(opponent_hand, deck)
        # Deal replacement cards if required.
        while len(player_hand) < 5:
            player_hand.append(deck.pop(0))
            opponent_hand.append(deck.pop(0))

        winner = compare_hands(player_hand, opponent_hand)
        if winner == "W":
            player_chips += bet
            print("You win!")
        elif winner == "L":
            player_chips -= bet
            print("You lose!")
        else:
            print("It's a tie!")
        print(f"You now have {player_chips} Copper.\n")
        input("Press enter to continue...")
        return player_chips

# Play the game
if __name__ == "__main__":
    chips = 100
    while True:
        cls()
        chips = play_luigi_poker(chips)