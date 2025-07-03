
import random
from treys import Card, Deck

def deal_hole_cards(deck, n_hands=1):
    """
    Deal n_hands of 2-card holes from deck.
    Returns list of lists, each inner list is two `treys.Card` ints.
    """
    holes = []
    for _ in range(n_hands):
        holes.append([deck.draw(1)[0], deck.draw(1)[0]])
    return holes

def deal_community_cards(deck, n_cards):
    """
    Deal n_cards from the deck as community cards.
    Returns a list of `treys.Card` ints.
    """
    return deck.draw(n_cards)

def parse_pretty_cards(card_str_list):
    """
    Convert list of human-readable strings like ['As', 'Kd'] to treys Card ints.
    Example: parse_pretty_cards(['As', 'Kd']) -> [Card.new('As'), Card.new('Kd')]
    """
    return [Card.new(cs) for cs in card_str_list]

def clear_deck():
    return Deck()
