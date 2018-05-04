import requests

API_KEY = "CtLmfNp5QKmsheqmTqDqa6coP1UEp1XYNu4jsnJCgRhkIsCJLP"


class CardsEnhancer:
    downloaded_cards = {}

    def __init__(self):
        pass

    def get_card(self, name):
        if name in self.downloaded_cards:
            return self.downloaded_cards[name]

        # Card unknown yet, perform the request
        url = "https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/" + name
        r = requests.get(url, headers={"X-Mashape-Key": API_KEY})
        cards = r.json()
        cards = list(filter(lambda a: a['type'] == 'Minion', cards))
        card = cards[0]

        self.downloaded_cards[name] = card
        return card


if __name__ == '__main__':
    enh = CardsEnhancer()
    c = enh.get_card("Murloc Tidehunter")
    print(c['attack'])
    c = enh.get_card("Murloc Tidehunter")
    print(c['attack'])