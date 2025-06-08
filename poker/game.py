from itertools import combinations
from collections import Counter
from card import Rank, Suit, Card, HoleCards
import random
from collections import Counter

PRINT_LOGS = False

# Optimization 1: https://github.com/ihendley/treys
# Optimization 2: avoid classes

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

    def __str__(self):
        return " ".join(map(str, self.cards))


class PokerHandEvaluator:
    """
    Evaluates poker hands and determines the best hand ranking.
    """

    HAND_RANKINGS = [
        "High Card",
        "One Pair",
        "Two Pair",
        "Three of a Kind",
        "Straight",
        "Flush",
        "Full House",
        "Four of a Kind",
        "Straight Flush",
        "Royal Flush",
    ]

    @staticmethod
    def evaluate_hand(hole_cards, community_cards):
        """
        Evaluates the best hand given hole cards and community cards.

        Args:
            hole_cards (HoleCards): Player's hole cards.
            community_cards (CommunityCards): Community cards.

        Returns:
            tuple: (rank_index, high_card), where rank_index is the index of the hand ranking
                   and high_card is the high card value for tiebreakers.
        """
        all_cards = [hole_cards.card1, hole_cards.card2] + community_cards.cards
        all_combinations = list(combinations(all_cards, 5))

        best_hand = (-1, -1)  # Start with no valid hand

        for combo in all_combinations:
            rank_index, high_card = PokerHandEvaluator._evaluate_combination(combo)
            if rank_index > best_hand[0] or (rank_index == best_hand[0] and high_card > best_hand[1]):
                best_hand = (rank_index, high_card)

        return best_hand

    @staticmethod
    def _evaluate_combination(cards):
        """
        Evaluates a specific combination of 5 cards.

        Args:
            cards (list[Card]): A list of 5 cards.

        Returns:
            tuple: (rank_index, high_card)
        """
        ranks = sorted([card.rank.value for card in cards], reverse=True)
        suits = [card.suit for card in cards]
        rank_counts = Counter(ranks)
        is_flush = len(set(suits)) == 1
        is_straight = PokerHandEvaluator._is_straight(ranks)

        # Check for hand rankings
        if is_straight and is_flush:
            if ranks[0] == Rank.ACE.value:  # Royal Flush
                return (9, ranks[0])
            return (8, ranks[0])  # Straight Flush
        if 4 in rank_counts.values():  # Four of a Kind
            return (7, PokerHandEvaluator._get_high_card(rank_counts, 4))
        if 3 in rank_counts.values() and 2 in rank_counts.values():  # Full House
            return (6, PokerHandEvaluator._get_high_card(rank_counts, 3))
        if is_flush:  # Flush
            return (5, ranks[0])
        if is_straight:  # Straight
            return (4, ranks[0])
        if 3 in rank_counts.values():  # Three of a Kind
            return (3, PokerHandEvaluator._get_high_card(rank_counts, 3))
        if list(rank_counts.values()).count(2) == 2:  # Two Pair
            return (2, PokerHandEvaluator._get_high_card(rank_counts, 2, multiple=True))
        if 2 in rank_counts.values():  # One Pair
            return (1, PokerHandEvaluator._get_high_card(rank_counts, 2))
        return (0, ranks[0])  # High Card

    @staticmethod
    def _is_straight(ranks):
        """
        Determines if the ranks form a straight.

        Args:
            ranks (list[int]): Sorted ranks in descending order.

        Returns:
            bool: True if the ranks form a straight, False otherwise.
        """
        unique_ranks = sorted(set(ranks), reverse=True)
        if len(unique_ranks) < 5:
            return False
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i] - unique_ranks[i + 4] == 4:
                return True
        # Special case for A-2-3-4-5 straight
        if set(unique_ranks[-5:]) == {Rank.ACE.value, 5, 4, 3, 2}:
            return True
        return False

    @staticmethod
    def _get_high_card(rank_counts, count, multiple=False):
        """
        Gets the high card for a given rank count.

        Args:
            rank_counts (Counter): Counter of card ranks.
            count (int): The rank count to look for (e.g., 4 for Four of a Kind).
            multiple (bool): True if looking for multiple high cards (e.g., Two Pair).

        Returns:
            int: The high card value.
        """
        matching_ranks = [rank for rank, cnt in rank_counts.items() if cnt == count]
        if multiple:
            return max(matching_ranks)
        return matching_ranks[0]


