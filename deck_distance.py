from loader import load_training_decks, load_training_games, load_test_decks
from collections import defaultdict
from crossval import crossval
from loader import bot_list


def calculate_deck_distance(deck1: dict, deck2: dict):
    if deck1['hero'] != deck2['hero']:
        return 31
    distance = 30
    for card in deck1['cards']:
        if card in deck2['cards']:
            distance -= min(deck1['cards'][card], deck2['cards'][card])
    return distance


class KNN:
    k = 1
    training_games = []
    training_decks = []
    training_results = defaultdict(lambda: defaultdict(lambda: (0, 0)))

    def __init__(self, training_games, training_decks, k=9):
        self.k = k
        self.training_games = training_games
        self.training_decks = training_decks
        for game in training_games:
            player0, player1 = (game['bot0'], game['deck0']), (game['bot1'], (game['deck1']))
            wins = self.training_results[player0][player1]
            if game['winner'] == 0:
                wins = (wins[0] + 1, wins[1])
            else:
                wins = (wins[0], wins[1] + 1)
            self.training_results[player0][player1] = wins
            self.training_results[player1][player0] = (wins[1], wins[0])

    # deck1 must be a deck from the training set
    # return the probability of deck0 winning the game
    def predict_match_result(self, bot0, deck0, bot1, deck1):
        player1 = (bot1, deck1)
        player1_results = self.training_results[player1]
        results_sum = (0, 0)
        used_decks = 0
        for deck in sorted(self.training_decks, key=lambda d: calculate_deck_distance(deck0, d)):
            if used_decks >= self.k:
                break
            r = player1_results[(bot0, deck['deckName'])]
            if r == (0, 0):
                continue
            results_sum = (results_sum[0] + r[0], results_sum[1] + r[1])
            used_decks += 1
        return results_sum[1] / sum(results_sum)

    # returns the predicted winrate of (bot, deck) vs all (bot, deck) pairs in the training set
    def predict(self, bot, deck):
        winrate = 0
        for player in self.training_results:
            winrate += self.predict_match_result(bot, deck, player[0], player[1])
        winrate /= len(self.training_results)
        return winrate * 100


def main():
    training_games = load_training_games()
    training_decks = load_training_decks()
    test_decks = sorted(load_test_decks(), key=lambda d: d['deckName'])
    # print('Score:', crossval(4, training_games, training_decks, KNN))
    knn = KNN(training_games, training_decks)
    with open('submission.csv', 'w') as f:
        for bot in bot_list:
            for deck in test_decks:
                print(bot, deck['deckName'])
                print('{};{};{}'.format(bot, deck['deckName'], knn.predict(bot, deck)), file=f)


if __name__ == '__main__':
    main()
