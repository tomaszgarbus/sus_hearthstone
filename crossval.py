import math
import random
from collections import defaultdict
from progress.bar import IncrementalBar

from base_model import *
from loader import bot_list


def crossval(folds: int, games: List[Game], decks: List[Deck], model: Type[BaseModel],
             model_config: ModelConfig) -> float:
    random.shuffle(decks)
    fold_decks = len(decks) // folds
    wins = defaultdict(lambda: (0, 0))
    for game in games:
        player0, player1 = (game['bot0'], game['deck0']), (game['bot1'], game['deck1'])
        wins0, wins1 = wins[player0], wins[player1]
        if game['winner'] == 0:
            wins0 = (wins0[0] + 1, wins0[1] + 1)
            wins1 = (wins1[0], wins1[1] + 1)
        else:
            wins0 = (wins0[0], wins0[1] + 1)
            wins1 = (wins1[0] + 1, wins1[1] + 1)
        wins[player0], wins[player1] = wins0, wins1
    winrates = {}
    for player, wr in wins.items():
        winrates[player] = 100 * wr[0] / wr[1]
    avg_rmse = 0
    for i in range(folds):
        test_decks = decks[i*fold_decks:(i+1)*fold_decks]
        training_decks = decks[:i*fold_decks] + decks[(i+1)*fold_decks:]
        training_deck_names = [d['deckName'] for d in training_decks]
        training_games = list(filter(
            lambda g: g['deck0'] in training_deck_names and g['deck1'] in training_deck_names, games))
        model_instance = model()
        model_instance.learn(training_games, training_decks, model_config)
        rmse = 0.0
        ctr = 0
        n = len(test_decks) * len(bot_list)
        bar = IncrementalBar('', max=n, suffix='%(index)d/%(max)d ETA: %(eta)ds')
        for deck in test_decks:
            for bot in bot_list:
                ctr += 1
                rmse += (model_instance.predict(bot, deck) - winrates[(bot, deck['deckName'])]) ** 2
                bar.message = '{}/{} | {:.5f}'.format(i + 1, folds, math.sqrt(rmse / ctr))
                bar.next()
        bar.finish()
        rmse = math.sqrt(rmse / n)
        avg_rmse += rmse
    avg_rmse /= folds
    return avg_rmse
