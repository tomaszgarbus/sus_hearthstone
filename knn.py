from collections import defaultdict

from base_model import *
from loader import bot_list
from tester import generate_submission, test_model


def calculate_deck_distance(deck1: Deck, deck2: Deck) -> int:
    distance = 30
    if deck1['hero'] != deck2['hero']:
        distance += 10
    for card in deck1['cards']:
        if card in deck2['cards']:
            distance -= min(deck1['cards'][card], deck2['cards'][card])
    return distance


class KNN(BaseModel):
    k = 1
    config = {}
    training_games = []
    training_decks = []
    training_results = defaultdict(lambda: defaultdict(lambda: (0, 0)))
    training_winrates = {}

    def learn(self, training_games: List[Game], training_decks: List[Deck], config: ModelConfig = None) -> None:
        self.k = config['k']
        self.config = config
        self.training_games = training_games
        self.training_decks = training_decks
        self.training_results = defaultdict(lambda: defaultdict(lambda: (0, 0)))
        self.training_winrates = {}
        for game in training_games:
            player0, player1 = (game['bot0'], game['deck0']), (game['bot1'], (game['deck1']))
            wins = self.training_results[player0][player1]
            if game['winner'] == 0:
                wins = (wins[0] + 0.5 + game['winner_hp'] / 30, wins[1])
            else:
                wins = (wins[0], wins[1] + 0.5 + game['winner_hp'] / 30)
            self.training_results[player0][player1] = wins
            self.training_results[player1][player0] = (wins[1], wins[0])
        for player0, results_dict in self.training_results.items():
            results_sum = (0, 0)
            for player1, results in results_dict.items():
                results_sum = (results_sum[0] + results[0], results_sum[1] + results[1])
            self.training_winrates[player0] = results_sum[0] / sum(results_sum)

    def predict_match_result(self, bot0: str, deck0: Deck, bot1: str, deck1: DeckName) -> float:
        player1 = (bot1, deck1)
        player1_results = self.training_results[player1]
        other_bots_results = []
        for bot in bot_list:
            if bot != bot0:
                other_bots_results.append(self.training_results[(bot, deck1)])
        results_sum = (0, 0)
        used_decks = 0
        for deck in sorted(self.training_decks, key=lambda d: calculate_deck_distance(deck0, d)):
            if used_decks >= self.k:
                break
            dist = calculate_deck_distance(deck0, deck)
            if dist >= 30:
                break
            # weight = 1
            weight = (30 - dist) / 30
            r = player1_results.get((bot0, deck['deckName']))
            if r is None:
                r = (0, 0)
            for results in other_bots_results:
                r2 = results.get((bot0, deck['deckName']))
                if r2 is None:
                    continue
                r = (r[0] + r2[0] * 0.5, r[1] + r2[1] * 0.5)
            if r == (0, 0):
                continue
            results_sum = (results_sum[0] + r[0] * weight, results_sum[1] + r[1] * weight)
            used_decks += 1
        if sum(results_sum) == 0:
            return 0.5
        return results_sum[1] / sum(results_sum)

    # returns the predicted winrate of (bot, deck) vs all (bot, deck) pairs in the training set
    def predict(self, bot: str, deck: Deck) -> float:
        if self.config.get('predict_each_game'):
            winrate = 0
            for player in self.training_results:
                winrate += self.predict_match_result(bot, deck, player[0], player[1])
            winrate /= len(self.training_results)
            return 100 * winrate
        else:
            winrate, weights = 0, 0
            used_decks = 0
            for deck1 in sorted(self.training_decks, key=lambda d: calculate_deck_distance(deck, d)):
                if used_decks >= self.k:
                    break
                dist = calculate_deck_distance(deck, deck1)
                if dist >= 30:
                    break
                weight = (30 - dist) / 30
                wr = self.training_winrates[(bot, deck1['deckName'])]
                winrate += wr * weight
                weights += weight
                used_decks += 1
            if weights == 0:
                print('Warning: weights == 0')
                return 50.0
            return 100 * winrate / weights


if __name__ == '__main__':
    best_k, best_result = -1, 1000
    # for k in list(range(1, 21)) + [1000]:
    # for k in [10, 1000]:
    #     print('k =', k)
    #     result = test_model(KNN, {'k': k, 'predict_each_game': True})
    #     if result < best_result:
    #         best_k, best_result = k, result
    # print('Best', best_k, best_result)
    generate_submission(KNN, {'k': 1000, 'predict_each_game': True})
