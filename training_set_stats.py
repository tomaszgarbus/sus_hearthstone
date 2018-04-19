from collections import defaultdict

from loader import *


def print_counter(ctr):
    print(len(ctr))
    print('min', min(ctr.items(), key=lambda x: x[1]))
    print('max', max(ctr.items(), key=lambda x: x[1]))


if __name__ == '__main__':
    print(load_training_decks()[0])
    training_games = load_training_games()
    bot_counter = defaultdict(lambda: 0)
    deck_counter = defaultdict(lambda: 0)
    pair_counter = defaultdict(lambda: 0)
    for game in training_games:
        bot_counter[game[1]] += 1
        bot_counter[game[3]] += 1
        deck_counter[game[2]] += 1
        deck_counter[game[4]] += 1
        pair_counter[(game[1], game[2])] += 1
        pair_counter[(game[3], game[4])] += 1
    print_counter(bot_counter)
    print_counter(deck_counter)
    print_counter(pair_counter)
