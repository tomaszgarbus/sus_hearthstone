import loader
from typing import List, Dict, Callable


def build_single_player_input(deck: Dict,
                bot_id: bool = True,
                hero_id: bool = True,
                cards_cardinality: bool = True,
                cards_cardinality_funs1: Callable[int] = [],
                cards_cardinality_funs2: Callable[int, int] = []):
    """
    Generates input vector for one player in a game.
    Following parameters will be appended with True:
    :param bot_id: Bot's id in hot-one format.
    :param hero_id: Bot's hero id in hot-one format.
    :param cards_cardinality: List containing count of each card in the deck.
    The following parameters generate additional features:
    :param cards_cardinality_funs1: List of functions applied to each element
        in list of cards cardinalities.
        For example, if cards_cardinality_funs1 = [lambda x: x**2, lambda x: x**3],
        squares and cubes of each card count will be also added to input vector.
    :param cards_cardinality_funs2: List of functions applied to each pair of
        elements in list of cards cardinalities.
        For example, if cards_cardinality_funs1 = [lambda x, y: x*y, lambda x, y: x*x*y*y],
        the product and squared product of each pair of card counts will be appended
        to input vector.
    :return:
    """
    raise NotImplementedError