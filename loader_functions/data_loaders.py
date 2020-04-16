import shelve

import os


def save_game(player, entities, game_map, message_log, game_state, cooldown_counter):
    with shelve.open('savegame.dat', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
        data_file['permanent_cooldown_counter'] = cooldown_counter

def load_game():
    if not os.path.isfile('savegame.dat.dat'):
        raise FileNotFoundError

    with shelve.open('savegame.dat', 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        permanent_cooldown_counter = data_file['permanent_cooldown_counter']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state, permanent_cooldown_counter
