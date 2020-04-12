import tcod as libtcod

from game_states import GameStates


def handle_keys(key, game_state):

    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    elif game_state == GameStates.SHOW_INVENTORY:
        return handle_inventory_keys(key)
    elif game_state == GameStates.ITEM_MENU:
        return handle_item_menu_keys(key)
    elif game_state == GameStates.SHOW_ABILITIES:
        return handle_ability_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)

    return {}

def handle_player_turn_keys(key):
    key_char = chr(key.c)

    if key.vk == libtcod.KEY_UP or key_char == 'w':
        return {'move': (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_char == 's':
        return {'move': (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_char == 'a':
        return {'move': (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_char == 'd':
        return {'move': (1, 0)}
    elif key_char == 'q':
        return {'move': (-1, -1)}
    elif key_char == 'e':
        return {'move': (1, -1)}
    elif key_char == 'z':
        return {'move': (-1, 1)}
    elif key_char == 'c':
        return {'move': (1, 1)}
    elif key_char == 'x':
        return {'wait': True}
    if key_char == 'g':
        return {'pickup': True}
    elif key_char == 'i':
        return {'show_inventory': True}
    elif key_char == 'p':
        return {'show_abilities': True}
    elif key.vk == libtcod.KEY_ENTER:
        return {'take_stairs': True}
    elif key.vk == libtcod.KEY_TAB:
        return {'show_character_screen': True}


    elif key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}

def handle_inventory_keys(key):
    index = key.c - ord('1')
    key_char = chr(key.c)

    if key.vk == libtcod.KEY_ESCAPE or key_char == 'i':
        return {'exit': True}

    if index >= 0:
        return {'inventory_index': index}

    return {}

def handle_item_menu_keys(key):
    key_char = chr(key.c)

    if key_char == '1':
        return {'use': True}
    elif key_char == '2':
        return {'drop': True}
    elif key.vk == libtcod.KEY_ESCAPE or key_char == 'i':
        return {'exit': True}

    return {}

def handle_ability_keys(key):
    index = key.c - ord('1')
    key_char = chr(key.c)

    if key.vk == libtcod.KEY_ESCAPE or key_char == 'p':
        return {'exit': True}

    if index >= 0:
        return {'ability_index': index}

    return {}

def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == '1':
        return {'new_game': True}
    elif key_char == '2':
        return {'load_game': True}
    elif key_char == '3' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_character_select(key):
    key_char = chr(key.c)

    if key_char == '1':
        return {'thief': True}
    elif key_char == '2':
        return {'brute': True}
    elif key_char == '3':
        return {'occultist': True}

    return {}

def handle_level_up_menu(key):
    key_char = chr(key.c)

    if key_char == '1':
        return {'level_up': 'hp'}
    elif key_char == '2':
        return {'level_up': 'str'}
    elif key_char == '3':
        return {'level_up': 'def'}
    elif key_char == '4':
        return {'level_up': 'dog'}
    elif key_char == '5':
        return {'level_up': 'ap'}
    elif key_char == '6':
        return {'level_up': 'crit'}

    return {}

def handle_character_screen(key):

    if key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_TAB:
        return {'exit': True}

    return {}