class GameWithHoleCards:
    """
    Poker game with predefined player hands.
    """

    def __init__(self, players):
        """
        Initializes the game with predefined player hands.

        Args:
            players (list[HoleCards]): A list of HoleCards representing the players' hole cards.
        """
        self.players = players
        self.num_players = len(players)
        self.deck = self._generate_deck()
        self.community_cards = CommunityCards()

        # Remove predefined player cards from the deck
        self._remove_player_cards()

    def _generate_deck(self):
        """
        Generates a shuffled deck of cards.

        Returns:
            list[Card]: A shuffled deck of cards.
        """
        deck = [Card(rank, suit) for rank in Rank for suit in Suit]
        random.shuffle(deck)
        return deck

    def _remove_player_cards(self):
        """
        Removes the predefined player cards from the deck.
        """
        for player in self.players:
            self.deck.remove(player.card1)
            self.deck.remove(player.card2)

    def deal_community_cards(self):
        """
        Deals the community cards (flop, turn, river).
        """
        self.deck.pop()  # Burn one card
        self.community_cards.add_cards([self.deck.pop() for _ in range(3)])  # Flop
        self.deck.pop()  # Burn one card
        self.community_cards.add_cards([self.deck.pop()])  # Turn
        self.deck.pop()  # Burn one card
        self.community_cards.add_cards([self.deck.pop()])  # River

    def determine_winner(self):
        """
        Determines the winner based on the best hand ranking.

        Returns:
            tuple: (winner_index, hand_rank)
        """
        best_hands = [
            PokerHandEvaluator.evaluate_hand(player, self.community_cards)
            for player in self.players
        ]
        winner = max(range(len(best_hands)), key=lambda i: best_hands[i])
        return winner, PokerHandEvaluator.HAND_RANKINGS[best_hands[winner][0]]

    def play(self):
        """
        Executes the poker game with predefined player hands and community cards.
        """
        if PRINT_LOGS:
            print("Game With Predefined Hole Cards Setup:")
            for i, player in enumerate(self.players):
                print(f"Player {i + 1} Hole Cards: {player}")

        self.deal_community_cards()
        if PRINT_LOGS:
            print(f"\nCommunity Cards: {self.community_cards}")

        winner, hand_rank = self.determine_winner()
        if PRINT_LOGS:
            print(f"\nPlayer {winner + 1} wins with a {hand_rank}!")

        return winner


def play_a_game():
    # Predefined player hands
    p1 = HoleCards(Card('A', 's'), Card('A', 'h'))  # Player 1: AsAh
    p2 = HoleCards(Card('K', 'c'), Card('Q', 'd'))  # Player 2: KcQd
    players = [p1, p2]

    # Create and play the game with predefined hole cards
    game = GameWithHoleCards(players)
    return game.play()


# # Example usage
# if __name__ == "__main__":
#     winning_counts = [0, 0]
#     number_of_games = 10000
#     for i in range(number_of_games):
#         winner = play_a_game()
#         winning_counts[winner] += 1
#     print('Total wins: ', winning_counts)
#     print('Win rates: ', [(i/number_of_games) for i in winning_counts])


def exhaustive_community_combinations_with_progress(players):
    """
    Exhaustively tries all combinations of 5 cards for the community cards from the remaining deck
    and prints progress every 100,000 games.

    Args:
        players (list[HoleCards]): A list of players with predefined hole cards.

    Returns:
        list[int]: A list of win counts for each player.
    """
    # Generate the deck
    deck = [Card(rank, suit) for rank in Rank for suit in Suit]

    # Remove cards in players' hole cards
    for player in players:
        deck.remove(player.card1)
        deck.remove(player.card2)

    # Generate all possible combinations of 5 cards for the community
    community_card_combinations = combinations(deck, 5)

    # Initialize counters
    winning_counts = Counter()
    total_games = 0

    # Iterate over all possible community card combinations
    for community_cards in community_card_combinations:
        # Create a CommunityCards object for evaluation
        community = CommunityCards()
        community.add_cards(list(community_cards))

        # Evaluate the game with the given community cards
        best_hands = [
            PokerHandEvaluator.evaluate_hand(player, community) for player in players
        ]
        winner = max(range(len(best_hands)), key=lambda i: best_hands[i])

        # Update counts
        winning_counts[winner] += 1
        total_games += 1

        # Print progress every 100,000 games
        if total_games % 100_000 == 0:
            win_rates = {player: f"{(count / total_games):.4f}" for player, count in winning_counts.items()}
            print(f"Games Played: {total_games:,} | Current Win Rates: {win_rates}")

    return winning_counts


# Example usage
# Battle: C(48,5) = 1_712_304
if __name__ == "__main__":
    # Predefined player hands
    p1 = HoleCards(Card('A', 's'), Card('A', 'h'))  # Player 1: AsAh
    p2 = HoleCards(Card('K', 'c'), Card('Q', 'd'))  # Player 2: KcQd
    players = [p1, p2]

    # Run the exhaustive test
    print("Starting exhaustive combination testing...")
    winning_counts = exhaustive_community_combinations_with_progress(players)

    # Final results
    total_combinations = sum(winning_counts.values())
    print(f"\nTotal Games Played: {total_combinations:,}")
    print("Total Wins: ", dict(winning_counts))
    final_win_rates = {player: f"{(count / total_combinations):.4f}" for player, count in winning_counts.items()}
    print("Final Win Rates: ", final_win_rates)




