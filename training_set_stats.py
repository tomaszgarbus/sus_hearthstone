from collections import defaultdict

from loader import load_training_decks, load_training_games


def print_counter(ctr: dict) -> None:
    print('count', len(ctr))
    print('min', min(ctr.items(), key=lambda x: x[1]))
    print('max', max(ctr.items(), key=lambda x: x[1]))


if __name__ == '__main__':
    print('example deck', load_training_decks()[0])
    training_games = load_training_games()
    print('example game', training_games[0])
    bot_counter = defaultdict(lambda: 0)
    deck_counter = defaultdict(lambda: 0)
    pair_counter = defaultdict(lambda: 0)
    for game in training_games:
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
