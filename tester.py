from loader import bot_list, LoadedData
from progress.bar import IncrementalBar
from progress.helpers import SHOW_CURSOR

from base_model import *
from crossval import crossval


def test_model(model: Type[BaseModel], model_config: ModelConfig = None) -> float:
    if model_config is None:
        model_config = {}
    print('Testing {} with cross validation'.format(model.__name__))
    try:
        avg_rmse = crossval(4, LoadedData.training_games, LoadedData.training_decks, model, model_config)
        print('Average RMSE:', avg_rmse)
        return avg_rmse
    except KeyboardInterrupt:
        print(SHOW_CURSOR)
        raise KeyboardInterrupt


def generate_submission(model: Type[BaseModel], model_config: ModelConfig = None) -> None:
    if model_config is None:
        model_config = {}
    print('Generating data/submission.csv with {}'.format(model.__name__))
    model_instance = model()
    model_instance.learn(LoadedData.training_games, LoadedData.training_decks, model_config)
    n = len(bot_list) * len(LoadedData.test_decks)
    try:
        bar = IncrementalBar('', max=n, suffix='%(index)d/%(max)d ETA: %(eta)ds')
        with open('data/submission.csv', 'w') as file:
            for bot in bot_list:
                bar.message = bot
                for deck in LoadedData.test_decks:
                    print('{};{};{}'.format(bot, deck['deckName'], model_instance.predict(bot, deck)), file=file)
                    bar.next()
        bar.finish()
    except KeyboardInterrupt:
        print(SHOW_CURSOR)
        raise KeyboardInterrupt
