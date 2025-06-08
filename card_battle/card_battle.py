import os
from flask import Flask, send_file
from flask_sock import Sock
from treys import Card, Evaluator, Deck
from itertools import combinations
import json
import random

# Initialize Flask and Sock
app = Flask(__name__)
sock = Sock(app)

# Initialize Treys evaluator
evaluator = Evaluator()


def calculate_remaining_combos_with_blocked_cards(player1_hand, player2_hand):
    """
    Calculate all possible community card combinations, excluding the blocked cards.
    """
    deck = Deck()
    blocked_cards = player1_hand + player2_hand
    deck.cards = [card for card in deck.cards if card not in blocked_cards]
    combos = list(combinations(deck.cards, 5))
    return random.shuffle(combos)


@app.route("/")
def home():
    """
    Serve the main HTML file for the Card Battle app.
    """
    html_path = os.path.join(os.path.dirname(__file__), "card_battle.html")
    return send_file(html_path)


@sock.route("/evaluate")
def evaluate(socket):
    """
    WebSocket endpoint to evaluate hands and calculate probabilities.
    """
    print("Evaluating: ")  # Log in the backend

    # Notify the frontend that evaluation has started
    socket.send(json.dumps({"type": "status", "message": "Evaluating..."}))

    # Receive data from the client
    data = socket.receive()
    data = json.loads(data)

    # Parse player hands
    player1_hand = [Card.new(data["p1_card1"]), Card.new(data["p1_card2"])]
    player2_hand = [Card.new(data["p2_card1"]), Card.new(data["p2_card2"])]

    # Generate all possible community card combinations
    community_combos = calculate_remaining_combos_with_blocked_cards(player1_hand, player2_hand)

    # Initialize counters
    p1_wins = 0
    p2_wins = 0
    ties = 0
    total_games = len(community_combos)

    # Evaluate each combination
    for i, community in enumerate(community_combos):
        p1_score = evaluator.evaluate(list(community), player1_hand)
        p2_score = evaluator.evaluate(list(community), player2_hand)

        if p1_score < p2_score:
            p1_wins += 1
        elif p2_score < p1_score:
            p2_wins += 1
        else:
            ties += 1

        # Send progress updates every 10,000 games or at the end
        if (i + 1) % 10_000 == 0 or (i + 1) == total_games:
            socket.send(json.dumps({
                "type": "progress",
                "games_played": i + 1,
                "total_games": total_games,
                "player1_win_prob": round((p1_wins / (i + 1)) * 100, 2),
                "player2_win_prob": round((p2_wins / (i + 1)) * 100, 2),
                "tie_prob": round((ties / (i + 1)) * 100, 2),
            }))

    # Send the final results
    socket.send(json.dumps({
        "type": "final",
        "total_games": total_games,
        "player1_win_prob": round((p1_wins / total_games) * 100, 2),
        "player2_win_prob": round((p2_wins / total_games) * 100, 2),
        "tie_prob": round((ties / total_games) * 100, 2),
    }))


if __name__ == "__main__":
    # Use the Render-assigned port or default to 5001
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
