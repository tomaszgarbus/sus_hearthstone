from typing import List, Dict

class BaseModel:

    def learn(self, training_games: List[Dict], training_decks: List[Dict], config: Dict) -> None:
        raise NotImplementedError

    # deck1 must be a deck from the training set
    # return the probability of deck0 winning the game
    def predict_match_result(self, bot0: str, deck0: Dict, bot1: str, deck1: Dict) -> float:
        raise NotImplementedError

    # returns the predicted winrate of (bot, deck) vs all (bot, deck) pairs in the training set
    def predict(self, bot: str, deck: Dict) -> float:
        raise NotImplementedError
