from itertools import combinations
from treys import Card as TreysCard, Evaluator, Deck
from card import Rank, Suit, Card, HoleCards
from collections import Counter

PRINT_LOGS = False

class CommunityCards:
    """
    Represents the community cards in a poker game.
    """

    def __init__(self):
        self.cards = []

    def add_cards(self, cards):
        """
        Adds cards to the community.

        Args:
            cards (list[Card]): A list of `Card` objects to add.
        """
        self.cards.extend(cards)

    def to_treys_format(self):
        """
        Converts the community cards to the `treys` card format.

        Returns:
            list[int]: A list of community cards in `treys` format.
        """
        return [TreysCard.new(str(card)) for card in self.cards]

    def __str__(self):
        return " ".join(map(str, self.cards))


def to_treys_card(card):
    """
    Converts a custom `Card` object to the `treys` card format.

    Args:
        card (Card): A custom `Card` object.

    Returns:
        int: The card in `treys` format.
    """
    suit_map = {
        "♠": "s",  # Spades
        "♥": "h",  # Hearts
        "♦": "d",  # Diamonds
        "♣": "c",  # Clubs
    }
    rank_str = str(card.rank)  # e.g., "A" for Ace
    suit_str = suit_map[str(card.suit)]  # e.g., "h" for Hearts
    return TreysCard.new(f"{rank_str}{suit_str}")



def exhaustive_community_combinations_with_treys(players):
    """
    Exhaustively tries all combinations of 5 cards for the community cards from the remaining deck
    using `treys` for evaluation and prints progress every 100,000 games.

    Args:
        players (list[HoleCards]): A list of players with predefined hole cards.

    Returns:
        list[int]: A list of win counts for each player.
    """
    # Generate the deck using Treys
    treys_deck = Deck()

    # Remove cards in players' hole cards from the Treys deck
    for player in players:
        treys_deck.cards.remove(to_treys_card(player.card1))
        treys_deck.cards.remove(to_treys_card(player.card2))

    # Generate all possible combinations of 5 cards for the community
    community_card_combinations = combinations(treys_deck.cards, 5)

    # Initialize counters
    winning_counts = Counter()
    total_games = 0

    # Treys evaluator
    evaluator = Evaluator()

    # Iterate over all possible community card combinations
    for community_cards in community_card_combinations:
        # Evaluate the game with the given community cards
        community_cards_treys = list(community_cards)
        best_hand_score = float('inf')
        winner = None

        for player_index, player in enumerate(players):
            player_cards_treys = [
                to_treys_card(player.card1),
                to_treys_card(player.card2),
            ]
            score = evaluator.evaluate(community_cards_treys, player_cards_treys)

            if score < best_hand_score:
                best_hand_score = score
                winner = player_index

        # Update counts
        winning_counts[winner] += 1
        total_games += 1

        # Print progress every 100,000 games
        if total_games % 100_000 == 0:
            win_rates = {player: f"{(count / total_games):.4f}" for player, count in winning_counts.items()}
            print(f"Games Played: {total_games:,} | Current Win Rates: {win_rates}")

    return winning_counts


# Example usage
if __name__ == "__main__":
    # Predefined player hands
    p1 = HoleCards(Card('A', 's'), Card('A', 'h'))  # Player 1: AsAh
    p2 = HoleCards(Card('K', 'c'), Card('Q', 'd'))  # Player 2: KcQd
    players = [p1, p2]

    # Run the exhaustive test
    print("Starting exhaustive combination testing with Treys...")
    winning_counts = exhaustive_community_combinations_with_treys(players)

    # Final results
    total_combinations = sum(winning_counts.values())
    print(f"\nTotal Games Played: {total_combinations:,}")
    print("Total Wins: ", dict(winning_counts))
    final_win_rates = {player: f"{(count / total_combinations):.4f}" for player, count in winning_counts.items()}
    print("Final Win Rates: ", final_win_rates)
