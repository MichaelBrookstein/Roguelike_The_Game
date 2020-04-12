import tcod as libtcod
from components.level import Level
from components.equipment import Equipment
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from game_functions.render_functions import RenderOrder
from loader_functions.create_characters import Character



def get_constants():
    window_title = 'Quest of Shadows'

    screen_width = 106
    screen_height = 65

    bar_width = 20
    panel_height = 20
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 30
    message_height = panel_height - 4

    map_width = 80
    map_height = 45

    info_width = screen_width - map_width
    info_x = screen_width - info_width

    player_con_width = screen_width - map_width
    player_con_x = screen_width - info_width
    player_con_y = int(screen_height / 2)

    room_max_size = 10
    room_min_size = 6
    max_rooms = 100

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    max_items_per_room = 2

    colors = {
        'background': libtcod.Color(7, 7, 7),
        'dark_ground': libtcod.Color(40, 40, 40),
        'dark_wall': libtcod.Color(20, 20, 20),
        'light_ground': libtcod.Color(110, 110, 110),
        'light_wall': libtcod.Color(80, 80, 80),
        'light_door': libtcod.Color(122, 81, 40),
        'dark_door': libtcod.Color(89, 55, 22)
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'info_width': info_width,
        'info_x': info_x,
        'player_con_width': player_con_width,
        'player_con_x': player_con_x,
        'player_con_y': player_con_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors
    }

    return constants

def initialize_game(constants, chosen):

    player_component, inventory_component, abilities_component, info_component, starting_equip, starting_feats, name = Character(chosen)

    level_component = Level()
    equipment_component = Equipment()


    player = Entity(0, 0, '@', libtcod.lightest_gray, name, blocks=True, render_order=RenderOrder.PLAYER,
                    fighter=player_component, inventory=inventory_component, abilities=abilities_component, level=level_component,
                    equipment=equipment_component, info=info_component)

    entities = [player]

    player.abilities.add_feat(starting_feats)
    player.inventory.add_item(starting_equip)
    player.equipment.toggle_equip(starting_equip)


    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state