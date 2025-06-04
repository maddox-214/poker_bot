import numpy as np
from treys import Deck, Card
from evaluator import score_hand
from utils import deal_hole_cards, deal_community_cards
from tqdm import tqdm

class MonteCarloSimulator:
    def __init__(self, n_players=2, n_simulations=10000):
        self.n_players = n_players
        self.n_simulations = n_simulations

    def simulate_win_prob(self, hole_cards, known_community=None):
        """
        Estimate win probability for `hole_cards` vs (n_players - 1) random opponents.
        hole_cards: list of two treys.Card ints for our bot.
        known_community: list of treys.Card ints (0 to 5 cards already on board).
        """
        wins = 0
        ties = 0
        for _ in range(self.n_simulations):
            deck = Deck()  # fresh deck
            # remove hole_cards and known community from deck
            for c in hole_cards:
                deck.cards.remove(c)
            if known_community:
                for c in known_community:
                    deck.cards.remove(c)

            # deal opponents' holes
            opp_holes = deal_hole_cards(deck, self.n_players - 1)

            # deal remaining community
            to_deal = 5 - (len(known_community) if known_community else 0)
            remaining_comm = deal_community_cards(deck, to_deal)
            full_community = (known_community or []) + remaining_comm

            # score our hand
            our_score = score_hand(hole_cards, full_community)

            # score opponents
            opp_scores = [score_hand(opp, full_community) for opp in opp_holes]

            all_scores = opp_scores + [our_score]
            best_score = min(all_scores)

            if our_score == best_score:
                # check ties
                if all_scores.count(best_score) > 1:
                    ties += 1
                else:
                    wins += 1

        win_prob = wins / self.n_simulations
        tie_prob = ties / self.n_simulations
        return win_prob, tie_prob

    def simulate_EV(self, hole_cards, known_community=None, pot_size=1, call_amount=1):
        """
        Compute EV.call: EV = win_prob * (pot_size) - (1 - win_prob) * call_amount
        """
        win_prob, tie_prob = self.simulate_win_prob(hole_cards, known_community)
        ev_call = win_prob * pot_size + tie_prob * (pot_size / self.n_players) - (1 - win_prob - tie_prob) * call_amount
        return ev_call
