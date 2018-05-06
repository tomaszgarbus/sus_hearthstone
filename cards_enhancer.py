import requests
import json
import os

API_KEY = "CtLmfNp5QKmsheqmTqDqa6coP1UEp1XYNu4jsnJCgRhkIsCJLP"


class CardsEnhancer:
    downloaded_cards = {}

    def __init__(self):
        if os.path.isfile('data/all_cards.json'):
            with open('data/all_cards.json') as f:
                self.downloaded_cards = json.load(f)

    def get_card(self, name):
        if name in self.downloaded_cards:
            return self.downloaded_cards[name]

        # Card unknown yet, perform the request
        url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/" + name
        r = requests.get(url, headers={"X-Mashape-Key": API_KEY})
        cards = r.json()
        # cards = list(filter(lambda a: a['type'] == 'Minion', cards))
        card = cards[0]

        if 'attack' not in card:
            print('Warning: card has no attack (type {0})'.format(card['type']))
            card['attack'] = 0

        if 'health' not in card:
            print('Warning: card has no health (type {0})'.format(card['type']))
            card['health'] = 0

        if 'cost' not in card:
            print('Warning: card has no cost (type {0})'.format(card['type']))
            card['cost'] = 0

        self.downloaded_cards[name] = card
        with open('data/all_cards.json', 'w') as f:
            f.write(json.dumps(self.downloaded_cards))
        return card


if __name__ == '__main__':
    enh = CardsEnhancer()
    c = enh.get_card("Murloc Tidehunter")
    print(c['attack'])
    c = enh.get_card("Murloc Tidehunter")
    print(c['attack'])