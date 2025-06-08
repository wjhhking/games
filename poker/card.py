from enum import Enum
from functools import total_ordering


class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        return {
            Rank.ACE: "A",
            Rank.KING: "K",
            Rank.QUEEN: "Q",
            Rank.JACK: "J",
            Rank.TEN: "10",
            Rank.NINE: "9",
            Rank.EIGHT: "8",
            Rank.SEVEN: "7",
            Rank.SIX: "6",
            Rank.FIVE: "5",
            Rank.FOUR: "4",
            Rank.THREE: "3",
            Rank.TWO: "2",
        }[self]

    @staticmethod
    def from_string(rank_str):
        rank_map = {
            "A": Rank.ACE,
            "K": Rank.KING,
            "Q": Rank.QUEEN,
            "J": Rank.JACK,
            "10": Rank.TEN,
            "9": Rank.NINE,
            "8": Rank.EIGHT,
            "7": Rank.SEVEN,
            "6": Rank.SIX,
            "5": Rank.FIVE,
            "4": Rank.FOUR,
            "3": Rank.THREE,
            "2": Rank.TWO,
        }
        rank = rank_map.get(rank_str.upper(), None)
        if rank is None:
            raise ValueError(f"Invalid rank: '{rank_str}'")
        return rank

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value


class Suit(Enum):
    SPADES = "♠"
    HEARTS = "♥"
    CLUBS = "♣"
    DIAMONDS = "♦"

    def __str__(self):
        return self.value

    @staticmethod
    def from_string(suit_str):
        suit_map = {
            "s": Suit.SPADES,
            "h": Suit.HEARTS,
            "c": Suit.CLUBS,
            "d": Suit.DIAMONDS,
        }
        suit = suit_map.get(suit_str.lower(), None)
        if suit is None:
            raise ValueError(f"Invalid suit: '{suit_str}'")
        return suit


@total_ordering
class Card:
    def __init__(self, rank, suit):
        if isinstance(rank, str):
            rank = Rank.from_string(rank)
        if isinstance(suit, str):
            suit = Suit.from_string(suit)

        if not isinstance(rank, Rank) or not isinstance(suit, Suit):
            raise ValueError("Invalid rank or suit")

        self.rank = rank
        self.suit = suit

    def __eq__(self, other):
        # Equality checks both rank and suit
        return self.rank == other.rank

    def __lt__(self, other):
        # Compare only by rank, ignoring suit
        return self.rank.value < other.rank.value

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def __hash__(self):
        # Hashing still considers both rank and suit for uniqueness
        return hash((self.rank, self.suit))


# Two cards, ordered by rank (descending) and suit (descending)
class HoleCards:
    def __init__(self, card1, card2):
        # Ensure card1 is the higher rank (or same rank but sorted by suit)
        if card1 > card2:
            self.card1, self.card2 = card1, card2
        else:
            self.card1, self.card2 = card2, card1

    def __str__(self):
        return f"{self.card1}-{self.card2}"

    def __repr__(self):
        return self.__str__()

