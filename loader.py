import csv
import json
<<<<<<< HEAD
import os
from typing import Dict, List
=======

from base_model import *

>>>>>>> d9f45f887d5b4e91a5dea13305853060fc7f929c

bot_list = ['A1', 'A2', 'B1', 'B2']


def remove_one_element_lists(d: dict) -> None:
    for key, value in d.items():
        if isinstance(value, list) and len(value) == 1:
            d[key] = value[0]
        if isinstance(d[key], dict):
            remove_one_element_lists(d[key])


def load_decks(filename: str) -> List[Deck]:
    decks = []
    with open(filename) as file:
        lines = file.read().strip().split('\n')
        for line in lines:
            deck = json.loads(line)
            remove_one_element_lists(deck)
            decks.append(deck)
    return decks


def load_training_decks() -> List[Deck]:
    return load_decks('data/trainingDecks.json')


def load_test_decks() -> List[Deck]:
    return load_decks('data/testDecks.json')


def load_training_games() -> List[Game]:
    if os.path.isfile('data/training_games_detailed.json'):
        with open('data/training_games_detailed.json') as file:
            games = json.load(file)
    else:
        print('Warning: data/training_games_detailed.json doesn\'t exist, loading from data/training_games.csv')
        with open('data/training_games.csv') as file:
            reader = csv.reader(file, delimiter=';')
            games = []
            field_names = ['id', 'bot0', 'deck0', 'bot1', 'deck1', 'winner']
            for line in reader:
                game = {}
                for name, value in zip(field_names, line):
                    game[name] = value
                game['winner'] = int(game['winner'][7])
                games.append(game)
    return games


def map_decks_by_name(decks: List[Deck]) -> Dict[DeckName, Deck]:
    decks_dict = {}
    for deck in decks:
        decks_dict[deck['deckName']] = deck
    return decks_dict


def all_card_names(decks: List[Deck]) -> Dict[str, int]:
    all_names = {}
    for deck in decks:
        for card_name in deck['cards']:
            if card_name in all_names:
                pass
            else:
                all_names[card_name] = len(all_names)
    return all_names


def all_hero_types(decks: List[Deck]) -> Dict[str, int]:
    all_heroes = {}
    for deck in decks:
        if deck['hero'] in all_heroes:
            pass
        else:
            all_heroes[deck['hero']] = len(all_heroes)
    return all_heroes


class LoadedData:
    training_games = load_training_games()
    training_decks = load_training_decks()
    test_decks = load_test_decks()
