import numpy as np

from base_model import *
from loader import LoadedData, all_card_names, map_decks_by_name

"""
    DECK FORMAT: {
        'deckName': '...',
        'cards': {  # Cardinality sums to 30
            "Card Number Uno": 1|2|...|30,
            ...
            },
        'hero': 'Paladin'|'Mage'|'Shaman'|'Warlock'|'Rogue'|'Warrior'|'Priest'|'Druid'|'Hunter'
    }
    
    GAME FORMAT: {
        'id': 100001|100002|...,
        'bot0': 'A1'|'A2'|'B1'|'B2',
        'deck0': 'deck...',
        'bot1': 'A1'|'A2'|'B1'|'B2',
        'deck1': 'deck...',
        'winner': 0|1
    }
"""


class InputBuilder:
    bot_names = {'A1': 0,
                 'A2': 1,
                 'B1': 0,
                 'B2': 1}

    heroes = {'Paladin': 2,
              'Mage': 7,
              'Shaman': 4,
              'Warlock': 3,
              'Rogue': 5,
              'Warrior': 0,
              'Priest': 1,
              'Druid': 8,
              'Hunter': 6}

    all_cards = None  # :Dict[str, int], maps card name to unique id
    distinct_cards = 0

    decks = None

    def __init__(self):
        self.all_cards = all_card_names(LoadedData.test_decks + LoadedData.training_decks)
        self.distinct_cards = len(self.all_cards)
        self.decks = map_decks_by_name(LoadedData.training_decks + LoadedData.test_decks)

    def _one_hot(self, val: int, N: int) -> np.ndarray:
        assert 0 <= val < N
        ret = np.zeros((N,), dtype='float32')
        ret[val] = 1.
        return ret

    def build_single_player_input(self,
                                  deck: Dict,
                                  bot: str) -> np.ndarray:
        features = []

        # Append bot
        features.append(self._one_hot(self.bot_names[bot], 4))

        # Append hero
        features.append(self._one_hot(self.heroes[deck['hero']], 9))

        # Append cards cardinality
        cards_counts = np.zeros(self.distinct_cards, dtype=np.float32)
        for card in deck['cards']:
            count = deck['cards'][card]
            cards_counts[self.all_cards[card]] = count
        features.append(cards_counts)

        # TODO: add support for cards_cardinality_funs1 and cards_cardinlity_funs2

        return np.concatenate(features)

    def build_game_input(self,
                         game: Dict) -> np.ndarray:
        bot0 = game['bot0']
        bot1 = game['bot1']
        deck0 = self.decks[game['deck0']]
        deck1 = self.decks[game['deck1']]
        input_player1 = self.build_single_player_input(deck0, bot0)
        input_player2 = self.build_single_player_input(deck1, bot1)

        return np.concatenate([input_player1, input_player2])
