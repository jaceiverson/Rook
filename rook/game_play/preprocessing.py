import json
import random

from game_play.game_objects import Card


def make_card(suit: str, number: int, pvalue: int, tvalue: int = None):
    """
    This function accepts the suit and value of the card and returns
    the constructed Card object with the suit and value
    assigned to the values passed on to the function.
    """
    return Card(suit, number, pvalue, tvalue)


def make_deck_list() -> list[Card]:
    """
    This function takes in a dictionary of card suit and value pairs,
    creates a list of Card objects and returns it
    """
    card_list = []
    with open("./rook/resources/deck.json", "r") as f:
        rook_deck = json.load(f)

    rook_deck = rook_deck["ROOK DECK"]

    for suit, number in rook_deck.items():
        for card in rook_deck[suit]:
            card_obj = make_card(suit, card["Number"], card["pValue"], card["tValue"])
            card_list.append(card_obj)

    return card_list


def shuffle_deck(full_deck: list[Card]) -> list[Card]:
    """
    This function takes in as input the list of Card objects, shuffles them
    and returns the shuffled list.
    """
    random.shuffle(full_deck)
    return full_deck
