import json
import csv
from typing import Dict, List
import logging


def load_training_decks() -> List[Dict]:
    with open('data/trainingDecks.json') as file:
        lines = file.read().split('\n')
        decks = list(map(json.JSONDecoder().decode, lines[:-1]))
        return decks


def load_test_decks() -> List[Dict]:
    with open('data/testDecks.json') as file:
        lines = file.read().split('\n')
        decks = list(map(json.JSONDecoder().decode, lines[:-1]))
        return decks


def load_training_games() -> List[List]:
    with open('data/training_games.csv') as file:
        reader = csv.reader(file, delimiter=';')
        games = []
        for line in reader:
            games.append(line)
        return games[1:]
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
    print(len(all_names))
    return all_names


if __name__ == '__main__':
    training_decks = load_training_decks()
    test_decks = load_test_decks()
    games = load_training_games()
    decks = map_decks_by_name(training_decks)
    print(decks)