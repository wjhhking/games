import unittest
from card import Rank, Suit, Card, HoleCards


class TestRank(unittest.TestCase):
    def test_rank_to_string(self):
        self.assertEqual(str(Rank.ACE), "A")
        self.assertEqual(str(Rank.KING), "K")
        self.assertEqual(str(Rank.QUEEN), "Q")
        self.assertEqual(str(Rank.TEN), "10")

    def test_rank_from_string(self):
        self.assertEqual(Rank.from_string("A"), Rank.ACE)
        self.assertEqual(Rank.from_string("K"), Rank.KING)
        self.assertEqual(Rank.from_string("Q"), Rank.QUEEN)
        self.assertEqual(Rank.from_string("10"), Rank.TEN)
        with self.assertRaises(ValueError):
            Rank.from_string("Invalid")

    def test_rank_comparison(self):
        self.assertTrue(Rank.ACE > Rank.KING)
        self.assertTrue(Rank.TWO < Rank.THREE)
        self.assertEqual(Rank.ACE, Rank.ACE)


class TestSuit(unittest.TestCase):
    def test_suit_to_string(self):
        self.assertEqual(str(Suit.SPADES), "♠")
        self.assertEqual(str(Suit.HEARTS), "♥")
        self.assertEqual(str(Suit.DIAMONDS), "♦")
        self.assertEqual(str(Suit.CLUBS), "♣")

    def test_suit_from_string(self):
        self.assertEqual(Suit.from_string("s"), Suit.SPADES)
        self.assertEqual(Suit.from_string("h"), Suit.HEARTS)
        self.assertEqual(Suit.from_string("d"), Suit.DIAMONDS)
        self.assertEqual(Suit.from_string("c"), Suit.CLUBS)
        with self.assertRaises(ValueError):
            Suit.from_string("Invalid")


class TestCard(unittest.TestCase):
    def test_card_initialization(self):
        card = Card(Rank.ACE, Suit.SPADES)
        self.assertEqual(card.rank, Rank.ACE)
        self.assertEqual(card.suit, Suit.SPADES)

        card = Card("A", "s")
        self.assertEqual(card.rank, Rank.ACE)
        self.assertEqual(card.suit, Suit.SPADES)

    def test_invalid_card_initialization(self):
        with self.assertRaises(ValueError):
            Card("InvalidRank", "s")
        with self.assertRaises(ValueError):
            Card("A", "InvalidSuit")

    def test_card_equality(self):
        card1 = Card(Rank.ACE, Suit.SPADES)
        card2 = Card("A", "s")
        self.assertEqual(card1, card2)

        card3 = Card(Rank.KING, Suit.HEARTS)
        self.assertNotEqual(card1, card3)

    def test_card_comparison(self):
        card1 = Card(Rank.ACE, Suit.SPADES)
        card2 = Card(Rank.KING, Suit.SPADES)
        card3 = Card(Rank.KING, Suit.HEARTS)
        self.assertTrue(card1 > card2)
        self.assertTrue(card2 < card1)
        self.assertFalse(card2 > card3)
        self.assertFalse(card2 < card3)

    def test_card_hashing(self):
        card_set = {Card(Rank.ACE, Suit.SPADES), Card("A", "s")}
        self.assertEqual(len(card_set), 1)

        card_set.add(Card("K", "s"))
        self.assertEqual(len(card_set), 2)

    def test_card_representation(self):
        card = Card(Rank.ACE, Suit.SPADES)
        self.assertEqual(repr(card), "A♠")


class TestHoleCards(unittest.TestCase):
    def test_hole_cards_initialization(self):
        card1 = Card(Rank.ACE, Suit.SPADES)
        card2 = Card(Rank.KING, Suit.HEARTS)
        hole_cards = HoleCards(card1, card2)
        self.assertEqual(hole_cards.card1, card1)
        self.assertEqual(hole_cards.card2, card2)

        # Reverse order
        hole_cards = HoleCards(card2, card1)
        self.assertEqual(hole_cards.card1, card1)
        self.assertEqual(hole_cards.card2, card2)

    def test_hole_cards_representation(self):
        card1 = Card(Rank.ACE, Suit.SPADES)
        card2 = Card(Rank.KING, Suit.HEARTS)
        hole_cards = HoleCards(card1, card2)
        self.assertEqual(str(hole_cards), "A♠-K♥")


if __name__ == "__main__":
    unittest.main()
