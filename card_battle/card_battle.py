import os
from flask import Flask, send_file
from flask_sock import Sock
from treys import Card, Evaluator, Deck
from itertools import combinations
import json

app = Flask(__name__)
sock = Sock(app)

evaluator = Evaluator()


def calculate_remaining_combos_with_blocked_cards(player1_hand, player2_hand):
    deck = Deck()
    blocked_cards = player1_hand + player2_hand
    deck.cards = [card for card in deck.cards if card not in blocked_cards]
    return list(combinations(deck.cards, 5))


@app.route("/")
def home():
    # Serve the card_battle.html file from the same directory
    html_path = os.path.join(os.path.dirname(__file__), "card_battle.html")
    return send_file(html_path)


@sock.route("/evaluate")
def evaluate(socket):
    data = socket.receive()
    data = json.loads(data)

    player1_hand = [Card.new(data["p1_card1"]), Card.new(data["p1_card2"])]
    player2_hand = [Card.new(data["p2_card1"]), Card.new(data["p2_card2"])]

    community_combos = calculate_remaining_combos_with_blocked_cards(player1_hand, player2_hand)

    p1_wins = 0
    p2_wins = 0
    ties = 0
    total_games = len(community_combos)

    for i, community in enumerate(community_combos):
        p1_score = evaluator.evaluate(list(community), player1_hand)
        p2_score = evaluator.evaluate(list(community), player2_hand)

        if p1_score < p2_score:
            p1_wins += 1
        elif p2_score < p1_score:
            p2_wins += 1
        else:
            ties += 1

        if (i + 1) % 100_000 == 0 or (i + 1) == total_games:
            socket.send(json.dumps({
                "type": "progress",
                "games_played": i + 1,
                "total_games": total_games,
                "player1_win_prob": round((p1_wins / (i + 1)) * 100, 2),
                "player2_win_prob": round((p2_wins / (i + 1)) * 100, 2),
                "tie_prob": round((ties / (i + 1)) * 100, 2),
            }))

    socket.send(json.dumps({
        "type": "final",
        "total_games": total_games,
        "player1_win_prob": round((p1_wins / total_games) * 100, 2),
        "player2_win_prob": round((p2_wins / total_games) * 100, 2),
        "tie_prob": round((ties / total_games) * 100, 2),
    }))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
