import json
import libarchive.public
import time

total_games = 299680

if __name__ == '__main__':
    converted_games = []
    with libarchive.public.file_reader(b'data/training_games_jsons.7z') as e:
        counter = 0
        start_time = time.time()
        for entry in e:
            data = ''.join((str(block, 'ascii') for block in entry.get_blocks()))
            dict_data = json.loads(data)
            print(dict_data['game'][50][0]['player']['hand'])
            break
            game_setup = dict_data['game_setup']
            last_turn = dict_data['game'][-1][0]
            winner = int(dict_data['result'][7])
            converted_games.append({
                'id': game_setup['game_id'],
                'bot0': game_setup['bot_1_ply'],
                'deck0': game_setup['deck_1_name'],
                'bot1': game_setup['bot_2_ply'],
                'deck1': game_setup['deck_2_name'],
                'winner': winner,
                'winner_hp': last_turn['player' if last_turn['active_player'] == winner else 'opponent']['hp'],
            })
            counter += 1
            if counter % 1000 == 0:
                eta = (time.time() - start_time) * (total_games - counter) / counter
                print('{}/{}, {:.2f}%, ETA: {}m{}s'.format(
                    counter, total_games, 100 * counter / total_games, int(eta // 60), int(eta) % 60))
    print('Finished reading, saving to file')
    with open('data/training_games_detailed.json', 'w') as f:
        json.dump(converted_games, f)
