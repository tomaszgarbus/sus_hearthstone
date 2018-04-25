from collections import defaultdict

from base_model import *
from loader import LoadedData, all_hero_types


def print_counter(ctr: Dict[Any, int]) -> None:
    print('count', len(ctr))
    print('min', min(ctr.items(), key=lambda x: x[1]))
    print('max', max(ctr.items(), key=lambda x: x[1]))


if __name__ == '__main__':
    print('example deck', LoadedData.training_decks[0])
    print('example game', LoadedData.training_games[0])
    print(all_hero_types(LoadedData.training_decks))
    bot_counter = defaultdict(lambda: 0)
    deck_counter = defaultdict(lambda: 0)
    pair_counter = defaultdict(lambda: 0)
    for game in LoadedData.training_games:
        bot_counter[game['bot0']] += 1
        bot_counter[game['bot1']] += 1
        deck_counter[game['deck0']] += 1
        deck_counter[game['deck1']] += 1
        pair_counter[(game['bot0'], game['deck0'])] += 1
        pair_counter[(game['bot1'], game['deck1'])] += 1
    print('bots')
    print_counter(bot_counter)
    print('decks')
    print_counter(deck_counter)
    print('bot/deck pairs')
    print_counter(pair_counter)
