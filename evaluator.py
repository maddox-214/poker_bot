from treys import Evaluator, Card

_evaluator = Evaluator()

def score_hand(hole_cards, community_cards):
    """
    hole_cards: list of two treys.Card ints
    community_cards: list of treys.Card ints (length 3, 4, or 5)
    Returns an integer score—lower is better (Treys convention).
    """
    return _evaluator.evaluate(community_cards, hole_cards)

def rank_to_string(rank):
    """
    Convert Treys rank (int) to a human-readable string.
    Example: 1 -> "Royal Flush", etc.
    """
    return _evaluator.class_to_string(rank)
