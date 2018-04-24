from loader import bot_list, load_test_decks, load_training_decks, load_training_games
from progress.bar import Bar
from progress.helpers import SHOW_CURSOR

from crossval import crossval


def test_model(model, model_config) -> None:
    print('Testing {} with cross validation'.format(model.__name__))
    training_games = load_training_games()
    training_decks = load_training_decks()
    try:
        print('Average RMSE:', crossval(4, training_games, training_decks, model, model_config))
    except KeyboardInterrupt:
        print(SHOW_CURSOR)


def generate_submission(model, model_config) -> None:
    print('Generating data/submission.csv with {}'.format(model.__name__))
    training_games = load_training_games()
    training_decks = load_training_decks()
    test_decks = load_test_decks()
    model_instance = model()
    model_instance.learn(training_games, training_decks, model_config)
    n = len(bot_list) * len(test_decks)
    try:
        bar = Bar('', max=n, suffix='%(index)d/%(max)d ETA: %(eta)ds')
        with open('data/submission.csv', 'w') as file:
            for bot in bot_list:
                bar.message = bot
                for deck in test_decks:
                    print('{};{};{}'.format(bot, deck['deckName'], model_instance.predict(bot, deck)), file=file)
                    bar.next()
        bar.finish()
    except KeyboardInterrupt:
        print(SHOW_CURSOR)
