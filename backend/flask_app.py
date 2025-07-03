from flask import Flask, request, jsonify
from flask_cors import CORS
from bot import PokerBot

app = Flask(__name__)
CORS(app)

# Initialize your PokerBot with parameters
bot = PokerBot(n_players=2, n_simulations=10000)

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    hole_cards = data.get("holeCards", [])
    community_cards = data.get("communityCards", [])

    if len(hole_cards) != 2:
        return jsonify({"error": "You must select exactly 2 hole cards."}), 400
    if len(community_cards) > 5:
        return jsonify({"error": "Maximum of 5 community cards allowed."}), 400

    bot = PokerBot()
    action, _, win_prob = bot.get_action(hole_cards, community_cards, pot_size=10, call_amount=2)

    return jsonify({
        "recommendation": action,
        "winProbability": round(win_prob, 2)
    })

    try:
        action, raise_amt = bot.get_action(hole_cards, community_cards, pot_size, call_amount)
        win_prob = bot.sim.last_win_prob  # Get the latest probability from simulator
        return jsonify({
            "winProbability": round(win_prob * 100, 2),
            "recommendation": action,
            "raiseAmount": raise_amt
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
