from typing import Any, Dict, List, Optional, Type, Union


Game = Dict[str, Union[str, int]]
Deck = Dict[str, Union[str, Dict[str, int]]]
DeckName = str
ModelConfig = Optional[Dict[str, Any]]


class BaseModel:
    def learn(self, training_games: List[Game], training_decks: List[Deck], config: ModelConfig = None) -> None:
        raise NotImplementedError

    # deck1 must be a deck from the training set
    # return the probability of deck0 winning the game
    def predict_match_result(self, bot0: str, deck0: Deck, bot1: str, deck1: DeckName) -> float:
        raise NotImplementedError

    # returns the predicted winrate of (bot, deck) vs all (bot, deck) pairs in the training set
    def predict(self, bot: str, deck: Deck) -> float:
        raise NotImplementedError
