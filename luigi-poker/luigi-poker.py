from asciicards.asciicards import show_hand, create_deck
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
        print("Congratulations! You win!")
    elif player_hand_value < opponent_hand_value:
        print("Sorry, you lose. Better luck next time.")
    else:
        print("It's a tie!")

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
def play_luigi_poker():
    deck = create_deck()
    player_hand = [deck.pop(0) for _ in range(5)]
    opponent_hand = [deck.pop(0) for _ in range(5)]

    print("Welcome to Luigi Poker!")

    # Discard phase
    player_hand, deck = discard_phase(player_hand, deck)

    # Deal replacement cards
    while len(player_hand) < 5:
        player_hand.append(deck.pop(0))
        opponent_hand.append(deck.pop(0))

    # Show final hands
    print("\nYour final hand:")
    print(show_hand(player_hand))
    print("\nOpponent's final hand:")
    print(show_hand(opponent_hand))

    compare_hands(player_hand, opponent_hand)

# Play the game
play_luigi_poker()