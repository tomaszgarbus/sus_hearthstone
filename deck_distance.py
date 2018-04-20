from loader import load_training_decks


def calculate_deck_distance(deck1: dict, deck2: dict):
    distance = 30
    for card in deck1['cards']:
        if card in deck2['cards']:
            distance -= min(deck1['cards'][card], deck2['cards'][card])
    return distance


if __name__ == '__main__':
    deck_distances = {}
    training_decks = sorted(load_training_decks(), key=lambda deck: deck['deckName'])
    for i in range(len(training_decks)):
        deck_i = training_decks[i]
        for j in range(i+1, len(training_decks)):
            deck_j = training_decks[j]
            deck_distances[(deck_i['deckName'], deck_j['deckName'])] = calculate_deck_distance(deck_i, deck_j)
