import sys
from treys import Card
from simulator import MonteCarloSimulator
from evaluator import rank_to_string
from utils import parse_pretty_cards


class PokerBot:
    def __init__(self, n_players=2, n_simulations=10000):
        self.sim = MonteCarloSimulator(n_players=n_players, n_simulations=n_simulations)
        self.last_win_prob = None

    def get_action(self, hole_cards_str, community_cards_str=None, pot_size=1, call_amount=1):
        """
        hole_cards_str: ['As', 'Kd']
        community_cards_str: e.g. ['2h','Jc','Ts'] or []
        Returns: (action, raise_amt, win_prob)
        """
        hole_cards = parse_pretty_cards(hole_cards_str)
        known_comm = parse_pretty_cards(community_cards_str) if community_cards_str else []

        ev_call, win_prob = self.sim.simulate_EV(hole_cards, known_comm, pot_size, call_amount)
        win_prob = max(0.0, min(1.0, win_prob))  # clamp to [0, 1] just in case

        if ev_call > 0:
            return "call", None, win_prob
        else:
            return "fold", None, win_prob


if __name__ == "__main__":
    # example usage:
    bot = PokerBot(n_players=2, n_simulations=10000)

    # read from command line:
    # python bot.py As Kd 2h Jc Ts
    if len(sys.argv) < 3:
        print("Usage: python bot.py <hole1> <hole2> [community1 ... communityN]")
        sys.exit(1)

    hole1, hole2 = sys.argv[1], sys.argv[2]
    community = sys.argv[3:] if len(sys.argv) > 3 else []

    action, raise_amt, win_prob = bot.get_action([hole1, hole2], community, pot_size=10, call_amount=2)
    print(f"Hole: {hole1} {hole2}")
    if community:
        print("Board:", " ".join(community))
    print("Decision:", action, raise_amt if raise_amt else "")
    print(f"Win Probability: {win_prob:.2%}")
