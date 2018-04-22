import math
import random
from collections import defaultdict
from loader import bot_list


def crossval(folds, games, decks, model):
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
        print('Fold {}/{}'.format(i + 1, folds))
        test_decks = decks[i*fold_decks:(i+1)*fold_decks]
        training_decks = decks[:i*fold_decks] + decks[(i+1)*fold_decks:]
        training_deck_names = [d['deckName'] for d in training_decks]
        training_games = list(filter(
            lambda g: g['deck0'] in training_deck_names and g['deck1'] in training_deck_names, games))
        trained_model = model(training_games, training_decks)
        rmse = 0
        ctr = 0
        n = len(test_decks) * len(bot_list)
        for deck in test_decks:
            for bot in bot_list:
                if ctr % (n // 5) == 0:
                    print('{}/{}'.format(ctr, n))
                ctr += 1
                rmse += (trained_model.predict(bot, deck) - winrates[(bot, deck['deckName'])]) ** 2
        rmse = math.sqrt(rmse / n)
        print('RMSE:', rmse)
        avg_rmse += rmse
    avg_rmse /= folds
    return avg_rmse
