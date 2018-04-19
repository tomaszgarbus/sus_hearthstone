import csv
import json

from typing import Dict, List


def remove_one_element_lists(d: dict):
    for key, value in d.items():
        if isinstance(value, list) and len(value) == 1:
            d[key] = value[0]
        if isinstance(d[key], dict):
            remove_one_element_lists(d[key])


def load_decks(filename: str) -> List[Dict]:
    decks = []
    with open(filename) as file:
        lines = file.read().strip().split('\n')
        for line in lines:
            deck = json.loads(line)
            remove_one_element_lists(deck)
            decks.append(deck)
    return decks


def load_training_decks() -> List[Dict]:
    return load_decks('data/trainingDecks.json')


def load_test_decks() -> List[Dict]:
    return load_decks('data/testDecks.json')


def load_training_games() -> List[List]:
    with open('data/training_games.csv') as file:
        reader = csv.reader(file, delimiter=';')
        games = []
        for line in reader:
            games.append(line)
        return games


def map_decks_by_name(decks: List[Dict]) -> Dict:
    decks_dict = {}
    for deck in decks:
        decks_dict[deck['deckName'][0]] = deck
    return decks_dict


def all_card_names(decks: List[Dict]) -> Dict[str, int]:
    all_names = {}
    for deck in decks:
        for card_name in deck['cards']:
            if card_name in all_names:
                pass
            else:
                all_names[card_name] = len(all_names)
    return all_names


def all_hero_types(decks: List[Dict]) -> Dict[str, int]:
    all_heroes = {}
    for deck in decks:
        if deck['hero'][0] in all_heroes:
            pass
        else:
            all_heroes[deck['hero'][0]] = len(all_heroes)
    return all_heroes