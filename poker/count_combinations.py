from flask import Flask, send_from_directory, request, jsonify
from treys import Card, Evaluator, Deck
from itertools import combinations
from collections import Counter

app = Flask(__name__, static_folder=".")

evaluator = Evaluator()

def calculate_remaining_combos_with_blocked_cards(player1_hand, player2_hand):
    """
    Calculates the possible combinations of community cards given blocked cards.

    Args:
        player1_hand (list): Cards held by Player 1.
        player2_hand (list): Cards held by Player 2.

    Returns:
        list: All valid combinations of community cards.
    """
    # Initialize deck
    deck = Deck()

    # Remove player cards from the deck
    blocked_cards = player1_hand + player2_hand
    deck.cards = [card for card in deck.cards if card not in blocked_cards]

    # Generate all combinations of 5 cards for the community cards
    return list(combinations(deck.cards, 5))


@app.route("/")
def home():
    return send_from_directory(app.static_folder, "card_battle.html")


@app.route("/evaluate", methods=["POST"])
def evaluate():
    """
    Evaluates the winning probabilities for the selected player hands.

    Returns:
        JSON: Win probabilities for Player 1, Player 2, and tie.
    """
    data = request.json

    # Parse player hands
    player1_hand = [Card.new(data["p1_card1"]), Card.new(data["p1_card2"])]
    player2_hand = [Card.new(data["p2_card1"]), Card.new(data["p2_card2"])]

    # Calculate all possible community card combinations
    community_combos = calculate_remaining_combos_with_blocked_cards(player1_hand, player2_hand)

    # Initialize win counters
    p1_wins = 0
    p2_wins = 0
    ties = 0

    # Evaluate each community card combination
    for community in community_combos:
        p1_score = evaluator.evaluate(list(community), player1_hand)
        p2_score = evaluator.evaluate(list(community), player2_hand)

        if p1_score < p2_score:
            p1_wins += 1
        elif p2_score < p1_score:
            p2_wins += 1
        else:
            ties += 1

    # Calculate total games
    total = p1_wins + p2_wins + ties

    # Return results as JSON
    return jsonify({
        "player1_win_prob": round((p1_wins / total) * 100, 2),
        "player2_win_prob": round((p2_wins / total) * 100, 2),
        "tie_prob": round((ties / total) * 100, 2),
    })


if __name__ == "__main__":
    app.run(debug=True)
