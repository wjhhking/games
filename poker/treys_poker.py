from treys import Card, Deck, Evaluator
from itertools import combinations
from collections import Counter

def play_exhaustive_with_treys():
    """
    Simulates all possible community card combinations for a poker game using Treys.
    Tracks wins for each player and handles draw cases.
    Prints progress every 100,000 games.
    """
    # Initialize player hands
    player1_hand = [Card.new('As'), Card.new('Ah')]  # Player 1: Ace of Spades, Ace of Hearts
    player2_hand = [Card.new('Kc'), Card.new('Qd')]  # Player 2: King of Clubs, Queen of Diamonds
    players = [player1_hand, player2_hand]

    # Initialize deck and evaluator
    deck = Deck()
    evaluator = Evaluator()

    # Remove player cards from the deck
    for card in player1_hand + player2_hand:
        deck.cards.remove(card)

    # Generate all possible community card combinations (C(48, 5))
    community_card_combinations = list(combinations(deck.cards, 5))

    # Initialize counters
    win_counts = Counter({0: 0, 1: 0, "draw": 0})
    total_games = 0

    # Iterate through all community card combinations
    for community in community_card_combinations:
        scores = []
        for hand in players:
            # Evaluate each player's hand with the community cards
            score = evaluator.evaluate(list(community), hand)
            scores.append(score)

        # Determine the winner
        min_score = min(scores)
        winners = [i for i, score in enumerate(scores) if score == min_score]

        if len(winners) == 1:
            # Single winner
            win_counts[winners[0]] += 1
        else:
            # Draw case
            win_counts["draw"] += 1

        total_games += 1

        # Print progress every 100,000 games
        if total_games % 100_000 == 0:
            win_rates = {
                f"Player {i+1}": f"{(win_counts[i] / total_games) * 100:.2f}%" for i in range(len(players))
            }
            win_rates["Draw"] = f"{(win_counts['draw'] / total_games) * 100:.2f}%"
            print(f"Games Played: {total_games:,} | Current Win Rates: {win_rates}")

    # Final results
    total_combinations = sum(win_counts.values())
    final_win_rates = {
        f"Player {i+1}": f"{(win_counts[i] / total_combinations) * 100:.2f}%" for i in range(len(players))
    }
    final_win_rates["Draw"] = f"{(win_counts['draw'] / total_combinations) * 100:.2f}%"

    print(f"\nTotal Games Played: {total_combinations:,}")
    print("Total Wins: ", dict(win_counts))
    print("Final Win Rates: ", final_win_rates)

if __name__ == "__main__":
    print("Starting exhaustive combination testing with Treys...")
    play_exhaustive_with_treys()
