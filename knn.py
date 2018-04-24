from collections import defaultdict
from typing import List, Dict

from base_model import BaseModel
from tester import generate_submission, test_model


def calculate_deck_distance(deck1: dict, deck2: dict) -> int:
    distance = 30
    if deck1['hero'] != deck2['hero']:
        distance += 10
    for card in deck1['cards']:
        if card in deck2['cards']:
            distance -= min(deck1['cards'][card], deck2['cards'][card])
    return distance


class KNN(BaseModel):
    k = 1
    training_games = []
    training_decks = []
    training_results = defaultdict(lambda: defaultdict(lambda: (0, 0)))

    def learn(self, training_games: List[dict], training_decks: List[dict], config: dict) -> None:
        self.k = config['k']
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

    def predict_match_result(self, bot0: str, deck0: dict, bot1: str, deck1: dict) -> float:
        player1 = (bot1, deck1)
        player1_results = self.training_results[player1]
        results_sum = (0, 0)
        used_decks = 0
        for deck in sorted(self.training_decks, key=lambda d: calculate_deck_distance(deck0, d)):
            if used_decks >= self.k:
                break
            dist = calculate_deck_distance(deck0, deck)
            if dist >= 30:
                continue
            weight = (30 - dist) / 30
            r = player1_results[(bot0, deck['deckName'])]
            if r == (0, 0):
                continue
            results_sum = (results_sum[0] + r[0] * weight, results_sum[1] + r[1] * weight)
            used_decks += 1
        if sum(results_sum) == 0:
            return 0.5
        return results_sum[1] / sum(results_sum)

    # returns the predicted winrate of (bot, deck) vs all (bot, deck) pairs in the training set
    def predict(self, bot: str, deck: Dict) -> float:
        winrate = 0
        for player in self.training_results:
            winrate += self.predict_match_result(bot, deck, player[0], player[1])
        winrate /= len(self.training_results)
        print(winrate)
        return winrate * 100


if __name__ == '__main__':
    test_model(KNN, {'k': 1000})
    # generate_submission(KNN, {'k': 1000})
